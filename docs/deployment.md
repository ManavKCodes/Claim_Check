# Phase 15: Deployment and Finalization

## Local production stack

The repository includes a PostgreSQL, FastAPI, and Nginx frontend Compose profile:

```powershell
docker compose up --build
```

- Frontend: `http://localhost:8080`
- Backend: `http://localhost:8000`
- Backend health: `http://localhost:8000/health`
- PostgreSQL: `localhost:5432`

The frontend Docker build accepts `VITE_API_URL`. Hosted deployments must set this to the public HTTPS backend URL and set backend `ALLOWED_ORIGINS` to the public frontend origin. Replace the local PostgreSQL password and configure a contact-bearing Open Food Facts User-Agent before deployment.

## Hosting plan

Deploy the backend container and PostgreSQL on a managed container platform, and deploy the frontend container or static `frontend/dist` output behind HTTPS. Configure environment variables through the platform secret/config store. Do not commit `.env` files or credentials.

## Deployment gates

1. Install dependencies and run backend tests.
2. Run frontend typecheck, build, and Playwright tests.
3. Verify `/health`, CORS, database connectivity, and PWA manifest over HTTPS.
4. Verify FSSAI rule source versions before enabling any production threshold.
5. Populate and quality-check the manual benchmark before publishing metrics.

No hosted URL or GitHub deployment is claimed in this repository. Credentials and a target hosting account were not supplied.
