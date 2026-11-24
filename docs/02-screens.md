# Salon Queue — Screens & Features Specification

## Screen 1: Home / Overview (`/`)
- **Purpose**: Gives managers, staff, and visitors an instant overview of salon queue load and barber chair status.
- **Top Metrics**:
  - Waiting count (customers in queue)
  - In service count (currently in chairs)
  - Served today (completed appointments)
  - Barbers available (active on-duty barbers with empty chairs)
- **Queue Right Now Table**: Clean table listing Token, Customer, Service, Status, Joined Time, Live Timer, Estimated Wait, and Barber.
- **Team Availability Panel**: Status chips for every barber: Available, Serving, On break, or Off duty.
- **Quick Action Bar**:
  - `Add customer`: Direct navigation to Join Queue intake.
  - `Reception desk`: Direct navigation to Reception Dashboard.
  - `Auto-assign queue`: Instant one-click dispatch matching waiting customers with free barbers.
  - `Live display`: Opens TV waiting area display.
  - `Quick walk-in expander`: Inline form for rapid walk-in intake directly on the overview page.

---

## Screen 2: Join Queue (`/join`)
- **Purpose**: Customer self-registration for remote mobile or kiosk queue entry.
- **Inputs**:
  - Customer name (min 2 characters, validated).
  - Mobile phone number (10 digits validated, rejects duplicate active bookings for the day).
  - Service selection: Multi-select services (max 3), with duration and pricing displayed per service.
  - Preferred barber selector: 'No preference (Any free barber)' or specific active barber.
- **Live Summary**: Real-time card showing combined duration (min), total price (₹), and estimated wait.
- **Confirmation Action**: `Get my token` button.
- **Intake Guard**: Automatically closes online intake 30 minutes before salon closing time or when disabled by owner settings.
- **Immediate Assignment**: If preferred (or any) barber is free, auto-assigns immediately and starts service upon token issuance.

---

## Screen 3: My Status / Track Token (`/status/:id`)
- **Purpose**: Live customer token tracker with real-time wait clock and status alerts.
- **Token Banner**: Large, bold token code (e.g., S-005) and customer name.
- **Waiting State**:
  - Live ticking client-side browser clock (incrementing seconds in real time).
  - People ahead metric and dynamic estimated wait time.
  - **2nd-in-Line Alert**: When the customer reaches 2nd in line (`pos == 2`), displays prominent alert banner: *"You are 2nd in line — Start coming to the salon!"*
  - **Cancel Spot Action**: `Cancel my spot` button allowing the customer to release their place in line.
- **In-Chair / Active State**:
  - Live service timer ticking elapsed minutes/seconds against target duration.
  - Shows assigned barber and chair notice.
- **Completed State**: "Your service is complete. Thank you for visiting."
- **Auto-Refresh**: Background `@st.fragment(run_every="5s")` updates customer screen automatically as queue advances.

---

## Screen 4: Reception Dashboard (`/reception`)
- **Purpose**: Operational command center for the receptionist.
- **Barber Chair Cards**: Grid showing each barber's status (Available, Serving, Break, Off duty), with manual `Call next for [Barber]` action.
- **Auto-Dispatch All Waiting**: One-click batch assignment matching all eligible waiting customers to free chairs.
- **Add Walk-In Form**: Registration with multi-service support, price calculation, and barber preference.
- **Waiting List**: Clean rows showing Token, Customer, Services, Waited Timer badge, Estimated Wait, Preferred Barber, instant `Call now` action, and `Cancel` button.
- **In Service List**: Active chair entries showing elapsed service time, `Complete service` button, and `No-show` resolution.

---

## Screen 5: Barber Desk (`/barber/:name`)
- **Purpose**: Mobile/tablet view for individual barbers at their styling chair.
- **Barber Selector**: Dropdown to switch between barbers (Ravi, Amit, Imran).
- **Current Customer Card**: Shows token, customer name, services selected, total duration, and price.
- **Service Timer**: Live elapsed timer (`In service: MM:SS / Target min`).
- **One-Click Completion**: `Complete service` button marks entry as done, frees chair, and triggers automated queue dispatch for the next eligible customer.
- **Break Management**: `Take a break` / `End break` toggle buttons (disabled when a customer is currently in chair).
- **Next Eligible Customers**: Queue preview of up to 5 customers eligible for this barber.

---

## Screen 6: Waiting Area TV (`/display`)
- **Purpose**: Public high-contrast digital signage view for waiting room screens.
- **Now Serving Section**: High-visibility cards per active barber showing token, barber name, and live in-service elapsed time.
- **Up Next Section**: Clean list of the next 6 waiting tokens with customer name, service, waited time, and estimated wait.
- **Waiting Lounge Ambience (Deluxe Saloon Radio)**: Toggleable retro 90s Indian barber shop ambient internet radio player embedded from `saloon.wtf` with un-interrupted streaming audio.
- **Hands-Free Auto-Refresh**: Background `@st.fragment(run_every="5s")` keeps the screen continuously updated without manual page reloads.

---

## Global Widget: Floating Rotating Vinyl Radio Pill (`saloon.wtf`)
- **Placement**: Fixed bottom-right corner across all application screens (`bottom: 24px; right: 24px; z-index: 999999`).
- **Aesthetic**: Deluxe Saloon terracotta-gradient capsule pill with rotating vinyl record canvas on the left.
- **Controls**: Previous track button, prominent circular white Play/Pause toggle, Next track button, and interactive progress scrubber.
- **Track Display**: Live title, artist, elapsed/total duration (`0:13 / 5:04`), and rotating album artwork.
- **Engine**: YouTube IFrame API streaming 32 retro Bollywood tracks from `saloon.wtf` with AAC audio fallback and autoplay.

---

## Screen 7: Owner Settings (`/admin`)
- **Purpose**: Salon configuration and administrative control.
- **Salon Operating Hours**: Salon name input, closing time picker, and online queue open/closed toggle.
- **Service Catalog Management**: Edit service names, target durations (min), prices (₹), and active status toggles.
- **Team Roster**: Toggle barbers on/off duty with instant roster synchronization.
- **Activity Summary & Export**: Metrics for joined, completed, and no-shows today, with one-click daily queue CSV download.
