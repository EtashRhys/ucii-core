# Cryptographic Architecture

UCII uses post-quantum cryptographic primitives.

---

## Signature Layer

Algorithm:

ML-DSA-65

Purpose:

- identity signing
- credential verification
- cryptographic authenticity

---

## Key Exchange Layer

Algorithm:

ML-KEM-768

Purpose:

- quantum-resistant key establishment

---

## Cryptographic Backend

UCII uses:

liboqs

for post-quantum cryptographic implementations.

---

## Hybrid Architecture

UCII supports hybrid cryptographic operation combining classical and post-quantum primitives where appropriate.
