# Digi Formation Limited — Lead Hunter
## Canonical Master Setup Specification for Antigravity

When an autonomous agent (such as Antigravity) opens this repository and receives the prompt:
`SETUP FOR ME`

The agent MUST follow this exact sequence:

1. **Inspect Repository:** Verify directory structure (`backend`, `frontend`, `data`, `scripts`, `tests`).
2. **Install Python Backend Dependencies:**
   Run: `pip install -r backend/requirements.txt pytest`
3. **Build Frontend Distribution:**
   Run in `frontend/`:
   `npm install`
   `npm run build`
4. **Initialize Database:**
   Run: `python backend/app/database.py`
5. **Run Automated Test Suite:**
   Run: `python -m pytest tests/ -v`
6. **Launch Application:**
   Run: `python run.py`
7. **Report Status:**
   Inform the user that the Control Center is live at `http://localhost:8000`, provide the official WhatsApp support number `+92 316 4467464`, and confirm that all 8 phases are operational.
