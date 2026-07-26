"""
UCII Sandbox Router

External research environment
for experiencing UCII identity primitives.

Phase 6:
Identity -> Capability -> Proof experience
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from ..config import get_db
from ..identity.models import IdentityType
from ..identity.schemas import IdentityCreate
from ..identity.service import IdentityService

from .capabilities import (
    attach_capability,
    get_capabilities,
)

from .proofs import (
    create_proof,
    get_proofs,
)

from .schemas import (
    SandboxCapabilityExperience,
    SandboxCapabilityRequest,
    SandboxCapabilityResponse,
    SandboxAuthorizationExperience,
    SandboxAuthorizationRequest,
    SandboxAuthorizationResponse,
    SandboxCredentialExperience,
    SandboxCredentialRequest,
    SandboxCredentialResponse,
    SandboxCreationExperience,
    SandboxDiscoveryExperience,
    SandboxIdentityCreate,
    SandboxIdentityDiscoveryResponse,
    SandboxIdentityResponse,
    SandboxRelationshipExperience,
    SandboxRelationshipResponse,
    SandboxProofExperience,
    SandboxProofRequest,
    SandboxProofResponse,
    SandboxVerificationExperience,
    SandboxVerificationRequest,
    SandboxVerificationResponse,
)


router = APIRouter(
    prefix="/sandbox",
    tags=["sandbox"],
)


@router.post(
    "/register",
    response_model=SandboxIdentityResponse,
    summary="Create sandbox identity",
)
def register_identity(
    identity_data: SandboxIdentityCreate,
    db: Session = Depends(get_db),
):

    service = IdentityService(db)

    try:

        identity = service.create_identity(
            IdentityCreate(
                identity_type=IdentityType.HUMAN,
                name=identity_data.name,
                description="UCII sandbox research identity",
            )
        )

        return SandboxIdentityResponse(
            identity_id=identity.id,
            type=identity.identity_type.value,
            status="active" if identity.is_active else "inactive",
            experience=SandboxCreationExperience(
                event="identity_created",
                message=(
                    "Your UCII cryptographic identity "
                    "has been created."
                ),
                explanation=(
                    "This is not a password account. "
                    "It is a cryptographic identity primitive "
                    "that can later hold capabilities and proofs."
                ),
                next=[
                    "Your identity now exists inside the UCII sandbox.",
                    "Future capabilities and proof relationships can be explored.",
                ],
            ),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.get(
    "/identity/{identity_id}",
    response_model=SandboxIdentityDiscoveryResponse,
    summary="Inspect sandbox identity",
)
def get_identity(
    identity_id: str,
    db: Session = Depends(get_db),
):

    service = IdentityService(db)

    try:

        identity = service.get_identity(identity_id)

        return SandboxIdentityDiscoveryResponse(
            identity_id=identity.id,
            type=identity.identity_type.value,
            status="active" if identity.is_active else "inactive",
            credentials=len(identity.credentials),
            experience=SandboxDiscoveryExperience(
                message="This identity exists inside UCII.",
                explanation=(
                    "An identity is the root primitive of UCII. "
                    "Capabilities and credentials can attach to it "
                    "without becoming the identity itself."
                ),
                next=[
                    "Your identity is ready for capability exploration.",
                    "Proof relationships can demonstrate identity interactions.",
                ],
            ),
        )

    except ValueError:

        raise HTTPException(
            status_code=404,
            detail="Identity not found",
        )


@router.get(
    "/identity/{identity_id}/capabilities",
    response_model=SandboxCapabilityResponse,
    summary="Inspect identity capabilities",
)
def get_identity_capabilities(
    identity_id: str,
    db: Session = Depends(get_db),
):

    service = IdentityService(db)

    try:

        service.get_identity(identity_id)

        capabilities = get_capabilities(identity_id)

        return SandboxCapabilityResponse(
            identity_id=identity_id,
            capability={
                "available": capabilities
            },
            experience=SandboxCapabilityExperience(
                message=(
                    "This identity can hold cryptographic capabilities."
                ),
                explanation=(
                    "Capabilities extend what an identity can participate in. "
                    "They do not define the identity itself."
                ),
                real_world=[
                    "A person could prove ownership of an identity.",
                    "A device could prove authenticity.",
                    "An AI agent could prove authorization.",
                ],
            ),
        )

    except ValueError:

        raise HTTPException(
            status_code=404,
            detail="Identity not found",
        )


@router.post(
    "/identity/{identity_id}/capabilities",
    response_model=SandboxCapabilityResponse,
    summary="Attach sandbox capability",
)
def add_capability(
    identity_id: str,
    capability_data: SandboxCapabilityRequest,
    db: Session = Depends(get_db),
):

    service = IdentityService(db)

    try:

        service.get_identity(identity_id)

        attach_capability(
            identity_id,
            capability_data.capability,
        )

        return SandboxCapabilityResponse(
            identity_id=identity_id,
            capability={
                "name": capability_data.capability,
                "status": "available",
            },
            experience=SandboxCapabilityExperience(
                message=(
                    "A capability has been associated "
                    "with this identity."
                ),
                explanation=(
                    "This demonstrates that identities "
                    "can possess capabilities without "
                    "those capabilities becoming the identity."
                ),
                real_world=[
                    "A person could prove ownership of an identity.",
                    "A device could prove authenticity.",
                    "An AI agent could prove authorization.",
                ],
            ),
        )

    except ValueError:

        raise HTTPException(
            status_code=404,
            detail="Identity not found",
        )


@router.post(
    "/identity/{identity_id}/proofs",
    response_model=SandboxProofResponse,
    summary="Create sandbox proof experience",
)
def add_proof(
    identity_id: str,
    proof_data: SandboxProofRequest,
    db: Session = Depends(get_db),
):

    service = IdentityService(db)

    try:

        service.get_identity(identity_id)

        create_proof(
            identity_id,
            proof_data.proof_type,
        )

        return SandboxProofResponse(
            identity_id=identity_id,
            proof={
                "type": proof_data.proof_type,
                "status": "available",
            },
            experience=SandboxProofExperience(
                message=(
                    "A proof relationship has been created."
                ),
                explanation=(
                    "This proof demonstrates a relationship "
                    "involving an identity. The proof does "
                    "not replace the identity."
                ),
                real_world=[
                    "A person could prove control of a credential.",
                    "A device could prove authenticity.",
                    "An AI agent could prove authorization.",
                ],
            ),
        )

    except ValueError:

        raise HTTPException(
            status_code=404,
            detail="Identity not found",
        )



@router.post(
    "/identity/{identity_id}/credentials",
    response_model=SandboxCredentialResponse,
    summary="Create sandbox credential relationship experience",
)
def add_credential(
    identity_id: str,
    credential_data: SandboxCredentialRequest,
    db: Session = Depends(get_db),
):

    service = IdentityService(db)

    try:

        service.get_identity(identity_id)

        return SandboxCredentialResponse(
            identity_id=identity_id,
            credential={
                "type": credential_data.credential_type,
                "status": "available",
            },
            experience=SandboxCredentialExperience(
                message=(
                    "A credential relationship has been "
                    "associated with this identity."
                ),
                explanation=(
                    "This demonstrates that credentials "
                    "belong to identities. They extend "
                    "identity capabilities but do not "
                    "define the identity itself."
                ),
                real_world=[
                    "A person could hold a verified credential.",
                    "A device could present an authenticity credential.",
                    "An AI agent could present an authorization credential.",
                ],
            ),
        )

    except ValueError:

        raise HTTPException(
            status_code=404,
            detail="Identity not found",
        )



@router.post(
    "/identity/{identity_id}/authorization",
    response_model=SandboxAuthorizationResponse,
    summary="Create sandbox authorization relationship experience",
)
def add_authorization(
    identity_id: str,
    authorization_data: SandboxAuthorizationRequest,
    db: Session = Depends(get_db),
):

    service = IdentityService(db)

    try:

        service.get_identity(identity_id)

        return SandboxAuthorizationResponse(
            identity_id=identity_id,
            authorization={
                "action": authorization_data.action,
                "status": "available",
            },
            experience=SandboxAuthorizationExperience(
                message=(
                    "An authorization relationship has been "
                    "associated with this identity."
                ),
                explanation=(
                    "This demonstrates that identities can "
                    "receive permissions without those "
                    "permissions becoming the identity itself."
                ),
                real_world=[
                    "A person could be authorized to access a service.",
                    "A device could be authorized to communicate with infrastructure.",
                    "An AI agent could be authorized to perform a task.",
                ],
            ),
        )

    except ValueError:

        raise HTTPException(
            status_code=404,
            detail="Identity not found",
        )



@router.post(
    "/identity/{identity_id}/verification",
    response_model=SandboxVerificationResponse,
    summary="Create sandbox verification outcome experience",
)
def add_verification(
    identity_id: str,
    verification_data: SandboxVerificationRequest,
    db: Session = Depends(get_db),
):

    service = IdentityService(db)

    try:

        service.get_identity(identity_id)

        return SandboxVerificationResponse(
            identity_id=identity_id,
            verification={
                "relationship": verification_data.relationship,
                "status": "verified",
            },
            experience=SandboxVerificationExperience(
                message=(
                    "A verification outcome has been "
                    "created."
                ),
                explanation=(
                    "Verification confirms a relationship "
                    "involving an identity. It does not "
                    "create or replace the identity itself."
                ),
                real_world=[
                    "A person could verify ownership of a credential.",
                    "A device could verify authenticity before connecting.",
                    "An AI agent could verify permission before performing a task.",
                ],
            ),
        )

    except ValueError:

        raise HTTPException(
            status_code=404,
            detail="Identity not found",
        )


@router.get(
    "/identity/{identity_id}/proofs",
    response_model=SandboxProofResponse,
    summary="Inspect sandbox proof experiences",
)
def inspect_proofs(
    identity_id: str,
    db: Session = Depends(get_db),
):

    service = IdentityService(db)

    try:

        service.get_identity(identity_id)

        proofs = get_proofs(identity_id)

        return SandboxProofResponse(
            identity_id=identity_id,
            proof={
                "available": proofs
            },
            experience=SandboxProofExperience(
                message=(
                    "This identity has proof relationships "
                    "inside the sandbox."
                ),
                explanation=(
                    "Proofs demonstrate relationships and "
                    "authorization possibilities without "
                    "becoming the identity itself."
                ),
                real_world=[
                    "A person could prove ownership.",
                    "A device could prove authenticity.",
                    "An AI agent could prove authorization.",
                ],
            ),
        )

    except ValueError:

        raise HTTPException(
            status_code=404,
            detail="Identity not found",
        )


@router.get(
    "/identity/{identity_id}/relationship-map",
    response_model=SandboxRelationshipResponse,
    summary="Inspect identity relationship map",
)
def relationship_map(
    identity_id: str,
    db: Session = Depends(get_db),
):

    service = IdentityService(db)

    try:

        identity = service.get_identity(identity_id)

        from .capabilities import get_capabilities
        from .proofs import get_proofs

        return SandboxRelationshipResponse(

            identity_id=identity_id,

            identity={
                "type": identity.identity_type.value,
                "status": (
                    "active"
                    if identity.is_active
                    else "inactive"
                ),
            },

            relationships={

                "capabilities": get_capabilities(
                    identity_id
                ),

                "proofs": get_proofs(
                    identity_id
                ),

                "credentials": len(
                    identity.credentials
                ),
            },

            experience=SandboxRelationshipExperience(

                message=(
                    "Identity is the root primitive "
                    "of UCII."
                ),

                explanation=(
                    "Capabilities, proofs, and credentials "
                    "attach to an identity. They extend "
                    "what an identity can do, but they do "
                    "not become the identity itself."
                ),

                layers=[
                    "Identity",
                    "Capabilities",
                    "Proof Relationships",
                    "Cryptographic Credentials",
                ],

            ),
        )


    except ValueError:

        raise HTTPException(
            status_code=404,
            detail="Identity not found",
        )
