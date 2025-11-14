"""
Animation system for The Hollow Path.
Handles sprite animation and animation state management.
"""
import pygame
from typing import List


class Animation:
    """Single animation sequence"""

    def __init__(self, frames: List[pygame.Surface], frame_duration: float,
                loop: bool = True):
        """
        Initialize an animation.

        Args:
            frames: List of sprite frames
            frame_duration: Duration of each frame in seconds
            loop: Whether to loop the animation
        """
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.time_accumulator = 0.0
        self.finished = False

    def update(self, dt: float):
        """Update animation frame based on time"""
        if self.finished and not self.loop:
            return

        self.time_accumulator += dt

        if self.time_accumulator >= self.frame_duration:
            self.time_accumulator = 0
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True

    def get_current_frame(self) -> pygame.Surface:
        """Get the current frame surface"""
        if not self.frames:
            # Return a default empty surface if no frames
            return pygame.Surface((32, 32))
        return self.frames[self.current_frame]

    def reset(self):
        """Reset animation to first frame"""
        self.current_frame = 0
        self.time_accumulator = 0
        self.finished = False


class AnimationController:
    """Manages multiple animations for an entity"""

    def __init__(self):
        self.animations = {}
        self.current_animation = None
        self.previous_animation = None

    def add_animation(self, name: str, animation: Animation):
        """
        Register an animation.

        Args:
            name: Animation name/state
            animation: Animation object
        """
        self.animations[name] = animation

    def play(self, name: str, force_restart: bool = False):
        """
        Play an animation by name.

        Args:
            name: Animation name to play
            force_restart: If True, restart even if already playing
        """
        if name not in self.animations:
            return

        if self.current_animation != name or force_restart:
            self.previous_animation = self.current_animation
            if self.previous_animation and self.previous_animation in self.animations:
                self.animations[self.previous_animation].reset()

            self.current_animation = name

    def update(self, dt: float):
        """Update current animation"""
        if self.current_animation and self.current_animation in self.animations:
            self.animations[self.current_animation].update(dt)

    def get_current_frame(self) -> pygame.Surface:
        """Get current frame of playing animation"""
        if self.current_animation and self.current_animation in self.animations:
            return self.animations[self.current_animation].get_current_frame()
        # Return default surface if no animation
        return pygame.Surface((32, 32))

    def is_finished(self) -> bool:
        """Check if current animation has finished (for non-looping animations)"""
        if self.current_animation and self.current_animation in self.animations:
            return self.animations[self.current_animation].finished
        return False
