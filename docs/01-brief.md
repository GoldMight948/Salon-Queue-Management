# Salon Queue — Project Brief & Scope

## Problem
On busy salon days and weekends, customers often wait 1 to 2 hours without clear visibility into their turn or estimated wait times. This causes congestion in waiting areas, customer drop-offs, and disputes regarding queue priority.

## Users
1. **Customer**: Joins queue remotely or upon arrival, tracks queue position, and monitors live wait times.
2. **Receptionist / Salon Staff**: Registers walk-in customers, monitors chairs, auto-dispatches waiting customers, and handles no-shows.
3. **Barber**: Sees current customer in their chair, tracks live service elapsed time, and completes services.
4. **Owner / Manager**: Configures service catalogs (durations and prices), controls barber roster availability, and manages online queue intake hours.

## Must-Have Features
1. **Remote & Walk-in Queue Entry**: Customers join from their mobile device or reception, selecting up to 3 services and an optional preferred barber (or 'Any free barber').
2. **Auto-Assignment & Auto-Start**: If the selected barber (or any barber) is free, the customer is assigned immediately and the service timer starts automatically.
3. **Live Status Tracking**: Customers track their queue position, live wait timer, 2nd-in-line arrival prompt ("Start coming to the salon"), and turn alerts.
4. **Reception Dashboard**: Live team availability, automated customer dispatch, manual call next, walk-in registration, and no-show management with grace periods.
5. **Barber Chair View**: Shows active customer, real-time service elapsed timer against service duration, break controls, and completion actions.
6. **Waiting-Area TV Display**: High-contrast display showing currently serving barbers and the next 5 tokens with automatic 5-second refreshes.
7. **Salon Settings**: Real-time management of active services, pricing, barber duty status, daily intake cutoffs, and daily activity CSV exports.
8. **Bilingual Support**: English and Gujarati (EN/GU) interface toggle for regional accessibility.

## Don't-Build List
- Online payment gateways or pre-authorizations
- Future-date appointment calendar bookings (same-day live queue only)
- Paid SMS/WhatsApp commercial gateway integrations
- Customer loyalty programs and multi-branch franchise management

## Look & Feel
Modern, minimal salon aesthetic: clean white and soft slate backgrounds (#F8F9FA), deep indigo accents (#171A2B), muted slate tags (#515A70), soft border radii (12-14px), monospace timer badges, responsive layouts, and zero unnecessary decorative emoji clutter.
