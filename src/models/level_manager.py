import json
import os
from typing import List, Tuple, Optional
from src.models.game_object import GameObject
from src.utils.settings_manager import SettingsManager
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT

class LevelManager:
    def __init__(self, levels_dir: str = "src/levels"):
        self.settings = SettingsManager()
        self.levels_dir = os.path.join("src", self.settings.get("game", "level_directory", default="levels"))
        self.current_level = 0
        self.levels = self._load_level_list()
        
        # ASCII level symbols mapping
        self.ascii_map = {
            '#': {"type": "platform", "color": [0, 255, 0]},  # Solid platform
            'G': {"type": "ghost_wall", "color": [128, 128, 255], "is_ghost_passable": True},  # Ghost wall
            'B': {"type": "box", "color": [255, 0, 0]},  # Red box
            'H': {"type": "blocking_box", "color": [139, 69, 19]},  # Heavy/blocking box
            'P': {"type": "player_start"},  # Player start
            'X': {"type": "goal", "color": [255, 215, 0]},  # Goal
            ' ': None  # Empty space
        }
        
    def _load_level_list(self) -> List[str]:
        """Load list of available level files."""
        try:
            if not os.path.exists(self.levels_dir):
                os.makedirs(self.levels_dir)
            return sorted([f for f in os.listdir(self.levels_dir) 
                         if f.endswith('.json') or f.endswith('.txt')])
        except Exception as e:
            print(f"Error loading levels: {e}")
            return []

    def load_ascii_level(self, level_txt: str) -> tuple:
        """Load a level from ASCII text representation."""
        static_objects = []
        dynamic_objects = []
        player_start = None
        goal = None
        
        lines = level_txt.strip().split('\n')
        height = len(lines)
        width = max(len(line) for line in lines)
        
        # Calculate grid cell size based on window dimensions
        cell_width = WINDOW_WIDTH // width
        cell_height = WINDOW_HEIGHT // height
        
        # Parse the ASCII grid
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char not in self.ascii_map or self.ascii_map[char] is None:
                    continue
                    
                obj_def = self.ascii_map[char]
                px = x * cell_width
                py = y * cell_height
                
                if obj_def["type"] == "player_start":
                    player_start = GameObject(px, py, 30, 50, (0, 0, 255))
                elif obj_def["type"] == "goal":
                    goal = GameObject(px, py, 30, 30, tuple(obj_def["color"]))
                elif obj_def["type"] in ["box", "blocking_box"]:
                    box = GameObject(px, py, 30, 30, tuple(obj_def["color"]))
                    if obj_def["type"] == "blocking_box":
                        box.is_pushable = False
                    dynamic_objects.append(box)
                else:  # Static objects (platforms, walls)
                    platform = GameObject(px, py, cell_width, cell_height, tuple(obj_def["color"]))
                    if "is_ghost_passable" in obj_def:
                        platform.is_ghost_passable = obj_def["is_ghost_passable"]
                    static_objects.append(platform)
        
        return static_objects, dynamic_objects, player_start, goal

    def load_level(self, level_number: int) -> Tuple[List[GameObject], List[GameObject], Optional[GameObject], Optional[GameObject]]:
        """Load a level by number and return its objects."""
        if not self.levels or level_number >= len(self.levels):
            return [], [], None, None

        level_path = os.path.join(self.levels_dir, self.levels[level_number])
        
        # Check if it's a text file (ASCII level) or JSON
        if level_path.endswith('.txt'):
            try:
                with open(level_path, 'r') as f:
                    return self.load_ascii_level(f.read())
            except Exception as e:
                print(f"Error loading ASCII level {level_number}: {e}")
                return [], [], None, None
                
        # Default JSON loading
        try:
            with open(level_path, 'r') as f:
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