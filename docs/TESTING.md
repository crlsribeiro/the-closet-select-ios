# Testing

## Test pyramid

| Level | Tool | Share | Runs |
|---|---|---|---|
| Unit | Swift Testing | ~55% | Every PR |
| Acceptance (BDD) | Swift Testing on ViewModels + XCUITest (Robot pattern) | — | Every PR |
| Integration | Swift Testing + Firebase Emulator Suite | ~20% | Every PR |
| Snapshot | swift-snapshot-testing (light/dark, Dynamic Type, skeleton, en/pt-BR) | ~15% | Every PR |
| UI / end-to-end | XCUITest | ~10% | PRs into `qa` and `main`, nightly |
| Accessibility | `performAccessibilityAudit()` | — | PRs into `qa` and `main` |
| Performance | `XCTMetric` (launch, memory) | — | Nightly |

Rules: no real network in unit tests; Given/When/Then naming; a flaky test is a bug — never disabled to get green.

Test plans: `Fast` (unit + snapshot, < 1 min locally), `PR`, `Regression`, `Nightly`.

## How TDD, BDD and regression fit together

```
BDD (outer loop):  user story → Gherkin scenarios → failing acceptance test
   TDD (inner loop, many times):  red → green → refactor
BDD:  acceptance test green → feature done → PR
Regression:  bug → failing test → fix → the test stays forever
```

## BDD

1. Every feature starts as a user story with Gherkin scenarios, in the issue and in [`docs/features/`](features/).
2. Each scenario becomes a test with the same name:

```swift
@Suite("Feature: Look of the day")
@MainActor
struct TodayLookAcceptanceTests {
    @Test("Scenario: Empty closet", .tags(.acceptance))
    func emptyCloset() async {
        // Given
        let sut = TodayViewModel(garments: FakeGarmentRepository(items: []))
        // When
        await sut.onAppear()
        // Then
        #expect(sut.state == .empty)
    }
}
```

3. A CI script checks that every `Scenario:` in the `.feature` files has a matching test.

## TDD

Mandatory for use cases, ViewModels, mappers and the look engine rules.

| Step | Commit |
|---|---|
| 🔴 Red — a small failing test | `test(today): expect footwear in generated look` |
| 🟢 Green — the minimum code | `feat(today): include footwear in look` |
| 🔵 Refactor — clean up, all green | `refactor(today): extract LookComposer` |

## Regression policy

> No bug is fixed without a test that failed before the fix and passes after it.

1. Issue (bug report template), e.g. #42.
2. Branch `fix/TCS-42-look-without-shoes`.
3. 🔴 Commit the test that reproduces the bug — CI shows it failing.
4. 🟢 Commit the fix.
5. PR with `Fixes #42` and the regression test name.

```swift
@Test(
    "Generated look always includes footwear",
    .tags(.regression),
    .bug("https://github.com/crlsribeiro/the-closet-select-ios/issues/42", id: 42)
)
func lookAlwaysHasFootwear() async throws { … }
```

- Regression tests live in `Tests/Regression/` folders, protected by CODEOWNERS.
- The `Regression` test plan runs on every PR.
- Danger fails a `fix/*` PR that does not touch any test.
- Visual bugs → snapshot test; flow bugs → XCUITest in `UITests/Regression/`.
