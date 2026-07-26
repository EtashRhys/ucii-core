# Contributing to ucii

Thank you for your interest in UCII.

## Status

The UCII implementation repository contains private infrastructure code.

Public documentation and developer resources are maintained separately at:

https://github.com/EtashRhys/UCII-Documentation

## How to Contribute

1. **Fork** the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests where possible
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a **Pull Request**

## Development Setup

```bash
# Clone the repo
git clone https://github.com/EtashRhys/UCII.git
cd UCII

# Install with uv (recommended)
uv sync --dev

# Or with pip
pip install -e ".[dev]"
