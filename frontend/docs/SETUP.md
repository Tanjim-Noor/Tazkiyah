# Frontend Setup

## Environment
Create `.env.local` in `frontend/` as needed:

```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Commands

```
npm install
npm run dev
npm run lint
npm run typecheck
npm run build
```

## Backend Dependency
Backend should be running for integration tests:
- `GET /health`
- `GET /api/v1/config`
- `POST /api/v1/chat`
- `POST /api/v1/chat/sync`
