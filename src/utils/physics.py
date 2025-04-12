from typing import List
import pygame
from src.models.game_object import GameObject
from src.utils.settings_manager import SettingsManager

class PhysicsSystem:
    def __init__(self):
        self.settings = SettingsManager()

    def handle_collisions(self, game_object: GameObject, static_objects: List[GameObject]):
        if not hasattr(game_object, 'collision_enabled') or game_object.collision_enabled:
            # Reset ground state at start of collision check
            was_on_ground = game_object.on_ground
            game_object.on_ground = False
            
            # Handle vertical collisions first (important for ground detection)
            for static_obj in static_objects:
                if game_object.collides_with(static_obj):
                    # Calculate overlap
                    if game_object.velocity_y >= 0:  # Moving down
                        overlap = game_object.rect.bottom - static_obj.rect.top
                        if overlap > 0:
                            game_object.rect.bottom = static_obj.rect.top
                            game_object.velocity_y = 0
                            game_object.on_ground = True
                    else:  # Moving up
                        overlap = static_obj.rect.bottom - game_object.rect.top
                        if overlap > 0:
                            game_object.rect.top = static_obj.rect.bottom
                            game_object.velocity_y = 0

            # Then handle horizontal collisions
            for static_obj in static_objects:
                if game_object.collides_with(static_obj):
                    # Calculate overlap for precise collision response
                    if game_object.velocity_x > 0:  # Moving right
                        overlap = game_object.rect.right - static_obj.rect.left
                        if overlap > 0:
                            game_object.rect.right = static_obj.rect.left
                            game_object.velocity_x *= -game_object.elasticity
                    elif game_object.velocity_x < 0:  # Moving left
                        overlap = static_obj.rect.right - game_object.rect.left
                        if overlap > 0:
                            game_object.rect.left = static_obj.rect.right
                            game_object.velocity_x *= -game_object.elasticity
                    
                    # Stop horizontal movement if very slow
                    if abs(game_object.velocity_x) < 0.1:
                        game_object.velocity_x = 0

            # Ground detection ray for walking off edges
            if was_on_ground and game_object.velocity_y <= 0:
                ground_check = pygame.Rect(
                    game_object.rect.x,
                    game_object.rect.bottom,
                    game_object.rect.width,
                    2
                )
                for static_obj in static_objects:
                    if ground_check.colliderect(static_obj.rect):
                        game_object.on_ground = True
                        if game_object.velocity_y > 0:  # Snap to ground if falling
                            game_object.rect.bottom = static_obj.rect.top
                            game_object.velocity_y = 0
                        break

    def handle_object_interaction(self, obj1: GameObject, obj2: GameObject):
        """Handle interaction between two dynamic objects."""
        if not obj1.collides_with(obj2):
            return

        # Skip collision if either object is ghostly
        if ((hasattr(obj1, 'collision_enabled') and not obj1.collision_enabled) or 
            (hasattr(obj2, 'collision_enabled') and not obj2.collision_enabled)):
            return

        # Handle momentum transfer based on mass
        if obj1.is_pushable and obj2.is_pushable:
            total_mass = obj1.mass + obj2.mass
            
            # Calculate new velocities based on conservation of momentum and elasticity
            avg_elasticity = (obj1.elasticity + obj2.elasticity) / 2
            
            v1_x = ((obj1.mass - obj2.mass) * obj1.velocity_x + 
                    2 * obj2.mass * obj2.velocity_x) / total_mass
            v2_x = ((obj2.mass - obj1.mass) * obj2.velocity_x + 
                    2 * obj1.mass * obj1.velocity_x) / total_mass
            
            # Apply elasticity
            v1_x *= avg_elasticity
            v2_x *= avg_elasticity
            
            # Apply velocities
            obj1.velocity_x = v1_x
            obj2.velocity_x = v2_x
            
            # Separate objects to prevent sticking
            if obj1.rect.centerx < obj2.rect.centerx:
                obj1.rect.right = obj2.rect.left
            else:
                obj1.rect.left = obj2.rect.right
        
        # Handle one-sided pushing (when one object is not pushable)
        elif obj1.is_pushable and not obj2.is_pushable:
            obj1.velocity_x *= -obj1.elasticity
            if obj1.rect.centerx < obj2.rect.centerx:
                obj1.rect.right = obj2.rect.left
            else:
                obj1.rect.left = obj2.rect.right
        
        elif not obj1.is_pushable and obj2.is_pushable:
            obj2.velocity_x *= -obj2.elasticity
            if obj2.rect.centerx < obj1.rect.centerx:
                obj2.rect.right = obj1.rect.left
            else:
                obj2.rect.left = obj1.rect.right

    def keep_in_bounds(self, game_object: GameObject):
        """Keep object within screen bounds."""
        window_width = self.settings.get("window", "width", default=800)
        window_height = self.settings.get("window", "height", default=600)
        
        # Allow ghostly objects to pass through bounds
        if hasattr(game_object, 'collision_enabled') and not game_object.collision_enabled:
            # Only reset position if completely outside bounds
            if (game_object.rect.right < 0 or 
                game_object.rect.left > window_width or 
                game_object.rect.bottom < 0 or 
                game_object.rect.top > window_height):
                game_object.rect.center = (window_width/2, window_height/2)
            return

        bound_elasticity = self.settings.get("physics", "object", "default_elasticity", default=0.2)
        
        # Keep object within screen bounds with bouncing
        if game_object.rect.left < 0:
            game_object.rect.left = 0
            game_object.velocity_x = abs(game_object.velocity_x) * bound_elasticity
        elif game_object.rect.right > window_width:
            game_object.rect.right = window_width
            game_object.velocity_x = -abs(game_object.velocity_x) * bound_elasticity
        
        if game_object.rect.top < 0:
            game_object.rect.top = 0
            game_object.velocity_y = abs(game_object.velocity_y) * bound_elasticity
        elif game_object.rect.bottom > window_height:
            game_object.rect.bottom = window_height
            game_object.velocity_y = -abs(game_object.velocity_y) * bound_elasticity
            game_object.on_ground = True

# Create a global physics system instance
physics_system = PhysicsSystem()

# Export the methods as module-level functions that use the global instance
def handle_collisions(game_object: GameObject, static_objects: List[GameObject]):
    physics_system.handle_collisions(game_object, static_objects)

def handle_object_interaction(obj1: GameObject, obj2: GameObject):
    physics_system.handle_object_interaction(obj1, obj2)

def keep_in_bounds(game_object: GameObject):
    physics_system.keep_in_bounds(game_object)