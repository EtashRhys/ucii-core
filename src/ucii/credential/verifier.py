"""
Credential Verification Engine

Coordinates credential verification.

This layer handles:

- credential lookup
- lifecycle checks
- algorithm routing
- cryptographic verification

Cryptographic implementations remain
inside ucii.pqc.
"""


from datetime import datetime

from sqlalchemy.orm import Session

from ..identity.models import (
    Credential,
    CredentialStatus,
)

from .algorithms import SignatureVerifier

from .schemas import (
    VerificationRequest,
    VerificationResponse,
)



class CredentialVerifier:
    """
    Credential verification orchestrator.
    """


    def __init__(
        self,
        algorithm_provider: SignatureVerifier,
    ):

        self.algorithm_provider = algorithm_provider



    def verify(
        self,
        db: Session,
        request: VerificationRequest,
    ) -> VerificationResponse:


        credential = (
            db.query(Credential)
            .filter(
                Credential.fingerprint == request.fingerprint
            )
            .first()
        )


        if credential is None:

            return VerificationResponse(
                verified=False,
                fingerprint=request.fingerprint,
                reason="Credential not found",
            )


        if credential.status != CredentialStatus.ACTIVE:

            return VerificationResponse(
                verified=False,
                fingerprint=request.fingerprint,
                identity_id=credential.identity_id,
                status=credential.status,
                reason="Credential is not active",
            )


        if (
            credential.expires_at
            and credential.expires_at < datetime.utcnow()
        ):

            return VerificationResponse(
                verified=False,
                fingerprint=request.fingerprint,
                identity_id=credential.identity_id,
                status=CredentialStatus.EXPIRED,
                reason="Credential expired",
            )



        verified = self.algorithm_provider.verify(
            credential.algorithm,
            credential.public_key,
            request.message,
            request.signature,
        )



        return VerificationResponse(
            verified=verified,
            fingerprint=request.fingerprint,
            identity_id=credential.identity_id,
            status=credential.status,
            reason=(
                None
                if verified
                else "Signature verification failed"
            ),
        )