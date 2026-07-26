"""
Internal Credential Management Service

Handles credential lifecycle operations.

This layer does NOT generate private keys.

It manages public cryptographic identity records.

Phase 2.5.4.3:
Credential rotation foundation.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from ..identity.models import (
    Credential,
    CredentialStatus,
)

from .schemas import CredentialCreate


class CredentialService:
    """
    Credential lifecycle manager.
    """

    @staticmethod
    def register(
        db: Session,
        credential_data: CredentialCreate,
    ) -> Credential:
        """
        Register a cryptographic credential.
        """

        credential = Credential(
            identity_id=credential_data.identity_id,
            credential_type=credential_data.credential_type,
            algorithm=credential_data.algorithm,
            public_key=credential_data.public_key,
            fingerprint=credential_data.fingerprint,
            key_version=credential_data.key_version,
            status=CredentialStatus.ACTIVE,
        )

        db.add(credential)

        db.commit()

        db.refresh(credential)

        return credential



    @staticmethod
    def get_by_fingerprint(
        db: Session,
        fingerprint: str,
    ) -> Credential | None:
        """
        Retrieve credential by fingerprint.
        """

        return (
            db.query(Credential)
            .filter(
                Credential.fingerprint == fingerprint
            )
            .first()
        )



    @staticmethod
    def revoke(
        db: Session,
        credential: Credential,
    ) -> Credential:
        """
        Revoke an active credential.
        """

        credential.status = CredentialStatus.REVOKED

        credential.revoked_at = datetime.utcnow()

        db.commit()

        db.refresh(credential)

        return credential



    @staticmethod
    def link_rotation(
        db: Session,
        old_credential: Credential,
        new_credential: Credential,
    ) -> Credential:
        """
        Link a replacement credential.

        Rotation preserves identity continuity.

        The old credential is not automatically revoked.
        """

        if old_credential.identity_id != new_credential.identity_id:

            raise ValueError(
                "Credential rotation requires same identity"
            )


        old_credential.replaced_by_id = (
            new_credential.id
        )

        old_credential.replaced_at = (
            datetime.utcnow()
        )


        db.commit()

        db.refresh(old_credential)

        return old_credential