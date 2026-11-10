# Step 2 — Push to GitHub and deploy

**Goal:** code is on GitHub, and both apps are live on Vercel (the assignment allows Vercel or Heroku — Vercel is free and handles Python + React).

Two Vercel projects, one GitHub repo:
- `backend/` → FastAPI (Python) app
- `frontend/` → React (Vite) app, points at the backend URL

---

## 1. Push to GitHub

The remote is already configured (`origin` → your `uk-wind-dashboard` repo):

```bash
git push -u origin main
```

Then open the repo and check the files are there.

### Make the repo anonymous (assignment asks for a random name)

1. GitHub → your repo → **Settings** → **General** → **Repository name** → rename it to a random string, e.g. `qzk7r2m`.
2. Point your local clone at the new URL:
   ```bash
   git remote set-url origin https://github.com/<your-username>/qzk7r2m.git
   ```

Also confirm: **Public** visibility, and `git status` shows no `.env` or secrets committed.

---

## 2. Deploy the backend (Vercel)

1. Go to <https://vercel.com/new> and sign in with GitHub.
2. Import your repo.
3. Settings on the import screen:
   - **Root Directory:** `backend` (click *Edit* and select it)
   - **Framework Preset:** should auto-detect **FastAPI**
   - Leave build/output settings empty
4. **Deploy**.

Vercel looks for a FastAPI `app` object at `app/main.py` (inside `src/`, `app/` or `api/`), installs `requirements.txt`, and sends every request to FastAPI. No `vercel.json` needed.

Check:
```
https://<backend-project>.vercel.app/api/health   ->  {"status":"ok"}
https://<backend-project>.vercel.app/docs         ->  Swagger UI
```

**If it returns 404**, force the entrypoint — add `backend/pyproject.toml`:
```toml
[project]
name = "wind-backend"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi", "uvicorn", "httpx"]

[tool.vercel]
entrypoint = "app.main:app"
```
then commit, push, redeploy.

> Vercel's Python runtime defaults to 3.12. Your local 3.14 code is compatible; if you later add a package, check it installs on 3.12.

---

## 3. Deploy the frontend (Vercel)

1. <https://vercel.com/new> → import the **same repo** again (separate project).
2. Settings:
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite (auto-detected)
   - **Environment Variable:** `VITE_API_URL` = `https://<backend-project>.vercel.app`
3. **Deploy**, then open `https://<frontend-project>.vercel.app`.

It should show **Backend status: ok**.

Why the env var: locally the Vite dev server proxies `/api` to `localhost:8000`; on Vercel the two apps are separate domains, so the browser calls the backend directly. The backend already allows `https://*.vercel.app` origins (CORS).

---

## 4. Verify like the grader will

Open both links in an **incognito window** (the assignment requires this check):
- [ ] Frontend loads and shows `ok`
- [ ] `backend.vercel.app/api/health` returns JSON
- [ ] Repo is public and opens in incognito
- [ ] Renaming the repo did not break the Vercel projects (if it does, re-link in Vercel → Settings → Git)

---

## 5. Later deploys

Every `git push` to `main` redeploys both projects automatically. Nothing else to do.

---

## Notes

- The **Docker** setup stays for local development and for the repo requirement; Vercel does not use it.
- Heroku works too but has no free tier, so Vercel is the cheaper route to the same "deployed app" requirement.
