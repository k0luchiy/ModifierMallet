import pygame
from enum import Enum
from src.utils.settings_manager import SettingsManager

# Initialize settings manager
settings = SettingsManager()

# Window settings
WINDOW_WIDTH = settings.get("window", "width", default=800)
WINDOW_HEIGHT = settings.get("window", "height", default=600)
WINDOW_TITLE = settings.get("window", "title", default="Modifier Mallet")
FPS = settings.get("window", "fps", default=60)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

# UI Colors
UI_BACKGROUND = tuple(settings.get("colors", "ui_background", default=[50, 50, 50]))
UI_TEXT = tuple(settings.get("colors", "ui_text", default=[255, 255, 255]))
MALLET_RANGE_COLOR = tuple(settings.get("colors", "mallet_range", default=[100, 100, 100, 150]))
COOLDOWN_BAR_COLOR = tuple(settings.get("colors", "cooldown_bar", default=[200, 200, 0]))

# Modifier Colors
MODIFIER_COLORS = {
    "bouncy": tuple(settings.get("colors", "modifiers", "bouncy", default=[0, 255, 255])),
    "heavy": tuple(settings.get("colors", "modifiers", "heavy", default=[139, 69, 19])),
    "floaty": tuple(settings.get("colors", "modifiers", "floaty", default=[255, 105, 180])),
    "sticky": tuple(settings.get("colors", "modifiers", "sticky", default=[128, 0, 128])),
    "reversed": tuple(settings.get("colors", "modifiers", "reversed", default=[255, 165, 0])),
    "ghostly": tuple(settings.get("colors", "modifiers", "ghostly", default=[128, 128, 128]))
}

# Physics constants
GRAVITY = settings.get("physics", "gravity", default=0.8)

# Player physics
PLAYER_MASS = settings.get("physics", "player", "mass", default=1.0)
PLAYER_SPEED = settings.get("physics", "player", "max_speed", default=7)
PLAYER_ACCELERATION = settings.get("physics", "player", "acceleration", default=0.5)
PLAYER_DECELERATION = settings.get("physics", "player", "deceleration", default=0.35)
PLAYER_AIR_ACCELERATION = settings.get("physics", "player", "air_acceleration", default=0.2)
PLAYER_JUMP_FORCE = settings.get("physics", "player", "jump_force", default=-15)
PLAYER_MAX_SPEED = settings.get("physics", "player", "max_speed", default=20)

# Object physics defaults
OBJECT_DEFAULT_MASS = settings.get("physics", "object", "default_mass", default=1.0)
OBJECT_DEFAULT_FRICTION = settings.get("physics", "object", "default_friction", default=0.5)
OBJECT_DEFAULT_ELASTICITY = settings.get("physics", "object", "default_elasticity", default=0.2)

# Modifier physics
BOUNCY_ELASTICITY = settings.get("physics", "modifiers", "bouncy_elasticity", default=0.9)
HEAVY_MASS_MULTIPLIER = settings.get("physics", "modifiers", "heavy_mass_multiplier", default=5)
FLOATY_GRAVITY_SCALE = settings.get("physics", "modifiers", "floaty_gravity_scale", default=0.1)
STICKY_DRAG_FORCE = settings.get("physics", "modifiers", "sticky_drag_force", default=10)
GHOSTLY_ALPHA = settings.get("physics", "modifiers", "ghostly_alpha", default=128)

# Controls
KEY_MOVE_LEFT = settings.get("controls", "move_left", default=pygame.K_a)
KEY_MOVE_RIGHT = settings.get("controls", "move_right", default=pygame.K_d)
KEY_JUMP = settings.get("controls", "jump", default=pygame.K_SPACE)
KEY_CYCLE_MOD_NEXT = settings.get("controls", "cycle_mod_next", default=pygame.K_e)
KEY_CYCLE_MOD_PREV = settings.get("controls", "cycle_mod_prev", default=pygame.K_q)
KEY_RESET_LEVEL = settings.get("controls", "reset_level", default=pygame.K_r)
KEY_PAUSE = settings.get("controls", "pause", default=pygame.K_ESCAPE)
MOUSE_USE_MALLET = settings.get("controls", "use_mallet", default=1)  # Left click

# Game settings
MAX_ACTIVE_MODIFIERS = settings.get("game", "max_active_modifiers", default=3)
LEVEL_DIRECTORY = settings.get("game", "level_directory", default="levels/")
MODIFIER_COOLDOWN = settings.get("game", "modifier_cooldown", default=0.5)
MALLET_RANGE = settings.get("game", "mallet_range", default=100)
MALLET_HIT_FORCE = settings.get("game", "mallet_hit_force", default=5)

# UI Settings
FONT_NAME = settings.get("ui", "font_name", default=None)
FONT_SIZE_NORMAL = settings.get("ui", "font_size_normal", default=24)
FONT_SIZE_HINT = settings.get("ui", "font_size_hint", default=18)
MODIFIER_SELECTOR_SCALE = settings.get("ui", "modifier_selector_scale", default=1.2)
MODIFIER_OUTLINE_THICKNESS = settings.get("ui", "modifier_outline_thickness", default=2)
SHOW_MODIFIER_ICONS = settings.get("ui", "show_modifier_icons", default=True)
SHOW_COOLDOWN = settings.get("ui", "show_cooldown", default=True)
SHOW_HINTS = settings.get("ui", "show_hints", default=True)

# Debug settings
DRAW_COLLIDERS = settings.get("debug", "draw_colliders", default=True)
SHOW_FPS = settings.get("debug", "show_fps", default=True)

# Game states
class GameState(Enum):
    MAIN_MENU = 0
    PLAYING = 1
    PAUSED = 2
    LEVEL_COMPLETE = 3
    GAME_OVER = 4