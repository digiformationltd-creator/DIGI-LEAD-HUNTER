# Verification Agent (Phase 02)
## Purpose
Conducts multi-point verification on prospective business candidates:
1. Physical identity & Google Maps presence
2. Official website verification (No website, Outdated/Weak, or Official website)
3. WhatsApp channel validation & phone normalization

## WhatsApp Validation Logic
- Pakistan numbers (03xx -> +92 3xx, 923xx) marked WHATSAPP_VERIFIED.
- UK numbers (07xxx -> +44 7xxx) marked WHATSAPP_VERIFIED.
- International mobile formats marked WHATSAPP_POSSIBLE.
- Generates direct https://wa.me/<number> link.

## Outputs
- Verified lead object with evidence records tagged E1 (Direct) to E4 (Uncertain).
