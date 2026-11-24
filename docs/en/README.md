# HumOS — English documentation hub

HumOS (Human Operating System) is a cognitive-management framework that applies operating-system concepts to working memory, attention, recurring thought loops, boundaries, and self-regulation. Its implementation combines the **LINGHOS** domain-specific language, a Python runtime, the **G.A.P.** protocol model, and the browser-based **HumOS Cockpit GUI**.

This repository contains both implemented software and evolving architectural documentation. Read the implementation-status notes in the specifications before treating a documented primitive or security property as a runtime guarantee.

## Start here

- [Root project README](../../README.md) — overview, architecture, quick start, and examples.
- [LINGHOS specification](../SPEC.md) — syntax and architectural reference.
- [Developer guide](../GUIDE.md) — implementation walkthrough and integration examples.
- [LINGHOS language notes](LINGHOS.md) — language concepts and design history.
- [HumOS framework document](HumOS-Framework.md) — broader conceptual framework.
- [HumOS Cockpit GUI](../../src/linghos/cockpit.html) — visual editor and runtime console.
- [Runnable examples](../../examples/) — scripts and Python integration sample.

## Governance and security

- [Contribution guidelines](../../CONTRIBUTING.md)
- [Security policy](../../SECURITY.md)
- [G.A.P.-001 protocol](../../protocols/en/GAP-001-protocol.md)
- [License](../../LICENSE.txt) — Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).

## Runtime commands

From the repository root:

```bash
python3 src/app.py
```

For the package CLI, from `src/` after installing the package:

```bash
python3 -m linghos --help
```

The package metadata declares Python 3.8 or newer. See the root README and package metadata for the current setup details.

---

[Italian documentation hub](../it/README.md) · [Repository on GitHub](https://github.com/SystemAdmin01/HumOS)
