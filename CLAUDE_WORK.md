# CLAUDE WORK — Honest Lead Verification (stop fake leads)

**By:** Claude (Opus 4.8), handed to the owner for Antigravity to push.
**Date:** 2026-10-08
**Goal:** stop the two kinds of FAKE lead the tool produced — (a) "WhatsApp" numbers that have no WhatsApp, and (b) "no website" businesses that actually already have a website.

---

## ⚠️ READ FIRST — reconcile with current `main`
The GitHub `main` branch already has Antigravity's **newer, stronger** verification:
`PhoneValidationService` (Google libphonenumber), `MultiSearchVerifier` (DuckDuckGo+Bing+Mojeek consensus), `DeepCrawlerService`, `DnsVerifierService`, and it already removed the fake default rating.

**That supersedes most of the work below.** Do **NOT** blindly overwrite `main` with these files. Use this as reference; cherry-pick only anything `main` is still missing. A reference branch is already on GitHub: **`claude/honest-verification`**.

---

## What Claude changed in this folder (files on disk already contain these edits)

### NEW — `backend/app/services/web_presence.py`
Bing-based live verifier: given a business name + city it searches the web and returns:
- `website_found` — the business's own official site (social/foodpanda/directories excluded), or `None` if a real search found none.
- `whatsapp_confirmed` — WhatsApp numbers the business **advertises** (wa.me / api.whatsapp.com) that **match** its phone.
- `searched` — True only when Bing actually served a results page (so "searched, none found" ≠ "search blocked").
Handles Bing's `ck/a` redirect decoding + retry/backoff + junk filtering.

### `backend/app/services/verification_service.py`
- Imports `research_presence`; runs it when the batch supplies `candidate["_city"]` (unit tests skip the network).
- WhatsApp: only `WHATSAPP_CONFIRMED` (with `whatsapp_verified=True`) when an advertised wa.me matches; otherwise `WHATSAPP_FORMAT_ONLY` (`whatsapp_verified=False`). Added `whatsapp_confidence`, `website_found_url`.
- Website: OSM has no site → live search. Found → `LIVE` (not a greenfield lead). Searched & none → confirmed `NO_WEBSITE`. Search unavailable → `NO_WEBSITE_UNVERIFIED` (never asserted as build-ready).

### `backend/app/services/classification_service.py`
- `has_contact_channel` accepts the new WhatsApp statuses (`WHATSAPP_FORMAT_ONLY`, `WHATSAPP_CONFIRMED`).
- New `NO_WEBSITE_UNVERIFIED` branch → capped at **P2** with loud "WEBSITE NOT VERIFIED" / "WHATSAPP NOT VERIFIED" flags (never P1 build-ready).
- `NO_WEBSITE` P1/P2 path adds a "WHATSAPP NOT VERIFIED" note when the WhatsApp was not confirmed.

### `batch_hunter.py`
- Injects `_city` / `_country` into each candidate before verification.
- Excel: header `WhatsApp (confidence)`; cell shows `+92… (CONFIRMED)` or `+92… (format-only, UNVERIFIED)`; banner wording honest.
- Removed the fabricated default rating (`4.5`) → shows `N/A` when none.

### tests — `tests/test_verification.py`, `tests/test_classification.py`, `tests/test_e2e_batch.py`
Rewritten to the honest contract (no more fictional `WHATSAPP_VERIFIED`). **Full suite: 11/11 passing** (`python -m pytest -q`).

---

## Guarantee (honest)
These changes ensure the tool never labels a number "verified WhatsApp" or a business "no website / build-ready" **on a guess** — unconfirmed items are clearly flagged for manual check. A 100% WhatsApp-account check is not possible for free (needs the WhatsApp API or a logged-in session); this is best-effort + honest. `main`'s libphonenumber + multi-search approach is a stronger take on the same goal.
