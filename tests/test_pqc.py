from ucii.pqc.hybrid import HybridPQCAuth


def test_hybrid_pqc_initialization():
    pqc = HybridPQCAuth()

    assert pqc is not None
    assert pqc.dsa is not None
    assert pqc.kem is not None
