# Architecture

## Overview

MVVM + Clean Architecture, split into **local Swift packages** so that each layer can be built and tested in isolation.

```
TheClosetSelect/
├── App/                      # @main, dependency container, Router, environment config
├── Packages/
│   ├── DesignSystem/         # colors, typography, components, skeleton, animations
│   ├── Core/                 # domain models, repository protocols, use cases, look engine
│   ├── Data/                 # Apollo GraphQL, Amplify Auth/Storage, WeatherKit, SwiftData
│   └── Features/
│       ├── Onboarding/       # splash, sign in, profile, color analysis, workplace
│       ├── Today/            # three looks carousel, daily energy card
│       ├── Closet/           # closet grid, fast capture, garment detail
│       ├── Palette/          # seasonal palette
│       └── Profile/
├── Widgets/                  # widget + Live Activity "look of the day"
└── Config/                   # Dev.xcconfig, QA.xcconfig, Prod.xcconfig
```

Dependency direction: `Features → Core ← Data`. `Core` imports no Apple UI framework and no backend SDK.

## Feature flow

```
View (SwiftUI) ──reads──▶ ViewModel (@Observable, @MainActor)
                              │ calls
                              ▼
                          UseCase (struct, pure, testable)
                              │ uses protocol
                              ▼
                          Repository (AppSync GraphQL · WeatherKit · S3 · SwiftData)
```

## Screen state

Every screen exposes one state value and renders all five cases:

```swift
enum ViewState<Value: Sendable>: Sendable {
    case idle
    case loading
    case loaded(Value)
    case empty
    case failed(AppError)
}
```

Loading is shown with a **skeleton** that mirrors the real layout (`.skeleton(isActive:)` in DesignSystem): shown only after 300 ms, kept at least 400 ms, gold shimmer disabled with Reduce Motion, hidden from VoiceOver. Cached data (SwiftData) is shown first and refreshed silently.

## Dependency injection

Protocol-based, injected through initializers and a small container exposed via SwiftUI `@Environment`. Tests use `Fake…Repository` types; no network in unit tests.

## Navigation

`NavigationStack` with a typed `NavigationPath` owned by a `Router`. Deep links (e.g. tapping the morning notification) resolve to routes.

## Data and backend

AWS, defined as code with Amplify Gen 2 in `the-closet-select-backend` ([ADR 0006](adr/0006-aws-backend-with-amplify-gen2.md)), single region us-east-1 ([ADR 0007](adr/0007-single-region-us-east-1.md)).

```
iPhone ── Apollo iOS (GraphQL) ──▶ AppSync ──▶ DynamoDB (owner-scoped)
   │                                  └──▶ Lambda (daily color, look descriptions, account deletion/export)
   ├── Amplify Auth ───────────────▶ Cognito (e-mail, Apple, Google)
   ├── Amplify Storage ────────────▶ S3 (private, pre-signed URLs)
   └── WeatherKit · Vision · local notification · SwiftData cache
EventBridge Scheduler ──▶ Lambda ──▶ DailyColor (12 signs per day)
```

| Concern | Choice |
|---|---|
| Auth | Cognito: e-mail/password, Sign in with Apple, Google |
| API | Single GraphQL API (AppSync); Lambdas exposed as custom queries/mutations |
| Data | DynamoDB: User, Garment, Look (`garmentIds`), WearEvent, DailyColor. `logWear` updates the event and garment counters atomically |
| Photos | S3 private bucket, per-user prefix, HEIC 1024 px + 300 px thumbnail, pre-signed URLs |
| Look engine and 30-day report | On device, in `Core` ([ADR 0009](adr/0009-on-device-look-engine-and-local-notification.md)) |
| Morning notification | Local notification at the user's chosen time |
| Weather | WeatherKit on device |
| AI descriptions | Lambda (Bedrock or external provider), per-user quota and cache, in the user's locale |
| Offline | SwiftData cache of closet and today's looks |

## Security and privacy

- **No third-party API keys in the app.** All AI and external APIs are called server-side.
- Every API call is authenticated with Cognito; authorization rules are owner-based and covered by cross-user tests.
- Selfie for color analysis is processed **on device** (Vision) and never uploaded or stored; only derived values (skin tone hex, season) are saved.
- Per-environment backend configuration (`amplify_outputs.json`) is injected by CI and never committed.
- LGPD / GDPR: explicit consent, data export and account deletion (including Sign in with Apple token revocation). Logs contain no personal data.
