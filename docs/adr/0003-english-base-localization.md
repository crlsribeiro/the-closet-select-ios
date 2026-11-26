# 3. English as the base language

- Status: Accepted
- Date: 2026-11-26

## Context
The first market is Brazil, but the product should be ready for other markets.

## Decision
English is the development language. Portuguese (Brazil) is a localization. The app follows the device language and falls back to English. All strings live in the String Catalog.

## Consequences
CI fails on missing translations. Tests run in both `en-US` and `pt-BR`.
