# UCII API Reference

Universal Cryptographic Identity Infrastructure API.

UCII provides cryptographic identity primitives secured by post-quantum cryptography and protected through x402 economic authorization.

---

# Discovery Endpoints

## Root Service Discovery

Endpoint:

GET /

Returns:

- service identity
- version information
- cryptographic capabilities
- supported identity classes
- ecosystem discovery links

---

## Machine Metadata

Endpoint:

GET /metadata

Returns machine-readable UCII capability metadata.

Includes:

- identity model
- supported identity classes
- PQC algorithms
- x402 economic layer
- service capabilities
- protocol information

---

## x402 Discovery

Endpoint:

GET /v1/x402/info

Returns:

- x402 service metadata
- supported operations
- pricing requirements
- settlement network

---

## OpenAPI Schema

Endpoint:

GET /openapi.json

Interactive documentation:

GET /docs

---

# Identity Operations

## Create Identity

Endpoint:

POST /v1/identity

Creates a new cryptographic identity.

Supported identity classes:

- HUMAN
- AI_AGENT
- ROBOT
- DEVICE
- SERVICE
- ORGANIZATION

---

## Retrieve Identity

Endpoint:

GET /v1/identity/{identity_id}

Retrieves a cryptographic identity record.

---

## List Identities

Endpoint:

GET /v1/identity

Returns available UCII identity records.

---

# Credential Operations

## Register Credential

Endpoint:

POST /v1/credentials/register

Registers a cryptographic credential associated with a UCII identity.

---

## Verify Credential

Endpoint:

POST /v1/credentials/verify

Verifies a cryptographic credential.

---

## Retrieve Credential

Endpoint:

GET /v1/credentials/{fingerprint}

Retrieves credential information by fingerprint.

---

## Revoke Credential

Endpoint:

POST /v1/credentials/{credential_id}/revoke

Revokes a cryptographic credential.

---

# Authentication Compatibility Layer

Authentication is implemented as a compatibility layer built on top of UCII identity primitives.

Identity remains the foundational object.

## Register Authentication User

Endpoint:

POST /v1/auth/register

Creates an authentication-compatible user representation.

---

## Login

Endpoint:

POST /v1/auth/login

Authenticates through the UCII compatibility authentication layer.

---

## Current Authentication Identity

Endpoint:

GET /v1/auth/me

Returns the current authenticated identity context.

---

## Refresh Session

Endpoint:

POST /v1/auth/refresh

Refreshes an authentication session.

---

## Logout

Endpoint:

POST /v1/auth/logout

Terminates an authentication session.

---

## Revoke Authentication Access

Endpoint:

POST /v1/auth/revoke

Revokes authentication access.

---

# x402 Economic Authorization

UCII infrastructure operations are protected through x402 economic authorization.

Paid operations use pay-per-operation settlement.

Read-only discovery endpoints remain publicly accessible.
