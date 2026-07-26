# UCII x402 Integration

UCII uses x402 as the economic authorization layer.

Identity remains the primitive.

x402 provides payment authorization for infrastructure operations.

---

# Payment Flow

1. Client requests a protected UCII operation.

2. UCII returns HTTP `402 Payment Required`.

3. Client submits payment authorization proof.

4. UCII verifies settlement.

5. Operation executes.

6. Settlement receipt is recorded.

---

# Discovery

UCII exposes:

GET /v1/x402/info

This endpoint provides:

- service identity
- supported capabilities
- operation pricing
- settlement network
- supported x402 operations

---

# Settlement

Current settlement configuration:

- Protocol: x402
- Currency: USDC
- Network: Solana
- Model: pay-per-operation

---

# Settlement Records

UCII exposes settlement information through:

GET /v1/x402/settlements

Settlement receipts are tracked to provide replay protection and payment verification history.

---

# Design Principle

UCII does not replace x402.

UCII uses x402 as the economic access mechanism for cryptographic identity infrastructure.

Identity is the primitive.

x402 is the economic authorization layer.
