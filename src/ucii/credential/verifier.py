"""
UCII Core Credential Verification

Provides credential verification concepts.

This module contains verification
logic only.

Storage, databases, APIs, and
runtime services remain outside
UCII Core.
"""

from datetime import datetime

from ..identity.models import (
    Credential,
    CredentialStatus,
)

from .algorithms import SignatureVerifier


class CredentialVerifier:
    """
    Credential verification engine.

    Accepts credential objects directly.

    Persistence and lookup are the
    responsibility of applications
    built on top of UCII Core.
    """


    def __init__(
        self,
        algorithm_provider: SignatureVerifier,
    ):
        self.algorithm_provider = algorithm_provider


    def verify(
        self,
        credential: Credential,
        message: bytes,
        signature: bytes,
    ) -> bool:
        """
        Verify control of a credential.

        Returns:

        True:
            signature is valid

        False:
            verification failed
        """


        if credential.status != CredentialStatus.ACTIVE:
            return False


        if (
            credential.expires_at
            and credential.expires_at < datetime.utcnow()
        ):
            return False


        return self.algorithm_provider.verify(
            credential.algorithm,
            credential.public_key,
            message,
            signature,
        )
