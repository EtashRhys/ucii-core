# Contributing to UCII Core

Thank you for your interest in contributing to UCII Core.

UCII Core is the open-source foundation for Universal Cryptographic Identity Infrastructure.

The project focuses on transparent, inspectable identity primitives and cryptographic infrastructure.

---

# Contribution Philosophy

UCII Core follows:

**Open Core. Private Operations.**

The public repository contains the foundational identity layer.

Contributions should preserve:

- transparency
- modularity
- interoperability
- cryptographic clarity
- developer usability

---

# Areas of Contribution

Contributions are welcome in:

- identity models
- identity lifecycle concepts
- credential structures
- verification workflows
- cryptographic validation
- post-quantum cryptographic foundations
- documentation
- examples
- testing
- developer tooling

---

# Development Setup

Clone the repository:

    git clone <repository-url>
    cd ucii-core

Create a virtual environment:

    python -m venv .venv
    source .venv/bin/activate

Install UCII Core:

    pip install -e .

Run validation:

    pytest

---

# Pull Requests

Before submitting:

1. Create a feature branch.
2. Make changes.
3. Add tests where appropriate.
4. Run the test suite.
5. Submit a pull request.

Example:

    git checkout -b feature/example-change
    git add .
    git commit -m "Describe change"
    git push origin feature/example-change

---

# Code Guidelines

Contributions should:

- remain focused
- avoid unnecessary dependencies
- include tests when practical
- maintain clear documentation
- preserve modular architecture

---

# Security

Please do not publicly disclose security vulnerabilities.

See:

SECURITY.md

---

# License

Contributions are provided under the project's license.

See:

LICENSE
