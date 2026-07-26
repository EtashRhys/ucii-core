"""
Identity Pydantic Schemas
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .models import IdentityType


class IdentityCreate(BaseModel):
    """
    Request to create a new identity.
    """

    identity_type: IdentityType

    name: str

    description: Optional[str] = None


class IdentityResponse(BaseModel):
    """
    Identity returned to clients.
    """

    id: str

    identity_type: IdentityType

    name: str

    description: Optional[str]

    is_active: bool

    created_at: datetime

    class Config:
        from_attributes = True