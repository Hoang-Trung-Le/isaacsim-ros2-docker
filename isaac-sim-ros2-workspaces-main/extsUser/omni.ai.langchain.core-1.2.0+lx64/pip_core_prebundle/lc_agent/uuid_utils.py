import uuid


def get_id_string() -> str:
    """
    Generate a UUID string
    """
    return str(uuid.uuid4())


class UUIDMixin:
    def uuid(self) -> str:
        """return the unique identifier for the mode otheriwe create one"""
        uuid = self.metadata.get("uuid", None)
        if not uuid:
            # we create one
            uuid = get_id_string()
            self.metadata["uuid"] = uuid

        return uuid
