# AGENTS.md — Salon Queue Management System

Queue management application for a modern salon: customers self-register and track live wait times from their phone; receptionists and barbers manage chairs and dispatch; waiting-area TV display shows real-time serving updates.

## Read First
- `docs/01-brief.md` -> Core problem, user roles, must-have features & boundaries.
- `docs/02-screens.md` -> Screen layouts, widgets, actions, and responsive views.
- `docs/03-flows-rules.md` -> Queue lifecycle rules, dispatch logic, and TA test checklist.

## Technology Stack
- **Framework**: Python 3.10+ with Streamlit
- **Persistence**: SQLite with row-level transaction locks (`salon_queue.db`)
- **Data Handling**: Pandas & UUID
- **Styling**: Minimalist modern typography (DM Sans + Manrope), responsive CSS, no emoji clutter
- **Auto-Refresh**: Streamlit `@st.fragment(run_every="5s")` for hands-free live TV and tracking sync

## Core Operating Rules
1. Statuses: `waiting` -> `in_chair` -> `done`. Cancellation allowed from `waiting`. No-show allowed from active chair. Never backwards.
2. Once a customer is called/assigned, service starts automatically and the service timer begins immediately.
3. Customer preferred barbers are strictly protected. Customers with no preference are load-balanced across available free barbers.
4. Barbers may only hold one customer in their chair at a time.
5. Online queue closes 30 minutes before configured salon closing time.
6. All labels support bilingual English / Gujarati (EN/GU) switching.

## How to Run
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
