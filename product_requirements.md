# Product Requirements Document: Modifier Mallet (Working Title)

---

## 1. Overview & Vision

*   **1.1. Game Title:** Modifier Mallet (Working Title - e.g., "Bonk!", "Whack & Switch", "Property Plonker")
*   **1.2. Game Genre:** 2D Puzzle Platformer
*   **1.3. Core Concept:** A physics-based puzzle game where the player uses a magical mallet to temporarily apply tangible property modifiers (e.g., `Bouncy`, `Heavy`, `Floaty`) to objects, the environment, and themselves to navigate levels and solve puzzles.
*   **1.4. Inspiration:** Draws inspiration from the rule manipulation of "Baba Is You" and the tool-based spatial problem-solving of "Portal", presented with a lighthearted, slapstick physics feel.
*   **1.5. Goal:** To create a functional and funny prototype game for practice, focusing on implementing a core unique mechanic, exploring specific software architectures (OOP, MVC, ECS principles), and potentially interesting algorithms within a manageable scope.
*   **1.6. Target Audience:** Players who enjoy puzzle games, physics-based sandboxes, indie games with unique mechanics, and lighthearted humour.

---

## 2. Gameplay & Mechanics

*   **2.1. Core Gameplay Loop:**
    1.  **Observe:** Analyze the level layout, obstacles, goal, and available modifiable objects.
    2.  **Strategize:** Determine which modifiers need to be applied to which objects (and potentially the player) in what order.
    3.  **Select Modifier:** Choose the desired modifier using the UI.
    4.  **Apply Modifier:** Use the Mallet to hit a modifiable target, applying the selected modifier (respecting the active modifier limit).
    5.  **Interact:** Utilize the modified object's new properties (jump on bouncy things, use heavy things on switches, etc.).
    6.  **Adapt:** Remove modifiers (by hitting again) or apply different ones as needed to overcome subsequent challenges.
    7.  **Solve & Progress:** Reach the level exit.
*   **2.2. Player Character ("Bonk")**
    *   **Controls:** Left/Right Movement, Jump, Swing Mallet, Select Modifier (e.g., scroll wheel, number keys).
    *   **Abilities:** Standard platformer movement. Can be targeted by the Mallet to gain modifiers (e.g., become `Bouncy`, `Floaty`).
    *   **Interaction:** Can push some objects (depending on weight/modifiers). Interacts physically with the environment based on standard physics and active modifiers.
*   **2.3. The Modifier Mallet**
    *   **Function:** Player's primary tool. Applies the currently selected modifier to valid targets upon impact. Removes modifier from an already modified target upon impact.
    *   **Feedback:** Clear visual and audio cues on swing, hit, successful application, and removal.
*   **2.4. Modifiers**
    *   **Initial Set (MVP):**
        *   `Bouncy`: Increases restitution dramatically. Objects (or player) bounce high on collision.
        *   `Heavy`: Increases mass significantly. Harder to push, effective on pressure plates, sinks in liquids (if added).
        *   `Floaty`: Reduces gravity effect or applies slight upward force. Slows descent or allows gentle rising.
    *   **Management:** Player can select which modifier the mallet will apply next.
    *   **Limit:** A strict limit on the number of concurrently active modifiers in the level (e.g., 3). UI must display current usage vs. limit.
*   **2.5. Modifiable Objects & Environment**
    *   **Types:** Player, Crates/Boxes, specific Floor/Wall tiles (visually distinct), Switches/Buttons, potentially simple Enemies later.
    *   **Interaction:** Objects respond physically according to standard physics *plus* the rules of their active modifier. Switches might require specific conditions (e.g., sustained weight from a `Heavy` object).
*   **2.6. Level Structure:**
    *   Self-contained 2D levels with a start point and an exit point.
    *   Obstacles include gaps, high ledges, locked doors (requiring switches/keys), simple hazards (spikes - avoidable by modifying self or path).
    *   Puzzle design focuses on creative combination and sequencing of modifier applications.

---

## 3. Art & Audio Style ("Magic Style")

*   **3.1. Visual Style:** 2D, Cartoony, perhaps slightly chunky or hand-drawn. Clear visual language is crucial.
    *   **Feedback:** Modifiable objects should be easily identifiable (e.g., outline, texture difference). Active modifiers should have clear visual indicators (e.g., persistent glow, particle effect, icon above object).
    *   **Character:** Simple, expressive "Bonk" character with clear animations for moving, jumping, swinging the mallet, and reacting to physics (getting bounced, floating).
    *   **Environment:** Clean, readable layouts. Backgrounds support the lighthearted, perhaps slightly chaotic workshop/magic lab theme.
*   **3.2. Audio Style:** Lighthearted, satisfying, and informative.
    *   **SFX:** Distinct sounds for Mallet swing, hits (different for modifiable vs. non-modifiable), modifier application (unique sound per modifier type - e.g., "Boing!" for `Bouncy`, "Thud!" for `Heavy`, "Whoosh!" for `Floaty`), modifier removal, jumping, landing, player reactions, puzzle element activations (switch clicks, door opens).
    *   **Music (Optional for MVP):** Upbeat, quirky background track that doesn't interfere with puzzle-solving focus.

---

## 4. Technical Requirements

*   **4.1. Platform:** PC (Windows, potentially Mac/Linux later).
*   **4.2. Game Engine:** Suitable 2D engine with robust physics support (e.g., Unity, Godot).
*   **4.3. Programming:**
    *   **Language:** C# (Unity) or GDScript (Godot) recommended.
    *   **OOP Principles:** Code should adhere to Object-Oriented Programming principles (Encapsulation, Inheritance, Polymorphism) where appropriate for clarity and maintainability.
*   **4.4. Architecture:**
    *   **MVC (Model-View-Controller):** Explore applying MVC pattern to separate concerns:
        *   **Model:** Game state, physics simulation, object properties, modifier logic, level data.
        *   **View:** Rendering sprites, handling animations, displaying UI elements, playing sounds.
        *   **Controller:** Handling player input, translating input into actions/commands for the Model.
    *   **ECS (Entity-Component-System) Principles:** While a full ECS framework might be overkill for the initial scope, incorporate ECS *principles*:
        *   **Entities:** Represent game objects (Player, Box, Switch).
        *   **Components:** Represent data/properties (`Position`, `Sprite`, `PhysicsBody`, `Modifiable`, `IsBouncy`, `IsHeavy`).
        *   **Systems:** Represent logic acting on entities with specific components (`MovementSystem`, `PhysicsSystem`, `ModifierApplicationSystem`, `RenderSystem`). Focus on data-oriented design and separating logic into systems. *Aim for a hybrid approach initially if a pure ECS is too complex for the practice goal.*
*   **4.5. Physics:** Utilize the engine's built-in 2D physics. Requires ability to dynamically change object properties like mass, friction, restitution (bounciness), and gravity scale at runtime based on applied modifiers.
*   **4.6. Interesting Algorithms (To Explore/Implement):**
    *   **State Management:** Implementing the modifier application/removal system, potentially using a State pattern or similar for managing object states based on modifiers.
    *   **Collision Detection Optimization:** If levels become complex, explore spatial partitioning (e.g., Quadtrees) to optimize physics queries or object lookups (e.g., "what did the mallet hit?").
    *   **Command Pattern:** Could be useful for handling player actions (applying/removing modifiers) and potentially implementing an Undo system (valuable in puzzle games, though maybe post-MVP).
    *   **Simple Rule Engine:** The core logic mapping modifiers to physics changes can be considered a basic rule engine.

---

## 5. Scope & Minimum Viable Product (MVP)

*   **5.1. MVP Features:**
    *   Player character with basic movement, jump, mallet swing.
    *   Mallet can apply/remove the initial 3 modifiers (`Bouncy`, `Heavy`, `Floaty`).
    *   At least one type of modifiable object (e.g., Crate).
    *   Functional active modifier limit system & UI indicator.
    *   Basic UI for modifier selection.
    *   Basic physics integration reacting correctly to the MVP modifiers.
    *   Start point and Exit point functionality.
    *   3-5 simple introductory levels demonstrating each MVP modifier and basic combinations.
    *   Placeholder art and sound sufficient for testing gameplay.
    *   Core structure implementing OOP and exploring MVC/ECS principles.
*   **5.2. Post-MVP / Future Considerations:** More modifiers, complex modifiable objects/environment pieces, simple enemies, hazards, polished art/audio, storyline elements, level editor, more complex algorithms (pathfinding for enemies, procedural elements), Undo feature.

---