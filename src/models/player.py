import pygame
import os
from src.models.game_object import GameObject
from src.models.modifier import Modifier
from src.models.sprite_manager import SpriteManager
from src.utils.constants import *

class Player(GameObject):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 30, 50, BLUE)
        self.speed = PLAYER_SPEED
        self.jump_force = PLAYER_JUMP_FORCE
        self.can_jump = False
        self.mallet_range = 100
        self.facing_right = True
        self.current_modifier_index = 0
        self.modifier_types = ["bouncy", "heavy", "floaty", "sticky", "reversed", "ghostly"]
        self.last_modifier_use = 0  # Time tracking for modifier cooldown
        self.modifier_cooldown = 0.5  # Half second cooldown between modifier uses
        
        # Animation states
        self.sprite_manager = SpriteManager()
        sprite_path = os.path.join("src", "assets", "images", "image.png")
        self.has_sprites = self.sprite_manager.load_spritesheet(sprite_path, 32, 32)
        self.state = "idle"
        self.state_changed = False
        self.last_state = "idle"

    def update(self):
        current_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
        keys = pygame.key.get_pressed()
        
        # Store previous state for animation changes
        self.last_state = self.state
        was_moving = abs(self.velocity_x) > 0.1  # Small threshold for movement
        
        # Horizontal movement with acceleration and deceleration
        if keys[pygame.K_LEFT]:
            self.velocity_x = max(-self.speed, self.velocity_x - PLAYER_ACCELERATION)
            self.facing_right = False
            self.state = "walk"
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = min(self.speed, self.velocity_x + PLAYER_ACCELERATION)
            self.facing_right = True
            self.state = "walk"
        else:
            # Apply deceleration
            if self.velocity_x > 0:
                self.velocity_x = max(0, self.velocity_x - PLAYER_DECELERATION)
            elif self.velocity_x < 0:
                self.velocity_x = min(0, self.velocity_x + PLAYER_DECELERATION)
            
            if abs(self.velocity_x) < 0.1:  # Small threshold for idle
                self.state = "idle"

        # Jumping
        if keys[pygame.K_SPACE] and self.can_jump:
            self.velocity_y = self.jump_force
            self.can_jump = False
            self.state = "jump"

        # Change modifier type with Q and E keys
        if keys[pygame.K_q]:
            self.current_modifier_index = (self.current_modifier_index - 1) % len(self.modifier_types)
        elif keys[pygame.K_e]:
            self.current_modifier_index = (self.current_modifier_index + 1) % len(self.modifier_types)

        # Update physics
        super().update()

        # Update animation state
        if not self.on_ground:
            self.state = "jump"
        elif abs(self.velocity_x) < 0.1 and self.on_ground:
            self.state = "idle"

        # Only update animation if state changed or in walking/jumping state
        self.state_changed = self.last_state != self.state
        if self.has_sprites:
            if self.state_changed or self.state in ["walk", "jump"]:
                self.sprite_manager.update_animation(1/FPS, self.state)

        # Reset jump if on ground
        if self.on_ground:
            self.can_jump = True

    def use_mallet(self, target_object: GameObject, modifier_type: str = None) -> bool:
        current_time = pygame.time.get_ticks() / 1000.0

        # Check cooldown
        if current_time - self.last_modifier_use < self.modifier_cooldown:
            return False

        if modifier_type is None:
            modifier_type = self.modifier_types[self.current_modifier_index]
            
        target_x, target_y = target_object.get_position()
        player_x, player_y = self.get_position()
        
        distance = ((target_x - player_x) ** 2 + (target_y - player_y) ** 2) ** 0.5
        
        if distance <= self.mallet_range:
            values = {}
            modifier = Modifier(f"{modifier_type}_modifier", modifier_type, values)
            
            # If object already has this type of modifier, remove it
            for active_mod in target_object.active_modifiers:
                if active_mod.effect_type == modifier_type:
                    target_object.remove_modifier(active_mod)
                    self.last_modifier_use = current_time
                    return True
                    
            success = target_object.add_modifier(modifier)
            if success:
                self.last_modifier_use = current_time
            return success
        return False

    def draw(self, screen: pygame.Surface):
        # Draw modifier effect indicators
        for mod in self.active_modifiers:
            effect_color = {
                "bouncy": (0, 255, 255),  # Cyan
                "heavy": (139, 69, 19),   # Brown
                "floaty": (255, 192, 203), # Pink
                "sticky": (128, 0, 128),   # Purple
                "reversed": (255, 165, 0), # Orange
                "ghostly": (200, 200, 200) # Light gray
            }.get(mod.effect_type, WHITE)
            
            pygame.draw.circle(screen, effect_color,
                             (int(self.rect.centerx), int(self.rect.centery)),
                             self.rect.width + 5, 2)

        if self.has_sprites:
            sprite = self.sprite_manager.get_current_animation_frame(self.state)
            if sprite:
                if not self.facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)
                sprite = pygame.transform.scale(sprite, (self.rect.width, self.rect.height))
                screen.blit(sprite, self.rect)
            else:
                super().draw(screen)
        else:
            super().draw(screen)

        # Draw mallet range indicator
        pygame.draw.circle(screen, (100, 100, 100), 
                         (int(self.rect.centerx), int(self.rect.centery)), 
                         self.mallet_range, 1)
        
        # Draw current modifier type and cooldown
        font = pygame.font.Font(None, 24)
        current_time = pygame.time.get_ticks() / 1000.0
        cooldown_remaining = max(0, self.modifier_cooldown - (current_time - self.last_modifier_use))
        
        if cooldown_remaining > 0:
            text = font.render(f"Modifier: {self.modifier_types[self.current_modifier_index]} ({cooldown_remaining:.1f}s)", True, WHITE)
        else:
            text = font.render(f"Modifier: {self.modifier_types[self.current_modifier_index]} (Ready!)", True, WHITE)
        screen.blit(text, (10, 10))