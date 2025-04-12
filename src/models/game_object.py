import pygame
from typing import Tuple, Optional
from src.utils.constants import *

class GameObject:
    def __init__(self, x: float, y: float, width: int, height: int, color: Tuple[int, int, int] = WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.original_color = color
        self.velocity_x = 0
        self.velocity_y = 0
        self.mass = 1
        self.gravity = GRAVITY
        self.on_ground = False
        self.active_modifiers = []
        self.prev_x = x
        self.prev_y = y
        self.is_pushable = True  # Objects can be pushed by default
        self.is_draggable = False  # Can be grabbed and dragged when sticky
        self.being_dragged = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    def update(self):
        # Store previous position
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y

        if self.being_dragged:
            # Follow mouse position when being dragged
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.rect.x = mouse_x - self.drag_offset_x
            self.rect.y = mouse_y - self.drag_offset_y
            self.velocity_x = 0
            self.velocity_y = 0
        else:
            # Apply gravity if not being dragged
            if not self.on_ground:
                self.velocity_y += self.gravity

            # Update position
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y

        # Limit vertical speed
        if self.velocity_y > PLAYER_MAX_SPEED:
            self.velocity_y = PLAYER_MAX_SPEED

    def revert_x(self):
        self.rect.x = self.prev_x
        self.velocity_x = 0

    def revert_y(self):
        self.rect.y = self.prev_y
        self.velocity_y = 0

    def draw(self, screen: pygame.Surface):
        # Draw the base object
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw modifier effects
        for modifier in self.active_modifiers:
            effect_color = {
                "bouncy": (0, 255, 255),  # Cyan
                "heavy": (139, 69, 19),   # Brown
                "floaty": (255, 192, 203), # Pink
                "sticky": (128, 0, 128),   # Purple
                "reversed": (255, 165, 0), # Orange
                "ghostly": (200, 200, 200) # Light gray
            }.get(modifier.effect_type, WHITE)
            
            # Draw outline effect
            pygame.draw.rect(screen, effect_color, self.rect, 2)
            
            # Draw additional visual effects based on modifier
            if modifier.effect_type == "bouncy":
                # Draw bounce arrows
                arrow_height = 10
                pygame.draw.polygon(screen, effect_color, [
                    (self.rect.centerx, self.rect.top - arrow_height),
                    (self.rect.centerx - 5, self.rect.top),
                    (self.rect.centerx + 5, self.rect.top)
                ])
            elif modifier.effect_type == "floaty":
                # Draw upward particles
                for i in range(3):
                    y_offset = (pygame.time.get_ticks() // 100 + i * 5) % 20
                    pygame.draw.circle(screen, effect_color,
                                    (self.rect.centerx, self.rect.bottom + y_offset - 20),
                                    2)
            elif modifier.effect_type == "ghostly":
                # Draw ghostly transparency effect
                s = pygame.Surface((self.rect.width, self.rect.height))
                s.set_alpha(128)
                s.fill(effect_color)
                screen.blit(s, self.rect)

    def add_modifier(self, modifier) -> bool:
        if len(self.active_modifiers) < MAX_ACTIVE_MODIFIERS:
            # Remove any existing modifier of the same type
            for existing_mod in self.active_modifiers:
                if existing_mod.effect_type == modifier.effect_type:
                    self.remove_modifier(existing_mod)
                    
            self.active_modifiers.append(modifier)
            modifier.apply(self)
            
            # Update object properties based on modifier
            if modifier.effect_type == "sticky":
                self.is_draggable = True
            elif modifier.effect_type == "heavy":
                self.is_pushable = False
            
            return True
        return False

    def remove_modifier(self, modifier):
        if modifier in self.active_modifiers:
            self.active_modifiers.remove(modifier)
            modifier.remove(self)
            
            # Reset object properties
            if modifier.effect_type == "sticky":
                self.is_draggable = False
                self.being_dragged = False
            elif modifier.effect_type == "heavy":
                self.is_pushable = True

    def start_drag(self, mouse_x: int, mouse_y: int):
        """Start dragging the object from current mouse position."""
        if self.is_draggable:
            self.being_dragged = True
            self.drag_offset_x = mouse_x - self.rect.x
            self.drag_offset_y = mouse_y - self.rect.y

    def stop_drag(self):
        """Stop dragging the object."""
        self.being_dragged = False

    def collides_with(self, other: 'GameObject') -> bool:
        return self.rect.colliderect(other.rect)

    def get_position(self) -> Tuple[float, float]:
        return self.rect.x, self.rect.y