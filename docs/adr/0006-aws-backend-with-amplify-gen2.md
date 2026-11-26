# 6. AWS backend with Amplify Gen 2

- Status: Accepted
- Date: 2026-11-26
- Updates: [ADR 0004](0004-no-secrets-in-the-client.md) (the principle stays; the backend is AWS)

## Context
The backend needs authentication (e-mail, Apple, Google), per-user data, photo storage, a daily job and server-side access to third-party APIs (horoscope, LLM). Firebase would be faster to deliver and is already used by the Android app. AWS and GraphQL are requested by the job market the developer is targeting.

## Decision
Use AWS with **Amplify Gen 2** (backend defined as TypeScript code) in a separate repository, `the-closet-select-backend`:

| Concern | Service |
|---|---|
| Authentication | Amazon Cognito (e-mail/password with SES, Sign in with Apple, Google) |
| API | AWS AppSync — a **single GraphQL API**; Lambdas are exposed as custom queries/mutations |
| Data | Amazon DynamoDB, owner-scoped records |
| Photos | Amazon S3, private bucket, per-user prefix, pre-signed URLs |
| Daily job | Amazon EventBridge Scheduler → Lambda |
| Secrets | `secret()` in Amplify Gen 2 (SSM Parameter Store, SecureString) |
| CI/CD | GitHub Actions + `ampx pipeline-deploy` with GitHub OIDC (no long-lived keys) |

The app never holds third-party API keys (ADR 0004 principle).

## Consequences
- More setup than Firebase; accepted for the career goal and infrastructure-as-code practice.
- The iOS app talks to the backend only through repository protocols in the `Data` package, so the backend can be replaced without touching features.
- **Checkpoint:** a one-week spike on Sign in with Apple + Cognito (including token revocation on account deletion). If it fails, revisit this decision.
