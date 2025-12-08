# Deployment to Render (Option B: separate Web Service + Static Site)

This document explains how to deploy the project to Render using two services:

- **Server**: Node web service running the Express + Socket.io server (`02-end-to-end/server`).
- **Client**: Static site built by Vite and published from `02-end-to-end/client/dist` (Render Static Site).

Summary (high-level)

1. Deploy the server as a **Web Service** (Node). Root directory: `02-end-to-end/server`.
2. Deploy the client as a **Static Site**. Root directory: `02-end-to-end/client`.
3. Configure the client build environment variable `VITE_SERVER` to point at your server's public URL.
4. Optionally configure `CLIENT_ORIGIN` on the server to restrict CORS to your client origin.

Step-by-step

1) Push your branch to GitHub (or connect your repo to Render).

2) Create the Server service on Render

- New → Web Service → Connect your repo → choose branch.
- Set the **Root Directory** to `02-end-to-end/server`.
- Environment: `Node` (no Docker required).
- Build Command: (Render will run `npm install` by default) — leave default or set `npm install`.
- Start Command: `node src/server.js`.
- Environment variables (optional):
  - `CLIENT_ORIGIN` = `https://<your-client>.onrender.com` (optional to restrict CORS; otherwise server allows any origin)

After the server deploys Render will provide a public URL like `https://your-server.onrender.com`.

3) Create the Client site on Render

- New → Static Site → Connect your repo → choose branch.
- Set the **Root Directory** to `02-end-to-end/client`.
- Build Command: `npm install && npm run build`
- Publish Directory: `dist`
- Build environment variables (important):
  - `VITE_SERVER` = `https://your-server.onrender.com` (set this to the server URL you got from step 2)

When Render builds the client it will bake `VITE_SERVER` into the build and the client will connect to the server over Socket.io.

Notes and tips

- The server now reads `process.env.CLIENT_ORIGIN` (if present) to restrict CORS. If you leave it unset the server allows all origins (useful for quick testing).
- Pyodide loads from CDN (https://cdn.jsdelivr.net). Static hosting must allow outbound network access (Render does).
- If you prefer a single service using Docker, see the `Dockerfile` in the repo (Option A). For separate services, Option B (Static + Web) is more cost-effective.

Example `render.yaml`

You can add a `render.yaml` to the repo to declare both services. Edit the placeholders before applying.

```yaml
services:
  - type: web
    name: e2e-server
    env: node
    root: 02-end-to-end/server
    buildCommand: npm install
    startCommand: node src/server.js
    envVars:
      - key: NODE_ENV
        value: production
      - key: CLIENT_ORIGIN
        value: https://your-client.onrender.com

  - type: static
    name: e2e-client
    root: 02-end-to-end/client
    buildCommand: npm install && npm run build
    publishPath: dist
    envVars:
      - key: VITE_SERVER
        value: https://your-server.onrender.com
```

You may prefer to leave `envVars` blank in `render.yaml` and set the values in the Render dashboard once services are created (this is often simpler).

Troubleshooting

- If the client cannot connect to the server, verify:
  - `VITE_SERVER` is set correctly at build time.
  - The server CORS allows the client origin (set `CLIENT_ORIGIN` accordingly).
  - Socket.io uses the same protocol (https) and the server is reachable.

Want me to prepare `render.yaml` with the placeholders filled from your Render service names? I can also prepare a `render-ci` workflow if you want GitHub Actions to automatically deploy.
