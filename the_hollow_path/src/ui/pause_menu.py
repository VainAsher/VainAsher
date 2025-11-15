"""
Pause menu for The Hollow Path.
Shows when game is paused with resume/options/help/quit.
"""
import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class PauseMenu:
    """Pause menu with multiple options"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 28)
        self.selected = 0
        self.options = ["Resume", "Controls", "Options", "Quit to Menu"]

    def run(self) -> str:
        """
        Show pause menu and wait for user choice.

        Returns:
            str: "resume", "controls", "options", or "quit"
        """
        clock = pygame.time.Clock()

        running = True
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        choice = self.options[self.selected].lower().replace(" ", "_")
                        if "resume" in choice:
                            return "resume"
                        elif "controls" in choice:
                            return "controls"
                        elif "options" in choice:
                            return "options"
                        elif "quit" in choice:
                            return "quit"
                    elif event.key == pygame.K_ESCAPE:
                        return "resume"

            self.render()

        return "resume"

    def render(self):
        """Render pause menu"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Pause title
        title = self.font_large.render("PAUSED", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        # Menu options
        y = 280
        for i, option in enumerate(self.options):
            if i == self.selected:
                color = (255, 255, 100)
                prefix = "> "
            else:
                color = (200, 200, 200)
                prefix = "  "

            text = self.font_medium.render(prefix + option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, rect)
            y += 70

        # Controls hint
        hint = "Arrow Keys / WASD to navigate, Enter to select, ESC to resume"
        hint_text = self.font_small.render(hint, True, (150, 150, 150))
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint_text, hint_rect)

        pygame.display.flip()
