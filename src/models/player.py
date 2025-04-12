import pygame
import os
from src.models.game_object import GameObject
from src.models.modifier import Modifier
from src.models.sprite_manager import SpriteManager
from src.utils.constants import *
from src.utils.settings_manager import SettingsManager

class Player(GameObject):
    def __init__(self, x: float, y: float, settings: SettingsManager):
        self.settings = settings
        player_mass = settings.get("physics", "player", "mass", default=1.0)
        super().__init__(x, y, 30, 50, tuple(settings.get("colors", "modifiers", "bouncy", default=[0, 0, 255])), mass=player_mass)
        
        # Load player settings
        self.speed = settings.get("physics", "player", "max_speed", default=7)
        self.acceleration = settings.get("physics", "player", "acceleration", default=0.5)
        self.deceleration = settings.get("physics", "player", "deceleration", default=0.35)
        self.air_acceleration = settings.get("physics", "player", "air_acceleration", default=0.2)
        self.jump_force = settings.get("physics", "player", "jump_force", default=-15)
        self.mallet_range = settings.get("mallet", "range", default=100)
        
        self.can_jump = False
        self.facing_right = True
        self.current_modifier_index = 0
        self.modifier_types = ["bouncy", "heavy", "floaty", "sticky", "reversed", "ghostly"]
        self.last_modifier_use = 0
        self.modifier_cooldown = settings.get("mallet", "cooldown", default=0.5)
        
        # Animation states
        self.sprite_manager = SpriteManager()
        sprite_path = os.path.join("src", "assets", "images", "image.png")
        self.has_sprites = self.sprite_manager.load_spritesheet(sprite_path, 32, 32)
        self.state = "idle"
        self.state_changed = False
        self.last_state = "idle"

    def update(self):
        current_time = pygame.time.get_ticks() / 1000.0
        keys = pygame.key.get_pressed()
        
        # Store previous state for animation changes
        self.last_state = self.state
        
        # Get control keys from settings
        key_left = self.settings.get("controls", "move_left", default=pygame.K_LEFT)
        key_right = self.settings.get("controls", "move_right", default=pygame.K_RIGHT)
        key_jump = self.settings.get("controls", "jump", default=pygame.K_SPACE)
        
        # Only allow horizontal movement control if not being knocked back
        if abs(self.velocity_x) < self.speed * 1.5:
            # Horizontal movement with acceleration
            if keys[key_left]:
                accel = self.air_acceleration if not self.on_ground else self.acceleration
                self.velocity_x = max(-self.speed, self.velocity_x - accel)
                self.facing_right = False
                self.state = "walk"
            elif keys[key_right]:
                accel = self.air_acceleration if not self.on_ground else self.acceleration
                self.velocity_x = min(self.speed, self.velocity_x + accel)
                self.facing_right = True
                self.state = "walk"
            else:
                # Apply deceleration
                if self.velocity_x > 0:
                    self.velocity_x = max(0, self.velocity_x - self.deceleration)
                elif self.velocity_x < 0:
                    self.velocity_x = min(0, self.velocity_x + self.deceleration)
                
                if abs(self.velocity_x) < 0.1:
                    self.state = "idle"

        # Store previous position before physics update
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y
        
        # Only apply gravity if not on ground
        if not self.on_ground:
            self.velocity_y += self.gravity
            self.state = "jump"
        elif keys[key_jump] and self.can_jump:
            self.velocity_y = self.jump_force
            self.can_jump = False
            self.state = "jump"
            self.on_ground = False

        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Limit speeds
        max_fall_speed = self.settings.get("physics", "player", "max_speed", default=20)
        if self.velocity_y > max_fall_speed:
            self.velocity_y = max_fall_speed

        # Modifier cycling
        key_next = self.settings.get("controls", "cycle_mod_next", default=pygame.K_e)
        key_prev = self.settings.get("controls", "cycle_mod_prev", default=pygame.K_q)
        if keys[key_next]:
            self.current_modifier_index = (self.current_modifier_index + 1) % len(self.modifier_types)
        elif keys[key_prev]:
            self.current_modifier_index = (self.current_modifier_index - 1) % len(self.modifier_types)

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
        for modifier in self.active_modifiers:
            effect_color = tuple(self.settings.get("colors", "modifiers", modifier.effect_type, 
                                                 default=[255, 255, 255]))
            thickness = self.settings.get("ui", "modifier_outline_thickness", default=2)
            pygame.draw.rect(screen, effect_color, self.rect, thickness)

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
        range_color = tuple(self.settings.get("colors", "mallet_range", default=[100, 100, 100, 150]))
        pygame.draw.circle(screen, range_color[:3], 
                         (int(self.rect.centerx), int(self.rect.centery)), 
                         self.mallet_range, 1)
        
        # Draw current modifier type and cooldown
        font_size = self.settings.get("ui", "font_size_normal", default=24)
        font = pygame.font.Font(None, font_size)
        text_color = tuple(self.settings.get("colors", "ui_text", default=[255, 255, 255]))
        
        current_time = pygame.time.get_ticks() / 1000.0
        cooldown_remaining = max(0, self.modifier_cooldown - (current_time - self.last_modifier_use))
        
        if cooldown_remaining > 0:
            text = font.render(f"Modifier: {self.modifier_types[self.current_modifier_index]} ({cooldown_remaining:.1f}s)", 
                             True, text_color)
        else:
            text = font.render(f"Modifier: {self.modifier_types[self.current_modifier_index]} (Ready!)", 
                             True, text_color)
        # Position the text below the level name (40 pixels down from top)
        screen.blit(text, (10, 40))

        # Draw debug info if enabled
        if self.settings.get("debug", "draw_colliders", default=False):
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)