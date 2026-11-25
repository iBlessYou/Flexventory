from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(
    title="Flexventory API",
    version="1.0.0",
    description="Flexible Inventory Management Platform"
)

app.include_router(api_router)
