import pygame
import json
import os
from typing import List, Optional
from src.models.player import Player
from src.models.game_object import GameObject
from src.models.level_manager import LevelManager
from src.utils.constants import *
from src.utils.physics import handle_collisions, keep_in_bounds, PhysicsSystem
from src.utils.settings_manager import SettingsManager

class GameController:
    def __init__(self):
        pygame.init()
        self.settings = SettingsManager()
        self.physics = PhysicsSystem()  # Initialize physics system
        
        # Initialize display with settings
        self.screen = pygame.display.set_mode((
            self.settings.get("window", "width", default=800),
            self.settings.get("window", "height", default=600)
        ))
        pygame.display.set_caption(self.settings.get("window", "title", default="Modifier Mallet"))
        self.clock = pygame.time.Clock()
        self.game_state = GameState.PLAYING
        
        # Initialize game objects
        self.level_manager = LevelManager(self.settings.get("game", "level_directory", default="levels/"))
        self.player = None
        self.static_objects = []
        self.dynamic_objects = []
        self.goal = None
        self.load_current_level()
        
        # FPS display
        self.fps_font = pygame.font.Font(None, 36)

        # Track the object being dragged
        self.dragged_object: Optional[GameObject] = None

    def load_current_level(self):
        """Load the current level from the level manager."""
        level_number = self.level_manager.current_level
        static_objects, dynamic_objects, player_start, goal = self.level_manager.load_level(level_number)
        
        self.static_objects = static_objects
        self.dynamic_objects = dynamic_objects
        self.goal = goal
        
        # Create player at start position
        if player_start:
            self.player = Player(player_start.rect.x, player_start.rect.y, self.settings)
        else:
            self.player = Player(50, self.settings.get("window", "height") - 100, self.settings)

        # Load level data for hints and description
        level_file = f"{self.settings.get('game', 'level_directory', default='levels/')}/level_{level_number + 1}.json"
        try:
            with open(level_file, 'r') as f:
                self.current_level_data = json.load(f)
        except:
            self.current_level_data = {
                "name": f"Level {level_number + 1}",
                "description": "",
                "hints": []
            }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = event.pos
                    clicked_on_draggable = False
                    # Check dynamic objects first for dragging
                    for obj in self.dynamic_objects:
                        if obj.is_draggable and obj.rect.collidepoint(mouse_x, mouse_y):
                            self.dragged_object = obj
                            obj.start_drag(mouse_x, mouse_y)
                            clicked_on_draggable = True
                            break  # Only drag one object at a time
                    
                    # If not starting a drag, try using the mallet
                    if not clicked_on_draggable:
                        self.handle_mallet_use(mouse_pos=event.pos)
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click release
                    # Stop dragging if an object is being dragged
                    if self.dragged_object:
                        self.dragged_object.stop_drag()
                        self.dragged_object = None
                        
            elif event.type == pygame.KEYDOWN:
                key_pause = self.settings.get("controls", "pause", default=pygame.K_ESCAPE)
                key_reset = self.settings.get("controls", "reset_level", default=pygame.K_r)
                if event.key == key_pause:
                    self.game_state = GameState.PAUSED if self.game_state == GameState.PLAYING else GameState.PAUSED
                elif event.key == key_reset:
                    # Ensure dragged object is released on reset
                    if self.dragged_object:
                        self.dragged_object.stop_drag()
                        self.dragged_object = None
                    self.load_current_level()
        return True

    def handle_mallet_use(self, mouse_pos):
        # This function is now only called if a drag didn't start
        closest_obj = None
        min_distance = float('inf')

        # Check all objects that can be hit with the mallet
        for obj in self.dynamic_objects + [self.player]: 
            dist_sq = (obj.rect.centerx - mouse_pos[0])**2 + (obj.rect.centery - mouse_pos[1])**2
            if dist_sq < min_distance**2 and dist_sq <= self.player.mallet_range**2:
                min_distance = dist_sq**0.5
                closest_obj = obj

        if closest_obj:
            # Apply mallet hit force (optional)
            hit_force = self.settings.get("game", "mallet_hit_force", default=5)
            if hit_force > 0 and closest_obj != self.player:
                 direction_x = closest_obj.rect.centerx - self.player.rect.centerx
                 direction_y = closest_obj.rect.centery - self.player.rect.centery
                 norm = (direction_x**2 + direction_y**2)**0.5
                 if norm > 0:
                     closest_obj.velocity_x += (direction_x / norm) * hit_force / closest_obj.mass
                     closest_obj.velocity_y += (direction_y / norm) * hit_force / closest_obj.mass
                     
            # Apply/Remove modifier
            self.player.use_mallet(closest_obj)

    def update(self):
        if self.game_state != GameState.PLAYING:
            return

        # Update player
        self.player.update()
        handle_collisions(self.player, self.static_objects)
        # Handle player collision with dynamic objects AFTER static collisions
        for obj in self.dynamic_objects:
             # Skip physics interaction if this object is being dragged
             if obj != self.dragged_object:
                 self.physics.handle_player_object_collision(self.player, obj)
        keep_in_bounds(self.player)

        # Update dynamic objects
        for obj in self.dynamic_objects:
            # Only update physics if not being dragged
            if not obj.being_dragged:
                obj.update()
                handle_collisions(obj, self.static_objects)
                # Handle interactions between dynamic objects
                for other_obj in self.dynamic_objects:
                    # Skip interaction if either object is being dragged
                    if obj != other_obj and obj != self.dragged_object and other_obj != self.dragged_object:
                        self.physics.handle_player_object_collision(obj, other_obj)
                keep_in_bounds(obj)
            else:
                # If dragged, just update position based on mouse (handled in GameObject.update)
                obj.update() 
                # Optional: Keep dragged object partially within bounds?
                # keep_in_bounds(obj) # Might feel weird, maybe allow dragging slightly out?

        # Check if player reached the goal
        if self.goal and self.player.collides_with(self.goal):
            if self.level_manager.next_level():
                self.load_current_level()
            else:
                self.show_victory_message()
                self.game_state = GameState.GAME_OVER

    def show_victory_message(self):
        font = pygame.font.Font(None, 74)
        if self.level_manager.current_level >= self.level_manager.get_level_count() - 1:
            text = font.render('Game Complete!', True, (255, 215, 0))
        else:
            text = font.render('Level Complete!', True, (255, 215, 0))
        text_rect = text.get_rect(center=(self.settings.get("window", "width")/2, self.settings.get("window", "height")/2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

    def draw(self):
        # Fill background
        self.screen.fill(tuple(self.settings.get("colors", "background", default=[0, 0, 0])))

        # Draw game objects
        for obj in self.static_objects:
            obj.draw(self.screen)

        for obj in self.dynamic_objects:
            obj.draw(self.screen)

        if self.goal:
            self.goal.draw(self.screen)

        self.player.draw(self.screen)

        # Draw level information
        if self.current_level_data:
            font_size = self.settings.get("ui", "font_size_normal", default=24)
            small_font_size = self.settings.get("ui", "font_size_hint", default=18)
            
            font = pygame.font.Font(None, font_size)
            small_font = pygame.font.Font(None, small_font_size)
            text_color = tuple(self.settings.get("colors", "ui_text", default=[255, 255, 255]))
            
            # Level name
            name_text = font.render(
                f"Level {self.level_manager.current_level + 1}: {self.current_level_data['name']}", 
                True, text_color
            )
            self.screen.blit(name_text, (10, 10))
            
            # Level hints
            for i, hint in enumerate(self.current_level_data.get("hints", [])):
                hint_text = small_font.render(hint, True, text_color)
                self.screen.blit(hint_text, (10, 50 + i * 25))

        # Draw FPS counter if enabled
        if self.settings.get("debug", "show_fps", default=False):
            fps = self.clock.get_fps()
            fps_text = self.fps_font.render(f"FPS: {int(fps)}", True, (255, 255, 0))
            self.screen.blit(fps_text, (10, self.settings.get("window", "height") - 40))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.settings.get("window", "fps", default=60))
        pygame.quit()