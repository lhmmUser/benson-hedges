from datetime import datetime
from typing import Dict, Any, Literal
from pydantic import BaseModel, Field

class EventLog(BaseModel):
    event_id: str = Field(...)
    flow_id: str = Field(...)
    direction: Literal["inbound", "outbound", "internal"] = "internal"
    event_type: str = "generic"
    payload: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
