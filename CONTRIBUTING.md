# Contributing

## Workflow

1. Every change starts from an **issue** (user story with Gherkin scenarios, or bug report).
2. Create a branch from `develop`:
   - `feature/TCS-<issue>-short-description`
   - `fix/TCS-<issue>-short-description`
   - `chore/…`, `docs/…`, `ci/…`
3. Work test-first (see [Testing](docs/TESTING.md)).
4. Open a pull request into `develop`. The PR title follows **Conventional Commits** — it becomes the squash commit.
5. Merge only with all checks green and conversations resolved.

## Commit messages

```
<type>(<scope>): <summary in imperative mood>

feat(today): add skeleton loading to the look card
fix(closet): keep background removal on rotated photos (#42)
test(look): reproduce #42 look generated without shoes
```

Types: `feat`, `fix`, `test`, `refactor`, `docs`, `chore`, `ci`, `perf`, `build`, `style`, `revert`.

## Before opening a PR

- Run the `Fast` test plan locally (< 1 minute).
- Run `swiftformat .` and `swiftlint`.
- Fill in the PR template, including the Definition of Done checklist.
