from typing import List
import pygame
from src.models.game_object import GameObject
from src.utils.settings_manager import SettingsManager

class PhysicsSystem:
    def __init__(self):
        self.settings = SettingsManager()
        self.friction_coefficient = 0.15  # Add friction coefficient
        self.bounce_multiplier = 1.5  # Bounce modifier multiplier

    def handle_collisions(self, game_object: GameObject, static_objects: List[GameObject]):
        if not hasattr(game_object, 'collision_enabled') or game_object.collision_enabled:
            was_on_ground = game_object.on_ground
            game_object.on_ground = False
            
            # --- Vertical Collision Pass ---
            game_object.rect.y += game_object.velocity_y
            
            for static_obj in static_objects:
                if game_object.collides_with(static_obj):
                    # Moving down / Landing
                    if game_object.velocity_y > 0:
                        game_object.rect.bottom = static_obj.rect.top
                        game_object.on_ground = True
                        
                        # Apply bounce if the object is bouncy
                        if hasattr(static_obj, 'modifiers') and 'Bouncy' in static_obj.modifiers:
                            game_object.velocity_y = -abs(game_object.velocity_y) * self.bounce_multiplier
                        else:
                            game_object.velocity_y = 0
                            
                        # Apply friction when landing on objects
                        if abs(game_object.velocity_x) > 0:
                            friction_force = self.friction_coefficient * (1 if game_object.velocity_x > 0 else -1)
                            game_object.velocity_x = max(0, abs(game_object.velocity_x) - friction_force) * (1 if game_object.velocity_x > 0 else -1)
                    
                    # Moving up / Hitting ceiling
                    elif game_object.velocity_y < 0:
                        game_object.rect.top = static_obj.rect.bottom
                        game_object.velocity_y = 0

            # --- Horizontal Collision Pass ---
            game_object.rect.x += game_object.velocity_x
            
            for static_obj in static_objects:
                if game_object.collides_with(static_obj):
                    # Moving right
                    if game_object.velocity_x > 0:
                        game_object.rect.right = static_obj.rect.left
                    # Moving left
                    elif game_object.velocity_x < 0:
                        game_object.rect.left = static_obj.rect.right
                    
                    # Stop horizontal movement on collision
                    game_object.velocity_x = 0

            # Additional stability check for standing on moving boxes
            if game_object.on_ground and not was_on_ground:
                for static_obj in static_objects:
                    if (game_object.rect.bottom == static_obj.rect.top and 
                        game_object.rect.right > static_obj.rect.left and 
                        game_object.rect.left < static_obj.rect.right):
                        # Ensure proper alignment when landing
                        game_object.rect.bottom = static_obj.rect.top

    def handle_object_interaction(self, obj1: GameObject, obj2: GameObject):
        # Check if either object has modifiers that affect interaction
        obj1_modifiers = getattr(obj1, 'modifiers', set())
        obj2_modifiers = getattr(obj2, 'modifiers', set())
        
        # Handle special modifier interactions
        if 'Bouncy' in obj1_modifiers or 'Bouncy' in obj2_modifiers:
            # Exchange velocities with bounce effect
            temp_vx = obj1.velocity_x
            temp_vy = obj1.velocity_y
            obj1.velocity_x = -obj2.velocity_x * self.bounce_multiplier
            obj1.velocity_y = -obj2.velocity_y * self.bounce_multiplier
            obj2.velocity_x = -temp_vx * self.bounce_multiplier
            obj2.velocity_y = -temp_vy * self.bounce_multiplier
        else:
            # Standard elastic collision
            temp_vx = obj1.velocity_x
            temp_vy = obj1.velocity_y
            obj1.velocity_x = obj2.velocity_x
            obj1.velocity_y = obj2.velocity_y
            obj2.velocity_x = temp_vx
            obj2.velocity_y = temp_vy

    def handle_player_object_collision(self, player: GameObject, obj: GameObject):
        """Handle collision specifically between player and a dynamic object."""
        if not player.collides_with(obj):
            return
            
        # Skip if player or object is ghostly and interaction is allowed
        if ((not getattr(player, 'collision_enabled', True) and getattr(obj, 'is_ghost_passable', False)) or 
            (not getattr(obj, 'collision_enabled', True) and getattr(player, 'is_ghost_passable', False))):
            return

        # Calculate overlap
        dx = player.rect.centerx - obj.rect.centerx
        dy = player.rect.centery - obj.rect.centery
        overlap_x = (player.rect.width / 2 + obj.rect.width / 2) - abs(dx)
        overlap_y = (player.rect.height / 2 + obj.rect.height / 2) - abs(dy)

        # Apply friction when player is on top of an object
        if player.on_ground and dy < 0:
            friction = self.settings.get("physics", "object", "friction", default=0.8)
            # Slow down player's horizontal movement
            player.velocity_x *= friction
            # Transfer some of player's horizontal movement to box
            if obj.is_pushable:
                transfer_factor = 0.3
                obj.velocity_x += player.velocity_x * transfer_factor

        # Resolve collision based on smallest overlap
        if overlap_x < overlap_y:
            # Horizontal collision
            push_force = 0.3  # Reduced push force for better control
            if dx > 0:  # Player is to the right of the object
                player.rect.left = obj.rect.right
                if obj.is_pushable:
                    # Scale push force by mass ratio
                    force = push_force * (player.mass / obj.mass) * abs(player.velocity_x)
                    obj.velocity_x = min(obj.velocity_x - force, -0.5)  # Ensure minimum movement
                player.velocity_x = max(0, player.velocity_x)
            else:  # Player is to the left
                player.rect.right = obj.rect.left
                if obj.is_pushable:
                    force = push_force * (player.mass / obj.mass) * abs(player.velocity_x)
                    obj.velocity_x = max(obj.velocity_x + force, 0.5)  # Ensure minimum movement
                player.velocity_x = min(0, player.velocity_x)
        else:
            # Vertical collision
            if dy > 0:  # Player is below the object
                player.rect.top = obj.rect.bottom
                player.velocity_y = 0
            else:  # Player is above the object (landing on it)
                player.rect.bottom = obj.rect.top
                player.on_ground = True
                
                # Enhanced bouncy behavior
                is_bouncy = any(mod.effect_type == 'bouncy' for mod in obj.active_modifiers)
                if is_bouncy:
                    bounce_force = self.settings.get("physics", "modifiers", "bouncy_elasticity", default=0.9)
                    # Scale bounce by falling speed with a minimum bounce
                    min_bounce = 8
                    impact_velocity = abs(player.velocity_y)
                    bounce_velocity = max(impact_velocity * bounce_force, min_bounce)
                    player.velocity_y = -bounce_velocity
                    
                    # Apply proportional downward force to the box
                    if obj.is_pushable:
                        obj.velocity_y = impact_velocity * 0.2 * (player.mass / obj.mass)
                else:
                    # Normal landing
                    player.velocity_y = 0
                    if obj.is_pushable:
                        # Apply gradual stabilizing force
                        obj.velocity_y = min(obj.velocity_y + 0.2 * (player.mass / obj.mass), 1.0)
                        # Dampen box horizontal movement when landed on
                        obj.velocity_x *= 0.9

    def keep_in_bounds(self, game_object: GameObject):
        """Keep object within screen bounds."""
        screen_width = self.settings.get_setting('screen_width', 800)
        screen_height = self.settings.get_setting('screen_height', 600)
        
        # Allow ghostly objects to pass through bounds
        if hasattr(game_object, 'collision_enabled') and not game_object.collision_enabled:
            # Only reset position if completely outside bounds
            if (game_object.rect.right < 0 or 
                game_object.rect.left > screen_width or 
                game_object.rect.bottom < 0 or 
                game_object.rect.top > screen_height):
                game_object.rect.center = (screen_width/2, screen_height/2)
            return

        # Keep object within screen bounds
        if game_object.rect.left < 0:
            game_object.rect.left = 0
            game_object.velocity_x = 0
        elif game_object.rect.right > screen_width:
            game_object.rect.right = screen_width
            game_object.velocity_x = 0
        
        if game_object.rect.top < 0:
            game_object.rect.top = 0
            game_object.velocity_y = 0
        elif game_object.rect.bottom > screen_height:
            game_object.rect.bottom = screen_height
            game_object.velocity_y = 0
            game_object.on_ground = True

# Create a global physics system instance
physics_system = PhysicsSystem()

# Export the methods as module-level functions that use the global instance
def handle_collisions(game_object: GameObject, static_objects: List[GameObject]):
    physics_system.handle_collisions(game_object, static_objects)

def handle_object_interaction(obj1: GameObject, obj2: GameObject):
    physics_system.handle_object_interaction(obj1, obj2)

def handle_player_object_collision(player: GameObject, obj: GameObject):
    # Special handling for player-specific interactions
    if hasattr(obj, 'modifiers'):
        if 'Bouncy' in obj.modifiers:
            # Enhanced bounce for player
            player.velocity_y = -abs(player.velocity_y) * physics_system.bounce_multiplier * 1.2
        # Add other modifier-specific interactions here

def keep_in_bounds(game_object: GameObject):
    physics_system.keep_in_bounds(game_object)