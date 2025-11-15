"""
Help/Controls screen for The Hollow Path.
Shows all controls and gameplay tips.
"""
import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class HelpScreen:
    """Help screen showing controls and gameplay info"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 52)
        self.font_section = pygame.font.Font(None, 36)
        self.font_text = pygame.font.Font(None, 26)

    def run(self):
        """Show help screen until user presses escape"""
        clock = pygame.time.Clock()

        running = True
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        running = False

            self.render()

    def render(self):
        """Render help screen"""
        self.screen.fill((20, 20, 30))

        y = 30

        # Title
        title = self.font_title.render("CONTROLS & HELP", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, y))
        self.screen.blit(title, title_rect)
        y += 60

        # Movement section
        y = self.draw_section(y, "MOVEMENT", [
            "A / D - Move left / right",
            "SPACE - Jump (First Step ability)",
            "SPACE (in air) - Double Jump (when unlocked)",
            "S - Crouch / Slide",
        ])

        # Advanced Movement section
        y = self.draw_section(y, "ADVANCED MOVEMENT", [
            "SHIFT - Dash (when unlocked)",
            "Q - Shadow Dash / Phase (when unlocked)",
            "E - Grapple Hook (aim with mouse)",
            "S (in air) - Down Smash (when unlocked)",
            "Wall proximity - Wall Slide (when unlocked)",
        ])

        # Combat section
        y = self.draw_section(y, "COMBAT", [
            "LEFT CLICK - Sword attack",
            "RIGHT CLICK - Throw shuriken",
            "C - Call companion (when acquired)",
        ])

        # Other section
        y = self.draw_section(y, "OTHER", [
            "1 / 2 / 3 / 4 - Use consumable items",
            "ESC - Pause menu",
            "F6 - Unlock all abilities (debug)",
        ])

        # Footer
        footer = self.font_text.render("Press ESC or ENTER to return", True, (150, 150, 150))
        footer_rect = footer.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        self.screen.blit(footer, footer_rect)

        pygame.display.flip()

    def draw_section(self, y: int, title: str, lines: list) -> int:
        """
        Draw a section of help text.

        Args:
            y: Starting y position
            title: Section title
            lines: List of text lines

        Returns:
            int: New y position after section
        """
        # Section title
        section_title = self.font_section.render(title, True, (255, 255, 100))
        self.screen.blit(section_title, (40, y))
        y += 40

        # Lines
        for line in lines:
            text = self.font_text.render(line, True, (200, 200, 200))
            self.screen.blit(text, (60, y))
            y += 28

        y += 20  # Space between sections
        return y
