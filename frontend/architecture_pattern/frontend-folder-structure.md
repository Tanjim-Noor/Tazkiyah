# Frontend Folder Structure Reference

This document captures the current frontend folder organization so it can be reused as a reference architecture.

## Repository Root (High-Level)

```text
.
|-- cypress/
|   |-- e2e/
|   |-- fixtures/
|   |-- support/
|   `-- videos/
|-- docker/
|-- eks/
|-- public/
|-- src/
|-- bitbucket-pipelines.old.yml
|-- bitbucket-pipelines.yml
|-- cypress.config.ts
|-- index.html
|-- latest_changes.txt
|-- package.json
|-- postcss.config.js
|-- README.md
|-- tailwind.config.js
|-- tsconfig.json
|-- tsconfig.node.json
`-- vite.config.ts
```

## Source Folder Layout

```text
src/
|-- assets/
|   |-- icons/
|   |   |-- fill/
|   |   `-- outline/
|   `-- images/
|       |-- app-images/
|       `-- login-images/
|-- common/
|   |-- apis/
|   |-- constants/
|   |-- hooks/
|   |-- interfaces/
|   |-- types/
|   `-- utils/
|-- components/
|   |-- error/
|   |-- layouts/
|   `-- partials/
|-- config/
|-- features/
|   |-- AppCenter/
|   |-- auth/
|   |-- BillModule/
|   |-- child-organization/
|   |-- child-organization-invite/
|   |-- clientFoodManagenent/
|   |-- employee-list/
|   |-- foodManagement/
|   |-- leave/
|   |-- Organization/
|   `-- setting/
|-- locales/
|   `-- en/
|-- pages/
|   |-- AppCenter/
|   |-- auth/
|   |-- BillModule/
|   |-- child-organization/
|   |-- employeeList/
|   |-- Food/
|   |-- FoodRequest/
|   |-- leave/
|   |-- Organization/
|   |-- Overview/
|   `-- setting/
|-- providers/
|-- routes/
|   `-- paths/
|-- store/
|   |-- selectors/
|   `-- slices/
|-- styles/
|-- App.cy.tsx
|-- App.tsx
|-- main.tsx
|-- styled.d.ts
|-- svg.d.ts
`-- vite-env.d.ts
```

## Folder Roles

- `assets`: Static resources (icons, images).
- `common`: Cross-cutting reusable code (constants, hooks, interfaces, utilities).
- `components`: Shared presentational and layout components.
- `config`: App-level initialization and configuration (axios, i18n, sentry, theme).
- `features`: Domain-oriented feature modules with internal structure.
- `locales`: Translation dictionaries.
- `pages`: Route-level page containers.
- `providers`: Root providers and app bootstrapping wrappers.
- `routes`: Route definitions, protected-route flow, and path contracts.
- `store`: Redux Toolkit store, slices, selectors, and RTK Query API slices.
- `styles`: Global and theme styling.

## Naming and Organization Patterns

- Domain folders in `features` and `pages` are mostly business-oriented.
- `common` is intended as a reusable shared layer independent from feature modules.
- `routes/paths` centralizes route constants to avoid hardcoded paths.
- State is a mix of global slices, feature slices, and API slices via RTK Query.
