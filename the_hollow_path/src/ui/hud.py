"""
HUD (Heads-Up Display) for The Hollow Path.
Shows player health, energy, and consumable slots.
"""
import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class HUD:
    """Heads-up display"""

    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

    def render(self, surface: pygame.Surface, player):
        """Draw HUD elements"""
        # Will (Health) bar
        self.draw_bar(
            surface,
            pos=(20, 20),
            current=player.will,
            maximum=player.max_will,
            color=(200, 50, 50),
            label="Will"
        )

        # Strength (Energy) bar
        self.draw_bar(
            surface,
            pos=(20, 50),
            current=player.strength,
            maximum=player.max_strength,
            color=(50, 150, 200),
            label="Strength"
        )

        # Consumable quick slots
        self.draw_consumable_slots(surface, player)

        # Currency (Hope Fragments)
        self.draw_currency(surface, player.currency)

        # Current region
        self.draw_region_name(surface, player.current_region)

    def draw_bar(self, surface: pygame.Surface, pos: tuple, current: float,
                maximum: float, color: tuple, label: str):
        """Draw a stat bar"""
        bar_width = 200
        bar_height = 20
        fill_width = int((current / maximum) * bar_width) if maximum > 0 else 0

        # Background
        pygame.draw.rect(surface, (30, 30, 40),
                        (pos[0], pos[1], bar_width, bar_height))

        # Fill
        if fill_width > 0:
            pygame.draw.rect(surface, color,
                            (pos[0], pos[1], fill_width, bar_height))

        # Border
        pygame.draw.rect(surface, (255, 255, 255),
                        (pos[0], pos[1], bar_width, bar_height), 2)

        # Label
        text = self.font.render(f"{label}: {int(current)}/{int(maximum)}",
                              True, (255, 255, 255))
        surface.blit(text, (pos[0], pos[1] - 22))

    def draw_consumable_slots(self, surface: pygame.Surface, player):
        """Draw quick-use consumable slots (1-4 keys)"""
        slot_size = 50
        spacing = 10
        start_x = SCREEN_WIDTH - (4 * (slot_size + spacing)) - 20
        start_y = SCREEN_HEIGHT - slot_size - 20

        for i in range(1, 5):
            x = start_x + (i - 1) * (slot_size + spacing)
            y = start_y

            slot_name = f"slot_{i}"
            item = player.consumables.get(slot_name)

            # Slot background
            color = (60, 60, 70) if item else (30, 30, 40)
            pygame.draw.rect(surface, color,
                           (x, y, slot_size, slot_size))
            pygame.draw.rect(surface, (255, 255, 255),
                           (x, y, slot_size, slot_size), 2)

            # Number label
            text = self.small_font.render(str(i), True, (255, 255, 255))
            surface.blit(text, (x + 5, y + 5))

            # Item name (if present)
            if item:
                item_text = self.small_font.render(item[:8], True, (200, 200, 200))
                surface.blit(item_text, (x + 5, y + 25))

    def draw_currency(self, surface: pygame.Surface, amount: int):
        """Draw hope fragments count"""
        text = self.font.render(f"Hope Fragments: {amount}",
                              True, (255, 255, 100))
        surface.blit(text, (20, 90))

    def draw_region_name(self, surface: pygame.Surface, region: str):
        """Draw current region name"""
        # Format region name
        formatted = region.replace("_", " ").title()
        text = self.font.render(formatted, True, (200, 200, 200))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        surface.blit(text, text_rect)
