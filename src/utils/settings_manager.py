import json
import os
import pygame
from typing import Any, Dict

class SettingsManager:
    def __init__(self, config_dir: str = "src/config"):
        self.config_dir = config_dir
        self.settings: Dict[str, Any] = {}
        self._load_settings()

    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration dictionary."""
        return {
            "window": {
                "width": 800,
                "height": 600,
                "title": "Modifier Mallet",
                "fps": 60
            },
            "colors": {
                "background": [0, 0, 0],
                "ui_background": [50, 50, 50],
                "ui_text": [255, 255, 255],
                "mallet_range": [100, 100, 100, 150],
                "cooldown_bar": [200, 200, 0],
                "modifiers": {
                    "bouncy": [0, 255, 255],
                    "heavy": [139, 69, 19],
                    "floaty": [255, 105, 180],
                    "sticky": [128, 0, 128],
                    "reversed": [255, 165, 0],
                    "ghostly": [128, 128, 128]
                }
            },
            "physics": {
                "gravity": 0.7,  # Slightly reduced from original
                "player": {
                    "acceleration": 0.4,  # More gradual acceleration
                    "deceleration": 0.4,  # Matching deceleration for smooth feel
                    "air_acceleration": 0.15,  # Reduced air control
                    "max_speed": 5.5,  # Slightly lower top speed
                    "jump_force": -13,  # Adjusted for new gravity
                    "mass": 1.0
                },
                "object": {
                    "default_mass": 1.0,
                    "default_friction": 0.5,
                    "default_elasticity": 0.2,
                    "push_force_scale": 0.8  # New: scales force applied when pushing objects
                },
                "modifiers": {
                    "bouncy_elasticity": 0.9,
                    "heavy_mass_multiplier": 5,
                    "floaty_gravity_scale": 0.1,
                    "sticky_drag_force": 10,
                    "ghostly_alpha": 128
                }
            },
            "mallet": {
                "range": 100,
                "cooldown": 0.5,
                "hit_force": 5
            },
            "game": {
                "max_active_modifiers": 3,
                "level_directory": "levels/"
            },
            "ui": {
                "font_name": None,
                "font_size_normal": 24,
                "font_size_hint": 18,
                "modifier_selector_scale": 1.2,
                "modifier_outline_thickness": 2
            },
            "audio": {
                "master_volume": 1.0,
                "sfx_volume": 0.8,
                "music_volume": 0.5
            },
            "debug": {
                "draw_colliders": False,
                "show_fps": True
            },
            "controls": {
                "move_left": pygame.K_LEFT,
                "move_right": pygame.K_RIGHT,
                "jump": pygame.K_SPACE,
                "cycle_mod_next": pygame.K_e,
                "cycle_mod_prev": pygame.K_q,
                "reset_level": pygame.K_r,
                "pause": pygame.K_ESCAPE
            }
        }

    def _load_settings(self):
        """Load settings from config file, create default if doesn't exist."""
        self.settings = self._create_default_config()
        
        config_path = os.path.join(self.config_dir, "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_settings = json.load(f)
                    # Deep update of settings with user values
                    self._deep_update(self.settings, user_settings)
            except json.JSONDecodeError:
                print("Warning: Invalid config.json file. Using default settings.")
            except Exception as e:
                print(f"Warning: Error loading config file: {e}")

    def _deep_update(self, d: dict, u: dict) -> None:
        """Recursively update nested dictionary with another dictionary."""
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                self._deep_update(d[k], v)
            else:
                d[k] = v

    def save_settings(self):
        """Save current settings to config file."""
        os.makedirs(self.config_dir, exist_ok=True)
        config_path = os.path.join(self.config_dir, "config.json")
        try:
            with open(config_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get(self, *keys: str, default: Any = None) -> Any:
        """
        Get a setting value using dot notation.
        Example: settings.get("physics", "player", "acceleration")
        """
        value = self.settings
        for key in keys:
            try:
                value = value[key]
            except (KeyError, TypeError):
                return default
        return value

    def set(self, value: Any, *keys: str) -> None:
        """
        Set a setting value using dot notation.
        Example: settings.set(0.6, "physics", "player", "acceleration")
        """
        if not keys:
            return

        current = self.settings
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value