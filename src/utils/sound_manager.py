import pygame
import os
from .settings_manager import SettingsManager

class SoundManager:
    def __init__(self):
        self.settings = SettingsManager()
        self.sounds = {}
        self.master_volume = self.settings.get("audio", "master_volume", default=1.0)
        self.sfx_volume = self.settings.get("audio", "sfx_volume", default=0.8)
        
        # Initialize mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()

    def load_sound(self, name: str, filepath: str):
        """Load a sound file and store it."""
        if not os.path.exists(filepath):
            print(f"Warning: Sound file not found: {filepath}")
            return
        try:
            sound = pygame.mixer.Sound(filepath)
            self.sounds[name] = sound
        except pygame.error as e:
            print(f"Error loading sound {filepath}: {e}")

    def play_sound(self, name: str):
        """Play a loaded sound."""
        if name in self.sounds:
            sound = self.sounds[name]
            # Apply volume settings
            sound.set_volume(self.master_volume * self.sfx_volume)
            sound.play()
        else:
            print(f"Warning: Sound '{name}' not loaded.")

    def load_sounds_from_config(self):
        """Load all sounds defined in the config file."""
        sound_files = self.settings.get("audio", "sound_files", default={})
        base_path = os.path.join("src", "assets", "sounds")
        for name, filename in sound_files.items():
            filepath = os.path.join(base_path, filename)
            self.load_sound(name, filepath)