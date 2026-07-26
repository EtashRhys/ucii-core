# UCII Core Open Source Boundary

## Purpose

This document defines the architectural boundary of the UCII Core repository.

UCII Core is the open-source identity foundation of Universal Cryptographic Identity Infrastructure.

The repository focuses on transparent, inspectable, and reusable identity primitives.

---

# Public UCII Core Components

## Identity Layer

Location:

src/ucii/identity

Purpose:

Defines identity primitives, lifecycle concepts, identity models, and identity relationships.

Status:

PUBLIC

---

## Credential Layer

Location:

src/ucii/credential

Purpose:

Defines credential structures, cryptographic ownership verification concepts, credential relationships, and verification primitives.

Status:

PUBLIC

---

## Post-Quantum Cryptography Layer

Location:

src/ucii/pqc

Purpose:

Provides post-quantum cryptographic foundations and hybrid cryptographic implementations.

Status:

PUBLIC

---

## Sandbox Reference Environment

Location:

src/ucii/sandbox

Purpose:

Provides reference demonstrations of identity relationships, capabilities, and proof concepts.

Status:

PUBLIC REFERENCE IMPLEMENTATION

Note:

The sandbox demonstrates concepts and relationships. It is not a hosted identity service.

---

## Developer Resources

Included:

- examples
- documentation
- security guidance
- contribution guidelines

Status:

PUBLIC

---

# Outside UCII Core

The following categories are intentionally outside this repository:

- hosted identity services
- production deployment infrastructure
- operational monitoring systems
- commercial service layers
- private infrastructure tooling

These systems may exist independently while UCII Core remains focused on the identity foundation.

---

# Architecture Principle

UCII follows the principle:

Open Core.

Private Operations.

The identity primitive should remain transparent and inspectable.

Operational systems built around deployment, hosting, measurement, and commercialization may remain separate.

---

# Repository Goal

UCII Core exists to provide:

- transparent identity primitives
- cryptographic foundations
- developer adoption
- interoperability
- research and experimentation

