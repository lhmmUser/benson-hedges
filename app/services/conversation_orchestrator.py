# app/services/conversation_orchestrator.py

from typing import List

from app.core.identifiers import generate_flow_id
from app.core.enums import ConversationState
from app.core import state_machine
from app.domain.dto.inbound_message import InboundMessageDTO
from app.domain.dto.outbound_message import OutboundMessageDTO
from app.domain.models.conversation import Conversation
from app.domain.models.event_log import EventLog
from app.domain.models.user_profile import UserProfile
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.user_repository import UserRepository
from app.repositories.event_repository import EventRepository
from app.services.flow_state_service import FlowStateService
from app.services.consent_service import ConsentService
from app.services.buddy_state_service import BuddyStateService
from app.services.external_api_service import ExternalApiService
from app.services.whatsapp_client import WhatsappClient


class ConversationOrchestrator:
    def __init__(
        self,
        conv_repo: ConversationRepository | None = None,
        user_repo: UserRepository | None = None,
        event_repo: EventRepository | None = None,
        flow_state_service: FlowStateService | None = None,
        consent_service: ConsentService | None = None,
        buddy_service: BuddyStateService | None = None,
        external_api_service: ExternalApiService | None = None,
        whatsapp_client: WhatsappClient | None = None,
    ) -> None:
        self.conv_repo = conv_repo or ConversationRepository()
        self.user_repo = user_repo or UserRepository()
        self.event_repo = event_repo or EventRepository()
        self.flow_state_service = flow_state_service or FlowStateService()
        self.consent_service = consent_service or ConsentService()
        self.buddy_service = buddy_service or BuddyStateService()
        self.external_api_service = external_api_service or ExternalApiService()
        self.whatsapp = whatsapp_client or WhatsappClient()  # ✅ inside __init__

    # ---------- internal helpers ----------

    def _log_event(self, flow_id: str, direction: str, event_type: str, payload: dict) -> None:
        event = EventLog(
            event_id=generate_flow_id(),
            flow_id=flow_id,
            direction=direction,
            event_type=event_type,
            payload=payload,
        )
        self.event_repo.create(event)

    def _get_or_create_user(self, whatsapp_number: str) -> UserProfile:
        user = self.user_repo.get_by_whatsapp_number(whatsapp_number)
        if user:
            return user

        user = UserProfile(
            user_id=generate_flow_id(),
            whatsapp_number=whatsapp_number,
        )
        self.user_repo.create(user)
        return user

    def _get_or_create_conversation(self, user: UserProfile) -> Conversation:
        existing = self.conv_repo.get_active_by_user(user.user_id)
        if existing:
            return existing

        conv = Conversation(
            flow_id=generate_flow_id(),
            user_id=user.user_id,
            current_state=ConversationState.NEW_USER,
        )
        self.conv_repo.create(conv)
        return conv

    # ---------- main entrypoint ----------

    def handle_incoming_message(self, message: InboundMessageDTO) -> List[OutboundMessageDTO]:
        """
        Main entry point from the webhook.
        """
        # 1) get or create user
        user = self._get_or_create_user(message.user_whatsapp_number)

        # 2) get or create conversation (flow)
        conversation = self._get_or_create_conversation(user)

        # 3) log inbound event
        self._log_event(
            flow_id=conversation.flow_id,
            direction="inbound",
            event_type="message",
            payload=message.raw_payload,
        )

        # 4) decide next state
        current_state = conversation.current_state
        next_state = state_machine.decide_next_state(
            current_state=current_state,
            message=message,
            context=conversation,
        )

        # 5) apply state transition (update fields like scene, name, etc.)
        conversation = self.flow_state_service.apply_state_transition(
            conversation=conversation,
            next_state=next_state,
            message=message,
        )

        # 6) side-effects for specific states (example: consent record)
        if next_state == ConversationState.WAITING_CONSENT_CONFIRMATION:
            self.consent_service.ensure_consent_record(
                flow_id=conversation.flow_id,
                user_id=conversation.user_id,
            )

        # 7) persist conversation
        self.conv_repo.update(conversation)

        # 8) choose what to send back TO WHATSAPP based on state
        if conversation.current_state == ConversationState.WAITING_TNC_ACCEPTANCE:
            reply = (
                "Hi! Before we begin, please read and accept our Terms & Conditions.\n\n"
                "Type *yes* to accept or *no* to decline."
            )
        elif conversation.current_state == ConversationState.WAITING_SCENE_SELECTION:
            reply = "Please choose a scene — type the scene name or number."
        elif conversation.current_state == ConversationState.WAITING_USER_NAME:
            reply = "Please share your name."
        else:
            reply = (
                f"Current state: {conversation.current_state.value}. "
                f"Expected input: {state_machine.get_expected_input_for_state(conversation.current_state)}"
            )

        outbound = OutboundMessageDTO(
            user_whatsapp_number=message.user_whatsapp_number,
            text=reply,
        )

        # 9) SEND to WhatsApp via Cloud API
        self.whatsapp.send_text(
            outbound.user_whatsapp_number,
            outbound.text or "",
        )

        # 10) log outbound
        self._log_event(
            flow_id=conversation.flow_id,
            direction="outbound",
            event_type="message",
            payload=outbound.dict(),
        )

        # 11) return list (for debugging / API response, WhatsApp ignores this)
        return [outbound]
