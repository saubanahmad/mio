# Mio Architecture

## Architectural Model

Mio uses a layered, tool-oriented architecture.

The primary conceptual flow is:

Presentation
↓
Application
↓
Tools
↓
Infrastructure

Future AI functionality follows:

AI
↓
Application
↓
Tools
↓
Infrastructure

The AI layer must not bypass the application and tool layers.

---

# 1. Presentation Layer

The presentation layer contains everything directly responsible for user interaction and visual presentation.

Responsibilities include:

- desktop pet
- animations
- menus
- dialogs
- utility windows
- notifications
- drag-and-drop interaction
- visual feedback

The presentation layer must not contain core business logic.

Examples:

```text
presentation/
├── pet/
├── menus/
├── windows/
├── dialogs/
└── notifications/
```

---

# 2. Application Layer

The application layer coordinates application behavior.

Responsibilities include:

* commands
* events
* tool registration
* task management
* application state
* coordination between presentation and tools

Conceptual structure:

```text
application/
├── commands/
├── events/
├── registry/
├── tasks/
└── state/
```

The application layer should coordinate functionality rather than directly implementing specialized utility logic.

---

# 3. Tool Layer

Tools contain the actual user-facing capabilities of Mio.

Initial planned categories include:

```text
tools/
├── notes/
├── images/
├── pdf/
├── files/
├── clipboard/
├── screenshots/
└── system/
```

A tool should have clearly defined:

* inputs
* validation
* execution
* results
* errors

Tools should return structured results wherever practical.

The same tool should be usable by:

* GUI actions
* drag-and-drop actions
* future AI commands
* other legitimate application workflows

This prevents multiple implementations of the same capability.

---

# 4. Infrastructure Layer

Infrastructure provides access to external system mechanisms.

Initial categories include:

```text
infrastructure/
├── filesystem/
├── windows/
├── storage/
├── logging/
└── configuration/
```

Infrastructure may interact with:

* Windows APIs
* filesystem
* clipboard
* Windows notifications
* system settings
* local database/storage
* other OS-level facilities

Higher-level application code should not scatter Windows-specific implementation throughout the project.

---

# 5. AI Layer

AI is a future subsystem.

It is not part of the initial implementation phase.

The intended architecture is:

User
↓
AI
↓
Tool selection
↓
Application command
↓
Tool
↓
Infrastructure

AI must not receive unrestricted execution privileges.

AI should operate through explicitly registered application tools.

AI should not directly execute arbitrary Python code.

AI should not directly modify files outside the defined tool and permission system.

---

# 6. Command System

The command system provides a consistent way to request application actions.

Conceptually:

```text
Command
↓
Application
↓
Tool
```

Multiple interfaces may eventually generate commands:

```text
GUI
Drag & Drop
AI
```

All should converge on the same application/tool implementation where appropriate.

---

# 7. Event System

The event system communicates that something happened.

Potential events include:

```text
PET_CLICKED
FILE_DROPPED
TASK_STARTED
TASK_PROGRESS
TASK_COMPLETED
TASK_FAILED
NOTE_CREATED
SCREENSHOT_CAPTURED
```

The final event list should be determined by actual implementation needs.

Do not create an event system merely for theoretical completeness.

---

# 8. Task System

Long-running operations must not block the user interface.

The task system should eventually support appropriate mechanisms for:

* background execution
* progress reporting
* completion
* failure
* cancellation where appropriate

The exact implementation should be selected when the first task requiring it is implemented.

---

# 9. Security and Permissions

Tools should be classified according to their risk.

Examples:

Read-only:

* search files
* list directories
* inspect metadata

Potentially modifying:

* compress files
* create PDF
* move files
* rename files

Destructive:

* delete files
* overwrite files
* bulk modifications

Future AI functionality must use these distinctions when deciding whether confirmation is required.

---

# 10. Dependency Direction

Preferred dependency direction:

```text
Presentation
    ↓
Application
    ↓
Tools
    ↓
Infrastructure
```

AI:

```text
AI
    ↓
Application
    ↓
Tools
    ↓
Infrastructure
```

Avoid circular dependencies.

Avoid having tools depend directly on presentation components.

Avoid having infrastructure depend on high-level application components.

---

# 11. Architecture Evolution

The architecture may evolve as real implementation requirements become clearer.

Architectural changes must:

1. Have a concrete reason.
2. Be documented.
3. Avoid unnecessary rewrites.
4. Preserve existing functionality where practical.

Do not introduce complexity merely because it might become useful later.
