# 2. SwiftUI with MVVM on the Observation framework

- Status: Accepted
- Date: 2026-11-26

## Context
The app is a rewrite of an Android app (Jetpack Compose, MVVM, StateFlow). We want the current Apple-native equivalent.

## Decision
- 100% SwiftUI; UIKit only if a feature requires it.
- MVVM: ViewModels are `@Observable @MainActor final class`, not `ObservableObject`.
- Swift 6 strict concurrency (`async/await`, actors).
- Clean Architecture layers in local Swift packages: `DesignSystem`, `Core`, `Data`, `Features/*`.

## Consequences
Views re-render only for the properties they read. `Core` stays framework-free and fully unit-testable.
