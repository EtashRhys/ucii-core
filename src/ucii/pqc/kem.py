"""
PQC KEM Module

Real ML-KEM implementation backed by liboqs-python.

Used for the PQC half of hybrid key exchange:
    X25519 + ML-KEM-768

This module is intentionally kept stable because it is consumed by:
    - pqc.hybrid
"""

from typing import Tuple

import oqs


DEFAULT_ALGORITHM = "ML-KEM-768"


class MLKEM:
    """
    ML-KEM wrapper using liboqs-python.

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

        enabled = oqs.get_enabled_kem_mechanisms()

        if self.algorithm not in enabled:
            raise ValueError(
                f"{self.algorithm} is not enabled in liboqs"
            )


    def generate_keypair(self) -> Tuple[bytes, bytes]:
        """
        Generate ML-KEM public and secret keys.

        Returns:
            (public_key, secret_key)
        """

        with oqs.KeyEncapsulation(
            self.algorithm
        ) as kem:

            public_key = kem.generate_keypair()

            secret_key = kem.export_secret_key()

            return (
                bytes(public_key),
                bytes(secret_key)
            )


    def encapsulate(
        self,
        public_key: bytes
    ) -> Tuple[bytes, bytes]:
        """
        Encapsulate a shared secret to a public key.

        Returns:
            (ciphertext, shared_secret)

        The ciphertext must be delivered to the holder of the
        matching secret key, who recovers the shared secret
        with decapsulate().
        """

        with oqs.KeyEncapsulation(
            self.algorithm
        ) as kem:

            ciphertext, shared_secret = kem.encap_secret(
                public_key
            )

            return (
                bytes(ciphertext),
                bytes(shared_secret)
            )


    def decapsulate(
        self,
        secret_key: bytes,
        ciphertext: bytes
    ) -> bytes:
        """
        Decapsulate a ciphertext with the secret key.

        Returns:
            The shared secret established by encapsulate().
        """

        with oqs.KeyEncapsulation(
            self.algorithm,
            secret_key
        ) as kem:

            return bytes(
                kem.decap_secret(ciphertext)
            )


    def get_ciphertext_length(self) -> int:
        """
        Return ML-KEM ciphertext size.
        """

        with oqs.KeyEncapsulation(
            self.algorithm
        ) as kem:

            return int(
                kem.length_ciphertext
            )


    def get_shared_secret_length(self) -> int:
        """
        Return ML-KEM shared secret size.
        """

        with oqs.KeyEncapsulation(
            self.algorithm
        ) as kem:

            return int(
                kem.length_shared_secret
            )


default_kem = MLKEM()
