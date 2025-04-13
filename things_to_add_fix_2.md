### 2.8 Requirement: Tune Player Movement and Jump Parameters

*   **ID:** TASK-008
*   **Type:** Balancing / Tuning
*   **Description:** The current player movement speed feels too fast, and the jump height allows the player to clear obstacles too easily, potentially trivializing intended platforming challenges. Adjust player physics constants.
*   **Goal:** Achieve a more controlled and balanced feel for player movement and jumping that suits the puzzle-platformer genre.
*   **Acceptance Criteria:**
    *   Player `PLAYER_MAX_SPEED`, `PLAYER_ACCELERATION`, and `PLAYER_JUMP_FORCE` constants (in `constants.py`) are adjusted.
    *   Movement feels responsive but not uncontrollably fast.
    *   Jump height is sufficient for intended platforming but doesn't allow bypassing core challenges easily.
    *   Gameplay testing confirms improved movement feel.

### 2.9 Requirement: Fix Player Interaction with Dynamic Boxes

*   **ID:** TASK-009
*   **Type:** Bugfix / Physics Interaction
*   **Description:** When the player attempts to stand on top of movable boxes, they are sometimes pushed off or slide uncontrollably. Furthermore, jumping on a box with the `Bouncy` modifier applied doesn't consistently propel the player upwards as expected.
*   **Goal:** Ensure stable and predictable physics interactions between the player and dynamic boxes, allowing players to stand on them and utilize their modified properties (like Bouncy).
*   **Acceptance Criteria:**
    *   The player can stand stably on top of stationary boxes without excessive sliding or being pushed off.
    *   Jumping onto a box with the `Bouncy` modifier correctly applies an upward force/bounce to the player.
    *   Collision response between player and box physics bodies is adjusted (potentially friction, restitution, collision shape adjustments).

### 2.10 Requirement: Create Initial Levels using ASCII Format

*   **ID:** TASK-010
*   **Type:** Content Creation / Implementation
*   **Description:** Create several initial game levels (e.g., 3-5 levels, including tutorial stages) using the newly implemented ASCII/Text Grid level format (`.txt` files). Include necessary metadata (level name, hints) potentially in a companion file or via comments/sections if the parser supports it.
*   **Goal:** Populate the game with playable content demonstrating the core mechanics and the new level format.
*   **Acceptance Criteria:**
    *   Multiple `.txt` level files are created in the `levels/` directory (or designated path).
    *   Levels are parsable and load correctly via TASK-002 implementation.
    *   Levels demonstrate core mechanics (movement, modifiers like Bouncy, Heavy, Floaty).
    *   Levels include player start, goal, platforms, and necessary dynamic objects.
    *   Associated metadata (name, description, hints) is correctly loaded and displayed (if applicable).

### 2.11 Requirement: Implement Object Type System & Add New Object Types

*   **ID:** TASK-011 (Revised)
*   **Type:** Feature / Refactor / Content Expansion
*   **Description:** Refactor game object creation to use a type-based system. Define distinct object types, each with default properties (sprite/color, physics settings, modifiability, behavior logic). Implement **at least four** new, diverse object types from the list of examples below (or similar concepts) to create more varied puzzle scenarios.
*   **Goal:** Create a more organized and extensible system for handling game objects and significantly increase the potential for varied and complex puzzle design.
*   **Acceptance Criteria:**
    *   A system (e.g., dictionary mapping, factory pattern, classes) exists to define default properties and behaviors based on an object `type` string.
    *   Object instantiation uses this type system.
    *   The level format supports specifying these new types and their necessary parameters (e.g., movement points, target IDs).
    *   **At least four** new object types (chosen from the list below or similar) are implemented and function correctly within the game engine and physics system.

#### **Potential New Object Types (Examples):**

1.  **`Moving_Platform`**
    *   **Function:** Traverses between two or more defined points (e.g., horizontally, vertically, diagonally, or in a loop). Carries the player and other dynamic objects.
    *   **Parameters:** List of points (`[{x:100, y:200}, {x:400, y:200}]`), speed, pause time at points.
    *   **Modifier Interaction:** `Heavy` might slow/stop it; `Reversed` might reverse path; `Ghostly` might allow phasing through ghost walls.

2.  **`Death_Zone` (e.g., Lava, Spikes, Acid)**
    *   **Function:** A static area triggering level reset/death on player contact.
    *   **Parameters:** Shape/area definition.
    *   **Modifier Interaction:** `Floaty` (Player) might help cross short gaps; `Ghostly` (Player) might allow passage only if zone itself is phaseable (rare); `Heavy` (Object) destroys object.

3.  **`Pressure_Plate` / `Switch_Timed`**
    *   **Function:** Activates linked objects (`target_id`) when sufficient weight is applied or for a set duration.
    *   **Parameters:** `target_id`, required weight (optional), activation time (for timed variant).
    *   **Modifier Interaction:** `Heavy` (Object) ideal for activation; `Floaty` likely insufficient; `Bouncy` might trigger briefly.

4.  **`Door_Toggle` / `Gate_Powered`**
    *   **Function:** Obstacle that opens/closes when triggered by a linked switch.
    *   **Parameters:** Initial state (open/closed), linked by `target_id` from switch.
    *   **Modifier Interaction:** `Ghostly` allows passing if closed; Door itself *could* potentially be modified (`Sticky` gets stuck, `Heavy` harder to open - optional).

5.  **`One_Way_Platform`**
    *   **Function:** Platform passable from below but solid from above.
    *   **Parameters:** Direction of pass-through (usually Up).
    *   **Modifier Interaction:** `Ghostly` might allow passing downwards; `Heavy` could break fragile variants.

6.  **`Target_Switch`**
    *   **Function:** Activates linked objects (`target_id`) when *hit* by another object or the mallet. Resettable or permanent.
    *   **Parameters:** `target_id`, reset delay (if applicable).
    *   **Modifier Interaction:** `Bouncy` (Object) good for ricochet activation; `Heavy` (Object) might trigger heavy impact variation.

7.  **`Conveyor_Belt`**
    *   **Function:** Surface automatically pushing player/objects in a specific direction.
    *   **Parameters:** Direction, speed.
    *   **Modifier Interaction:** `Reversed` could invert perceived direction; `Heavy` might resist force; `Sticky` might stick to belt or resist push.

8.  **`Enemy_Patrol_Simple`**
    *   **Function:** Simple entity moving between points; resets level on player contact.
    *   **Parameters:** Patrol points, speed.
    *   **Modifier Interaction:** Core mechanic! `Bouncy` (harmless bounce?), `Heavy` (slow/stop?), `Floaty` (float away?), `Sticky` (get stuck/grabbable?), `Reversed` (change direction?), `Ghostly` (pass walls?).

9.  **`Modifier_Neutralizer_Zone`**
    *   **Function:** Area removing active modifiers from objects/player entering it.
    *   **Parameters:** Shape/area definition.
    *   **Modifier Interaction:** Removes modifiers.

10. **`Fragile_Block` / `Crate_Weak`**
    *   **Function:** Breaks after sustained weight, heavy impact, or long fall.
    *   **Parameters:** Health/duration/impact threshold.
    *   **Modifier Interaction:** `Heavy` can break it; `Floaty` might prevent impact breakage.

### 2.12 Requirement: Refine Ghostly Collision Logic (Floor/Edges/Special Walls)

*   **ID:** TASK-012
*   **Type:** Bugfix / Refinement (Refines TASK-004)
*   **Description:** Further refine the collision logic for the `Ghostly` modifier. Specifically ensure that Ghostly objects do not pass through the floor or exit the screen boundaries. Confirm that Ghostly phasing *only* occurs with specifically designated "ghost walls" or "phaseable" object types, and not standard walls or platforms.
*   **Goal:** Ensure the Ghostly modifier is robust, predictable, and works exactly as intended without causing game-breaking bugs like falling out of the world.
*   **Acceptance Criteria:**
    *   Ghostly objects collide correctly with all designated `GROUND` layer/type objects.
    *   Ghostly objects collide with invisible screen boundaries (or world limits) to prevent exiting the playable area.
    *   A specific type/layer exists for walls/objects intended to be phased through (e.g., `GHOST_WALL`).
    *   Ghostly objects only ignore collisions with objects of type/layer `GHOST_WALL`.
    *   Ghostly objects collide normally with all other standard wall/platform types.

---