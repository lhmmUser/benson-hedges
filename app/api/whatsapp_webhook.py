from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    Query,
    Response,
    BackgroundTasks,
)
import os
from dotenv import load_dotenv

# ✅ this is your legacy flow with the full WhatsApp logic & state machine
from main import receive_webhook as legacy_receive_webhook

load_dotenv()

router = APIRouter(tags=["whatsapp"])

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
print(f"VERIFY_TOKEN is set to: {VERIFY_TOKEN}")


@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_challenge: str = Query(alias="hub.challenge"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
):
    """
    Meta verification endpoint.
    """
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        # Meta expects the raw challenge value back as plain text
        return Response(content=hub_challenge, media_type="text/plain")

    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook")
async def handle_whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
):
    """
    Delegate to the legacy receive_webhook() from root main.py
    so the flow behaves exactly like before (hi → T&C → scene → ...).
    """
    return await legacy_receive_webhook(request, background_tasks)
