"""
Sprite loading system with placeholder support for The Hollow Path.
Creates colored rectangles when sprite files don't exist.
"""
import pygame
from typing import Tuple, Optional

PLACEHOLDER_COLORS = {
    "player": (100, 150, 255),
    "shadow_self": (50, 50, 50),
    "gatekeeper": (150, 50, 50),
    "echo": (255, 100, 255),
    "spiral": (200, 50, 200),
    "amalgamation": (100, 0, 100),
    "companion": (255, 200, 100),
    "platform": (100, 100, 100),
    "background": (30, 30, 40),
    "save_point": (100, 255, 100),
    "ability_pickup": (255, 255, 100),
    "npc": (200, 200, 150),
    "door": (150, 100, 50),
    "projectile": (255, 255, 0),
    "effect": (255, 200, 200)
}


def create_placeholder_sprite(entity_type: str, width: int, height: int,
                              outline: bool = True) -> pygame.Surface:
    """
    Create a colored rectangle as a placeholder sprite.

    Args:
        entity_type: Type of entity (determines color)
        width: Width in pixels
        height: Height in pixels
        outline: Whether to draw a border

    Returns:
        pygame.Surface with the placeholder sprite
    """
    surface = pygame.Surface((width, height))
    color = PLACEHOLDER_COLORS.get(entity_type, (255, 0, 255))  # Magenta for unknown
    surface.fill(color)

    if outline:
        outline_color = tuple(max(0, c - 50) for c in color)
        pygame.draw.rect(surface, outline_color, surface.get_rect(), 2)

    return surface


def load_sprite(path: str, fallback_type: str, width: int, height: int,
                colorkey: Optional[Tuple[int, int, int]] = None) -> pygame.Surface:
    """
    Load a sprite from file, or create placeholder if file doesn't exist.

    Args:
        path: Path to sprite file
        fallback_type: Entity type for placeholder
        width: Width for placeholder
        height: Height for placeholder
        colorkey: Optional transparent color

    Returns:
        pygame.Surface with the sprite
    """
    try:
        sprite = pygame.image.load(path).convert()
        if colorkey:
            sprite.set_colorkey(colorkey)
        return sprite
    except (pygame.error, FileNotFoundError):
        print(f"Warning: Could not load {path}, using placeholder")
        return create_placeholder_sprite(fallback_type, width, height)


def create_animation_frames(entity_type: str, width: int, height: int,
                            frame_count: int) -> list:
    """
    Create placeholder animation frames.

    Args:
        entity_type: Type of entity
        width: Frame width
        height: Frame height
        frame_count: Number of frames

    Returns:
        List of pygame.Surface frames
    """
    frames = []
    base_color = PLACEHOLDER_COLORS.get(entity_type, (255, 0, 255))

    for i in range(frame_count):
        surface = pygame.Surface((width, height))
        # Slightly vary the color for each frame to show animation
        variation = 20 * (i % 2)
        color = tuple(min(255, c + variation) for c in base_color)
        surface.fill(color)
        pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), 2)
        frames.append(surface)

    return frames
