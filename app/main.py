from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.api.routes_auth import router as auth_router
from app.db.base import Base
from app.db.session import engine
from app.db.session import SessionLocal
from app.db.init_admin import create_admin

import app.db.models

app = FastAPI(title="OmniBioAI Auth Service")

Base.metadata.create_all(bind=engine)

# bootstrap admin
db = SessionLocal()
create_admin(db)
db.close()

app.include_router(auth_router)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/health")
def health():
    return {"status": "ok"}