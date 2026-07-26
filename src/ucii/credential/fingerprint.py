"""
Credential Fingerprint Generation

Creates stable identifiers for
cryptographic credentials.

A fingerprint identifies a credential
by hashing its public verification material.

Private keys are never used.

The fingerprint represents the
cryptographic credential itself.
"""


import hashlib



def generate_fingerprint(
    public_key: bytes,
) -> str:
    """
    Generate a deterministic credential fingerprint.

    Fingerprints are derived only from public
    cryptographic material.

    Args:
        public_key:
            Raw public key bytes.

    Returns:
        Hexadecimal SHA-256 fingerprint string.
    """

    return hashlib.sha256(
        public_key
    ).hexdigest()