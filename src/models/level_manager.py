import json
import os
from typing import List, Tuple, Optional
from src.models.game_object import GameObject
from src.utils.settings_manager import SettingsManager

class LevelManager:
    def __init__(self, levels_dir: str = "src/levels"):
        self.settings = SettingsManager()
        self.levels_dir = os.path.join("src", self.settings.get("game", "level_directory", default="levels"))
        self.current_level = 0
        self.levels = self._load_level_list()
        
    def _load_level_list(self) -> List[str]:
        """Load list of available level files."""
        try:
            if not os.path.exists(self.levels_dir):
                os.makedirs(self.levels_dir)
            return sorted([f for f in os.listdir(self.levels_dir) 
                         if f.endswith('.json')])
        except Exception as e:
            print(f"Error loading levels: {e}")
            return []

    def load_level(self, level_number: int) -> Tuple[List[GameObject], List[GameObject], Optional[GameObject], Optional[GameObject]]:
        """Load a level by number and return its objects."""
        if not self.levels or level_number >= len(self.levels):
            return [], [], None, None

        level_file = os.path.join(self.levels_dir, self.levels[level_number])
        try:
            with open(level_file, 'r') as f:
                level_data = json.load(f)
        except Exception as e:
            print(f"Error loading level {level_number}: {e}")
            return [], [], None, None

        static_objects = []
        dynamic_objects = []
        player_start = None
        goal = None

        # Create static objects (platforms, walls)
        for obj in level_data.get('static_objects', []):
            game_obj = GameObject(
                obj['x'], obj['y'],
                obj['width'], obj['height'],
                tuple(obj.get('color', [0, 255, 0]))  # Default to green
            )
            # Set ghost-passable property if specified
            game_obj.is_ghost_passable = obj.get('is_ghost_passable', False)
            static_objects.append(game_obj)

        # Create dynamic objects (boxes, etc)
        for obj in level_data.get('dynamic_objects', []):
            game_obj = GameObject(
                obj['x'], obj['y'],
                obj['width'], obj['height'],
                tuple(obj.get('color', [255, 0, 0]))  # Default to red
            )
            game_obj.is_ghost_passable = obj.get('is_ghost_passable', False)
            if obj.get('type') == 'blocking_box':
                game_obj.is_pushable = False
            dynamic_objects.append(game_obj)

        # Create player start position
        if 'player_start' in level_data:
            ps = level_data['player_start']
            player_start = GameObject(ps['x'], ps['y'], 30, 50, (0, 0, 255))

        # Create goal
        if 'goal' in level_data:
            g = level_data['goal']
            goal = GameObject(g['x'], g['y'], 30, 30, (255, 215, 0))  # Gold color

        return static_objects, dynamic_objects, player_start, goal

    def next_level(self) -> bool:
        """Move to next level if available."""
        if self.current_level + 1 < len(self.levels):
            self.current_level += 1
            return True
        return False

    def get_level_count(self) -> int:
        """Get total number of available levels."""
        return len(self.levels)