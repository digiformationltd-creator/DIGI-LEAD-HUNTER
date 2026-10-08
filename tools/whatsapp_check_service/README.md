# WhatsApp Existence-Check Service (real `onWhatsApp`)

The lead pipeline can only tell **mobile vs landline** from the phone number
(libphonenumber). A mobile number may still have **no WhatsApp account** — that
is why some leads showed a WhatsApp chat button for numbers that aren't on
WhatsApp. The only honest fix is to ask WhatsApp itself. This tiny service does
that with a logged-in session (Baileys `onWhatsApp`).

## Run (once)
```bash
cd tools/whatsapp_check_service
npm install
node index.js
```
Scan the printed QR in **WhatsApp → Linked Devices**. Leave it running.

## Point the lead pipeline at it
Set the env var the backend reads:
```bash
setx WHATSAPP_CHECK_URL http://127.0.0.1:8790/check   # Windows
# or:  export WHATSAPP_CHECK_URL=http://127.0.0.1:8790/check
```
Now every lead run verifies each number against the live WhatsApp network:
- `exists:true`  → the lead is shown as **WhatsApp verified** (chat button enabled).
- `exists:false` → the number is dropped as **NO_WHATSAPP** (no fake lead).
- service off / `WHATSAPP_CHECK_URL` unset → numbers stay **mobile, WhatsApp unconfirmed** (never claimed as WhatsApp).

## Endpoint
`GET /check?number=<digits or E.164>` → `{ "number": "...", "exists": true|false|null }`

> Use a WhatsApp number you control. Keep request volume reasonable; this talks to
> the real WhatsApp network via your linked session.
