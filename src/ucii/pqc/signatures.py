"""
PQC Signature Module

Real ML-DSA implementation backed by liboqs-python.

Hybrid identity foundation:
    Ed25519 + ML-DSA-65

This module is intentionally kept stable because it is consumed by:
    - pqc.hybrid
    - utils.jwt
"""

from typing import Tuple

import oqs


DEFAULT_ALGORITHM = "ML-DSA-65"


class MLDSA:
    """
    ML-DSA wrapper using liboqs-python.

    Compatible with:
        liboqs-python 0.15.0
    """

    def __init__(
        self,
        algorithm: str = DEFAULT_ALGORITHM
    ):
        self.algorithm = algorithm

        self._validate_algorithm()


    def _validate_algorithm(self):
        """
        Verify algorithm availability.
        """

        enabled = oqs.get_enabled_sig_mechanisms()

        if self.algorithm not in enabled:
            raise ValueError(
                f"{self.algorithm} is not enabled in liboqs"
            )


    def generate_keypair(self) -> Tuple[bytes, bytes]:
        """
        Generate ML-DSA public and secret keys.
        """

        with oqs.Signature(
            self.algorithm
        ) as signer:

            public_key = signer.generate_keypair()

            secret_key = signer.export_secret_key()

            return (
                bytes(public_key),
                bytes(secret_key)
            )


    def sign(
        self,
        message: bytes,
        secret_key: bytes
    ) -> bytes:
        """
        Sign message with ML-DSA secret key.
        """

        with oqs.Signature(
            self.algorithm,
            secret_key
        ) as signer:

            return bytes(
                signer.sign(message)
            )


    def verify(
        self,
        message: bytes,
        signature: bytes,
        public_key: bytes
    ) -> bool:
        """
        Verify ML-DSA signature.
        """

        with oqs.Signature(
            self.algorithm
        ) as verifier:

            return bool(
                verifier.verify(
                    message,
                    signature,
                    public_key
                )
            )


    def get_signature_length(self) -> int:
        """
        Return ML-DSA signature size.
        """

        with oqs.Signature(
            self.algorithm
        ) as signer:

            return int(
                signer.length_signature
            )


default_dsa = MLDSA()
