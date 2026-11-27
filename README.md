# The Closet Select · iOS

> **Your personal stylist, every morning.** Three office-ready outfits from the clothes you already own — matched to your colors, your day and the weather.

![Swift](https://img.shields.io/badge/Swift-6-F05138?logo=swift&logoColor=white)
![SwiftUI](https://img.shields.io/badge/SwiftUI-iOS-0A84FF?logo=apple&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-MVVM%20%2B%20Clean-black)
![Status](https://img.shields.io/badge/status-Sprint%200-D4AF37)

---

## The problem

Every morning, busy professionals lose time and energy deciding what to wear — and a big closet makes it worse. Most fashion apps solve this by selling you *more* clothes.

**The Closet Select does the opposite: it styles the closet you already have.**

## How it works

1. **Sign in** with Apple, Google or e-mail.
2. **Complete your profile** — birth date (zodiac sign) and a guided selfie + quiz that finds your **seasonal color palette** (12 seasons). The selfie is processed **on device** and never stored.
3. **Tell us about your workplace** — dress code and air conditioning.
4. **Add your clothes** — fast capture: one photo per piece, automatic background removal, AI-suggested details you confirm with one tap. Nine pieces are enough to start.
5. **Every morning at 6:30** a notification arrives: *"Your 3 looks for today are ready."* Tap it and swipe through three outfits.
6. **Every 30 days** a cycle report shows how much of your closet you wear and brings forgotten pieces back.

## Design principles: the 3 S

| | Meaning |
|---|---|
| **Simple** | One main action per screen. From app icon to today's look in ≤ 2 taps. |
| **Sexy** | Dark editorial look with gold accents, Liquid Glass, real photos of *your* clothes. |
| **Surprising** | Small moments of delight — the "golden thread" splash, outfits that assemble piece by piece, virtual color draping. Never in the user's way. |

## Tech stack

| Area | Choice |
|---|---|
| Language | Swift 6 (strict concurrency) |
| UI | SwiftUI, Liquid Glass, SF Symbols |
| Architecture | MVVM with `@Observable` + Clean Architecture (UseCases, Repositories) in local Swift packages |
| Persistence | SwiftData (offline cache) |
| Backend | Firebase Auth, Firestore, Storage, App Check, Cloud Functions |
| Platform services | WeatherKit, Vision / VisionKit, AVFoundation, Core Location, UserNotifications, StoreKit 2 |
| AI | Server-side only (Cloud Functions) — **no API keys in the app** |
| Testing | Swift Testing, XCUITest, snapshot tests — TDD, BDD and regression policy |
| Quality | SwiftLint, SwiftFormat, SonarQube Cloud, Danger |
| CI/CD | GitHub Actions + Fastlane → TestFlight / App Store |
| Localization | English (base) + Portuguese (Brazil), following the device language |

## Environments and release flow

| Environment | Branch | Bundle ID suffix | Distribution |
|---|---|---|---|
| Dev | `develop` | `.dev` | TestFlight · internal |
| QA | `qa` | `.qa` | TestFlight · QA group |
| Production | `main` | — | App Store |

```
feature/* ──PR──▶ develop ──PR──▶ qa ──PR──▶ main ──▶ App Store
```

No direct pushes. Every change goes through a pull request with green checks; QA and Production releases also require a manual deployment approval.

## Documentation

| Document | Content |
|---|---|
| [Product](docs/PRODUCT.md) | Persona, user journey, MVP scope, look engine rules |
| [Architecture](docs/ARCHITECTURE.md) | Modules, MVVM flow, data and security |
| [Engineering](docs/ENGINEERING.md) | Environments, branching, commits, CI/CD, Definition of Done |
| [Testing](docs/TESTING.md) | Test pyramid, TDD, BDD and regression policy |
| [Style guide](docs/STYLE_GUIDE.md) | Naming, language and code style |
| [Contributing](CONTRIBUTING.md) | How to work in this repository |
| [ADRs](docs/adr/) | Architecture Decision Records |
| [Features](docs/features/) | Gherkin specifications (living documentation) |

## Getting started

Requirements: macOS, Xcode 26 (the project also builds with Xcode 16), Homebrew and an Apple Developer account. Deployment target: **iOS 18** ([ADR 0005](docs/adr/0005-minimum-ios-18-progressive-enhancement.md)).

```bash
brew install xcodegen swiftlint swiftformat
xcodegen generate
open TheClosetSelect.xcodeproj
```

The `.xcodeproj` is generated from [`project.yml`](project.yml) and is not committed. To run on a device, create `Config/Local.xcconfig` (git-ignored) with your team:

```
DEVELOPMENT_TEAM = XXXXXXXXXX
```

Schemes: `TheClosetSelect-Dev`, `TheClosetSelect-QA`, `TheClosetSelect-Prod`. Each installs as a separate app.

Package tests run anywhere Swift runs:

```bash
swift test --package-path Packages/Core
swift test --package-path Packages/DesignSystem
```

## Status

Sprint 0 — repository, standards and pipeline.

## License

© 2026 Carlos Ribeiro. **All rights reserved.** The source code is public for portfolio purposes; no license is granted to copy, modify or distribute it.
