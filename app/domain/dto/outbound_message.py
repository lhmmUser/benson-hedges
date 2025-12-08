from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class OutboundMessageDTO(BaseModel):
    user_whatsapp_number: str = Field(...)
    text: Optional[str] = None
    media_url: Optional[str] = None
    template_name: Optional[str] = None
    template_variables: Dict[str, Any] = Field(default_factory=dict)
