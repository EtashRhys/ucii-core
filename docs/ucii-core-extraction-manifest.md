# UCII Core Architecture Manifest

## Purpose

Defines the public architecture boundary of the UCII Core repository.

UCII Core contains the foundational identity infrastructure components intended for public inspection, research, integration, and ecosystem development.

---

# Included Components

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

The sandbox demonstrates concepts and relationships. It is not a hosted production identity service.

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

# Excluded Components

UCII Core does not include:

- hosted infrastructure
- production service deployment
- operational analytics systems
- commercial management systems
- private operational tooling

---

# Architecture Principle

UCII Core represents the open identity foundation.

Operational systems built around running infrastructure may exist separately.

Principle:

Open Core.

Private Operations.

---

# Repository Goal

The purpose of UCII Core is to provide:

- transparent identity primitives
- cryptographic foundations
- developer adoption
- interoperability
- research and experimentation
