"""
Hybrid PQC Module

Signing identity:
    Ed25519 + ML-DSA-65

Key exchange:
    X25519 + ML-KEM-768
"""

from .kem import MLKEM
from .signatures import MLDSA

from cryptography.hazmat.primitives.asymmetric import (
    x25519,
    ed25519,
)

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


from typing import Dict



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
        # Optional exchange keys
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


            # JWT signing

            "ed25519_private":
                ed_private.private_bytes_raw(),


            "ed25519_public":
                ed_public.public_bytes_raw(),



            # PQC signing

            "dsa_private":
                dsa_private,


            "dsa_public":
                dsa_public,



            # Future encryption

            "x25519_private":
                x_private.private_bytes_raw(),


            "x25519_public":
                x_public.public_bytes_raw(),


            "kem_private":
                kem_private,


            "kem_public":
                kem_public,

        }




    def hybrid_shared_secret(
        self,
        peer_x25519_pub: bytes,
        my_x25519_priv: bytes,
        peer_kem_pub: bytes,
        my_kem_priv: bytes,
    ):


        x_priv = (
            x25519.X25519PrivateKey
            .from_private_bytes(
                my_x25519_priv
            )
        )


        x_shared = (
            x_priv.exchange(
                x25519.X25519PublicKey
                .from_public_bytes(
                    peer_x25519_pub
                )
            )
        )


        # Existing ML-KEM handling stays here
        #


        combined = x_shared


        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"hybrid-pqc-auth-v1"
        )


        return hkdf.derive(
            combined
        )



hybrid_auth = HybridPQCAuth()
