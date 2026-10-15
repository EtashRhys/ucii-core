"""
Hybrid PQC Module

Signing identity (dual signatures, both must verify):
    Ed25519 + ML-DSA-65

Key exchange (hybrid KEM combiner):
    X25519 + ML-KEM-768

The hybrid KEM derives the shared secret from BOTH the classical
X25519 exchange and the ML-KEM encapsulation, combined through
HKDF-SHA256. An attacker must break both primitives to recover
the secret.

NOTE: hybrid_shared_secret() from earlier versions was removed.
It derived the "hybrid" secret from X25519 alone and could not
carry a KEM ciphertext, so it was not hybrid. Use
hybrid_encapsulate() / hybrid_decapsulate() instead.
"""

from .kem import MLKEM
from .signatures import MLDSA

from cryptography.hazmat.primitives.asymmetric import (
    x25519,
    ed25519,
)

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from cryptography.exceptions import InvalidSignature

from typing import Dict, Tuple


# Ed25519 signatures are always this long, so the dual-signature
# bundle can be split deterministically.
ED25519_SIGNATURE_LENGTH = 64


# Domain separation for the hybrid KEM combiner. Must differ from
# any other HKDF info string in the system.
HYBRID_KEM_INFO = b"ucii-hybrid-kem-v1"


class HybridPQCAuth:


    def __init__(
        self,
        kem_alg="ML-KEM-768",
        dsa_alg="ML-DSA-65"
    ):

        self.kem = MLKEM(kem_alg)

        self.dsa = MLDSA(dsa_alg)



    def generate_hybrid_keypair(
        self
    ) -> Dict[str, bytes]:


        #
        # Classical signing key
        #
        ed_private = (
            ed25519.Ed25519PrivateKey.generate()
        )

        ed_public = (
            ed_private.public_key()
        )


        #
        # PQC signing key
        #
        dsa_public, dsa_private = (
            self.dsa.generate_keypair()
        )


        #
        # Key exchange keys
        #
        x_private = (
            x25519.X25519PrivateKey.generate()
        )

        x_public = (
            x_private.public_key()
        )


        kem_public, kem_private = (
            self.kem.generate_keypair()
        )



        return {


            # Classical signing

            "ed25519_private":
                ed_private.private_bytes_raw(),


            "ed25519_public":
                ed_public.public_bytes_raw(),



            # PQC signing

            "dsa_private":
                dsa_private,


            "dsa_public":
                dsa_public,



            # Key exchange

            "x25519_private":
                x_private.private_bytes_raw(),


            "x25519_public":
                x_public.public_bytes_raw(),


            "kem_private":
                kem_private,


            "kem_public":
                kem_public,

        }



    def hybrid_sign(
        self,
        message: bytes,
        ed25519_private: bytes,
        dsa_private: bytes,
    ) -> bytes:
        """
        Create a dual signature over a message.

        Signs with Ed25519 AND ML-DSA-65 and concatenates the two
        signatures:

            signature = ed25519_sig (64 bytes) || mldsa_sig

        Returns:
            The concatenated dual signature bytes.
        """

        ed_private = (
            ed25519.Ed25519PrivateKey
            .from_private_bytes(
                ed25519_private
            )
        )

        ed_signature = ed_private.sign(message)

        dsa_signature = self.dsa.sign(
            message,
            dsa_private,
        )

        return ed_signature + dsa_signature



    def hybrid_verify(
        self,
        message: bytes,
        signature: bytes,
        ed25519_public: bytes,
        dsa_public: bytes,
    ) -> bool:
        """
        Verify a dual signature over a message.

        Returns True only if BOTH the Ed25519 and the ML-DSA-65
        signatures verify. Returns False on any failure, including
        malformed input. Never raises.
        """

        try:

            if len(signature) <= ED25519_SIGNATURE_LENGTH:
                return False

            ed_signature = signature[:ED25519_SIGNATURE_LENGTH]

            dsa_signature = signature[ED25519_SIGNATURE_LENGTH:]

            if len(dsa_signature) != self.dsa.get_signature_length():
                return False


            ed_public = (
                ed25519.Ed25519PublicKey
                .from_public_bytes(
                    ed25519_public
                )
            )

            ed_public.verify(
                ed_signature,
                message,
            )


            if not self.dsa.verify(
                message,
                dsa_signature,
                dsa_public,
            ):
                return False


            return True

        except (InvalidSignature, ValueError, Exception):
            return False



    def _combine_secrets(
        self,
        x25519_secret: bytes,
        kem_secret: bytes,
    ) -> bytes:
        """
        Combine the classical and PQC shared secrets into one.

        Concatenation followed by HKDF-SHA256. Both inputs must
        be present; neither alone determines the output.
        """

        combined = x25519_secret + kem_secret

        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=HYBRID_KEM_INFO,
        )

        return hkdf.derive(combined)



    def hybrid_encapsulate(
        self,
        peer_x25519_public: bytes,
        peer_kem_public: bytes,
    ) -> Dict[str, bytes]:
        """
        Establish a hybrid shared secret with a peer.

        Performs an ephemeral X25519 exchange against the peer's
        static X25519 public key and an ML-KEM encapsulation against
        the peer's KEM public key, then combines both secrets.

        Returns:
            {
                "x25519_ephemeral_public": bytes,
                    # send to the peer
                "kem_ciphertext": bytes,
                    # send to the peer
                "shared_secret": bytes,
                    # keep private
            }
        """

        ephemeral_private = (
            x25519.X25519PrivateKey.generate()
        )

        ephemeral_public = (
            ephemeral_private.public_key()
        )

        x_shared = ephemeral_private.exchange(
            x25519.X25519PublicKey.from_public_bytes(
                peer_x25519_public
            )
        )

        kem_ciphertext, kem_shared = self.kem.encapsulate(
            peer_kem_public
        )

        shared_secret = self._combine_secrets(
            x_shared,
            kem_shared,
        )

        return {

            "x25519_ephemeral_public":
                ephemeral_public.public_bytes_raw(),

            "kem_ciphertext":
                kem_ciphertext,

            "shared_secret":
                shared_secret,

        }



    def hybrid_decapsulate(
        self,
        x25519_ephemeral_public: bytes,
        my_x25519_private: bytes,
        kem_ciphertext: bytes,
        my_kem_private: bytes,
    ) -> bytes:
        """
        Recover the hybrid shared secret from a peer's encapsulation.

        Completes the X25519 exchange with our static private key
        and decapsulates the KEM ciphertext, then combines both
        secrets exactly as hybrid_encapsulate() does.

        Returns:
            The shared secret. Matches the sender's shared_secret
            if and only if all inputs are correct.
        """

        x_private = (
            x25519.X25519PrivateKey
            .from_private_bytes(
                my_x25519_private
            )
        )

        x_shared = x_private.exchange(
            x25519.X25519PublicKey.from_public_bytes(
                x25519_ephemeral_public
            )
        )

        kem_shared = self.kem.decapsulate(
            my_kem_private,
            kem_ciphertext,
        )

        return self._combine_secrets(
            x_shared,
            kem_shared,
        )



hybrid_auth = HybridPQCAuth()
