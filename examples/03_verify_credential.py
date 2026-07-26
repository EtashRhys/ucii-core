from ucii import Identity, IdentityType
from ucii.identity.models import (
    Credential,
    CredentialType,
)

from ucii.pqc import MLDSA


identity = Identity(
    name="Example Human",
    identity_type=IdentityType.HUMAN,
)


dsa = MLDSA()

public_key, private_key = (
    dsa.generate_keypair()
)


credential = Credential(
    identity_id=identity.id,
    credential_type=CredentialType.ML_DSA_SIGNING_KEY,
    algorithm="ML-DSA-65",
    public_key=public_key.hex(),
    fingerprint="example-fingerprint",
)


message = b"UCII Core verification example"


signature = dsa.sign(
    message,
    private_key,
)


verified = dsa.verify(
    message,
    signature,
    public_key,
)


print("UCII Core Credential Verification Example")
print()

print("Identity:")
print("  ID:", identity.id)
print("  Type:", identity.identity_type.value)

print()

print("Credential:")
print("  ID:", credential.id)
print("  Algorithm:", credential.algorithm)

print()

print("Proof Verification:")
print("  Result:", "SUCCESS" if verified else "FAILED")
