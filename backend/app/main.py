import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.convert import router as convert_router

app = FastAPI(title="Markify API", version="1.0.0")

_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
allowed_origins = [o.strip() for o in _origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(convert_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "Markify API"}
