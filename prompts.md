# Prompts Log — Salon Queue Management System

This document logs the development prompts executed during the vibe coding lab in sequence.

## Prompt 1: Initial Setup & Workspace Review
> Review project structure, SQLite schema, and Streamlit workspaces including Overview, Join Queue, Reception, Barber Desk, Live Display, Admin Settings, and Track Token.

## Prompt 2: Fix Quick Actions & Navigation
> Make the quick actions at the front page work, have the timer for the waiting customer work, automatically add the customer to their selected barber if one otherwise add them to any free barber.
- Fixed widget synchronization by implementing direct callback navigation (`on_click=set_workspace`).
- Implemented automated barber assignment logic matching preferred barbers when free and load-balancing non-preferred customers.
- Integrated queue dispatch upon service completion.

## Prompt 3: Minimalist Refinement & Navigation Hardening
> Make the quick actions buttons work, remove the emojis added for the site to look minimal.
- Converted all front-page actions and tracking triggers to native Streamlit callbacks.
- Removed all decorative emojis across views, badges, headers, buttons, and tables.
- Styled clean monochrome monospace timer pills and high-contrast badges.

## Prompt 4: Automatic Service Start on Call
> Once customer is called, start service and timer automatically.
- Updated queue transition logic so that calling an entry immediately transitions it to `in_chair`.
- Set both `called_at` and `started_at` simultaneously.
- Started the live in-service elapsed timer immediately without requiring manual "Start service" button clicks.

## Prompt 5: TA Handout Compliance & Verification
> Go through these requirements to confirm everything is covered.
- Audited implementation against `docs/01-brief.md`, `docs/02-screens.md`, and `docs/03-flows-rules.md`.
- Added multi-select service support (max 3) with live duration/price calculation in Join Queue.
- Added 2nd-in-line alert banner ("Start coming to the salon") in Track Token.
- Added customer self-cancellation button ("Cancel my spot") in Track Token.
- Implemented English / Gujarati (EN/GU) language toggle.
- Created all required documentation deliverables for MSc IT submission.

## Prompt 6: Ergonomic Button Placement & Intuitive Layout Redesign
> Can you place the buttons on the website more intuitively? Do all.
- Re-architected button placements into contextual action bars.
- Implemented inline quick walk-in drawer on the Overview page.
- Converted Reception dashboard into a responsive 2-column tablet layout.
- Added full-width 48px touch targets for Barber Desk chairs.
- Enclosed destructive cancellations in safe 2-step confirmation dialogs.
- Bound all workspace navigation buttons to instant state callbacks.

## Prompt 7: Integration of Deluxe Saloon Audio (saloon.wtf)
> https://saloon.wtf/ Any chance you can integrate this in the website? 2 and 4.
- Integrated ambient radio player into Screen 6 (Waiting Area Live TV Display) with persistent un-interrupted streaming outside the 5s queue sync fragment.
- Implemented global floating corner pill button (`Radio · Saloon Radio` / `Radio · સલૂન રેડિયો`) at the bottom right corner with slide-up popover drawer.
- Embedded retro 90s Indian barber shop melodies via native Streamlit `st.iframe`.
- Added complete bilingual English / Gujarati translations for all audio player controls and headings.

## Prompt 8: Custom Floating Vinyl Player Pill with Autoplay
> maybe convert 2nd into a floating pill at the bottom right with a rotating canvas, play button forward and backward something like the screenshot uploaded and have it autoplay
- Extracted 32 authentic tracks from saloon.wtf with album art covers, titles, artists, and audio stream links.
- Built a floating capsule/pill player at the bottom right viewport (`floating_player.html`).
- Replicated screenshot layout: rotating vinyl album disc with center cutout hole, song metadata, progress scrubber with elapsed/total time, previous button, circular white play/pause toggle, and next button.
- Integrated continuous playback with YouTube IFrame API and AAC audio fallback, automatic autoplay, and seamless next-track looping.
