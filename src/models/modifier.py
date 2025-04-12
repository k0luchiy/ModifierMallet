from typing import Dict, Any
from src.utils.settings_manager import SettingsManager
from src.utils.constants import *

class Modifier:
    def __init__(self, name: str, effect_type: str, values: Dict[str, Any]):
        self.settings = SettingsManager()
        self.name = name
        self.effect_type = effect_type
        self.values = values
        self.target = None
        self._original_values = {}

    def apply(self, target):
        self.target = target
        if self.effect_type == "bouncy":
            self._original_values["elasticity"] = target.elasticity
            target.elasticity = self.settings.get("physics", "modifiers", "bouncy_elasticity", default=0.9)
        
        elif self.effect_type == "heavy":
            self._original_values["mass"] = target.mass
            multiplier = self.settings.get("physics", "modifiers", "heavy_mass_multiplier", default=5)
            target.mass = target.mass * multiplier
        
        elif self.effect_type == "floaty":
            self._original_values["gravity"] = target.gravity
            scale = self.settings.get("physics", "modifiers", "floaty_gravity_scale", default=0.1)
            target.gravity = target.gravity * scale
        
        elif self.effect_type == "sticky":
            self._original_values["velocity_x"] = target.velocity_x
            self._original_values["velocity_y"] = target.velocity_y
            self._original_values["friction"] = target.friction
            target.velocity_x = 0
            target.velocity_y = 0
            target.friction = self.settings.get("physics", "modifiers", "sticky_drag_force", default=10)
            target.is_draggable = True
        
        elif self.effect_type == "reversed":
            self._original_values["velocity_x"] = target.velocity_x
            target.velocity_x *= -1
            self._original_values["control_reversed"] = True
        
        elif self.effect_type == "ghostly":
            self._original_values["collision_enabled"] = getattr(target, "collision_enabled", True)
            target.collision_enabled = False
            alpha = self.settings.get("physics", "modifiers", "ghostly_alpha", default=128)
            target.alpha = alpha

    def remove(self, target):
        if self.effect_type == "bouncy":
            target.elasticity = self._original_values.get("elasticity", 
                self.settings.get("physics", "object", "default_elasticity", default=0.2))
        
        elif self.effect_type == "heavy":
            target.mass = self._original_values.get("mass", 
                self.settings.get("physics", "object", "default_mass", default=1.0))
        
        elif self.effect_type == "floaty":
            target.gravity = self._original_values.get("gravity", 
                self.settings.get("physics", "gravity", default=0.8))
        
        elif self.effect_type == "sticky":
            target.velocity_x = self._original_values.get("velocity_x", 0)
            target.velocity_y = self._original_values.get("velocity_y", 0)
            target.friction = self._original_values.get("friction", 
                self.settings.get("physics", "object", "default_friction", default=0.5))
            target.is_draggable = False
        
        elif self.effect_type == "reversed":
            target.velocity_x = self._original_values.get("velocity_x", 0)
            if self._original_values.get("control_reversed", False):
                target.velocity_x *= -1
        
        elif self.effect_type == "ghostly":
            target.collision_enabled = self._original_values.get("collision_enabled", True)
            target.alpha = 255  # Reset transparency
        
        self.target = None
        self._original_values = {}