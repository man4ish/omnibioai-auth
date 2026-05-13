from fastapi import FastAPI
from app.api.routes_auth import router as auth_router
from app.db.base import Base
from app.db.session import engine

import app.db.models  # noqa

app = FastAPI(title="OmniBioAI Auth Service")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok"}