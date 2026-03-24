# Frontend Codebase Architecture Reference

This document describes how the current frontend is wired at runtime and how modules are expected to interact.

## Technology Stack

- Build tool: Vite
- UI runtime: React 18 + TypeScript
- Routing: React Router v6
- State management: Redux Toolkit + RTK Query + redux-persist
- Styling: Tailwind CSS, SCSS, styled-components, design system provider
- HTTP: Axios
- i18n: react-i18next
- Monitoring: Sentry (enabled by environment)
- Testing: Cypress (E2E + component)

## Runtime Bootstrap Flow

1. `src/main.tsx` mounts React and renders `App`.
2. `src/App.tsx` wraps routing with `AppProvider`.
3. `src/providers/AppProvider.tsx` initializes app infrastructure:
   - i18n init
   - optional Sentry init
   - Error boundary
   - Redux provider
   - Design system provider
   - Global styles + custom styles
   - styled-components theme provider
   - Browser router
4. `src/routes/Router.tsx` chooses route sets based on authentication and role checks.

## Routing and Access Model

- Route modules are split by domain (`auth.route.tsx`, `food.route.tsx`, `setting.route.tsx`, etc.).
- `Router.tsx` determines whether user is authenticated.
- If authenticated and role is SaaS Admin, admin routes are loaded; otherwise protected app routes are loaded.
- If unauthenticated and not on auth pages, user is redirected to login.
- Centralized path constants under `routes/paths` avoid string duplication.

## State Architecture

Store composition (`src/store/index.ts`):

- API slices:
  - `publicApiSlice`
  - `protectedApiSlice`
- UI and app slices:
  - `global`
  - `drawer`
- Auth and permissions:
  - `auth` (persisted)
  - `rbac`

Patterns in use:

- RTK Query for server-state and API middleware.
- Standard Redux slices for client-side UI/app state.
- `redux-persist` to keep auth session data across reloads.
- Selectors are separated under `store/selectors`.

## Layered Module Boundaries

Suggested interpretation of current boundaries:

- App shell layer:
  - `main.tsx`, `App.tsx`, `providers`, `styles`
- Platform/config layer:
  - `config`, `common/constants`
- Domain layer:
  - `features`, `pages`, domain route files
- Shared layer:
  - `common`, `components`, shared hooks/utils/interfaces
- Data layer:
  - `store/api.ts`, feature APIs, axios setup

## Feature Module Pattern (Reference)

A feature folder in `src/features` is intended to act like a mini application boundary. For reuse in your own project, keep this internal shape:

```text
features/<feature-name>/
|-- components/
|-- hooks/
|-- slices/ or store/
|-- services/ or apis/
|-- constants/
|-- interfaces/ and types/
`-- pages/ (optional)
```

## Practical Blueprint For Your Own Project

Use this sequence to replicate the architecture:

1. Create base folders: `assets`, `common`, `components`, `config`, `features`, `pages`, `providers`, `routes`, `store`, `styles`.
2. Implement root provider composition (error boundary, store, theme, router).
3. Create route constants first, then route modules per domain.
4. Set up RTK Query public/protected API clients and core slices.
5. Keep reusable utilities in `common`; keep domain logic in `features`.
6. Map each top-level route to one page container in `pages`.
7. Add Cypress structure early for E2E/component tests.

## Architecture Strengths To Reuse

- Clear separation between shared utilities and domain modules.
- Route composition by domain instead of one monolithic router file.
- Consistent provider-based app bootstrap.
- Role-aware routing decision path.
- Scalable Redux Toolkit setup with API middleware and persistence.

## Areas You Can Improve In A New Project

- Enforce naming consistency between feature and page folders.
- Define strict import boundaries (lint rules) between layers.
- Add architecture decision records (ADRs) for routing/state choices.
- Add per-feature README files for onboarding speed.
