import uuid

def generate_flow_id() -> str:
    return str(uuid.uuid4())

def generate_entity_id(entity_name: str) -> str:
    # entity_name is not used inside UUID, but could be used for logging
    return str(uuid.uuid4())

def is_valid_id(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False
