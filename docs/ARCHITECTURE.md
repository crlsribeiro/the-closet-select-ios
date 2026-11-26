# Architecture

## Overview

MVVM + Clean Architecture, split into **local Swift packages** so that each layer can be built and tested in isolation.

```
TheClosetSelect/
├── App/                      # @main, dependency container, Router, environment config
├── Packages/
│   ├── DesignSystem/         # colors, typography, components, skeleton, animations
│   ├── Core/                 # domain models, repository protocols, use cases, look engine
│   ├── Data/                 # Firebase, WeatherKit, AI gateway, SwiftData
│   └── Features/
│       ├── Onboarding/       # splash, sign in, profile, color analysis, workplace
│       ├── Today/            # three looks carousel, daily energy card
│       ├── Closet/           # closet grid, fast capture, garment detail
│       ├── Palette/          # seasonal palette
│       └── Profile/
├── Widgets/                  # widget + Live Activity "look of the day"
└── Config/                   # Dev.xcconfig, QA.xcconfig, Prod.xcconfig
```

Dependency direction: `Features → Core ← Data`. `Core` imports no Apple UI framework and no Firebase.

## Feature flow

```
View (SwiftUI) ──reads──▶ ViewModel (@Observable, @MainActor)
                              │ calls
                              ▼
                          UseCase (struct, pure, testable)
                              │ uses protocol
                              ▼
                          Repository (Firestore · WeatherKit · AI gateway · SwiftData)
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

| Concern | Choice |
|---|---|
| Auth | Firebase Auth: e-mail/password, Sign in with Apple, Google |
| Data | Firestore (user profile, garments, daily looks, wear history) |
| Images | Firebase Storage (garment photos with background removed) |
| Offline | SwiftData cache of closet and today's looks |
| Daily looks | Scheduled Cloud Function per time zone: weather + daily color + look engine → Firestore → APNs |
| Weather | WeatherKit (REST on the server, native on device) |
| AI | Cloud Function gateway, protected by Auth + App Check. Receives the user locale and returns text in that language. |

## Security and privacy

- **No third-party API keys in the app.** All AI and external APIs are called server-side.
- Firebase App Check on every backend call.
- Selfie for color analysis is processed **on device** (Vision) and never uploaded or stored; only derived values (skin tone hex, season) are saved.
- Per-environment Firebase projects; config files are injected by CI and never committed.
- LGPD / GDPR: explicit consent screens, data export and account deletion.
