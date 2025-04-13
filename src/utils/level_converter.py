"""Utility to convert ASCII level files to JSON format."""
import json
import os

def convert_ascii_to_json(ascii_file_path: str, json_file_path: str):
    """Convert an ASCII level file to JSON format."""
    with open(ascii_file_path, 'r') as f:
        ascii_lines = f.readlines()

    level_data = {
        "width": len(ascii_lines[0].strip()),
        "height": len(ascii_lines),
        "player": None,
        "exit": None,
        "platforms": [],
        "boxes": []
    }

    for y, line in enumerate(ascii_lines):
        for x, char in enumerate(line.strip()):
            if char == '#':  # Wall/Platform
                level_data["platforms"].append({
                    "x": x * 32,  # 32 pixels per tile
                    "y": y * 32,
                    "width": 32,
                    "height": 32,
                    "type": "static"
                })
            elif char == 'P':  # Player
                level_data["player"] = {
                    "x": x * 32,
                    "y": y * 32
                }
            elif char == 'X':  # Exit
                level_data["exit"] = {
                    "x": x * 32,
                    "y": y * 32
                }
            elif char == 'B':  # Basic Box
                level_data["boxes"].append({
                    "x": x * 32,
                    "y": y * 32,
                    "width": 32,
                    "height": 32,
                    "type": "dynamic",
                    "initial_modifiers": []
                })
            elif char == 'H':  # Heavy Box
                level_data["boxes"].append({
                    "x": x * 32,
                    "y": y * 32,
                    "width": 32,
                    "height": 32,
                    "type": "dynamic",
                    "initial_modifiers": ["heavy"]
                })
            elif char == 'G':  # Ghostly Box
                level_data["boxes"].append({
                    "x": x * 32,
                    "y": y * 32,
                    "width": 32,
                    "height": 32,
                    "type": "dynamic",
                    "initial_modifiers": ["ghostly"]
                })

    with open(json_file_path, 'w') as f:
        json.dump(level_data, f, indent=4)

def convert_all_levels():
    """Convert all ASCII level files in the levels directory to JSON."""
    levels_dir = "src/levels"
    for filename in os.listdir(levels_dir):
        if filename.endswith(".txt"):
            ascii_path = os.path.join(levels_dir, filename)
            json_path = os.path.join(levels_dir, filename.replace(".txt", ".json"))
            convert_ascii_to_json(ascii_path, json_path)
            print(f"Converted {filename} to JSON format")

if __name__ == "__main__":
    convert_all_levels()