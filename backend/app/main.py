from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.web.routes import frontend, router as web_router

from app.api.router import api_router

app = FastAPI(
    title="Flexventory API",
    version="1.0.0",
    description="Flexible Inventory Management Platform"
)

app.include_router(api_router)

app.mount("/static/css", StaticFiles(directory=frontend / "css"), name="css")
app.mount("/static/js", StaticFiles(directory=frontend / "js"), name="js")
app.include_router(web_router)
