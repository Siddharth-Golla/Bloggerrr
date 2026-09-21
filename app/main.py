from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)


app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Welcome to Bloggerrr API"}