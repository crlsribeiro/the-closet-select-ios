# 8. Apollo iOS for GraphQL, Amplify only for Auth and Storage

- Status: Accepted
- Date: 2026-11-26

## Decision
- GraphQL operations are written as `.graphql` files and compiled into typed Swift code by **Apollo iOS**, which talks to AppSync with a Cognito token interceptor.
- **Amplify Swift** is used only for Auth (Cognito) and Storage (S3 pre-signed URLs).
- Both live in the `Data` package behind repository protocols.

## Rationale
Typed operations checked at compile time, fewer generated models to maintain, better fit with Swift 6 strict concurrency, and Apollo is the GraphQL client most requested in iOS job posts.

## Consequences
GraphQL subscriptions (not needed in the MVP) would require AppSync's real-time protocol.
