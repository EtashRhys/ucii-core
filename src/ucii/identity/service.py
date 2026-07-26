"""
Identity Business Logic

No FastAPI dependencies.

Responsible for:
- identity creation
- identity retrieval
"""

from sqlalchemy.orm import Session

import uuid

from .models import Identity
from .schemas import IdentityCreate


class IdentityService:

    def __init__(
        self,
        db: Session
    ):
        self.db = db


    def create_identity(
        self,
        identity_data: IdentityCreate
    ) -> Identity:

        identity = Identity(
            id=str(uuid.uuid4()),
            identity_type=identity_data.identity_type,
            name=identity_data.name,
            description=identity_data.description,
        )

        self.db.add(identity)

        self.db.commit()

        self.db.refresh(identity)

        return identity


    def get_identity(
        self,
        identity_id: str
    ) -> Identity:

        identity = (
            self.db.query(Identity)
            .filter(
                Identity.id == identity_id
            )
            .first()
        )

        if not identity:
            raise ValueError(
                "Identity not found"
            )

        return identity


    def list_identities(
        self
    ):

        return (
            self.db.query(Identity)
            .all()
        )