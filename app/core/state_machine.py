from typing import Tuple
from .enums import ConversationState
from ..domain.dto.inbound_message import InboundMessageDTO
from ..domain.models.conversation import Conversation

def decide_next_state(
    current_state: ConversationState,
    message: InboundMessageDTO,
    context: Conversation,
) -> ConversationState:
    """
    Pure function: decides next state based on current state + message.
    Right now it's a stub; you must fill the actual rules.
    """

    # Minimal stub logic – you MUST replace with real transitions.
    if current_state == ConversationState.NEW_USER:
        return ConversationState.WAITING_TNC_ACCEPTANCE

    if current_state == ConversationState.WAITING_TNC_ACCEPTANCE:
        # Example: if user says "yes" -> next step
        if message.text and message.text.strip().lower().startswith("y"):
            return ConversationState.WAITING_SCENE_SELECTION
        else:
            return ConversationState.WAITING_TNC_ACCEPTANCE

    # For the rest, just return same state for now.
    return current_state

def get_expected_input_for_state(state: ConversationState) -> str:
    mapping = {
        ConversationState.WAITING_TNC_ACCEPTANCE: "yes/no",
        ConversationState.WAITING_SCENE_SELECTION: "scene selection",
        ConversationState.WAITING_USER_NAME: "user name",
        ConversationState.WAITING_USER_GENDER: "user gender",
        ConversationState.WAITING_USER_PICTURE: "user picture (image)",
        ConversationState.WAITING_CONSENT_CONFIRMATION: "consent confirmation",
        ConversationState.WAITING_BUDDY_NAME: "buddy name",
        ConversationState.WAITING_BUDDY_GENDER: "buddy gender",
        ConversationState.WAITING_BUDDY_PICTURE: "buddy picture (image)",
        ConversationState.WAITING_BUDDY_APPROVAL: "buddy approval status",
    }
    return mapping.get(state, "no specific input expected")

def is_terminal_state(state: ConversationState) -> bool:
    return state in {ConversationState.COMPLETED, ConversationState.FAILED}
