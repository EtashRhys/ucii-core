"""
UCII Core Identity Models

Identity is the root primitive.

Authentication, authorization,
credentials, and payments attach
to identity relationships.

This module contains pure identity
concepts and does not depend on
databases or application runtimes.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class IdentityType(str, Enum):
    """
    Supported identity classes.
    """

    HUMAN = "HUMAN"
    AI_AGENT = "AI_AGENT"
    ROBOT = "ROBOT"
    DEVICE = "DEVICE"
    SERVICE = "SERVICE"
    ORGANIZATION = "ORGANIZATION"


class CredentialType(str, Enum):
    """
    Cryptographic credential classes.

    Credentials represent proof mechanisms,
    not identity itself.
    """

    ML_DSA_SIGNING_KEY = "ML_DSA_SIGNING_KEY"
    DEVICE_KEY = "DEVICE_KEY"
    SERVICE_KEY = "SERVICE_KEY"
    CERTIFICATE = "CERTIFICATE"
    ATTESTATION_KEY = "ATTESTATION_KEY"


class CredentialStatus(str, Enum):
    """
    Credential lifecycle states.
    """

    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    REPLACED = "REPLACED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"


@dataclass
class Identity:
    """
    Root identity object.

    Identity represents the actor.

    Credentials and capabilities
    attach to identity.
    """

    name: str
    identity_type: IdentityType
    description: Optional[str] = None

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    is_active: bool = True

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )


@dataclass
class Credential:
    """
    Cryptographic credential.

    Credentials prove control over
    cryptographic material.

    Private keys are never stored.
    """

    identity_id: str
    credential_type: CredentialType
    algorithm: str
    public_key: str
    fingerprint: str

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    status: CredentialStatus = (
        CredentialStatus.ACTIVE
    )

    key_version: str = "1"

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    expires_at: Optional[datetime] = None

    previous_credential_id: Optional[str] = None
