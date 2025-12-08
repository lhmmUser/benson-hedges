from typing import Dict, Any
import httpx
from ..app.config import get_settings
from ..domain.models.conversation import Conversation
from ..domain.models.buddy_state import BuddyState
from ..domain.models.consent import ConsentRecord

class ExternalApiService:
    def __init__(self):
        self.settings = get_settings()

    def build_payload_from_flow(
        self,
        conversation: Conversation,
        buddy_state: BuddyState,
        consent: ConsentRecord,
    ) -> Dict[str, Any]:
        return {
            "flow_id": conversation.flow_id,
            "user": {
                "name": conversation.user_name,
                "gender": conversation.user_gender,
                "picture_url": conversation.user_picture_url,
            },
            "buddy": {
                "name": buddy_state.buddy_name,
                "gender": buddy_state.buddy_gender,
                "picture_url": buddy_state.buddy_picture_url,
                "approval_status": buddy_state.approval_status.value,
            },
            "scene": conversation.scene,
            "consent_status": consent.status.value,
        }

    def call_external_api(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Replace with real endpoint and auth
        url = f"{self.settings.EXTERNAL_API_BASE}/flow"
        # For now, just return payload as a stub
        # You SHOULD use httpx here with try/except.
        return {"status": "stubbed", "payload": payload}

    def handle_api_result(self, flow_id: str, result: Dict[str, Any]) -> None:
        # Hook to log/store result.
        # You might want to update conversation status here.
        pass
