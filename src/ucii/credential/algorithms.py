"""
Credential Verification Algorithm Interfaces

Defines cryptographic verification contracts.

This layer does not implement cryptographic
algorithms.

Concrete implementations live under:

    credential.providers

and may internally use:

    ucii.pqc
"""

from abc import ABC, abstractmethod


class SignatureVerifier(ABC):
    """
    Abstract signature verification provider.

    Implementations verify ownership of a
    credential using the specified algorithm.
    """

    @abstractmethod
    def verify(
        self,
        algorithm: str,
        public_key: str,
        message: str,
        signature: str,
    ) -> bool:
        """
        Verify a digital signature.

        Args:
            algorithm:
                Cryptographic algorithm name
                (e.g. ML-DSA-65).

            public_key:
                Public verification key.

            message:
                Original message.

            signature:
                Digital signature.

        Returns:
            True if the signature is valid.
            False otherwise.
        """

        raise NotImplementedError