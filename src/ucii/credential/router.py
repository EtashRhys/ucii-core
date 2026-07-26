"""
FastAPI Router for Internal Credential Management

Handles:

- credential registration
- credential retrieval
- credential revocation
- credential verification

Business logic remains isolated inside:

CredentialService
CredentialVerifier

Cryptographic implementations remain isolated inside:

verification providers
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from ..config import get_db

from .schemas import (
    CredentialCreate,
    CredentialResponse,
    VerificationRequest,
    VerificationResponse,
)

from .service import CredentialService
from .verifier import CredentialVerifier

# Concrete verification provider
from .providers.pqc import PQCSignatureVerifier


router = APIRouter(
    prefix="/v1/credentials",
    tags=["credentials"],
)


# ============================================================
# REGISTER CREDENTIAL
# ============================================================

@router.post(
    "/register",
    response_model=CredentialResponse,
    summary="Register a cryptographic credential",
    description=(
        "Registers a cryptographic credential associated "
        "with a UCII identity."
    ),
    operation_id="register_credential",
)
def register_credential(
    credential_data: CredentialCreate,
    db: Session = Depends(get_db),
):

    try:

        return CredentialService.register(
            db,
            credential_data,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )


# ============================================================
# GET CREDENTIAL BY FINGERPRINT
# ============================================================

@router.get(
    "/{fingerprint}",
    response_model=CredentialResponse,
    summary="Retrieve a credential",
    description=(
        "Returns a cryptographic credential using its fingerprint."
    ),
    operation_id="get_credential",
)
def get_credential(
    fingerprint: str,
    db: Session = Depends(get_db),
):

    credential = (
        CredentialService.get_by_fingerprint(
            db,
            fingerprint,
        )
    )

    if credential is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credential not found",
        )

    return credential


# ============================================================
# REVOKE CREDENTIAL
# ============================================================

@router.post(
    "/{credential_id}/revoke",
    response_model=CredentialResponse,
    summary="Revoke a credential",
    description=(
        "Revokes an active cryptographic credential."
    ),
    operation_id="revoke_credential",
)
def revoke_credential(
    credential_id: str,
    db: Session = Depends(get_db),
):

    from ..identity.models import Credential

    credential = (
        db.query(Credential)
        .filter(
            Credential.id == credential_id
        )
        .first()
    )

    if credential is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Credential not found",
        )

    return CredentialService.revoke(
        db,
        credential,
    )


# ============================================================
# VERIFY CREDENTIAL
# ============================================================

@router.post(
    "/verify",
    response_model=VerificationResponse,
    summary="Verify credential ownership",
    description=(
        "Verifies cryptographic proof of credential ownership "
        "using the configured verification provider."
    ),
    operation_id="verify_credential",
)
def verify_credential(
    verification_request: VerificationRequest,
    db: Session = Depends(get_db),
):
    """
    Verify cryptographic proof of credential ownership.

    Phase 2.5 wires the concrete PQC verification provider
    into the verification pipeline using dependency injection.

    Router
        ↓
    CredentialVerifier
        ↓
    SignatureVerifier
        ↓
    PQCSignatureVerifier
        ↓
    MLDSA
        ↓
    liboqs
    """

    verifier = CredentialVerifier(
        algorithm_provider=PQCSignatureVerifier(),
    )

    return verifier.verify(
        db,
        verification_request,
    )