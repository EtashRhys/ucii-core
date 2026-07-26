"""
Credential API Schemas

Defines request and response structures
for credential lifecycle management.
"""

from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
)

from ..identity.models import (
    CredentialType,
    CredentialStatus,
)



class CredentialCreate(BaseModel):
    """
    Register public credential material.
    """

    identity_id: str

    credential_type: CredentialType

    algorithm: str

    public_key: str

    fingerprint: str

    key_version: str = "1"



class CredentialRotationRequest(BaseModel):
    """
    Credential replacement relationship.

    Used to link an existing credential
    to a new credential.
    """

    old_credential_id: str

    new_credential_id: str



class CredentialResponse(BaseModel):
    """
    Public credential representation.
    """

    id: str

    identity_id: str

    credential_type: CredentialType

    algorithm: str

    fingerprint: str

    key_version: str

    status: CredentialStatus

    created_at: datetime

    expires_at: Optional[datetime] = None

    revoked_at: Optional[datetime] = None

    revocation_reason: Optional[str] = None

    replaced_by_id: Optional[str] = None

    replaced_at: Optional[datetime] = None


    model_config = ConfigDict(
        from_attributes=True
    )



class CredentialRevoke(BaseModel):
    """
    Credential revocation request.
    """

    reason: Optional[str] = None



class VerificationRequest(BaseModel):
    """
    Credential verification request.
    """

    fingerprint: str

    message: str

    signature: str



class VerificationResponse(BaseModel):
    """
    Credential verification result.
    """

    verified: bool

    fingerprint: str

    identity_id: Optional[str] = None

    status: Optional[CredentialStatus] = None

    reason: Optional[str] = None