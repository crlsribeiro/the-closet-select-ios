# 9. Look engine, 30-day report and morning notification run on device

- Status: Accepted
- Date: 2026-11-26

## Decision
- The look engine (rules R1–R10) and the 30-day cycle report are pure Swift in the `Core` package, unit-tested with TDD (also on Linux).
- The morning notification is a **local notification** scheduled on the iPhone at the user's chosen time, with a generic message. It is rescheduled when the time or the time zone changes.
- On open, the app reads the daily color (AppSync), the weather (WeatherKit) and generates the three looks; only the short AI descriptions need the network.
- **Golden test vectors** (JSON input → expected looks) are versioned so a future Android implementation produces the same results.

## Rationale
No server job per time zone, no APNs in the MVP, works offline with the cached closet, near-zero backend cost.

## Consequences
Looks are generated per device; the chosen look is saved to the backend (`logWear`). A server-side engine can be added later by running the same `Core` package in a Swift container.
