from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class InboundMessageDTO(BaseModel):
    provider_message_id: str = Field(...)
    user_whatsapp_number: str = Field(...)
    text: Optional[str] = None
    media_urls: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    raw_payload: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_provider_payload(cls, payload: Dict[str, Any]) -> "InboundMessageDTO":
        """
        You MUST adapt this mapping to your provider's webhook format.
        Right now it's a dummy extraction.
        """
        # Example dummy extraction, replace this with real mapping
        message = payload.get("message", {})
        return cls(
            provider_message_id=str(message.get("id", "")),
            user_whatsapp_number=str(message.get("from", "")),
            text=message.get("text", {}).get("body"),
            media_urls=[],
            raw_payload=payload,
        )
