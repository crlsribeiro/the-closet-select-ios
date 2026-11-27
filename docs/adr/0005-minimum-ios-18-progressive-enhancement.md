# 5. Minimum iOS 18 with progressive enhancement for iOS 26

- Status: Accepted
- Date: 2026-11-26

## Context
iOS 26 introduces Liquid Glass and new APIs, but it drops iPhone XS, XS Max and XR, and not every user updates right away. Companies usually support the current iOS version plus one or two previous versions.

## Decision
- Deployment target: **iOS 18.0**.
- Features that need iOS 26 are added as **progressive enhancement** and isolated in `DesignSystem`. Example: `auraGlass()` uses Liquid Glass (`glassEffect`) on iOS 26 and `.ultraThinMaterial` on iOS 18.
- Feature code never calls `#available` for visual APIs; it uses DesignSystem modifiers.
- AI runs server-side, so the iOS 26 on-device Foundation Models framework is not required.
- CI and snapshot tests cover both iOS 18 and iOS 26 simulators.

## Consequences
Wider device reach and realistic backward-compatibility practice. A small amount of fallback code lives in DesignSystem. Revisit the minimum version before launch using Apple's published adoption figures.
