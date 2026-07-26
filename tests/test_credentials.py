from ucii.credential.verifier import CredentialVerifier


def test_credential_verifier_initialization():
    verifier = CredentialVerifier(
        algorithm_provider=None
    )

    assert verifier is not None
