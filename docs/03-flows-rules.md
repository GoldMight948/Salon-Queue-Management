# Salon Queue — Flows, Rules & Test Checklist

## Main Flows

### 1. Remote Customer Flow
1. Customer opens Home (`/`) or Join Queue (`/join`).
2. Enters Name and 10-digit Phone, selects up to 3 services, and picks preferred barber (or 'No preference').
3. System verifies phone has no active tokens today and that intake is open.
4. Auto-assignment check:
   - If selected barber is free: customer is assigned immediately (`status='in_chair'`), service timer starts automatically, and token is issued.
   - If no preference and any barber is free: customer is assigned immediately to free barber (`status='in_chair'`) and service timer starts automatically.
   - If all eligible barbers are busy: customer enters waiting queue (`status='waiting'`).
5. Customer monitors `Track Token` (`/status/:id`).
6. When position reaches 2nd in line (`pos == 2`), customer receives alert: *"You are 2nd in line — Start coming to the salon!"*
7. When chair opens, customer is called / in-chair; live service timer runs.
8. Barber clicks `Complete service` -> entry marked `done`, token leaves queue.

### 2. Walk-in Customer Flow
1. Receptionist opens Reception (`/reception`) or Overview quick walk-in.
2. Enters customer details, chooses services, and selects barber preference.
3. Customer is appended to today's queue; if eligible barber is free, auto-dispatched immediately.

---

## Queue Operating Rules
1. **Queue Lifecycle**:
   - `waiting` -> `in_chair` -> `done`.
   - `waiting` -> `cancelled`.
   - `in_chair` -> `no_show` or `cancelled`.
   - Entries never move backwards.
2. **First-Come, First-Served (FIFO)**:
   - Waiting customers are strictly ordered by `created_at ASC, rowid ASC`.
3. **Barber Preference Protection**:
   - A customer who chose Barber X is **never** assigned to another barber.
   - A customer who chose 'No preference' is assigned to the first available free barber.
4. **Single-Customer Chair Lock**:
   - A barber can have only one active customer in their chair at a time (`current_entry_id`).
5. **Auto-Start Service**:
   - Once a customer is called/assigned, service starts automatically and the service timer runs immediately.
6. **One Active Token Per Phone**:
   - Duplicate active phone numbers for the same day are rejected with a notice of their existing token.
7. **No-Show Handling**:
   - If a customer does not arrive or leaves, they can be marked `no_show`.
   - If they return later, they must be registered as a new token at the end of the queue.
8. **Automated Cutoff**:
   - Online intake automatically disables 30 minutes before the configured closing time; reception walk-ins remain available.
9. **Barber Break Rules**:
   - A barber cannot take a break while an active customer is in their chair.
   - When on break, customers waiting for that barber are held until the barber returns.
10. **Waiting Time Calculation**:
    - Estimated wait = sum of remaining service durations ahead divided across eligible on-duty barbers.

---

## Test Checklist (TA Verification)
- [x] **Join with multiple services**: Combined duration and price calculated and recorded correctly.
- [x] **Duplicate phone prevention**: Joining with an existing active number shows existing token notice without creating duplicates.
- [x] **Barber preference respected**: Calling next or auto-dispatching for Barber A never takes a customer who selected Barber B.
- [x] **Automatic service start**: Calling a customer immediately transitions status to `in_chair` and starts the service timer.
- [x] **2nd-in-line alert**: Customer sees "Start coming to the salon" notification when 2nd in queue.
- [x] **Customer cancel spot**: Waiting customer can cancel their own token from the tracking screen.
- [x] **Barber view completion**: Clicking "Complete service" frees the chair and auto-dispatches the next waiting customer.
- [x] **Grace period & No-show**: Marking no-show completes the chair cycle; re-registering places them at the end of the queue.
- [x] **Intake cutoff**: Closing online queue disables registration with a clear message while keeping walk-in intake active.
- [x] **Bilingual support (EN / GU)**: Language toggle switches labels between English and Gujarati smoothly.
- [x] **Real-time synchronization**: Multi-window state across TV display, reception, and customer phone updates within 5 seconds.
