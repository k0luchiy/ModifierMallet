from typing import List
from src.models.game_object import GameObject
from src.utils.constants import *

def handle_collisions(game_object: GameObject, static_objects: List[GameObject]):
    game_object.on_ground = False
    
    # Handle horizontal collisions first
    for static_obj in static_objects:
        if not hasattr(static_obj, 'collision_enabled') or static_obj.collision_enabled:
            if game_object.collides_with(static_obj):
                if game_object.velocity_x > 0:  # Moving right
                    game_object.rect.right = static_obj.rect.left
                    game_object.velocity_x = 0
                elif game_object.velocity_x < 0:  # Moving left
                    game_object.rect.left = static_obj.rect.right
                    game_object.velocity_x = 0
                game_object.revert_x()

    # Then handle vertical collisions
    for static_obj in static_objects:
        if not hasattr(static_obj, 'collision_enabled') or static_obj.collision_enabled:
            if game_object.collides_with(static_obj):
                if game_object.velocity_y > 0:  # Falling
                    game_object.rect.bottom = static_obj.rect.top
                    game_object.velocity_y = 0
                    game_object.on_ground = True
                elif game_object.velocity_y < 0:  # Jumping
                    game_object.rect.top = static_obj.rect.bottom
                    game_object.velocity_y = 0
                game_object.revert_y()

def handle_object_interaction(obj1: GameObject, obj2: GameObject):
    if obj1.collides_with(obj2):
        # Handle momentum transfer based on mass
        total_mass = obj1.mass + obj2.mass
        
        # Calculate new velocities based on conservation of momentum
        v1_x = ((obj1.mass - obj2.mass) * obj1.velocity_x + 
                2 * obj2.mass * obj2.velocity_x) / total_mass
        v2_x = ((obj2.mass - obj1.mass) * obj2.velocity_x + 
                2 * obj1.mass * obj1.velocity_x) / total_mass
        
        # Apply new velocities
        obj1.velocity_x = v1_x
        obj2.velocity_x = v2_x

def keep_in_bounds(game_object: GameObject):
    # Keep object within screen bounds
    if game_object.rect.left < 0:
        game_object.rect.left = 0
        game_object.velocity_x = 0
    elif game_object.rect.right > WINDOW_WIDTH:
        game_object.rect.right = WINDOW_WIDTH
        game_object.velocity_x = 0
        
    if game_object.rect.top < 0:
        game_object.rect.top = 0
        game_object.velocity_y = 0
    elif game_object.rect.bottom > WINDOW_HEIGHT:
        game_object.rect.bottom = WINDOW_HEIGHT
        game_object.velocity_y = 0
        game_object.on_ground = True