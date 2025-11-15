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
    """
    Create a comprehensive test level showcasing all abilities and mechanics.

    Layout (left to right):
    - Spawn area
    - Jump/Double Jump challenge
    - Wall Climb section
    - Dash obstacle course
    - Shadow Dash phase test
    - Grapple hook area
    - Down Smash section
    - Crouch tunnel
    - Combat arena
    - Save point area
    """
    tilemap = Tilemap(150, 30)

    # === GROUND LAYER (y=22) ===
    for x in range(150):
        tilemap.set_tile(x, 22, "platform")

    # === BOUNDARY WALLS ===
    for y in range(0, 23):
        tilemap.set_tile(0, y, "wall")
        tilemap.set_tile(149, y, "wall")

    # === SECTION 1: SPAWN & BASIC JUMP (x: 5-20) ===
    # Starting platform (player spawns at 640, 400 = tile 20, 12.5)
    for x in range(5, 15):
        tilemap.set_tile(x, 18, "platform")

    # Jump test platforms
    for x in range(18, 23):
        tilemap.set_tile(x, 16, "platform")

    for x in range(26, 31):
        tilemap.set_tile(x, 14, "platform")

    # === SECTION 2: DOUBLE JUMP TEST (x: 32-45) ===
    # High platform requiring double jump
    for x in range(35, 40):
        tilemap.set_tile(x, 11, "platform")

    # Very high platform (definitely needs double jump)
    for x in range(42, 47):
        tilemap.set_tile(x, 8, "platform")

    # === SECTION 3: WALL CLIMB (x: 48-60) ===
    # Tall wall
    for y in range(10, 22):
        tilemap.set_tile(50, y, "wall")
        tilemap.set_tile(51, y, "wall")

    # Platform at top of wall
    for x in range(52, 58):
        tilemap.set_tile(x, 9, "platform")

    # Wall jump practice (narrow shaft)
    for y in range(12, 22):
        tilemap.set_tile(60, y, "wall")
        tilemap.set_tile(64, y, "wall")

    # === SECTION 4: DASH COURSE (x: 66-80) ===
    # Gap requiring dash to cross
    for x in range(66, 70):
        tilemap.set_tile(x, 18, "platform")
    # Gap of 5 tiles
    for x in range(75, 80):
        tilemap.set_tile(x, 18, "platform")

    # Spike pit (visual indicator for gap)
    for x in range(70, 75):
        tilemap.set_tile(x, 21, "spike")

    # === SECTION 5: SHADOW DASH / PHASE (x: 82-95) ===
    # Solid barrier that blocks normal movement
    for y in range(15, 23):
        tilemap.set_tile(87, y, "wall")
        tilemap.set_tile(88, y, "wall")
        tilemap.set_tile(89, y, "wall")

    # Platforms on both sides
    for x in range(82, 87):
        tilemap.set_tile(x, 18, "platform")

    for x in range(90, 95):
        tilemap.set_tile(x, 18, "platform")

    # === SECTION 6: GRAPPLE POINTS (x: 96-110) ===
    # Platform with gap
    for x in range(96, 100):
        tilemap.set_tile(x, 18, "platform")

    # Grapple anchor point (single block high up)
    tilemap.set_tile(105, 10, "platform")

    # Landing platform
    for x in range(108, 113):
        tilemap.set_tile(x, 18, "platform")

    # === SECTION 7: DOWN SMASH TEST (x: 114-125) ===
    # High platform
    for x in range(114, 119):
        tilemap.set_tile(x, 10, "platform")

    # Breakable blocks below (visual indicator)
    for x in range(115, 118):
        tilemap.set_tile(x, 20, "platform")

    # Landing area
    for x in range(114, 125):
        tilemap.set_tile(x, 21, "platform")

    # === SECTION 8: CROUCH TUNNEL (x: 126-138) ===
    # Low ceiling tunnel
    for x in range(126, 138):
        tilemap.set_tile(x, 18, "platform")  # Floor
        tilemap.set_tile(x, 16, "wall")       # Low ceiling (2 tiles high)

    # === SECTION 9: COMBAT ARENA (x: 139-148) ===
    # Large open arena
    for x in range(139, 148):
        tilemap.set_tile(x, 20, "platform")

    # Some cover obstacles
    for y in range(18, 20):
        tilemap.set_tile(142, y, "wall")
        tilemap.set_tile(145, y, "wall")

    # === SAVE POINT MARKERS ===
    tilemap.set_tile(10, 17, "save_point")
    tilemap.set_tile(70, 17, "save_point")
    tilemap.set_tile(140, 19, "save_point")

    return tilemap
