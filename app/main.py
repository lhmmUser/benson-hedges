from fastapi import FastAPI
from app.api.whatsapp_webhook import router as whatsapp_router
from app.api.health import router as health_router

def create_app() -> FastAPI:
    app = FastAPI(title="WhatsApp Flow Service")

    app.include_router(health_router, prefix="/api")
    app.include_router(whatsapp_router, prefix="/api")

    return app

app = create_app()
