"""
Credential Rotation Service

Provides credential replacement lifecycle.

Rotation preserves identity continuity.

Important:

- Private keys are never handled here.
- Key generation belongs to external
  cryptographic providers, wallets,
  HSMs, or key management systems.

This service manages:

Credential v1
        |
        v
Credential v2

while preserving historical trust records.

The replacement credential points backward
to the credential it replaces.
"""


from sqlalchemy.orm import Session

from ..identity.models import (
    Credential,
    CredentialStatus,
)

from .schemas import CredentialCreate



class CredentialRotationService:
    """
    Credential replacement lifecycle manager.
    """


    @staticmethod
    def rotate(
        db: Session,
        existing_credential: Credential,
        replacement_data: CredentialCreate,
    ) -> Credential:
        """
        Replace an existing active credential.

        Flow:

        ACTIVE credential

              |
              v

        create replacement credential

              |
              v

        link lineage

              |
              v

        mark original REPLACED


        Credentials are never deleted.
        """


        if (
            existing_credential.status
            != CredentialStatus.ACTIVE
        ):
            raise ValueError(
                "Only active credentials can be rotated"
            )


        if (
            existing_credential.identity_id
            != replacement_data.identity_id
        ):
            raise ValueError(
                "Credential rotation requires same identity"
            )


        replacement = Credential(
            identity_id=replacement_data.identity_id,
            credential_type=replacement_data.credential_type,
            algorithm=replacement_data.algorithm,
            public_key=replacement_data.public_key,
            fingerprint=replacement_data.fingerprint,
            key_version=replacement_data.key_version,
            status=CredentialStatus.ACTIVE,

            previous_credential_id=(
                existing_credential.id
            ),

            rotation_reason="credential_rotation",
        )


        db.add(replacement)

        db.flush()


        existing_credential.status = (
            CredentialStatus.REPLACED
        )

        existing_credential.rotated_at = (
            replacement.created_at
        )


        db.commit()

        db.refresh(
            replacement
        )


        return replacement