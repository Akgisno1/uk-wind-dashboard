from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app=FastAPI()

@app.get("/api/health")
def health_check():
    return {"status": "ok",message: "FastAPI backend is running"}

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
