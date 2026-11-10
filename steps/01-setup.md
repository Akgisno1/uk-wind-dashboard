# Step 1 — One repo: React frontend + FastAPI backend + Docker

> **Status: done.** This scaffold is already built and committed, and verified with `docker compose up`. The doc below explains how it is put together.

**Goal of this step:** one git repo, two apps in it, both running locally and in Docker, and a health check proving they talk to each other. No Elexon data yet.

---

## 0. Final structure (what you are aiming at)

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── .dockerignore
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/          <- created by Vite
│   ├── src/App.jsx
│   ├── nginx.conf
│   ├── Dockerfile
│   └── vite.config.js
├── steps/
├── .gitignore
├── assignment.md
└── docker-compose.yml
```

One repo, two folders. Never a second `git init` inside `backend/` or `frontend/`.

---

## 1. Clean the current repo (one time only)

The repo already exists and the old scaffold is deleted in the working tree. Save that state as the starting point:

```bash
git add -A
git commit -m "chore: remove old scaffold, keep assignment brief"
```

---

## 2. Backend (FastAPI)

```bash
mkdir -p backend/app
touch backend/app/__init__.py
```

`backend/requirements.txt`
```
fastapi
uvicorn
httpx
```
(`httpx` is what will call Elexon later. Plain `uvicorn` keeps the Docker build small and avoids compiled extras — `[standard]` needs a compiler if a wheel is missing. Pin exact versions with `pip freeze` once things work.)

`backend/app/main.py`
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Wind Forecast Portal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}
```

Run it:
```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate      # Windows Git Bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Check: <http://localhost:8000/api/health> → `{"status":"ok"}`, and <http://localhost:8000/docs> opens.

---

## 3. Frontend (React via Vite)

From the **repo root**:

```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

`frontend/vite.config.js` — dev server forwards `/api` to FastAPI, so frontend code never hardcodes `localhost:8000`:
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: { '/api': 'http://localhost:8000' },
  },
})
```

`frontend/src/App.jsx`
```jsx
import { useEffect, useState } from 'react'

const API = import.meta.env.VITE_API_URL || ''

export default function App() {
  const [status, setStatus] = useState('loading...')

  useEffect(() => {
    fetch(`${API}/api/health`)
      .then((r) => r.json())
      .then((d) => setStatus(d.status))
      .catch(() => setStatus('backend not reachable'))
  }, [])

  return <h1>Backend status: {status}</h1>
}
```

Run it (`cd frontend && npm run dev`), open <http://localhost:5173> → shows **ok**.

> Keep `VITE_API_URL` support from day one: on Vercel the frontend and backend are separate apps, so you only set this env var instead of rewriting code.

---

## 4. Docker

`backend/Dockerfile`
```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

`backend/.dockerignore`
```
.venv
__pycache__
*.pyc
```

`frontend/Dockerfile` — build React, then serve the static files with nginx:
```dockerfile
FROM node:24-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

`frontend/nginx.conf`
```nginx
server {
    listen 80;

    location /api/ {
        proxy_pass http://backend:8000;
    }

    location / {
        root /usr/share/nginx/html;
        try_files $uri /index.html;
    }
}
```

`frontend/.dockerignore`
```
node_modules
dist
```

`docker-compose.yml` (repo root)
```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    ports:
      - "5173:80"
    depends_on:
      - backend
```

Run the whole thing:
```bash
docker compose up --build
```
- <http://localhost:5173> → **backend status: ok** (through nginx proxy)
- <http://localhost:8000/api/health> → `{"status":"ok"}`

---

## 5. Root `.gitignore`

```
node_modules/
dist/
.venv/
__pycache__/
*.pyc
.env
.DS_Store
```

---

## 6. Commit

```bash
git add -A
git commit -m "feat: scaffold React frontend and FastAPI backend with Docker"
```

---

## Done when

- [ ] `git status` is clean, one repo, no nested `.git` folders
- [ ] `uvicorn` + `npm run dev` both run, page shows **ok**
- [ ] `docker compose up --build` works on a clean start (stop containers first)
- [ ] `.env` is ignored; nothing secret is committed
- [ ] No hardcoded `localhost:8000` in React code (uses `/api` + `VITE_API_URL`)
