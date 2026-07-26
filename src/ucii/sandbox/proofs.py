"""
Sandbox Proof Experience Store

Research-only proof experience layer.

This does NOT create real cryptographic proofs.
It demonstrates how identities may
participate in proof relationships.
"""

sandbox_proofs: dict[str, list[str]] = {}


def create_proof(
    identity_id: str,
    proof_type: str,
):
    """
    Associate a simulated proof experience
    with a sandbox identity.
    """

    if identity_id not in sandbox_proofs:
        sandbox_proofs[identity_id] = []

    if proof_type not in sandbox_proofs[identity_id]:
        sandbox_proofs[identity_id].append(
            proof_type
        )

    return proof_type


def get_proofs(
    identity_id: str,
):
    """
    Retrieve sandbox proof experiences.
    """

    return sandbox_proofs.get(
        identity_id,
        []
    )
