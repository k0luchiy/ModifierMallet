# Modifier Mallet - Game Documentation

## Overview
Modifier Mallet is a 2D puzzle platformer where players use a magical mallet to apply different modifiers to objects and solve physics-based puzzles. The game features multiple modifiers that can be applied to objects to change their properties, creating interesting gameplay mechanics and puzzle solutions.

## Game Mechanics

### Core Mechanics
1. **Movement**
   - Left/Right arrow keys for movement (with acceleration/deceleration)
   - Space to jump
   - Mouse for aiming and using the mallet
   - Q/E to cycle through modifiers

2. **The Mallet**
   - Left-click to apply/remove modifiers
   - Has a visible range indicator (grey circle)
   - Has a cooldown period (0.5 seconds) between uses
   - Can apply modifiers to objects within range

### Modifiers
1. **Bouncy**
   - Makes objects bounce with high restitution
   - Visual Effect: Cyan outline with upward arrows
   - Great for reaching high places

2. **Heavy**
   - Increases mass significantly
   - Makes objects harder to push
   - Visual Effect: Brown outline
   - Useful for holding down pressure plates or pushing other objects

3. **Floaty**
   - Reduces gravity effect
   - Makes objects float or fall slowly
   - Visual Effect: Pink outline with upward particles
   - Helpful for controlled vertical movement

4. **Sticky**
   - Allows objects to be grabbed and dragged
   - Visual Effect: Purple outline
   - Useful for precise object placement

5. **Reversed**
   - Inverts horizontal movement
   - Visual Effect: Orange outline
   - Can create interesting movement puzzles

6. **Ghostly**
   - Allows objects to pass through walls
   - Visual Effect: Semi-transparent grey overlay
   - Useful for bypassing obstacles

## Game Objects

### Player Character
- Has sprite-based animations for different states (idle, walk, jump)
- Can carry the mallet and apply modifiers
- Features smooth movement with acceleration/deceleration
- Can be affected by modifiers themselves

### Interactive Objects
1. **Static Objects**
   - Platforms
   - Walls
   - Ground
   - Cannot be moved but can be modified

2. **Dynamic Objects**
   - Boxes (can be pushed, pulled when sticky, made bouncy, etc.)
   - Various puzzle elements
   - Fully physics-enabled
   - Can interact with other objects

3. **Goal Object**
   - Represents level completion point
   - Golden colored
   - Triggers level transition when reached

## Level System

### Level Structure
Levels are defined in JSON format, making them easy to create and modify. Each level file contains:
- Level name and description
- Player starting position
- Goal position
- Static objects (platforms, walls)
- Dynamic objects (movable boxes)
- Hint messages
- Required modifiers for solution

### Level Progression
- Levels are loaded sequentially
- Each level introduces new mechanics or combinations
- Players can reset levels with 'R' key
- Victory screen shown upon level completion

## Technical Implementation

### Project Structure
```
src/
├── main.py                 # Main game entry point
├── assets/
│   ├── images/            # Sprite sheets and graphics
│   └── sounds/            # Sound effects and music
├── controllers/
│   ├── __init__.py
│   └── game_controller.py # Main game loop and logic
├── levels/
│   ├── level_1.json      # Level definition files
│   └── level_2.json
├── models/
│   ├── __init__.py
│   ├── game_object.py    # Base class for game objects
│   ├── level_manager.py  # Level loading and management
│   ├── modifier.py       # Modifier effects implementation
│   ├── player.py        # Player character implementation
│   └── sprite_manager.py # Animation and sprite handling
├── utils/
│   ├── __init__.py
│   ├── constants.py      # Game constants and settings
│   └── physics.py        # Physics handling
└── views/
    ├── __init__.py
    └── game_view.py      # Rendering and display
```

### Key Components

1. **GameObject Class**
   - Base class for all game objects
   - Handles physics, collision, and modifier effects
   - Supports visual feedback for active modifiers

2. **Player Class**
   - Handles player input and movement
   - Manages mallet usage and modifier application
   - Controls animation states

3. **SpriteManager Class**
   - Handles sprite sheet loading and animation
   - Manages different animation states
   - Controls animation timing and frame selection

4. **LevelManager Class**
   - Loads and parses level JSON files
   - Manages level progression
   - Creates game objects from level data

5. **Physics System**
   - Handles collision detection and resolution
   - Manages object interactions
   - Implements modifier physics effects

## Controls Summary
- **Left/Right Arrow**: Move
- **Space**: Jump
- **Q/E**: Cycle through modifiers
- **Left Click**: Use mallet/drag sticky objects
- **R**: Reset level
- **ESC**: Pause game

## Visual Feedback
- Each modifier has a unique color and visual effect
- Active modifiers show outlines and particle effects
- Current modifier and cooldown displayed on screen
- Level information and hints shown during gameplay
- Range indicator shows mallet's effective area

## Future Improvements
1. Add sound effects for different modifiers
2. Implement more complex puzzle mechanics
3. Add a level editor
4. Enhance visual effects and animations
5. Add more modifier types
6. Implement a scoring system