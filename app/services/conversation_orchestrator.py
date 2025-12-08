from typing import List
from ..core.identifiers import generate_flow_id
from ..core.enums import ConversationState, ConsentStatus
from ..core import state_machine
from ..domain.dto.inbound_message import InboundMessageDTO
from ..domain.dto.outbound_message import OutboundMessageDTO
from ..domain.models.conversation import Conversation
from ..domain.models.event_log import EventLog
from ..repositories.conversation_repository import ConversationRepository
from ..repositories.user_repository import UserRepository
from ..repositories.event_repository import EventRepository
from ..services.flow_state_service import FlowStateService
from ..services.consent_service import ConsentService
from ..services.buddy_state_service import BuddyStateService
from ..services.external_api_service import ExternalApiService
from ..domain.models.user_profile import UserProfile

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
    ):
        self.conv_repo = conv_repo or ConversationRepository()
        self.user_repo = user_repo or UserRepository()
        self.event_repo = event_repo or EventRepository()
        self.flow_state_service = flow_state_service or FlowStateService()
        self.consent_service = consent_service or ConsentService()
        self.buddy_service = buddy_service or BuddyStateService()
        self.external_api_service = external_api_service or ExternalApiService()

    def _log_event(self, flow_id: str, direction: str, event_type: str, payload: dict):
        event = EventLog(
            event_id=generate_flow_id(),  # or generate_entity_id("event")
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
        new_user = UserProfile(
            user_id=generate_flow_id(),
            whatsapp_number=whatsapp_number,
        )
        self.user_repo.create(new_user)
        return new_user

    def _get_or_create_conversation(self, user: UserProfile) -> Conversation:
        existing = self.conv_repo.get_active_by_user(user.user_id)
        if existing:
            return existing
        flow_id = generate_flow_id()
        conv = Conversation(
            flow_id=flow_id,
            user_id=user.user_id,
            current_state=ConversationState.NEW_USER,
        )
        self.conv_repo.create(conv)
        return conv

    def handle_incoming_message(
        self,
        message: InboundMessageDTO,
    ) -> List[OutboundMessageDTO]:
        """
        Main entrypoint from webhook.
        """
        user = self._get_or_create_user(message.user_whatsapp_number)
        conversation = self._get_or_create_conversation(user)

        self._log_event(
            flow_id=conversation.flow_id,
            direction="inbound",
            event_type="message",
            payload=message.raw_payload,
        )

        current_state = conversation.current_state

        next_state = state_machine.decide_next_state(
            current_state=current_state,
            message=message,
            context=conversation,
        )

        conversation = self.flow_state_service.apply_state_transition(
            conversation=conversation,
            next_state=next_state,
            message=message,
        )

        # Example: ensure consent record when we reach consent state
        if next_state == ConversationState.WAITING_CONSENT_CONFIRMATION:
            self.consent_service.ensure_consent_record(
                flow_id=conversation.flow_id,
                user_id=conversation.user_id,
            )

        # Example: if ready for API call
        outbound_messages: List[OutboundMessageDTO] = []

        if next_state == ConversationState.READY_FOR_API_CALL:
            consent_record = self.consent_service.ensure_consent_record(
                flow_id=conversation.flow_id,
                user_id=conversation.user_id,
            )
            buddy_state = self.buddy_service.get_or_create_for_flow(conversation.flow_id)
            payload = self.external_api_service.build_payload_from_flow(
                conversation=conversation,
                buddy_state=buddy_state,
                consent=consent_record,
            )
            result = self.external_api_service.call_external_api(payload)
            self.external_api_service.handle_api_result(conversation.flow_id, result)
            # you should also set conversation.current_state = COMPLETED/FAILED based on result

        self.conv_repo.update(conversation)

        # Very simple outgoing text for now – you MUST customize this.
        response_text = f"Current state: {conversation.current_state.value}. Expected input: {state_machine.get_expected_input_for_state(conversation.current_state)}"

        outbound = OutboundMessageDTO(
            user_whatsapp_number=message.user_whatsapp_number,
            text=response_text,
        )

        self._log_event(
            flow_id=conversation.flow_id,
            direction="outbound",
            event_type="message",
            payload=outbound.dict(),
        )

        outbound_messages.append(outbound)
        return outbound_messages
