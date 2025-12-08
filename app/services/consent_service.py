from typing import Optional
from ..repositories.consent_repository import ConsentRepository
from ..core.identifiers import generate_entity_id
from ..core.enums import ConsentStatus
from ..domain.models.consent import ConsentRecord

class ConsentService:
    def __init__(self, consent_repo: Optional[ConsentRepository] = None):
        self.consent_repo = consent_repo or ConsentRepository()

    def ensure_consent_record(self, flow_id: str, user_id: str) -> ConsentRecord:
        existing = self.consent_repo.get_by_flow_id(flow_id)
        if existing:
            return existing

        consent = ConsentRecord(
            consent_id=generate_entity_id("consent"),
            flow_id=flow_id,
            user_id=user_id,
        )
        self.consent_repo.create(consent)
        return consent

    def mark_consent_given(self, consent_id: str) -> ConsentRecord:
        # In real system, you'd load by consent_id
        # For now just a simple approach
        # This is a bit naive; you likely need get_by_consent_id in repo
        raise NotImplementedError("Add get_by_consent_id and implement this")

    def get_consent_status(self, flow_id: str) -> ConsentStatus:
        record = self.consent_repo.get_by_flow_id(flow_id)
        if not record:
            return ConsentStatus.PENDING
        return record.status
