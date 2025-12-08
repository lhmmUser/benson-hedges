from fastapi import APIRouter, Depends, Request, HTTPException
from typing import List
from ..services.conversation_orchestrator import ConversationOrchestrator
from ..domain.dto.inbound_message import InboundMessageDTO
from ..domain.dto.outbound_message import OutboundMessageDTO

router = APIRouter(tags=["whatsapp"])

def get_orchestrator() -> ConversationOrchestrator:
    # In real world, use dependency injection container
    return ConversationOrchestrator()

@router.post("/webhook/whatsapp", response_model=List[OutboundMessageDTO])
async def handle_whatsapp_webhook(
    request: Request,
    orchestrator: ConversationOrchestrator = Depends(get_orchestrator),
):
    payload = await request.json()

    # TODO: Adapt this parsing to your provider payload
    try:
        message = InboundMessageDTO.from_provider_payload(payload)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid payload: {exc}")

    outbound_messages = orchestrator.handle_incoming_message(message)
    return outbound_messages
