"""
Sandbox Schemas

Simplified external experience layer
for UCII identity discovery.
"""

from pydantic import BaseModel


class SandboxIdentityCreate(BaseModel):
    """
    Request to create a sandbox identity.
    """

    name: str


class SandboxCapabilityRequest(BaseModel):
    """
    Research-only capability attachment request.

    This does NOT create a real credential.
    """

    capability: str



class SandboxCredentialRequest(BaseModel):
    """
    Research-only credential relationship request.

    This does NOT create a production credential.
    """

    credential_type: str


class SandboxCredentialExperience(BaseModel):
    message: str
    explanation: str
    real_world: list[str]


class SandboxCredentialResponse(BaseModel):
    identity_id: str
    credential: dict
    experience: SandboxCredentialExperience



class SandboxAuthorizationRequest(BaseModel):
    """
    Research-only authorization relationship request.

    This does NOT grant a production authorization.
    """

    action: str


class SandboxAuthorizationExperience(BaseModel):
    message: str
    explanation: str
    real_world: list[str]


class SandboxAuthorizationResponse(BaseModel):
    identity_id: str
    authorization: dict
    experience: SandboxAuthorizationExperience



class SandboxVerificationRequest(BaseModel):
    """
    Research-only verification outcome request.

    This does NOT verify a production identity.
    It demonstrates a verification relationship outcome.
    """

    relationship: str


class SandboxVerificationExperience(BaseModel):
    message: str
    explanation: str
    real_world: list[str]


class SandboxVerificationResponse(BaseModel):
    identity_id: str
    verification: dict
    experience: SandboxVerificationExperience


class SandboxProofRequest(BaseModel):
    """
    Research-only proof experience request.

    This does NOT create a real cryptographic proof.
    """

    proof_type: str


class SandboxCreationExperience(BaseModel):
    event: str
    message: str
    explanation: str
    next: list[str]


class SandboxDiscoveryExperience(BaseModel):
    message: str
    explanation: str
    next: list[str]


class SandboxCapabilityExperience(BaseModel):
    message: str
    explanation: str
    real_world: list[str]


class SandboxProofExperience(BaseModel):
    message: str
    explanation: str
    real_world: list[str]


class SandboxRelationshipExperience(BaseModel):
    message: str
    explanation: str
    layers: list[str]


class SandboxIdentityResponse(BaseModel):
    identity_id: str
    type: str
    status: str
    experience: SandboxCreationExperience


class SandboxIdentityDiscoveryResponse(BaseModel):
    identity_id: str
    type: str
    status: str
    credentials: int
    experience: SandboxDiscoveryExperience


class SandboxCapabilityResponse(BaseModel):
    identity_id: str
    capability: dict
    experience: SandboxCapabilityExperience


class SandboxProofResponse(BaseModel):
    identity_id: str
    proof: dict
    experience: SandboxProofExperience


class SandboxRelationshipResponse(BaseModel):
    identity_id: str
    identity: dict
    relationships: dict
    experience: SandboxRelationshipExperience
