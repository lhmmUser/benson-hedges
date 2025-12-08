from typing import Optional
from ..repositories.buddy_state_repository import BuddyStateRepository
from ..core.identifiers import generate_entity_id
from ..core.enums import BuddyApprovalStatus
from ..domain.models.buddy_state import BuddyState

class BuddyStateService:
    def __init__(self, buddy_repo: Optional[BuddyStateRepository] = None):
        self.buddy_repo = buddy_repo or BuddyStateRepository()

    def get_or_create_for_flow(self, flow_id: str) -> BuddyState:
        existing = self.buddy_repo.get_by_flow_id(flow_id)
        if existing:
            return existing

        buddy_state = BuddyState(
            buddy_state_id=generate_entity_id("buddy_state"),
            flow_id=flow_id,
        )
        self.buddy_repo.create(buddy_state)
        return buddy_state

    def update_buddy_basic_details(
        self, flow_id: str, name: Optional[str], gender: Optional[str]
    ) -> BuddyState:
        state = self.get_or_create_for_flow(flow_id)
        if name:
            state.buddy_name = name
        if gender:
            state.buddy_gender = gender
        self.buddy_repo.update(state)
        return state

    def update_buddy_picture(self, flow_id: str, picture_url: str) -> BuddyState:
        state = self.get_or_create_for_flow(flow_id)
        state.buddy_picture_url = picture_url
        self.buddy_repo.update(state)
        return state

    def update_buddy_approval(
        self, flow_id: str, approval_status: BuddyApprovalStatus
    ) -> BuddyState:
        state = self.get_or_create_for_flow(flow_id)
        state.approval_status = approval_status
        self.buddy_repo.update(state)
        return state
