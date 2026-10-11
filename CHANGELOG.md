markdown
CHANGELOG.md
# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-10-02

### Added
- Member management: register, login, profile update, deactivate
- Product management: add, edit, withdraw products with per-unit and per-kg pricing
- Round management: create rounds with open/closed/packed states
- Order management: place, edit, cancel orders during open round
- Order aggregation: coordinator views all orders and product totals
- Packing sheet: printable sheet organized by crate number with bay locations
- Core pricing logic: correct per-unit and per-kg calculation with price locking
- Automated tests for pricing logic (pytest)
- Configuration management: .env.example, requirements.txt, .gitignore, README
