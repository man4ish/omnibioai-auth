from fastapi import FastAPI
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


@app.get("/health")
def health():
    return {"status": "ok"}