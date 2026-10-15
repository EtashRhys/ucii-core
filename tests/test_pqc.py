from ucii.pqc.hybrid import HybridPQCAuth
from ucii.pqc.kem import MLKEM
from ucii.pqc.signatures import MLDSA


def test_hybrid_pqc_initialization():
    pqc = HybridPQCAuth()

    assert pqc is not None
    assert pqc.dsa is not None
    assert pqc.kem is not None


def test_kem_roundtrip():
    kem = MLKEM()

    public_key, secret_key = kem.generate_keypair()

    ciphertext, shared_secret_a = kem.encapsulate(public_key)

    shared_secret_b = kem.decapsulate(secret_key, ciphertext)

    assert shared_secret_a == shared_secret_b
    assert len(shared_secret_a) == kem.get_shared_secret_length()


def test_kem_wrong_key_mismatch():
    kem = MLKEM()

    public_key, _secret_key = kem.generate_keypair()

    _other_public, other_secret = kem.generate_keypair()

    ciphertext, shared_secret_a = kem.encapsulate(public_key)

    shared_secret_wrong = kem.decapsulate(other_secret, ciphertext)

    assert shared_secret_a != shared_secret_wrong


def test_hybrid_kem_roundtrip():
    pqc = HybridPQCAuth()

    # Bob's long-term keys
    bob_keys = pqc.generate_hybrid_keypair()

    # Alice encapsulates to Bob
    result = pqc.hybrid_encapsulate(
        bob_keys["x25519_public"],
        bob_keys["kem_public"],
    )

    assert len(result["shared_secret"]) == 32

    # Bob decapsulates
    recovered = pqc.hybrid_decapsulate(
        result["x25519_ephemeral_public"],
        bob_keys["x25519_private"],
        result["kem_ciphertext"],
        bob_keys["kem_private"],
    )

    assert recovered == result["shared_secret"]


def test_hybrid_kem_tampered_ciphertext():
    pqc = HybridPQCAuth()

    bob_keys = pqc.generate_hybrid_keypair()

    result = pqc.hybrid_encapsulate(
        bob_keys["x25519_public"],
        bob_keys["kem_public"],
    )

    tampered = bytearray(result["kem_ciphertext"])
    tampered[0] ^= 0xFF
    tampered = bytes(tampered)

    recovered = pqc.hybrid_decapsulate(
        result["x25519_ephemeral_public"],
        bob_keys["x25519_private"],
        tampered,
        bob_keys["kem_private"],
    )

    # ML-KEM implicitly rejects: decapsulation yields a random
    # secret, so it must not match the sender's secret.
    assert recovered != result["shared_secret"]


def test_hybrid_signature_roundtrip():
    pqc = HybridPQCAuth()

    keys = pqc.generate_hybrid_keypair()

    message = b"ucii test message"

    signature = pqc.hybrid_sign(
        message,
        keys["ed25519_private"],
        keys["dsa_private"],
    )

    assert pqc.hybrid_verify(
        message,
        signature,
        keys["ed25519_public"],
        keys["dsa_public"],
    )


def test_hybrid_signature_tampered_message():
    pqc = HybridPQCAuth()

    keys = pqc.generate_hybrid_keypair()

    signature = pqc.hybrid_sign(
        b"original",
        keys["ed25519_private"],
        keys["dsa_private"],
    )

    assert not pqc.hybrid_verify(
        b"tampered",
        signature,
        keys["ed25519_public"],
        keys["dsa_public"],
    )


def test_hybrid_signature_wrong_key():
    pqc = HybridPQCAuth()

    keys = pqc.generate_hybrid_keypair()
    other_keys = pqc.generate_hybrid_keypair()

    message = b"ucii test message"

    signature = pqc.hybrid_sign(
        message,
        keys["ed25519_private"],
        keys["dsa_private"],
    )

    assert not pqc.hybrid_verify(
        message,
        signature,
        other_keys["ed25519_public"],
        other_keys["dsa_public"],
    )


def test_hybrid_signature_malformed():
    pqc = HybridPQCAuth()

    keys = pqc.generate_hybrid_keypair()

    # Never raises; returns False on garbage input.
    assert not pqc.hybrid_verify(
        b"message",
        b"too short",
        keys["ed25519_public"],
        keys["dsa_public"],
    )
