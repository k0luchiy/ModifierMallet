import pygame
from typing import Tuple, Optional
from src.utils.constants import *
from src.utils.settings_manager import SettingsManager

class GameObject:
    def __init__(self, x: float, y: float, width: int, height: int, color: Tuple[int, int, int] = WHITE, mass: float = None):
        self.settings = SettingsManager()
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.original_color = color
        self.velocity_x = 0
        self.velocity_y = 0
        self.mass = mass if mass is not None else self.settings.get("physics", "object", "default_mass", default=1.0)
        self.gravity = self.settings.get("physics", "gravity", default=0.8)
        self.friction = self.settings.get("physics", "object", "default_friction", default=0.5)
        self.elasticity = self.settings.get("physics", "object", "default_elasticity", default=0.2)
        self.on_ground = False
        self.active_modifiers = []
        self.prev_x = x
        self.prev_y = y
        self.is_pushable = True
        self.is_draggable = False
        self.being_dragged = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.is_ghost_passable = False  # New property to mark objects that can be passed through when ghostly
        self.collision_enabled = True

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
            # Apply gravity if not on ground
            if not self.on_ground:
                self.velocity_y += self.gravity

            # Apply friction when on ground
            if self.on_ground and abs(self.velocity_x) > 0:
                friction_force = self.friction * (1 if self.velocity_x > 0 else -1)
                self.velocity_x = max(0, abs(self.velocity_x) - friction_force) * (1 if self.velocity_x > 0 else -1)

            # Update position one axis at a time to prevent tunneling
            self.rect.x += self.velocity_x
            
            # Update y position with smaller steps if moving fast
            remaining_y = self.velocity_y
            step_size = 4  # Maximum pixels per step
            
            while abs(remaining_y) > 0:
                step = max(-step_size, min(step_size, remaining_y))
                self.rect.y += step
                remaining_y -= step

                # Break early if we hit something
                if self.on_ground and self.velocity_y > 0:
                    break

        # Limit vertical speed
        max_speed = self.settings.get("physics", "player", "max_speed", default=20)
        if self.velocity_y > max_speed:
            self.velocity_y = max_speed

    def revert_x(self):
        """Revert x position after collision."""
        self.rect.x = self.prev_x
        if abs(self.velocity_x) > 0:
            self.velocity_x *= -self.elasticity

    def revert_y(self):
        """Revert y position after collision."""
        self.rect.y = self.prev_y
        if abs(self.velocity_y) > 0:
            self.velocity_y *= -self.elasticity

    def draw(self, screen: pygame.Surface):
        # Draw the base object
        if hasattr(self, 'settings') and self.settings.get("debug", "draw_colliders", default=False):
            # Draw collision box
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
        
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw modifier effects
        for modifier in self.active_modifiers:
            effect_color = self.settings.get("colors", "modifiers", modifier.effect_type, 
                                          default=[255, 255, 255])
            effect_color = tuple(effect_color)  # Convert list to tuple for pygame
            
            # Draw outline effect
            outline_thickness = self.settings.get("ui", "modifier_outline_thickness", default=2)
            pygame.draw.rect(screen, effect_color, self.rect, outline_thickness)
            
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
                alpha = self.settings.get("physics", "modifiers", "ghostly_alpha", default=128)
                s = pygame.Surface((self.rect.width, self.rect.height))
                s.set_alpha(alpha)
                s.fill(effect_color)
                screen.blit(s, self.rect)

    def add_modifier(self, modifier) -> bool:
        max_modifiers = self.settings.get("game", "max_active_modifiers", default=3)
        if len(self.active_modifiers) < max_modifiers:
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
        # Skip collision if either object is ghostly and the other is ghost-passable
        if hasattr(self, 'collision_enabled') and not self.collision_enabled and other.is_ghost_passable:
            return False
        if hasattr(other, 'collision_enabled') and not other.collision_enabled and self.is_ghost_passable:
            return False
        return self.rect.colliderect(other.rect)

    def get_position(self) -> Tuple[float, float]:
        return self.rect.x, self.rect.y