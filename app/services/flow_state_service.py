from typing import Optional
from ..core.enums import ConversationState
from ..domain.models.conversation import Conversation
from ..domain.dto.inbound_message import InboundMessageDTO

class FlowStateService:
    """
    Applies state transitions: updates Conversation fields based on current state and message.
    """

    def apply_state_transition(
        self,
        conversation: Conversation,
        next_state: ConversationState,
        message: InboundMessageDTO,
    ) -> Conversation:
        # Example: fill simple fields based on previous state
        prev_state = conversation.current_state

        if prev_state == ConversationState.WAITING_TNC_ACCEPTANCE:
            conversation.tnc_accepted = bool(
                message.text and message.text.strip().lower().startswith("y")
            )

        elif prev_state == ConversationState.WAITING_SCENE_SELECTION and message.text:
            conversation.scene = message.text.strip()

        elif prev_state == ConversationState.WAITING_USER_NAME and message.text:
            conversation.user_name = message.text.strip()

        elif prev_state == ConversationState.WAITING_USER_GENDER and message.text:
            conversation.user_gender = message.text.strip()

        elif prev_state == ConversationState.WAITING_USER_PICTURE and message.media_urls:
            conversation.user_picture_url = message.media_urls[0]

        elif prev_state == ConversationState.WAITING_BUDDY_NAME and message.text:
            conversation.buddy_name = message.text.strip()

        elif prev_state == ConversationState.WAITING_BUDDY_GENDER and message.text:
            conversation.buddy_gender = message.text.strip()

        elif prev_state == ConversationState.WAITING_BUDDY_PICTURE and message.media_urls:
            conversation.buddy_picture_url = message.media_urls[0]

        conversation.current_state = next_state
        conversation.touch()
        return conversation
