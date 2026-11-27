# Style guide

## Language

| What | Language |
|---|---|
| Code, comments, commits, PRs, issues, technical docs | English |
| App text | String Catalog: English (base) + Portuguese (Brazil). No hardcoded strings. |

## Code style

- Swift API Design Guidelines + Airbnb Swift Style Guide.
- SwiftFormat (`.swiftformat`) formats; SwiftLint (`.swiftlint.yml`) enforces. No force unwrap, force try or force cast.
- Function body ≤ 40 lines, file ≤ 400 lines, cyclomatic complexity ≤ 10.

## Naming

| Item | Pattern | Example |
|---|---|---|
| View | `<Name>View` | `TodayView` |
| ViewModel | `<Name>ViewModel` (`@Observable @MainActor final class`) | `TodayViewModel` |
| Use case | verb + `UseCase` | `GenerateLooksUseCase` |
| Repository protocol | `<Name>Repository` | `GarmentRepository` |
| Implementation | source + name | `AppSyncGarmentRepository` |
| Test fake | `Fake` + name | `FakeGarmentRepository` |
| Tests | `<Type>Tests` | `TodayViewModelTests` |
| Localization key | `feature.screen.element` | `today.wear.button` |

## Localization

- Temperatures with `Measurement<UnitTemperature>` (°C / °F by locale), dates with `Date.FormatStyle`, prices with `Product.displayPrice`.
- Push notifications use `loc-key` / `loc-args` so the device localizes them.
- Zodiac signs, seasons, categories and colors are enums with localization keys.
