# V1 Desktop Companion

## Objective

V1 establishes Mio as a persistent Windows desktop companion.

The objective is not to create a large utility application.

The objective is to establish the core companion interaction model that future Mio functionality will build upon.

---

# V1 Scope

V1 includes:

- transparent desktop pet window
- pet visual/animation system
- draggable pet
- mouse interaction
- basic pet states
- context interaction
- drag-and-drop file detection
- basic application lifecycle
- clean application exit
- appropriate Windows desktop behavior

---

# V1 Explicitly Excludes

V1 does not include:

- AI
- natural-language commands
- image compression
- PDF creation
- sticky notes
- clipboard history
- screenshot utilities
- file organization
- advanced Windows automation
- cloud services
- accounts
- remote APIs unless required by an explicitly approved feature

Do not implement excluded functionality as part of V1.

---

# Pet Interaction

The pet should support:

## Left mouse interaction

Used for the primary pet interaction.

The exact behavior should be defined by the current implementation task.

Do not invent a large interaction system before it is needed.

## Dragging

The user should be able to reposition Mio on the desktop.

Dragging should feel natural and should not interfere unnecessarily with normal clicking.

## Right-click interaction

A context interaction should eventually provide basic application controls such as:

- settings
- future utilities
- exit

Only functionality actually implemented in V1 should be exposed.

## File drag-and-drop

The pet should accept files dragged from Windows Explorer.

V1 only needs to detect and report the dropped files.

It does not need to process them yet.

---

# Pet States

The initial state model should support only states justified by V1.

Candidate states include:

- idle
- happy
- thinking
- working
- sleeping
- error

Not every state needs to be implemented immediately.

States should be represented independently from animation assets.

The state system should determine the current semantic state.

The animation system should determine how that state is visually represented.

---

# Animation

Animation should be treated as a presentation concern.

The architecture should allow:

```text
Pet State
    ↓
Animation Controller
    ↓
Visual Animation
```

Do not hard-code business behavior into animation code.

Animation assets should be replaceable without changing application logic.

---

# Window Requirements

The Mio pet window should support the characteristics required for a desktop companion.

Expected characteristics include:

* transparent background
* frameless presentation
* appropriate window size
* appropriate z-order behavior
* mouse interaction
* dragging
* no unnecessary standard window decorations

The exact Qt flags and implementation details should be selected during implementation.

Do not hard-code platform-specific behavior outside the appropriate infrastructure/presentation boundary.

---

# File Drop Behavior

When files are dropped onto Mio:

1. Detect the drop.
2. Collect the dropped paths.
3. Validate that the paths are accessible.
4. Produce a structured application event/result.
5. Provide basic visual feedback.

V1 does not perform utility operations on the files.

Future versions will connect file-drop events to tools.

---

# Lifecycle

Mio must:

* start cleanly
* initialize required application resources
* remain responsive
* handle normal exit
* release resources appropriately

Unexpected exceptions should not be silently swallowed.

---

# V1 Completion Criteria

V1 is considered functionally complete when:

* Mio launches successfully on Windows.
* The pet is visible with the intended transparent presentation.
* The pet can be moved around the desktop.
* Basic mouse interaction works.
* The pet has a working state/animation mechanism.
* Files can be dragged onto the pet and detected.
* The application can be exited cleanly.
* The UI remains responsive during normal interaction.
* Relevant automated tests exist for non-visual logic.
* The implementation follows `ARCHITECTURE.md`.
