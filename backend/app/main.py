from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.convert import router as convert_router

app = FastAPI(title="DocMark API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(convert_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "DocMark API"}
