"""
PQC Credential Verification Provider

Adapter between the credential verification
layer and ucii.pqc cryptographic
implementations.
"""

import base64

from ..algorithms import SignatureVerifier

from ...pqc.signatures import MLDSA


class PQCSignatureVerifier(SignatureVerifier):
    """
    Post-Quantum signature verification provider.

    Supports verification of credentials using
    algorithms backed by ucii.pqc.
    """

    def verify(
        self,
        algorithm: str,
        public_key: str,
        message: str,
        signature: str,
    ) -> bool:

        try:

            verifier = MLDSA(algorithm)

            public_key_bytes = base64.b64decode(
                public_key
            )

            signature_bytes = base64.b64decode(
                signature
            )

            message_bytes = message.encode()

            return verifier.verify(
                message_bytes,
                signature_bytes,
                public_key_bytes,
            )

        except Exception:

            return False