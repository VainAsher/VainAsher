"""
Audio system for The Hollow Path.
Handles music and sound effects.
"""
import pygame
from typing import Dict, Optional


class AudioManager:
    """Manages all game audio"""

    def __init__(self):
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            self.available = True
        except Exception as e:
            print(f"Warning: Audio system unavailable: {e}")
            self.available = False
            return

        # Volume settings
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.master_volume = 1.0

        # State
        self.current_music = None
        self.sounds: Dict[str, pygame.mixer.Sound] = {}

        # Region music mapping
        self.region_music = {
            "the_depths": "depths_theme.ogg",
            "courtroom_maze": "courtroom_theme.ogg",
            "the_void": "void_theme.ogg",
            "support_circle": "support_theme.ogg",
            "the_garden": "garden_theme.ogg",
            "the_bridge": "bridge_theme.ogg",
            "the_watchtower": "watchtower_theme.ogg"
        }

    def load_sounds(self):
        """Load all sound effects"""
        if not self.available:
            return

        sfx_list = [
            "jump", "land", "dash", "attack", "hurt",
            "shuriken", "grapple", "menu_select",
            "item_collect", "save"
        ]

        for sfx in sfx_list:
            try:
                sound = pygame.mixer.Sound(f"assets/audio/sfx/{sfx}.wav")
                self.sounds[sfx] = sound
            except Exception:
                # Create placeholder silent sound
                pass

    def play_sfx(self, name: str):
        """Play a sound effect"""
        if not self.available or name not in self.sounds:
            return

        volume = self.sfx_volume * self.master_volume
        self.sounds[name].set_volume(volume)
        self.sounds[name].play()

    def play_music(self, region_name: str, fade_ms: int = 2000):
        """Play music for a region"""
        if not self.available:
            return

        if region_name not in self.region_music:
            return

        music_file = self.region_music[region_name]

        # Don't restart if already playing
        if self.current_music == music_file:
            return

        # Fade out current music
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_ms)

        # Load and play new music
        try:
            pygame.mixer.music.load(f"assets/audio/music/{music_file}")
            volume = self.music_volume * self.master_volume
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1, fade_ms=fade_ms)  # Loop forever
            self.current_music = music_file
        except Exception as e:
            print(f"Warning: Could not load music {music_file}: {e}")

    def stop_music(self, fade_ms: int = 1000):
        """Stop music"""
        if not self.available:
            return

        pygame.mixer.music.fadeout(fade_ms)
        self.current_music = None

    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.available and pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)

    def set_sfx_volume(self, volume: float):
        """Set SFX volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))

    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        if self.available and pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(self.music_volume * self.master_volume)
