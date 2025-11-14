"""
Tilemap system for The Hollow Path.
Handles tile-based world rendering and collision.
"""
import pygame
from config.settings import TILE_SIZE
from typing import List, Tuple


class Tile:
    """Individual tile"""

    def __init__(self, tile_type: str, x: int, y: int):
        self.tile_type = tile_type
        self.x = x
        self.y = y
        self.solid = tile_type in ["platform", "wall"]
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def get_color(self):
        """Get tile color based on type"""
        colors = {
            "platform": (100, 100, 100),
            "wall": (80, 80, 80),
            "background": (40, 40, 50),
            "spike": (200, 50, 50),
            "save_point": (100, 255, 100)
        }
        return colors.get(self.tile_type, (255, 0, 255))


class Tilemap:
    """2D tilemap grid"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.tiles = {}  # Dict of (x, y) -> Tile
        self.solid_tiles = []

    def set_tile(self, x: int, y: int, tile_type: str):
        """Set a tile at grid position"""
        tile = Tile(tile_type, x, y)
        self.tiles[(x, y)] = tile
        if tile.solid:
            self.solid_tiles.append(tile.rect)

    def get_tile(self, x: int, y: int):
        """Get tile at grid position"""
        return self.tiles.get((x, y))

    def remove_tile(self, x: int, y: int):
        """Remove tile at grid position"""
        if (x, y) in self.tiles:
            tile = self.tiles[(x, y)]
            if tile.rect in self.solid_tiles:
                self.solid_tiles.remove(tile.rect)
            del self.tiles[(x, y)]

    def get_tiles_in_rect(self, rect: pygame.Rect) -> List[Tile]:
        """Get all tiles that intersect with a rectangle"""
        # Convert rect to tile coordinates
        start_x = max(0, rect.left // TILE_SIZE)
        end_x = min(self.width, (rect.right // TILE_SIZE) + 1)
        start_y = max(0, rect.top // TILE_SIZE)
        end_y = min(self.height, (rect.bottom // TILE_SIZE) + 1)

        tiles = []
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                if (x, y) in self.tiles:
                    tiles.append(self.tiles[(x, y)])

        return tiles

    def get_collision_rects(self, rect: pygame.Rect) -> List[pygame.Rect]:
        """Get collision rectangles near an entity"""
        tiles = self.get_tiles_in_rect(rect)
        return [tile.rect for tile in tiles if tile.solid]

    def render(self, surface: pygame.Surface, camera_offset: Tuple[int, int] = (0, 0)):
        """Render visible tiles"""
        # Calculate visible tile range
        screen_rect = pygame.Rect(
            camera_offset[0],
            camera_offset[1],
            surface.get_width(),
            surface.get_height()
        )

        # Get visible tiles
        visible_tiles = self.get_tiles_in_rect(screen_rect)

        # Draw tiles
        for tile in visible_tiles:
            draw_rect = tile.rect.copy()
            draw_rect.x -= camera_offset[0]
            draw_rect.y -= camera_offset[1]
            pygame.draw.rect(surface, tile.get_color(), draw_rect)
            # Draw border for solid tiles
            if tile.solid:
                pygame.draw.rect(surface, (150, 150, 150), draw_rect, 1)


def create_test_level() -> Tilemap:
    """Create a simple test level"""
    tilemap = Tilemap(100, 50)

    # Ground
    for x in range(100):
        tilemap.set_tile(x, 15, "platform")

    # Platforms
    for x in range(10, 20):
        tilemap.set_tile(x, 12, "platform")

    for x in range(25, 35):
        tilemap.set_tile(x, 10, "platform")

    for x in range(40, 50):
        tilemap.set_tile(x, 8, "platform")

    # Walls
    for y in range(10, 16):
        tilemap.set_tile(0, y, "wall")
        tilemap.set_tile(99, y, "wall")

    return tilemap
