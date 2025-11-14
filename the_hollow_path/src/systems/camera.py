"""
Camera system for The Hollow Path.
Follows the player with smooth scrolling.
"""
import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Camera:
    """Camera that follows the player"""

    def __init__(self):
        self.offset = pygame.Vector2(0, 0)
        self.target = None
        self.smoothing = 0.1  # Camera smoothing factor (0-1, lower is smoother)

    def set_target(self, target):
        """Set the camera target (usually the player)"""
        self.target = target

    def update(self, dt: float):
        """Update camera position"""
        if not self.target:
            return

        # Calculate desired camera position (center on target)
        desired_x = self.target.pos.x - SCREEN_WIDTH // 2
        desired_y = self.target.pos.y - SCREEN_HEIGHT // 2

        # Smooth camera movement
        self.offset.x += (desired_x - self.offset.x) * self.smoothing
        self.offset.y += (desired_y - self.offset.y) * self.smoothing

    def get_offset(self) -> tuple:
        """Get camera offset as tuple"""
        return (int(self.offset.x), int(self.offset.y))

    def apply(self, entity_pos: pygame.Vector2) -> pygame.Vector2:
        """Apply camera offset to a position"""
        return pygame.Vector2(
            entity_pos.x - self.offset.x,
            entity_pos.y - self.offset.y
        )

    def world_to_screen(self, world_pos: pygame.Vector2) -> pygame.Vector2:
        """Convert world position to screen position"""
        return self.apply(world_pos)

    def screen_to_world(self, screen_pos: pygame.Vector2) -> pygame.Vector2:
        """Convert screen position to world position"""
        return pygame.Vector2(
            screen_pos.x + self.offset.x,
            screen_pos.y + self.offset.y
        )
