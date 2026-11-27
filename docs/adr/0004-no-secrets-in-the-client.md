# 4. No third-party secrets in the client

- Status: Accepted — implementation updated by [ADR 0006](0006-aws-backend-with-amplify-gen2.md) (AWS instead of Firebase)
- Date: 2026-11-26

## Context
The Android version shipped AI and weather API keys inside the app binary, where they can be extracted.

## Decision
The iOS app holds no third-party API keys. AI, horoscope and other external APIs are called from Cloud Functions protected by Firebase Auth and App Check. Weather uses WeatherKit.

## Consequences
Every AI feature needs a backend endpoint. Keys can be rotated without an app release.
