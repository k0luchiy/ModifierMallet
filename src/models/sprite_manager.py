import pygame
import os
from typing import Dict, Optional

class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.current_frame = 0
        self.animation_speed = 0.1  # Base animation speed
        self.animation_timer = 0
        
        # Define frame counts and speeds for different states
        self.state_frame_counts = {
            "idle": 4,    # Frames in idle animation
            "walk": 6,    # Frames in walk animation
            "jump": 2     # Frames in jump animation
        }
        
        self.state_speeds = {
            "idle": 0.2,  # Slower idle animation
            "walk": 0.1,  # Normal walk speed
            "jump": 0.15  # Medium jump speed
        }

    def load_spritesheet(self, filepath: str, sprite_width: int, sprite_height: int) -> bool:
        """Load a spritesheet and split it into individual frames."""
        if not os.path.exists(filepath):
            print(f"Warning: Sprite file {filepath} not found!")
            return False
            
        try:
            spritesheet = pygame.image.load(filepath).convert_alpha()
            sheet_width = spritesheet.get_width()
            sheet_height = spritesheet.get_height()
            
            # Calculate number of sprites in the sheet
            cols = sheet_width // sprite_width
            rows = sheet_height // sprite_height
            
            # Split the spritesheet into individual sprites
            for row in range(rows):
                for col in range(cols):
                    x = col * sprite_width
                    y = row * sprite_height
                    sprite = spritesheet.subsurface((x, y, sprite_width, sprite_height))
                    self.sprites[f"{row}_{col}"] = sprite
                    
            return True
        except Exception as e:
            print(f"Error loading spritesheet: {e}")
            return False
        
    def get_sprite(self, row: int, col: int) -> Optional[pygame.Surface]:
        """Get a specific sprite from the loaded sprites."""
        key = f"{row}_{col}"
        return self.sprites.get(key)
        
    def update_animation(self, dt: float, state: str):
        """Update animation based on current state."""
        # Get state-specific animation speed
        speed = self.state_speeds.get(state, self.animation_speed)
        
        self.animation_timer += dt
        if self.animation_timer >= speed:
            self.animation_timer = 0
            frame_count = self.state_frame_counts.get(state, 4)
            
            # Update frame counter
            self.current_frame = (self.current_frame + 1) % frame_count
            
    def get_current_animation_frame(self, state: str) -> Optional[pygame.Surface]:
        """Get the current frame based on animation state."""
        row = {
            "idle": 0,
            "walk": 1,
            "jump": 2
        }.get(state, 0)
        
        return self.get_sprite(row, self.current_frame % self.state_frame_counts.get(state, 4))