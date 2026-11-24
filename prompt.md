# Prompt Log & Development Audit Trail — Salon Queue Management System

This document contains the complete, unedited chronological record of all prompts submitted during the development of the Salon Queue Management System, including what was attempted, the exact errors or failures encountered, and how they were resolved.

---

## Prompt 1: Initial Quick Actions, Live Timer & Auto-Assignment
**Date & Time:** `2026-11-24 21:21:09 +05:30`  
**User Prompt:**
> `make the quick actions at the front page work, have the timer for the waiting customer work, automatically add the customer to their selected barber if one otherwise add them to any free barber`

### 1. Objective
- Make front-page quick actions ("Add customer", "Reception desk", "Live display") functional.
- Implement a live ticking wait timer for waiting customers.
- Automatically assign newly registered customers to their preferred barber if free; otherwise assign them to any free on-duty barber.

### 2. What Did NOT Work Initially (Failures & Errors)
- **Navigation Desynchronization Bug**: Clicking any quick action button on the Overview page updated an internal state variable, but Streamlit's `st.radio("Workspace", PAGES, ...)` immediately re-evaluated its own stored widget key (`workspace_nav_radio`) and reverted back to `"Overview"`. The user click appeared completely ignored.
- **Database Schema Limitation**: The SQLite table `queue_entries` had no `assigned_barber` column. Previous test records had `status = 'called'` with a NULL `started_at` timestamp, which broke duration calculations and chair occupancy checks.
- **PowerShell Syntax Failures**: Attempting inline Python one-liners via PowerShell threw syntax errors due to unescaped double quotes (`"` and `\"`) within nested command arguments.

### 3. Resolution
- Switched navigation to native Streamlit callbacks (`on_click=set_workspace, args=(target,)`) bound directly to `st.session_state["workspace_nav_radio"]`, eliminating race conditions.
- Migrated `salon_queue.db` by executing `ALTER TABLE queue_entries ADD COLUMN assigned_barber TEXT`.
- Backfilled legacy `called` entries to `in_chair` with `started_at = COALESCE(called_at, created_at)`.
- Standardized shell execution by writing dedicated temporary `.py` script files instead of fragile inline shell strings.

---

## Prompt 2: Minimalist Aesthetic & Emoji Purge
**Date & Time:** `2026-11-24 21:55:23 +05:30`  
**User Prompt:**
> `make the quick actions buttons work, remove the emojis added for the site to look minimal`

### 1. Objective
- Finalize the quick action button workflows.
- Remove all decorative emojis across the entire UI for a clean, minimalist typography aesthetic.

### 2. What Did NOT Work Initially (Failures & Errors)
- **Dual Navigation State Clash**: The script was reading from a detached state key `st.session_state["active_workspace"]` while `st.radio` held its own separate key state `st.session_state["workspace_nav_radio"]`. Selecting a page in the sidebar and clicking a button on the page conflicted.
- **Scattered Emojis**: Emojis were embedded across over 80 lines in headers, markdown pills, button labels (e.g., scissors, clocks, chairs, checkmarks), metric labels, and alert boxes.

### 3. Resolution
- Unified navigation on a single state key `st.session_state["workspace_nav_radio"]`.
- Conducted an automated regex audit (`[\U00010000-\U0010ffff]|[\u2600-\u27bf]`) and removed every emoji from `app.py`.
- Replaced emojis with clean modern typography (DM Sans + Manrope) and monochrome monospace timer badges (`timer-pill-calm`, `timer-pill-warn`, `timer-pill-alert`).

---

## Prompt 3: Automatic Service Start & Timer Trigger
**Date & Time:** `2026-11-24 22:13:36 +05:30`  
**User Prompt:**
> `Once customer is called, start service and timer automatically`

### 1. Objective
- Eliminate the manual 2-step process (`called` -> `in_chair`) so calling a customer immediately starts service and begins the live chair timer.

### 2. What Did NOT Work Initially (Failures & Errors)
- **Lifecycle Transition Block**: In `update_entry`, calling a customer set `status = 'called'`. The customer sat in an intermediate state awaiting a manual "Start service" button click. As a result, active chair timers showed `00:00` until the second button was clicked.
- **Component Filtering**: The live service clock HTML component was explicitly filtering only `in_chair` records, meaning any customer with status `called` had no visible timer.

### 3. Resolution
- Updated `update_entry` so that transitioning to `called` or `in_chair` immediately writes `status = 'in_chair'` and sets both `called_at` and `started_at` to `stamp()`.
- The live in-service elapsed timer now begins ticking the exact second the customer is called.

---

## Prompt 4: TA Handout Requirements & Specification Audit
**Date & Time:** `2026-11-24 22:23:38 +05:30`  
**User Prompt:**
> `Go through these requirements to confirm everything is covered`  
> *(Attached: `Salon_Queue_Management_Vibe_Coding_Guide.txt` / MSc IT TA Lab Handout)*

### 1. Objective
- Audit entire application against TA requirements, 7 screen specifications, queue lifecycle rules, and submission deliverables.

### 2. What Did NOT Work Initially (Missing Requirements & Test Failures)
- **Single Service Restriction**: `add_customer` only permitted choosing 1 service, whereas the TA handout required selecting up to 3 services with aggregated duration and price calculation.
- **Missing 2nd-in-Line Alert**: TA rule #6 required notifying customers when they are 2nd in line ("Start coming to the salon — You are 2nd in line!"). This was not implemented.
- **Missing Self-Cancellation**: Customers had no way to cancel their spot from the Track Token screen.
- **Missing Bilingual Language Toggle**: TA handout specified English / Gujarati (EN/GU) language switching; the app only had English.
- **Missing Documentation Files**: Required deliverables (`docs/01-brief.md`, `docs/02-screens.md`, `docs/03-flows-rules.md`, `AGENTS.md`) did not exist.
- **Test Assertion Failure**: Test script threw `AssertionError: assert app.fmt_timer_seconds(3600) == '60m 00s'` because `fmt_timer_seconds` returned `"1h 00m 00s"`.
- **Function Signature Mismatch**: Test script called `app.add_customer(..., preferred_barber='Amit')`, throwing `TypeError: unexpected keyword argument 'preferred_barber'` (the actual parameter was `preferred`).

### 3. Resolution
- Updated `add_customer` and Join Queue form to support `st.multiselect(..., max_selections=3)` with dynamic duration/price summation.
- Added 2nd-in-line alert banner and guarded spot cancellation expander on Track Token.
- Implemented `TRANSLATIONS` dictionary with 50 keys in both English and Gujarati with sidebar radio switch.
- Generated all documentation deliverables (`01-brief.md`, `02-screens.md`, `03-flows-rules.md`, `AGENTS.md`, `README.md`).

---

## Prompt 5: Ergonomic Placement Analysis
**Date & Time:** `2026-11-24 22:54:49 +05:30`  
**User Prompt:**
> `For now, do not do any changes, rather tell me that can you place the buttons on the website more intuitively?`

### 1. Objective
- Analyze UI/UX and ergonomics of button placement across all 7 screens without making file changes.

### 2. Identified Ergonomic Deficiencies
- Overview: Ambiguous detached buttons at bottom; needed contextual action bar directly above queue table.
- Reception: Long vertical layout caused scrolling fatigue on tablet devices; needed a side-by-side chairs vs. queue layout.
- Barber Desk: Buttons were too small for quick chair-side taps; needed full-width 48px touch targets.
- Track Token: "Cancel spot" button was too close to primary action; needed safe 2-step confirmation dialog.
- Admin Settings: Individual save buttons per service row caused repetitive clicking; needed unified batch save.

---

## Prompt 6: Execution of Intuitive Layout Redesign
**Date & Time:** `2026-11-24 22:56:04 +05:30`  
**User Prompt:**
> `Do all`

### 1. Objective
- Implement all proposed button placements and layout improvements across the application.

### 2. What Did NOT Work Initially (Failures & Errors)
- **Table Width Distortion**: Placing action buttons in narrow table columns crushed customer names and wait times on desktop views.
- **Accidental Cancellation Risk**: An instant single-click cancellation button caused accidental cancellations during testing.

### 3. Resolution
- Restructured Reception into a 2-column tablet layout (Chairs on left, Waiting queue with instant action bar on right).
- Added an inline "Quick Walk-in" expandable drawer directly on the Overview page.
- Created 48px full-width touch targets for Barber Desk chairs ("Complete service", "Take a break", "Call next").
- Wrapped cancellation in a safe confirmation dialog (`st.expander` / `st.popover`).
- Unified Admin settings into a single "Save operating settings" and "Save all service changes" batch action.

---

## Prompt 7: Integration Analysis for saloon.wtf
**Date & Time:** `2026-11-24 23:17:28 +05:30`  
**User Prompt:**
> `https://saloon.wtf/ Any chance you can integrate this in the website? First tell me before making changes`

### 1. Objective
- Investigate `saloon.wtf` (Deluxe Saloon ambient retro Indian barber shop internet radio) and analyze integration feasibility without making changes.

### 2. Findings
- Inspected network headers: HTTP 200, no restrictive `X-Frame-Options` or blocking `Content-Security-Policy`.
- Presented 4 architectural options: Sidebar ambient player, Waiting area TV display integration, Dedicated "Salon Vibe" tab, and Floating corner pill.

---

## Prompt 8: Dual Integration Selection (TV Display & Floating Pill)
**Date & Time:** `2026-11-24 23:20:16 +05:30`  
**User Prompt:**
> `2 and 4`

### 1. Objective
- Implement Option 2 (Waiting Area Live TV Display) and Option 4 (Floating Corner Pill).

### 2. What Did NOT Work Initially (Failures & Errors)
- **Audio Interruption on TV Display**: Embedding the iframe inside `@st.fragment(run_every="5s")` caused the iframe to re-render every 5 seconds, repeatedly cutting off and restarting the music stream.
- **Streamlit Deprecation Warning**: `components.html` emitted a deprecation warning recommending `st.iframe`.
- **Popover UX Friction**: Option 4 rendered as a small button that opened a large popover drawer, requiring manual clicking rather than feeling like an ambient player.

### 3. Resolution
- Moved the audio player outside the `@st.fragment` queue sync container on Live Display, ensuring uninterrupted streaming.
- Migrated to first-class `st.iframe(src="https://saloon.wtf/", height=460)`.

---

## Prompt 9: Custom Floating Rotating Vinyl Player Pill with Autoplay
**Date & Time:** `2026-11-24 23:33:03 +05:30`  
**User Prompt:**
> `maybe convert 2nd into a floating pill at the bottom right with a rotating canvas, play button forward and backward something like the screenshot uploaded and have it autoplay`  
> *(Attached: Screenshot of Deluxe Saloon terracotta pill player with rotating vinyl disc, track info, scrubber, and playback controls)*

### 1. Objective
- Convert the ambient radio into a custom floating player capsule widget matching the uploaded screenshot:
  - Terracotta/amber frosted-glass capsule pill fixed at bottom-right viewport.
  - Rotating vinyl album art disc on the left (`animation: rotateDisc 10s linear infinite`).
  - Track title, artist, live progress scrubber, elapsed/total time (`0:13 / 5:04`).
  - Backward (`|<<`), circular white Play/Pause toggle, and Forward (`>>|`) buttons.
  - Autoplay capability.

### 2. What Did NOT Work Initially (Failures & Errors)
- **IFrame HTML Sanitization**: Attempting to inject the player HTML via `st.markdown(..., unsafe_allow_html=True)` resulted in DOMPurify stripping the player's inner `<iframe>` container.
- **Browser Autoplay Policy Gate**: Modern browsers block unmuted audio playback on initial page load without a user gesture (`NotAllowedError: play() failed because the user didn't interact with the document first`).
- **PowerShell Script Parsing**: Extracting the 32 song chunks via inline PowerShell commands failed due to nested string quote termination.

### 3. Resolution
- Reverse-engineered `saloon.wtf` JavaScript chunks and extracted all **32 authentic retro Bollywood songs** (titles, artists, covers, YouTube IDs, and AAC stream links) into `saloon_songs.json`.
- Built `floating_player.html` combining the YouTube IFrame API with AAC audio fallback, live progress scrubber, and spinning vinyl disc with dark spindle center cutout.
- Injected an autoplay unlocker (`window.addEventListener('click', ..., { once: true })`) so audio plays immediately on page load or on the very first user interaction.
- Positioned the player fixed at `bottom: 24px; right: 24px; z-index: 999999` using CSS.

---

## Prompt 10: Complete Prompts Documentation Log
**Date & Time:** `2026-11-24 23:45:57 +05:30`  
**User Prompt:**
> `create a prompt.md that contains all the prompts used even those that did not work`

### 1. Objective
- Generate this comprehensive log documenting all 10 user prompts executed throughout the project, detailing objectives, initial failures, and final resolutions.
- Save as both `prompt.md` and `prompts.md` across project directories for full accessibility.

---

## Summary of All Executed Prompts

| # | Prompt Summary | Key Challenges / Failures Encountered | Outcome / Resolution |
| :--- | :--- | :--- | :--- |
| **1** | Quick actions, live timer, auto-assign | Widget state reset, missing DB column, PowerShell string parsing | Fixed via callback navigation, SQLite migration, backfilled timestamps |
| **2** | Minimalist aesthetic & emoji removal | Dual-state clash, 80+ scattered emojis across UI | Unified state key, automated emoji purge, DM Sans typography |
| **3** | Auto-start service on call | Manual 2-step transition, timer stayed at 00:00 | Merged `called` directly into `in_chair`, immediate service timer start |
| **4** | TA Handout compliance audit | Single service limit, missing 2nd-in-line alert, missing Gujarati, missing docs | Added multi-select, alert banner, cancellation dialog, bilingual EN/GU, full docs |
| **5** | Ergonomic button placement review | UI clutter on tablet, small chair targets, destructive cancel proximity | Proposed contextual action bars, 2-column layout, 48px touch targets |
| **6** | Execute intuitive layout redesign | Table column crowding, accidental mobile spot cancellation | Implemented tablet layout, inline walk-in drawer, guarded popover dialogs |
| **7** | saloon.wtf integration feasibility | Checking headers and iframe security constraints | Confirmed 200 OK & no X-Frame-Options; presented 4 clean options |
| **8** | Dual integration (TV display & pill) | Fragment 5s auto-refresh killed audio stream, deprecation warning | Moved outside fragment, migrated to `st.iframe` |
| **9** | Rotating vinyl floating pill with autoplay | Browser autoplay blocks, DOMPurify stripped iframes, shell quote parsing | Extracted 32 songs, custom rotating disc canvas, YouTube API + AAC fallback |
| **10** | Comprehensive prompt log | Capturing all failed iterations and transcripts | Complete `prompt.md` generated with full audit trail |
