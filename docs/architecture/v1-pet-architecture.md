# V1 Pet Architecture

## Purpose

This document defines the architecture specifically for the V1 desktop companion.

V1 should remain small while establishing boundaries that future versions can extend.

---

# Components

The initial V1 architecture consists of:

```text
Mio Application
│
├── Pet Presentation
│   ├── Pet Window
│   ├── Interaction Handling
│   ├── Animation Controller
│   └── Visual Assets
│
├── Application Coordination
│   ├── Application Lifecycle
│   ├── Pet State
│   └── File Drop Events
│
└── Windows/Desktop Infrastructure
```

Do not introduce additional architectural layers unless justified by an actual requirement.

---

# Pet Window

The Pet Window owns:

* visual presentation
* mouse interaction
* drag interaction
* drag-and-drop UI interaction
* visual feedback

It must not implement future utility logic.

---

# Pet State

Pet state represents what Mio is conceptually doing.

Example:

```text
IDLE
HAPPY
THINKING
WORKING
SLEEPING
ERROR
```

The state model should remain independent from specific animation assets.

---

# Animation Controller

The animation controller maps semantic states to visual animation.

Example:

```text
IDLE
 ↓
idle animation

HAPPY
 ↓
happy animation

WORKING
 ↓
working animation
```

The controller should not contain business logic.

---

# Application Coordination

Application-level coordination is responsible for:

* startup
* shutdown
* state transitions
* file-drop event propagation
* future command/event integration

Do not put this logic inside animation classes.

---

# File Drop Flow

The intended flow is:

```text
Windows Explorer
       ↓
Pet Window
       ↓
Drop Handler
       ↓
Application Event
       ↓
Future Tool System
```

In V1, the final tool-system step does not exist.

The event should instead terminate in a structured V1 result/feedback mechanism.

---

# Dependency Direction

Preferred dependency direction:

```text
Pet Presentation
       ↓
Application Coordination
       ↓
Windows Infrastructure
```

Presentation should not depend on future AI systems.

V1 should not introduce the AI layer.

---

# Threading

The GUI thread must remain responsive.

Long-running work should not execute directly on the GUI thread.

Do not introduce background threading merely for theoretical future requirements.

Introduce the appropriate task mechanism when an actual operation requires it.

---

# Testability

Pure logic should be separated from Qt-specific UI behavior wherever practical.

Tests should prioritize:

* state transitions
* file-drop path handling
* validation
* application logic

Visual behavior may require manual verification or appropriate GUI testing mechanisms.
