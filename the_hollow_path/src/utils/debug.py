"""
Debug utilities for The Hollow Path.
"""
import pygame
from typing import Optional


class Debug:
    """Debug mode controller and display"""

    def __init__(self):
        self.enabled = False
        self.show_hitboxes = False
        self.show_fps = False
        self.godmode = False
        self.noclip = False
        self.font = None

    def init_font(self):
        """Initialize debug font"""
        if not self.font:
            self.font = pygame.font.Font(None, 24)

    def toggle_hitboxes(self):
        """Toggle hitbox display"""
        self.show_hitboxes = not self.show_hitboxes
        print(f"Hitboxes: {'ON' if self.show_hitboxes else 'OFF'}")

    def toggle_fps(self):
        """Toggle FPS display"""
        self.show_fps = not self.show_fps
        print(f"FPS Display: {'ON' if self.show_fps else 'OFF'}")

    def toggle_godmode(self):
        """Toggle god mode"""
        self.godmode = not self.godmode
        print(f"God Mode: {'ON' if self.godmode else 'OFF'}")

    def toggle_noclip(self):
        """Toggle no-clip mode"""
        self.noclip = not self.noclip
        print(f"No-Clip: {'ON' if self.noclip else 'OFF'}")

    def draw_hitbox(self, surface: pygame.Surface, rect: pygame.Rect,
                   color: tuple = (255, 0, 0), camera_offset: Optional[tuple] = None):
        """Draw a hitbox rectangle"""
        if not self.show_hitboxes:
            return

        draw_rect = rect.copy()
        if camera_offset:
            draw_rect.x -= camera_offset[0]
            draw_rect.y -= camera_offset[1]

        pygame.draw.rect(surface, color, draw_rect, 2)

    def draw_fps(self, surface: pygame.Surface, clock: pygame.time.Clock):
        """Draw FPS counter"""
        if not self.show_fps:
            return

        self.init_font()
        fps = int(clock.get_fps())
        text = self.font.render(f"FPS: {fps}", True, (255, 255, 0))
        surface.blit(text, (10, 10))

    def draw_debug_info(self, surface: pygame.Surface, player, world=None):
        """Draw comprehensive debug info"""
        if not self.enabled:
            return

        self.init_font()
        y = 40
        spacing = 25

        debug_lines = [
            f"Pos: ({int(player.pos.x)}, {int(player.pos.y)})",
            f"Vel: ({player.velocity.x:.1f}, {player.velocity.y:.1f})",
            f"State: {player.state}",
            f"On Ground: {player.on_ground}",
            f"Will: {player.will}/{player.max_will}",
            f"Strength: {player.strength}/{player.max_strength}",
        ]

        if self.godmode:
            debug_lines.append("GOD MODE")
        if self.noclip:
            debug_lines.append("NO-CLIP")

        for line in debug_lines:
            text = self.font.render(line, True, (255, 255, 0))
            surface.blit(text, (10, y))
            y += spacing


# Global debug instance
debug = Debug()
