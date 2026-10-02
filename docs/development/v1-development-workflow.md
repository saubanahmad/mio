# V1 Development Workflow

## Principle

Mio V1 should be developed in small, verifiable increments.

Do not implement the entire V1 in one task.

---

# Implementation Order

Use the following sequence unless a documented technical reason requires a change.

## Step 1 — Application Bootstrap

Create the minimal PySide6 application lifecycle.

Verify:

- application starts
- application exits
- no unnecessary UI exists

---

## Step 2 — Pet Window

Implement:

- transparent window
- frameless presentation
- appropriate size
- initial position
- appropriate desktop behavior

Verify manually on Windows.

---

## Step 3 — Dragging

Implement natural mouse-based pet dragging.

Verify:

- click does not accidentally trigger dragging
- dragging moves the pet correctly
- releasing the mouse ends dragging correctly

---

## Step 4 — Pet State

Implement the initial state model.

Begin with only the states required by the current functionality.

Do not implement unused complexity.

---

## Step 5 — Animation

Connect semantic pet states to animation.

Animation assets must remain replaceable.

---

## Step 6 — Interaction

Add the required mouse/context interactions.

Do not add utilities yet.

---

## Step 7 — File Drop

Implement file drag-and-drop detection.

At this stage:

- detect paths
- validate paths
- create the appropriate event/result
- show basic feedback

Do not process the files.

---

## Step 8 — Lifecycle and Cleanup

Verify:

- startup
- shutdown
- resource cleanup
- error handling

---

## Step 9 — Testing

Add appropriate tests for non-visual logic.

Run the test suite.

---

# Agent Rules During V1

Before modifying code:

1. Read `AGENTS.md`.
2. Read `PROJECT.md`.
3. Read `ARCHITECTURE.md`.
4. Read `ROADMAP.md`.
5. Read the relevant V1 documentation.
6. Inspect existing code.

Before creating a new abstraction:

1. Search the repository.
2. Check whether the capability already exists.
3. Reuse existing code where appropriate.

After implementation:

1. Run relevant tests.
2. Check for lint/type issues when configured.
3. Verify the application manually when the change is visual.
4. Report exactly what changed.

Do not implement unrelated functionality.
