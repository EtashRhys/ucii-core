"""
Universal Cryptographic Identity Infrastructure Core.

UCII Core provides identity primitives,
credential relationships, verification concepts,
and post-quantum cryptographic foundations.
"""

from .identity import (
    Identity,
    IdentityType,
    Credential,
    CredentialType,
    CredentialStatus,
)

from .pqc import HybridPQCAuth


__version__ = "0.1.0"


__all__ = [
    "Identity",
    "IdentityType",
    "Credential",
    "CredentialType",
    "CredentialStatus",
    "HybridPQCAuth",
]
