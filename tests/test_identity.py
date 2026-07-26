from ucii.identity.models import Identity, IdentityType


def test_identity_creation():
    identity = Identity(
        name="Test Identity",
        identity_type=IdentityType.HUMAN,
    )

    assert identity.name == "Test Identity"
    assert identity.identity_type == IdentityType.HUMAN
