import pygame
from typing import List, Optional
from src.models.player import Player
from src.models.game_object import GameObject
from src.models.level_manager import LevelManager
from src.utils.constants import *
from src.utils.physics import handle_collisions, handle_object_interaction, keep_in_bounds

class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("The Modifier Mallet")
        self.clock = pygame.time.Clock()
        self.game_state = GameState.PLAYING
        
        # Initialize level system
        self.level_manager = LevelManager()
        self.static_objects = []
        self.dynamic_objects = []
        self.player = None
        self.goal = None
        self.current_level_data = None
        self.load_current_level()

    def load_current_level(self):
        """Load the current level from the level manager."""
        level_number = self.level_manager.current_level
        static_objects, dynamic_objects, player_start, goal = self.level_manager.load_level(level_number)
        
        self.static_objects = static_objects
        self.dynamic_objects = dynamic_objects
        self.goal = goal
        
        # Create player at start position
        if player_start:
            self.player = Player(player_start.rect.x, player_start.rect.y)
        else:
            self.player = Player(50, WINDOW_HEIGHT - 100)  # Default position

        # Load level data for hints and description
        level_file = f"src/levels/level_{level_number + 1}.json"
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
                    # Check for draggable objects first
                    draggable_clicked = False
                    for obj in self.dynamic_objects:
                        if obj.is_draggable and obj.rect.collidepoint(mouse_x, mouse_y):
                            obj.start_drag(mouse_x, mouse_y)
                            draggable_clicked = True
                            break
                    
                    # If no draggable object was clicked, use mallet
                    if not draggable_clicked:
                        self.handle_mallet_use()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click release
                    # Stop dragging any objects being dragged
                    for obj in self.dynamic_objects:
                        if obj.being_dragged:
                            obj.stop_drag()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.PAUSED if self.game_state == GameState.PLAYING else GameState.PLAYING
                elif event.key == pygame.K_r:  # Reset level
                    self.load_current_level()
        return True

    def handle_mallet_use(self):
        mouse_pos = pygame.mouse.get_pos()
        closest_obj = None
        min_distance = float('inf')

        # Check all objects that can be hit with the mallet
        for obj in self.dynamic_objects + [self.player]:
            dist = ((obj.rect.centerx - mouse_pos[0]) ** 2 + 
                   (obj.rect.centery - mouse_pos[1]) ** 2) ** 0.5
            if dist < min_distance and dist <= self.player.mallet_range:
                min_distance = dist
                closest_obj = obj

        if closest_obj:
            self.player.use_mallet(closest_obj)

    def update(self):
        if self.game_state != GameState.PLAYING:
            return

        # Update player
        self.player.update()
        keep_in_bounds(self.player)
        handle_collisions(self.player, self.static_objects)

        # Update dynamic objects
        for obj in self.dynamic_objects:
            obj.update()
            keep_in_bounds(obj)
            handle_collisions(obj, self.static_objects)

            # Handle interactions between dynamic objects
            for other_obj in self.dynamic_objects:
                if obj != other_obj:
                    handle_object_interaction(obj, other_obj)

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
        text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

    def draw(self):
        self.screen.fill(BLACK)

        # Draw static objects
        for obj in self.static_objects:
            obj.draw(self.screen)

        # Draw dynamic objects
        for obj in self.dynamic_objects:
            obj.draw(self.screen)

        # Draw goal
        if self.goal:
            self.goal.draw(self.screen)

        # Draw player
        self.player.draw(self.screen)

        # Draw level information and hints
        if self.current_level_data:
            font = pygame.font.Font(None, 36)
            name_text = font.render(f"Level {self.level_manager.current_level + 1}: {self.current_level_data['name']}", True, WHITE)
            self.screen.blit(name_text, (10, 10))
            
            small_font = pygame.font.Font(None, 24)
            for i, hint in enumerate(self.current_level_data.get("hints", [])):
                hint_text = small_font.render(hint, True, WHITE)
                self.screen.blit(hint_text, (10, 50 + i * 25))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()