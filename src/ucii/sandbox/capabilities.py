"""
Sandbox Capability Store

Research-only capability experience layer.

This does NOT create real credentials.
It only demonstrates the relationship
between identity and capability.
"""

sandbox_capabilities: dict[str, list[str]] = {}


def attach_capability(
    identity_id: str,
    capability: str,
):
    """
    Associate a simulated capability
    with a sandbox identity.
    """

    if identity_id not in sandbox_capabilities:
        sandbox_capabilities[identity_id] = []

    if capability not in sandbox_capabilities[identity_id]:
        sandbox_capabilities[identity_id].append(
            capability
        )

    return sandbox_capabilities[identity_id]


def get_capabilities(
    identity_id: str,
):
    """
    Retrieve sandbox capabilities.
    """

    return sandbox_capabilities.get(
        identity_id,
        []
    )
