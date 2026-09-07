# Phase 11: Progressive Web App

The frontend is now installable as a Progressive Web App through:

- `frontend/public/manifest.webmanifest`
- `frontend/public/service-worker.js`
- Local ClaimCheck icon assets
- Manifest and metadata links in `frontend/index.html`
- Production-only registration in `frontend/src/main.tsx`

The service worker caches the frontend shell and same-origin static GET requests. It deliberately bypasses `/api/` requests and cross-origin requests, so product lookups and verification never use stale cached responses. Development mode does not register the worker, which keeps local iteration predictable.

Installability and offline behavior require a production build served over HTTPS (or localhost). The production build was verified locally at `http://127.0.0.1:4173`: the app rendered, the manifest and service worker returned HTTP 200, and one service-worker registration was active. A browser install prompt and Lighthouse score were not measured.
