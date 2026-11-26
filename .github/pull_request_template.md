## What
<!-- One or two sentences: what does this PR change? -->

## Why
<!-- Link the issue. Use "Fixes #123" for bugs or "Closes #123" for stories. -->
Fixes #

## How to test
1.
2.

## Screenshots / video
<!-- Required when the UI changes: before / after, light and dark mode. -->

## Tests
- Acceptance scenarios (BDD) covered:
- Unit tests written first (TDD):
- Regression test (bug fixes only):

## Definition of Done
- [ ] All checks are green (build, tests, lint, Sonar Quality Gate)
- [ ] New feature: every Gherkin scenario has an acceptance test
- [ ] Domain and ViewModel code written with TDD (`test:` commit before `feat:`)
- [ ] Bug fix: regression test that failed before the fix, tagged `.regression` and `.bug`
- [ ] New screen: skeleton + `empty` and `failed` states
- [ ] Strings in the String Catalog (en + pt-BR), no hardcoded text
- [ ] Works with large Dynamic Type, VoiceOver, light and dark mode
- [ ] ADR added if the architecture changed
