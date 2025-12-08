# Online Coding Interview - End-to-End

Quickstart

1. Install root dev deps:

```bash
cd 02-end-to-end
npm install
npm run start
```

This runs the server on `:4000` and the client Vite dev server on `:5173` concurrently.

Server endpoints:
- `POST /session` - create session, returns `{ id }`
- `GET /session/:id` - get session info

Client:
- Open `http://localhost:5173` to access the app.
