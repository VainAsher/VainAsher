"""
Death screen for The Hollow Path.
Shows when player dies with restart/quit options.
"""
import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class DeathScreen:
    """Death screen with restart/quit options"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.selected = 0
        self.options = ["Restart from Last Save", "Return to Main Menu"]
        self.fade_alpha = 0
        self.fade_speed = 200  # Alpha units per second

    def run(self, deaths: int = 0) -> str:
        """
        Show death screen and wait for user choice.

        Args:
            deaths: Total death count

        Returns:
            str: "restart" or "quit"
        """
        clock = pygame.time.Clock()
        self.fade_alpha = 0

        running = True
        while running:
            dt = clock.tick(60) / 1000.0

            # Fade in
            if self.fade_alpha < 255:
                self.fade_alpha = min(255, self.fade_alpha + self.fade_speed * dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.selected == 0:
                            return "restart"
                        else:
                            return "quit"
                    elif event.key == pygame.K_ESCAPE:
                        return "quit"

            self.render(deaths)

        return "quit"

    def render(self, deaths: int):
        """Render death screen"""
        # Semi-transparent dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((10, 10, 15))
        overlay.set_alpha(int(self.fade_alpha * 0.85))
        self.screen.blit(overlay, (0, 0))

        # Death message
        death_text = self.font_large.render("YOU FELL", True, (200, 50, 50))
        death_rect = death_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(death_text, death_rect)

        # Thematic message
        quote = "Even in darkness, you can rise again."
        quote_text = self.font_small.render(quote, True, (150, 150, 150))
        quote_rect = quote_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(quote_text, quote_rect)

        # Death count
        if deaths > 0:
            count_text = self.font_small.render(f"Deaths: {deaths}", True, (100, 100, 100))
            count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, 270))
            self.screen.blit(count_text, count_rect)

        # Options
        y = 350
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
        hint = "Arrow Keys / WASD to navigate, Enter to select"
        hint_text = self.font_small.render(hint, True, (120, 120, 120))
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint_text, hint_rect)

        pygame.display.flip()
