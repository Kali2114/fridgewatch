# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [1.0.0] - 2026-09-16

v1: a deployable fridge inventory tracker with auth, an expiry dashboard, and daily email reminders.

### Added

- **Fridge inventory**: full CRUD for items (name, quantity, added date, expiry date) via `POST/GET/PUT/DELETE /items`, backed by SQLite through SQLAlchemy. Each item belongs to its owner — reading, updating, or deleting another user's item returns 404, not just a permission error, so item ids can't be used to probe what other users have.
- **Accounts**: `POST /auth/register` and `POST /auth/login`, passwords hashed with bcrypt, JWT access tokens for authenticated requests. A duplicate email on registration returns 409; a bad login (unknown email or wrong password) returns a generic 401 either way, so one can't be distinguished from the other.
- **Expiry dashboard**: items come back sorted soonest-to-expire first, each tagged `fresh` / `expiring_soon` / `expired`. A single-page web UI (`static/index.html`, no framework — plain HTML/CSS/JS) covers registration, login, and a traffic-light list of what's in the fridge, with quick add/delete.
- **Daily reminder email**: a background job runs once a day, finds everything expiring within 2 days across all users, and emails each affected user a summary.
- Config via environment variables (`.env`, see `.env.sample`) for the JWT secret and SMTP credentials.

### Infrastructure

- Pre-commit hooks (ruff, black, hygiene checks) and GitHub Actions CI (lint + test on every push/PR).
- Test suite: 78 tests, 100% line coverage.
