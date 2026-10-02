# Mio Roadmap

## Development Philosophy

Mio will be developed incrementally.

Each phase should produce a usable and testable result.

Do not implement future-phase functionality early unless explicitly requested.

---

# V1 — Desktop Companion

Goal:

Create the basic Mio desktop companion experience.

Planned capabilities:

- transparent desktop pet window
- always-on-top behavior where appropriate
- draggable pet
- basic animation/state system
- mouse interaction
- context/menu interaction
- drag-and-drop file detection
- clean application exit
- initial Windows desktop integration

No AI.

No large utility suite.

No unnecessary future infrastructure.

---

# V2 — Personal Utilities

Goal:

Add useful personal utilities while preserving the existing architecture.

Initial candidates:

- sticky notes
- image compression
- PDF creation

All functionality should be implemented through the tool architecture.

---

# V3 — Desktop Utilities

Goal:

Expand Mio into a useful desktop utility hub.

Potential capabilities:

- file utilities
- clipboard tools
- screenshot tools
- additional quick utilities
- Windows integration

Exact feature scope should be determined before implementation.

---

# V3.5 — Tool Architecture Hardening

Goal:

Ensure the application has a mature foundation before AI is introduced.

Potential work:

- tool registry
- command system
- event system
- task management
- structured tool results
- permission/confirmation model
- logging
- testing improvements
- documentation improvements

Only implement systems that are justified by actual project requirements.

---

# V4 — AI Assistant

Goal:

Allow users to control existing Mio capabilities using natural language.

Examples:

"Compress these images."

"Create a PDF from these files."

"Take a screenshot."

"Create a note."

AI should interact with Mio through registered tools.

AI must not bypass the application/tool architecture.

---

# V5 — Local File Intelligence

Goal:

Allow Mio to understand and operate on local user files through natural-language commands.

Potential examples:

"Compress all the images in this folder."

"Find the presentation I worked on last week."

"Organize these PDFs."

"Find duplicate images."

"Create a PDF from the screenshots I just took."

All file operations must remain subject to appropriate permissions and confirmation rules.

---

# Current Phase

The project begins in:

**V1 — Desktop Companion**

The immediate objective is to establish the project foundation and then implement the smallest useful V1 incrementally.
