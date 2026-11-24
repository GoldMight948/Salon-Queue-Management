# Salon Queue Management System

**Live demo:** https://salon-queue-streamlit.streamlit.app  
**Hosted on:** Streamlit Community Cloud  
**Test Staff Access:** All workspaces available via the sidebar navigation (Overview, Join Queue, Reception, Barber Desk, Live Display, Admin Settings, Track Token)

---

## About
A high-performance queue management system for modern hair salons. Built with Python and Streamlit, it provides seamless real-time coordination between remote customers, in-person walk-ins, receptionists, and styling chairs.

## Key Features
- **Remote Self-Registration**: Join the queue from any mobile device, choose up to 3 services, select a preferred barber or 'Any free barber'.
- **Automated Chair Assignment**: Automatically matches customers with free barbers upon entry and immediately starts the service timer.
- **Real-Time Customer Tracking**: Live countdown clock, queue position indicator, and automatic alert when 2nd in line (*"Start coming to the salon"*).
- **Reception Command Center**: Full control over chairs, walk-in registration, auto-dispatch, and no-show resolution.
- **Barber Chair View**: Live service elapsed timer, one-click service completion, and break management.
- **Digital TV Signage**: High-contrast, 5-meter-readable display showing active chairs and up-next tokens with automatic 5-second updates.
- **Admin Settings**: Service catalog management (time & price), barber roster toggles, daily online cutoff, and CSV export.
- **Bilingual Interface**: Seamless one-click English and Gujarati (EN/GU) language toggle.

## How to Run Locally

```bash
# Clone the repository and navigate to the project directory
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The application will launch on your local host (typically `http://localhost:8501`).

## Submission Artifacts
- `docs/01-brief.md`: Project scope, user roles, must-have features & boundaries.
- `docs/02-screens.md`: Specification of all 7 screens, UI elements, and interactions.
- `docs/03-flows-rules.md`: Queue lifecycle flows, assignment rules, and TA test checklist.
- `AGENTS.md`: Instruction sheet for agent development.
- `prompts.md`: Chronological log of prompts used during the lab.
