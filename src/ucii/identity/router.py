"""
Identity API Router

Public identity creation layer.

Authentication and authorization
will be attached in future phases.
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from ..config import get_db

from .schemas import (
    IdentityCreate,
    IdentityResponse,
)

from .service import IdentityService


router = APIRouter(
    prefix="/v1/identity",
    tags=["identity"]
)



@router.post(
    "",
    response_model=IdentityResponse,
    summary="Create a cryptographic identity",
    description=(
        "Creates a UCII identity root entity. "
        "An identity represents a cryptographic subject "
        "independent from authentication credentials."
    ),
    operation_id="create_identity",
)
def create_identity(
    identity_data: IdentityCreate,
    db: Session = Depends(get_db)
):

    service = IdentityService(db)

    try:

        return service.create_identity(
            identity_data
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )



@router.get(
    "/{identity_id}",
    response_model=IdentityResponse,
    summary="Retrieve an identity",
    description=(
        "Returns a UCII identity record using its identity identifier."
    ),
    operation_id="get_identity",
)
def get_identity(
    identity_id: str,
    db: Session = Depends(get_db)
):

    service = IdentityService(db)

    try:

        return service.get_identity(
            identity_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )



@router.get(
    "",
    response_model=list[IdentityResponse],
    summary="List identities",
    description=(
        "Returns available UCII identity records."
    ),
    operation_id="list_identities",
)
def list_identities(
    db: Session = Depends(get_db)
):

    service = IdentityService(db)

    return service.list_identities()