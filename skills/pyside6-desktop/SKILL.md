# PySide6 Desktop Development Skill

## Purpose

This skill provides project-specific guidance for developing Mio's Windows desktop UI with PySide6.

It applies when working on:

- desktop windows
- the Mio pet
- Qt widgets
- mouse interaction
- drag-and-drop
- animations
- menus
- dialogs
- desktop presentation

---

# General Rules

Follow the project's:

- `AGENTS.md`
- `PROJECT.md`
- `ARCHITECTURE.md`

before applying this skill.

This skill does not override project architecture.

---

# UI Architecture

Keep Qt-specific presentation code inside the presentation layer.

Do not place application business logic inside QWidget subclasses unless the behavior is inherently presentation-specific.

Prefer explicit controllers or application-layer coordination for behavior that affects the rest of the application.

---

# Responsiveness

Never perform expensive synchronous work on the GUI thread.

If an operation becomes computationally or I/O intensive, use the project's task/background execution mechanism.

Do not introduce unnecessary threading for trivial operations.

---

# Signals and Events

Use Qt signals/events where they naturally represent UI interaction.

Do not create excessive signal chains when a simple method call is clearer.

Application-level events should remain distinct from purely visual Qt events.

---

# Window Behavior

Mio's pet is a desktop companion, not a conventional application window.

The implementation should use appropriate Qt window configuration for:

- transparency
- frameless presentation
- interaction
- z-order
- desktop positioning

Do not copy window flags from unrelated projects without understanding their effect on Windows behavior.

---

# Mouse Interaction

Mouse interaction should distinguish between:

- click
- press
- movement
- drag
- release

Dragging should use the correct coordinate relationship between the cursor and the pet window.

Avoid behavior that causes the pet to jump when dragging begins.

---

# Drag and Drop

File drag-and-drop should:

1. Accept appropriate drag-enter events.
2. Validate whether usable file URLs/paths are present.
3. Provide visual feedback.
4. Process the drop.
5. Convert paths into the application's appropriate representation.

The presentation layer should not directly perform future file utilities.

---

# Animation

Animation should be controlled through semantic pet states.

Prefer:

```text
Pet State
    ↓
Animation Controller
    ↓
Animation
```

Avoid:

```text
Business Event
    ↓
Hard-coded animation asset
```

Animation assets should remain replaceable.

---

# Resource Management

Resources such as:

* images
* animations
* icons
* sounds

should be loaded through a consistent resource mechanism.

Do not hard-code fragile absolute filesystem paths.

---

# Testing

Prioritize testing of:

* state logic
* path handling
* event translation
* non-visual application logic

Visual behavior should be manually verified during V1.

---

# Dependencies

Do not add additional GUI frameworks.

Mio's desktop UI framework is PySide6 unless an explicit architectural decision changes it.
