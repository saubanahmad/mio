# Mio

## Product

Mio is a Windows desktop companion and utility hub.

The product combines a cute desktop companion interface with a collection of useful local desktop utilities.

The pet is the interface.

The utilities are the product.

AI will eventually provide a natural-language interface for controlling those utilities.

---

## Product Vision

Mio should gradually evolve from a simple desktop companion into a useful local desktop assistant.

The intended progression is:

V1 → Desktop companion

V2 → Personal utilities

V3 → Desktop utilities

V3.5 → Mature tool architecture

V4 → AI assistant

V5 → Local file intelligence and natural-language commands

---

## Core Principles

### Interface First

The pet should make the application feel approachable and distinctive.

The pet should not be responsible for implementing the underlying functionality.

### Capability First

Every useful capability should exist as a properly defined application tool before AI is expected to control it.

### AI as a Control Layer

AI should select and use existing application capabilities.

AI should not directly implement business logic or bypass the application's tool architecture.

### Local First

Whenever practical, functionality should operate locally on the user's Windows machine.

External services should only be introduced when they provide a clear capability that cannot reasonably be provided locally.

### Privacy

Mio should avoid collecting or transmitting user data unnecessarily.

Local files should not be sent to external AI or other services unless the user explicitly enables functionality that requires it.

### Predictability

Mio should behave consistently.

Actions that can modify or destroy user data must have appropriate safeguards.

### Incremental Development

Each version should be useful on its own.

Future functionality should not complicate the current version unnecessarily.

---

## Target Platform

Primary target:

- Windows 10
- Windows 11

The application should be designed specifically for the Windows desktop environment.

Cross-platform support is not currently a project requirement.

---

## Distribution Direction

Mio is intended to eventually become a publicly distributed Windows desktop application.

The project should therefore prioritize:

- maintainable source code
- reproducible development setup
- clear dependency management
- privacy-conscious behavior
- safe handling of local files
- no secrets in source control
- clear versioning
- eventual standalone Windows packaging

Packaging and installers are a later project phase. They are not part of the current V1 implementation.

---

## Product Personality

Mio should feel:

- cute
- friendly
- lightweight
- responsive
- useful
- unobtrusive

The personality belongs primarily to the presentation layer.

It must not compromise the technical architecture or reliability of the application.
