"""
Identity Database Models

Identity is the root primitive of the system.

Authentication, authorization,
credentials, and x402 metering
attach to identity layers.

Phase 2.5.5.2:
- Credentials support cryptographic lineage
- Historical credential ancestry is preserved
- Rotation continuity foundation added
- Credential replacement lifecycle added
"""

from datetime import datetime
import uuid
import enum

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Text,
    Enum,
    JSON,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from ..database import Base


print("Loading identity.models")


class IdentityType(str, enum.Enum):
    """
    Supported identity classes.
    """

    HUMAN = "HUMAN"
    AI_AGENT = "AI_AGENT"
    ROBOT = "ROBOT"
    DEVICE = "DEVICE"
    SERVICE = "SERVICE"
    ORGANIZATION = "ORGANIZATION"


class CredentialType(str, enum.Enum):
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


class CredentialStatus(str, enum.Enum):
    """
    Credential lifecycle states.

    REPLACED means the credential was valid
    but superseded by a newer credential.

    It is different from REVOKED.

    REVOKED:
        Credential should no longer be trusted.

    REPLACED:
        Credential was intentionally migrated.
    """

    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    REPLACED = "REPLACED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"



class Identity(Base):
    """
    Root identity object.

    Identity represents the actor.

    Authentication and credentials
    attach to identity.
    """

    __tablename__ = "identities"


    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )


    identity_type = Column(
        Enum(IdentityType),
        nullable=False,
        index=True
    )


    name = Column(
        String,
        nullable=False,
        index=True
    )


    description = Column(
        Text,
        nullable=True
    )


    is_active = Column(
        Boolean,
        default=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    profiles = relationship(
        "IdentityProfile",
        back_populates="identity",
        cascade="all, delete-orphan"
    )


    credentials = relationship(
        "Credential",
        back_populates="identity",
        cascade="all, delete-orphan"
    )


    def __repr__(self):
        return (
            f"<Identity "
            f"{self.identity_type}: "
            f"{self.name}>"
        )



class IdentityProfile(Base):
    """
    Identity-specific metadata extension.

    Profile data changes depending
    on identity type.
    """

    __tablename__ = "identity_profiles"


    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )


    identity_id = Column(
        String,
        ForeignKey("identities.id"),
        nullable=False,
        index=True
    )


    profile_type = Column(
        Enum(IdentityType),
        nullable=False,
        index=True
    )


    profile_data = Column(
        JSON,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    identity = relationship(
        "Identity",
        back_populates="profiles"
    )



class Credential(Base):
    """
    Cryptographic credential.

    A credential proves control over
    cryptographic material.

    Private keys are NEVER stored here.

    Credentials are historical objects.

    They are never deleted.

    Rotation creates a new credential
    while preserving ancestry.
    """

    __tablename__ = "credentials"


    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )


    identity_id = Column(
        String,
        ForeignKey("identities.id"),
        nullable=False,
        index=True
    )


    credential_type = Column(
        Enum(CredentialType),
        nullable=False,
        index=True
    )


    algorithm = Column(
        String,
        nullable=False
    )


    public_key = Column(
        Text,
        nullable=False
    )


    fingerprint = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )


    key_version = Column(
        String,
        default="1",
        nullable=False
    )


    status = Column(
        Enum(CredentialStatus),
        default=CredentialStatus.ACTIVE,
        nullable=False,
        index=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    expires_at = Column(
        DateTime,
        nullable=True
    )


    revoked_at = Column(
        DateTime,
        nullable=True
    )


    revocation_reason = Column(
        String,
        nullable=True
    )


    # ========================================================
    # Credential lineage
    #
    # New credentials point backward
    # to the credential they replaced.
    #
    # Example:
    #
    # Credential v3
    #       |
    #       v
    # Credential v2
    #       |
    #       v
    # Credential v1
    #
    # ========================================================


    previous_credential_id = Column(
        String,
        ForeignKey("credentials.id"),
        nullable=True,
        index=True
    )


    rotation_reason = Column(
        String,
        nullable=True
    )


    rotated_at = Column(
        DateTime,
        nullable=True
    )


    previous_credential = relationship(
        "Credential",
        remote_side="Credential.id",
        foreign_keys=[previous_credential_id],
        uselist=False
    )


    identity = relationship(
        "Identity",
        back_populates="credentials"
    )


    def __repr__(self):
        return (
            f"<Credential "
            f"{self.credential_type} "
            f"{self.status}>"
        )