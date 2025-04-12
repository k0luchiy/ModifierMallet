import pygame
from enum import Enum
from src.utils.settings_manager import SettingsManager

# Initialize settings manager
settings = SettingsManager()

# Window settings (from config)
WINDOW_WIDTH = settings.get("window", "width", default=800)
WINDOW_HEIGHT = settings.get("window", "height", default=600)
FPS = settings.get("window", "fps", default=60)

# Colors (from config)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Physics constants (from config)
GRAVITY = settings.get("physics", "gravity", default=0.8)
PLAYER_SPEED = settings.get("physics", "player", "max_speed", default=5)
PLAYER_ACCELERATION = settings.get("physics", "player", "acceleration", default=0.5)
PLAYER_DECELERATION = settings.get("physics", "player", "deceleration", default=0.35)
PLAYER_AIR_ACCELERATION = settings.get("physics", "player", "air_acceleration", default=0.2)
PLAYER_JUMP_FORCE = settings.get("physics", "player", "jump_force", default=-15)
PLAYER_MAX_SPEED = settings.get("physics", "player", "max_speed", default=20)

# Modifier physics
BOUNCY_FORCE = settings.get("physics", "modifiers", "bouncy_elasticity", default=0.9)
HEAVY_MASS = settings.get("physics", "modifiers", "heavy_mass_multiplier", default=5)
FLOATY_GRAVITY = settings.get("physics", "modifiers", "floaty_gravity_scale", default=0.1)

# Game settings
MAX_ACTIVE_MODIFIERS = settings.get("game", "max_active_modifiers", default=3)

# Game states
class GameState(Enum):
    MAIN_MENU = 0
    PLAYING = 1
    PAUSED = 2
    LEVEL_COMPLETE = 3
    GAME_OVER = 4