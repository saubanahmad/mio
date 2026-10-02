# Mio Agent Instructions

## Project Identity

Mio is a Windows desktop companion and utility hub.

The desktop pet is the primary interface.

The underlying utility and tool system is the actual product.

AI is a future control layer over the existing tool system. AI must not become the architecture of the entire application.

---

## Source of Truth

The following documents define the project:

- `PROJECT.md` — product purpose and principles
- `ARCHITECTURE.md` — technical architecture and boundaries
- `ROADMAP.md` — development phases and scope
- `docs/decisions/` — architectural decisions and their rationale
- `docs/features/` — detailed feature specifications
- `docs/development/` — development-specific procedures

When implementing a feature, read the relevant documentation before modifying the code.

If the documentation and implementation disagree, do not silently invent a third approach. Identify the discrepancy and determine which source should be updated.

---

## Core Development Rules

### 1. Do not invent architecture

Do not introduce architectural patterns, frameworks, libraries, services, or subsystems unless they are required by the current task and consistent with `ARCHITECTURE.md`.

If a proposed change would alter the architecture, document the decision before implementing it.

### 2. Respect project phases

Do not implement functionality belonging to a future roadmap phase unless explicitly instructed to do so.

The current phase is defined in `ROADMAP.md`.

### 3. Keep responsibilities separated

Presentation code must not contain business logic.

Tools must not directly depend on presentation components.

AI must not bypass the application/tool layer.

Windows-specific infrastructure must remain behind appropriate infrastructure abstractions.

### 4. Reuse existing functionality

Before creating a new abstraction, service, helper, utility, or tool:

1. Search the repository.
2. Determine whether equivalent functionality already exists.
3. Reuse or extend it when appropriate.

Do not create duplicate implementations.

### 5. Dependencies

Do not add a dependency simply because it is convenient.

A dependency must have a clear technical reason.

Prefer the Python standard library when it is sufficient.

When a third-party dependency is necessary, use a maintained and appropriate library and document why it is required.

### 6. Minimal changes

When implementing a task, modify only what is necessary to accomplish that task.

Do not refactor unrelated code.

Do not redesign existing systems without a documented reason.

### 7. Testing

New functionality must have appropriate tests.

Do not consider a task complete merely because the code runs once.

Run relevant tests after making changes.

### 8. Error handling

Do not silently swallow errors.

Errors should be handled at an appropriate layer and communicated through structured results, logging, or user-facing feedback when appropriate.

### 9. Security

Never give AI unrestricted access to arbitrary Python execution or unrestricted filesystem operations.

Future AI functionality must operate through explicitly defined tools and permission boundaries.

Destructive operations must have appropriate confirmation mechanisms.

### 10. Documentation

If an implementation changes an architectural decision, update the appropriate documentation.

If a feature introduces a significant new behavior, document it.

Do not allow the documentation to become permanently inconsistent with the code.

### 11. Secrets

Never commit to the repository:

- API keys
- access tokens
- passwords
- private certificates
- credentials
- personal secrets
- private user data

Use environment variables or appropriate local configuration mechanisms when secrets are eventually required.

Never place real secrets in `.env.example`.

### 12. Public Repository Hygiene

Do not commit to the repository:

- Python virtual environments
- build artifacts
- generated caches
- local application data
- user-specific configuration
- IDE-specific personal settings
- temporary files
- test data containing personal information

Before adding a new generated or local file, determine whether it belongs in source control.

### 13. Dependencies

Keep dependencies explicitly declared in the project configuration.

Do not rely on packages being installed globally.

---

## Current Task Rule

When given a development task:

1. Read the relevant project documentation.
2. Inspect the existing repository.
3. Identify the smallest appropriate implementation.
4. Implement it.
5. Test it.
6. Report what changed, what was tested, and any unresolved issues.

Do not begin unrelated work.

---

## Communication Rule

When uncertain about a requirement that materially affects architecture or behavior, do not silently guess.

State the ambiguity and identify the available options.

Do not fabricate requirements.

---

## Quality Goal

Mio should be developed as a real maintainable desktop application, not as a disposable prototype.

Prioritize:

- clear architecture
- maintainability
- predictable behavior
- local-first operation where practical
- user privacy
- testability
- graceful error handling
- polished interaction
- incremental development
