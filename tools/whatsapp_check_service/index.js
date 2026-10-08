/**
 * WhatsApp existence-check microservice (Baileys).
 *
 * This is the ONLY honest way to know a phone number is on WhatsApp. It logs in
 * once via QR (your WhatsApp → Linked Devices → scan), keeps the session, and
 * answers:  GET /check?number=<E164 or digits>  ->  { number, exists }
 * using Baileys `sock.onWhatsApp()`, which asks the WhatsApp network directly.
 *
 * The Python lead pipeline calls this when WHATSAPP_CHECK_URL points here, e.g.
 *   setx WHATSAPP_CHECK_URL http://127.0.0.1:8790/check
 *
 * Run:
 *   cd tools/whatsapp_check_service && npm install && node index.js
 * Scan the QR once. Leave it running while you hunt leads.
 */
const express = require("express");
const QR = require("qrcode-terminal");
const QRCode = require("qrcode");
const fs = require("fs");
const path = require("path");
const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require("@whiskeysockets/baileys");

const PORT = process.env.PORT || 8790;
let sock = null;
let ready = false;
let currentQR = null;

async function start() {
  const { state, saveCreds } = await useMultiFileAuthState("./wa_auth");
  sock = makeWASocket({ auth: state, printQRInTerminal: false });
  sock.ev.on("creds.update", saveCreds);
  sock.ev.on("connection.update", async (u) => {
    const { connection, lastDisconnect, qr } = u;
    if (qr) {
      currentQR = qr;
      console.log("\nScan this QR in WhatsApp → Linked Devices:\n");
      QR.generate(qr, { small: true });
      try {
        await QRCode.toFile(path.join(__dirname, "qr.png"), qr, { width: 400 });
        console.log("QR saved to qr.png and available on http://127.0.0.1:" + PORT + "/qr");
      } catch (err) {
        console.error("Failed to save QR png:", err);
      }
    }
    if (connection === "open") {
      ready = true;
      currentQR = null;
      console.log("WhatsApp session READY. Check service live on /check");
    }
    if (connection === "close") {
      ready = false;
      const code = lastDisconnect?.error?.output?.statusCode;
      if (code !== DisconnectReason.loggedOut) { console.log("reconnecting…"); start(); }
      else console.log("Logged out — delete ./wa_auth and restart to re-link.");
    }
  });
}

const app = express();
app.get("/health", (_req, res) => res.json({ ok: true, ready }));
app.get("/qr-data", async (_req, res) => {
  if (ready) return res.json({ ready: true });
  if (!currentQR) return res.json({ ready: false, qr: null });
  try {
    const dataUrl = await QRCode.toDataURL(currentQR, { width: 360, margin: 2 });
    res.json({ ready: false, qr: dataUrl });
  } catch (e) {
    res.json({ ready: false, error: e.message });
  }
});
app.get("/qr", async (_req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>DIGI Lead Hunter — WhatsApp QR Link</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #0b0f19; color: #fff; margin: 0; padding: 40px 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 80vh; text-align: center; }
        .card { background: #131a2a; border: 1px solid #23314f; border-radius: 20px; padding: 32px 28px; max-width: 440px; width: 100%; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h2 { margin: 0 0 8px 0; font-size: 22px; color: #60a5fa; }
        p.subtitle { color: #94a3b8; font-size: 14px; margin: 0 0 24px 0; }
        .qr-box { background: #fff; padding: 14px; border-radius: 16px; display: inline-block; box-shadow: 0 4px 15px rgba(0,0,0,0.3); min-height: 360px; min-width: 360px; display: flex; align-items: center; justify-content: center; margin: 0 auto; }
        .qr-box img { display: block; border-radius: 8px; max-width: 100%; }
        .status-badge { display: inline-block; margin-top: 20px; padding: 6px 14px; border-radius: 9999px; font-size: 13px; font-weight: 600; background: #1e293b; color: #38bdf8; border: 1px solid #334155; }
        .success-box { background: #064e3b; border: 1px solid #059669; color: #a7f3d0; border-radius: 16px; padding: 24px; margin-top: 10px; }
        .instructions { text-align: left; background: #0f172a; border-radius: 12px; padding: 16px 20px; margin-top: 24px; font-size: 13px; color: #cbd5e1; line-height: 1.6; border: 1px solid #1e293b; }
        .instructions ol { margin: 8px 0 0 0; padding-left: 20px; }
      </style>
    </head>
    <body>
      <div class="card">
        <h2>DIGI Lead Hunter</h2>
        <p class="subtitle">WhatsApp Network Verifier (Live Pairing)</p>
        <div id="content">
          <div class="qr-box">
            <div id="loading" style="color:#64748b;font-weight:600;">Generating live QR code...</div>
            <img id="qrImg" src="" style="display:none;" alt="QR Code" />
          </div>
          <div id="badge" class="status-badge">🔄 Auto-updating in real-time...</div>
        </div>
        <div class="instructions">
          <strong>Steps on WhatsApp Mobile:</strong>
          <ol>
            <li>Open WhatsApp &rarr; <strong>Settings / ⋮ Menu</strong></li>
            <li>Tap <strong>Linked Devices</strong> (منسلک آلات)</li>
            <li>Tap <strong>Link a Device</strong></li>
            <li>Scan the live QR code above</li>
          </ol>
        </div>
      </div>
      <script>
        async function checkQR() {
          try {
            const res = await fetch('/qr-data');
            const data = await res.json();
            if (data.ready) {
              document.getElementById('content').innerHTML = \`
                <div class="success-box">
                  <h3 style="margin:0 0 8px 0;font-size:20px;color:#34d399;">✓ WhatsApp Connected!</h3>
                  <p style="margin:0;font-size:14px;">The session is active and verified. Zero fake leads will be generated. You can safely close this tab.</p>
                </div>
              \`;
              return;
            }
            if (data.qr) {
              const img = document.getElementById('qrImg');
              const load = document.getElementById('loading');
              if (img.src !== data.qr) {
                img.src = data.qr;
              }
              img.style.display = 'block';
              if (load) load.style.display = 'none';
              document.getElementById('badge').innerText = '🟢 Live QR ready — scan now';
            }
          } catch(e) {}
          setTimeout(checkQR, 2000);
        }
        checkQR();
      </script>
    </body>
    </html>
  `);
});
app.get("/check", async (req, res) => {
  const digits = String(req.query.number || "").replace(/\D/g, "");
  if (!digits) return res.status(400).json({ error: "number required" });
  if (!ready || !sock) return res.json({ number: digits, exists: null, note: "session not ready" });
  try {
    const r = await sock.onWhatsApp(digits + "@s.whatsapp.net");
    const hit = Array.isArray(r) ? r[0] : null;
    res.json({ number: digits, exists: !!(hit && hit.exists), jid: hit?.jid || null });
  } catch (e) {
    res.json({ number: digits, exists: null, error: String(e?.message || e) });
  }
});
app.listen(PORT, () => console.log(`WhatsApp check service on http://127.0.0.1:${PORT}  (GET /check?number=...)`));
start();
