# --- Stage 1: Build the React Frontend ---
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# --- Stage 2: Setup Python Backend & Bundle ---
FROM python:3.10-slim
WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend source code
COPY backend/ ./backend/

# Copy React build artifacts from Stage 1 into the backend static folder
COPY --from=frontend-build /app/frontend/dist ./backend/app/static

# Expose port and start FastAPI server
EXPOSE 8000
CMD uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}