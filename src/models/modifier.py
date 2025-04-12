from typing import Dict, Any
from src.utils.constants import *

class Modifier:
    def __init__(self, name: str, effect_type: str, values: Dict[str, Any]):
        self.name = name
        self.effect_type = effect_type
        self.values = values
        self.target = None
        self._original_values = {}

    def apply(self, target):
        self.target = target
        if self.effect_type == "bouncy":
            self._original_values["velocity_y"] = target.velocity_y
            target.velocity_y = BOUNCY_FORCE
        elif self.effect_type == "heavy":
            self._original_values["mass"] = target.mass
            target.mass = HEAVY_MASS
        elif self.effect_type == "floaty":
            self._original_values["gravity"] = target.gravity
            target.gravity = FLOATY_GRAVITY
        elif self.effect_type == "sticky":
            self._original_values["velocity_x"] = target.velocity_x
            self._original_values["velocity_y"] = target.velocity_y
            target.velocity_x = 0
            target.velocity_y = 0
        elif self.effect_type == "reversed":
            self._original_values["velocity_x"] = target.velocity_x
            target.velocity_x *= -1
        elif self.effect_type == "ghostly":
            self._original_values["collision_enabled"] = getattr(target, "collision_enabled", True)
            target.collision_enabled = False

    def remove(self, target):
        if self.effect_type == "bouncy":
            target.velocity_y = self._original_values.get("velocity_y", 0)
        elif self.effect_type == "heavy":
            target.mass = self._original_values.get("mass", 1)
        elif self.effect_type == "floaty":
            target.gravity = self._original_values.get("gravity", GRAVITY)
        elif self.effect_type == "sticky":
            target.velocity_x = self._original_values.get("velocity_x", 0)
            target.velocity_y = self._original_values.get("velocity_y", 0)
        elif self.effect_type == "reversed":
            target.velocity_x = self._original_values.get("velocity_x", 0)
        elif self.effect_type == "ghostly":
            target.collision_enabled = self._original_values.get("collision_enabled", True)
        
        self.target = None
        self._original_values = {}