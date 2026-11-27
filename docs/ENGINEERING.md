# Engineering

## Environments

| | Dev | QA | Production |
|---|---|---|---|
| Branch | `develop` | `qa` | `main` |
| Bundle ID | `….closetselect.dev` | `….closetselect.qa` | `….closetselect` |
| App icon | "DEV" ribbon | "QA" ribbon | official |
| Backend environment | Amplify `develop` | Amplify `qa` | Amplify `main` |
| Distribution | TestFlight · internal | TestFlight · QA group | App Store |
| Gate | PR checks | PR checks + environment approval | PR checks + environment approval |

Each environment is an Xcode build configuration + scheme with its own `.xcconfig`, so the three apps can be installed side by side.

## Branching

```
feature/TCS-12-skeleton-home
        │  PR → green checks
        ▼
   develop ──────▶ CI ships a DEV build to TestFlight
        │  PR "Release 1.2.0 → QA"
        ▼
      qa ─────────▶ approval → CI ships a QA build to TestFlight
        │  PR "Release 1.2.0 → Production"
        ▼
     main ────────▶ approval → tag v1.2.0 → App Store review
```

- Rulesets on `main`, `qa`, `develop`: pull request required, required status checks, conversations resolved, no force push, no deletion.
- Hotfix: `hotfix/*` from `main`, merged back through PRs into `main` **and** `develop`.
- Merge strategy: **squash only**, commit message = PR title.

## Commits and versions

- Conventional Commits, enforced on the PR title.
- Semantic Versioning (`MAJOR.MINOR.PATCH`); build number set by CI.
- Changelog generated from commits on every release.

## CI/CD

| Workflow | Trigger | Jobs |
|---|---|---|
| `pr.yml` | Every PR | Conventional title, secrets scan, SwiftLint, package tests (Linux), app build and tests (iOS simulator), coverage and SonarQube Cloud Quality Gate |
| `deploy-dev.yml` | Merge into `develop` | Fastlane → TestFlight (Dev) |
| `deploy-qa.yml` | Merge into `qa` | Environment approval → Fastlane → TestFlight (QA) |
| `release.yml` | Merge into `main` | Environment approval → Fastlane → App Store Connect |

Tools: GitHub Actions (macOS runners), Fastlane + match for signing, Danger for PR hygiene, Dependabot.

## Quality gate (SonarQube Cloud, new code)

| Metric | Target |
|---|---|
| Coverage | ≥ 80% |
| Duplication | ≤ 3% |
| New bugs / vulnerabilities | 0 |
| Security hotspots reviewed | 100% |
| Maintainability rating | A |

## Definition of Done

- All checks green (build, tests, lint, Sonar)
- New feature: every Gherkin scenario has an acceptance test
- Domain and ViewModel code written with TDD
- Bug fix: regression test that failed before the fix
- New screen: skeleton + `empty` and `failed` states
- Strings in the String Catalog (en + pt-BR)
- Large Dynamic Type, VoiceOver, light and dark mode
- Screenshot or video in the PR when the UI changes
- ADR when the architecture changes
