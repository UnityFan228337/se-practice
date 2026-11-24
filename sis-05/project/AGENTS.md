# AGENTS.md — Smart Campus Room Availability Checker

Instructions for any coding agent working in this project. Read this file before you change
anything, and follow it over any general habit of yours.

## Purpose

A React + TypeScript page (Vite) that tells a student whether a campus room is free for a
requested time. The booking rule lives in `src/booking.ts` (`canBook`); the page is `src/App.tsx`;
the tests are in `src/booking.test.ts`.

Use one fictional room and fictional bookings only; do not use real KBTU data, names or timetables.

## Architecture

- `src/booking.ts`: booking validation and availability result types.
- `src/App.tsx`: React UI and conversion of time inputs to minutes.
- `src/booking.test.ts`: Vitest behaviour tests.
- `src/main.tsx` and `src/index.css`: app entry point and styles.
- `package.json` and `package-lock.json`: scripts and pinned dependency versions.

## Setup

Run `npm ci` from `sis-05/project/`, then use the commands below.

## Safe commands

- Install only after review: `npm ci`
- Dev server: `npm run dev`
- Tests: `npm test`
- Lint/type check: `npm run lint`
- Build: `npm run build`

## Coding conventions

- Use TypeScript with explicit types for exported data structures.
- Keep availability rules in `src/booking.ts`, not in React components.
- Preserve the existing acceptance contract and do not add persistence or external services.
- Keep changes focused and review every dependency or generated-file change.

## Test expectations

- Preserve AC1-AC6.
- Run `npm test` and `npm run build` before accepting a change.
- Add a focused test for changed availability behaviour.
- Do not claim a test passes unless its real output was observed.

## Forbidden actions

- Never commit secrets, credentials, API keys, passwords or `.env` files.
- Never deploy to production or publish a release automatically.
- Never run destructive commands such as `rm -rf`, `git reset --hard`, or forced resets.
- Never change dependencies or the lockfile without human review.
