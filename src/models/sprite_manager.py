import pygame
import os

class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.current_frame = 0
        self.animation_speed = 0.1  # Faster animation speed
        self.animation_timer = 0
        self.frame_count = 0
        self.state_frame_counts = {
            "idle": 4,    # Number of frames for idle animation
            "walk": 6,    # Number of frames for walk animation
            "jump": 2     # Number of frames for jump animation
        }
        
    def load_spritesheet(self, filepath: str, sprite_width: int, sprite_height: int):
        """Load a spritesheet and split it into individual frames."""
        if not os.path.exists(filepath):
            print(f"Warning: Sprite file {filepath} not found!")
            return False
            
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
        
    def get_sprite(self, row: int, col: int) -> pygame.Surface:
        """Get a specific sprite from the loaded sprites."""
        key = f"{row}_{col}"
        return self.sprites.get(key, None)
        
    def update_animation(self, dt: float, state: str):
        """Update animation based on current state."""
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            frame_count = self.state_frame_counts.get(state, 4)
            
            if state == "idle":
                # Slower idle animation
                self.animation_timer = -0.2  # Add delay between idle frames
                
            self.current_frame = (self.current_frame + 1) % frame_count
            
    def get_current_animation_frame(self, state: str) -> pygame.Surface:
        """Get the current frame based on animation state."""
        row = {
            "idle": 0,
            "walk": 1,
            "jump": 2
        }.get(state, 0)
        
        return self.get_sprite(row, self.current_frame)