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
app.get("/qr", async (_req, res) => {
  if (ready) return res.send("<h2 style='font-family:sans-serif;color:green'>✓ WhatsApp session is already CONNECTED and ACTIVE!</h2>");
  if (!currentQR) return res.send("<h2 style='font-family:sans-serif;color:orange'>Waiting for QR code generation... Please refresh in a few seconds.</h2>");
  try {
    const dataUrl = await QRCode.toDataURL(currentQR, { width: 350 });
    res.send(`
      <div style="font-family:sans-serif;text-align:center;padding:40px;">
        <h2>Scan this QR in WhatsApp &rarr; Linked Devices</h2>
        <img src="${dataUrl}" style="border:8px solid #eee;border-radius:16px;box-shadow:0 4px 12px rgba(0,0,0,0.15);" />
        <p style="color:#666;margin-top:16px;">Open WhatsApp on your phone &gt; Settings &gt; Linked Devices &gt; Link a Device</p>
      </div>
    `);
  } catch (err) {
    res.status(500).send("Error rendering QR: " + err.message);
  }
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
