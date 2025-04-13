# Product Requirements Document: Modifier Mallet - Development Phase 2

## 1. Overview

This document outlines specific requirements, features, and bug fixes identified for the current development phase of the "Modifier Mallet" game prototype. These tasks aim to improve core mechanics, usability, level creation workflow, and overall stability.

---

## 2. Current Development Tasks / Requirements

### 2.1 Requirement: Refactor Settings into `constants.py`

*   **ID:** TASK-001
*   **Type:** Refactor / Maintainability
*   **Description:** Consolidate scattered game parameters (physics values, colors, keys, UI settings, etc.) into a single, dedicated `constants.py` file. All game code should reference this central file for configuration values.
*   **Goal:** Improve code maintainability, simplify game tuning, and establish a single source of truth for configuration.
*   **Acceptance Criteria:**
    *   All relevant magic numbers and configuration literals are moved to `constants.py`.
    *   Code successfully imports and utilizes constants from `constants.py`.
    *   The game runs correctly with the centralized constants.

### 2.2 Requirement: Implement ASCII/Text Grid Level Loading

*   **ID:** TASK-002
*   **Type:** Feature / Tooling
*   **Description:** Implement a level loading system capable of parsing simple text files (`.txt`) where ASCII characters represent different game objects and tiles on a grid. This should replace or supplement the manual JSON coordinate entry.
*   **Goal:** Provide a faster, more visual, and less error-prone method for level design compared to direct coordinate input.
*   **Acceptance Criteria:**
    *   A clear mapping between ASCII characters and game object types is defined.
    *   The `LevelManager` (or equivalent) can parse a `.txt` level file.
    *   Game objects (player start, goal, platforms, boxes, etc.) are correctly instantiated at positions derived from their grid location in the text file.
    *   The game can successfully load and play levels defined in this format.

### 2.3 Requirement: Add Cooldown to Modifier Cycling

*   **ID:** TASK-003
*   **Type:** Bugfix / User Experience (UX)
*   **Description:** Implement a short time delay (cooldown) after the player presses the modifier cycle keys (Q/E) before another cycle input is registered. Currently, cycling is too fast, making selection difficult.
*   **Goal:** Improve the usability and reduce frustration when selecting the desired modifier.
*   **Acceptance Criteria:**
    *   Pressing Q or E rapidly only cycles the modifier selection at a controlled, slower rate (e.g., once every ~0.15 seconds).
    *   Modifier selection feels responsive but controlled.

### 2.4 Requirement: Prevent Ghostly Objects from Falling Through Floor

*   **ID:** TASK-004
*   **Type:** Bugfix / Core Mechanic
*   **Description:** Objects with the `Ghostly` modifier applied should phase through designated obstacles (e.g., specific wall types) but must still collide correctly with essential solid surfaces like the main ground/floor to prevent falling out of the level.
*   **Goal:** Ensure the `Ghostly` modifier works as intended for bypassing specific obstacles without breaking core level integrity.
*   **Acceptance Criteria:**
    *   A mechanism (e.g., physics layers/masks or collision type checks) is implemented to differentiate between phaseable obstacles and essential solid ground.
    *   Ghostly objects correctly collide with and rest upon designated ground surfaces.
    *   Ghostly objects can still pass through designated "ghost walls" or similar obstacles.

### 2.5 Requirement: Implement Full Interaction for Dynamic Boxes

*   **ID:** TASK-005
*   **Type:** Feature / Core Mechanic
*   **Description:** Ensure movable box objects ("Red Boxes") function as fully interactive physics objects. They should be pushable by the player and react correctly to all applied modifiers (Bouncy, Heavy, Floaty, Sticky, Reversed, Ghostly).
*   **Goal:** Make boxes a core interactive puzzle element that behaves consistently with the game's modifier system.
*   **Acceptance Criteria:**
    *   Boxes have appropriate physics bodies and colliders.
    *   The player can exert force on boxes to move them.
    *   Applying `Bouncy` makes boxes bounce significantly upon collision.
    *   Applying `Heavy` increases their mass, making them harder to push and effective on switches.
    *   Applying `Floaty` reduces their gravity influence.
    *   (Dependencies) Applying `Sticky` allows grabbing/dragging (see TASK-007).
    *   Applying `Reversed` inverts their horizontal reaction to forces (if applicable).
    *   Applying `Ghostly` allows them to pass through appropriate obstacles (while respecting TASK-004).

### 2.6 Requirement: Fix Edge/Wall Jump Exploit

*   **ID:** TASK-006
*   **Type:** Bugfix / Core Mechanic
*   **Description:** Prevent the player from gaining an extra jump or excessive vertical height by jumping against the vertical edge or side of platforms while already in the air.
*   **Goal:** Ensure jumping behaves consistently and predictably, preventing sequence breaks or unintended shortcuts.
*   **Acceptance Criteria:**
    *   The player's `is_grounded` status is reliably determined based on contact with a surface *below* them.
    *   Jumping is only possible when the player is correctly grounded.
    *   Colliding with the side of a platform mid-air does not reset the player's ability to jump.

### 2.7 Requirement: Implement "Grab and Drag" for Sticky Modifier

*   **ID:** TASK-007
*   **Type:** Feature / Core Mechanic
*   **Description:** Implement the primary functionality for the `Sticky` modifier, allowing the player to "grab" objects marked as Sticky and drag them around the environment using mouse input (or equivalent).
*   **Goal:** Introduce a precise object manipulation mechanic for puzzle-solving via the Sticky modifier.
*   **Acceptance Criteria:**
    *   Objects with the `Sticky` modifier applied can be targeted by the player (e.g., mouse click).
    *   A dragging mechanic (preferably physics-based force application) moves the grabbed object towards the player's cursor/target point.
    *   The player can release the grabbed object.
    *   The grab is automatically released if the `Sticky` modifier is removed from the object mid-drag.
    *   Dragging interacts reasonably with other physics forces and modifiers (e.g., dragging a `Heavy` object feels heavier).

---