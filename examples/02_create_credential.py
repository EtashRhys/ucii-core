from ucii import (
    Identity,
    IdentityType,
    Credential,
    CredentialType,
)


identity = Identity(
    name="Example Human",
    identity_type=IdentityType.HUMAN,
)


credential = Credential(
    identity_id=identity.id,
    credential_type=CredentialType.ML_DSA_SIGNING_KEY,
    algorithm="ML-DSA-65",
    public_key="example-public-key",
    fingerprint="example-fingerprint",
)


print("UCII Core Credential Example")
print()

print("Identity:")
print("  ID:", identity.id)
print("  Type:", identity.identity_type.value)

print()

print("Credential:")
print("  ID:", credential.id)
print("  Type:", credential.credential_type.value)
print("  Algorithm:", credential.algorithm)
print("  Fingerprint:", credential.fingerprint)
