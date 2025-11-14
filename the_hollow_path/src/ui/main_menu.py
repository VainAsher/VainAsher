"""
Main menu for The Hollow Path.
Shows content warning and main menu options.
"""
import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from config.narrative_config import CONTENT_WARNING


class MainMenu:
    """Main menu screen"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.selected = 0
        self.options = ["New Game", "Continue", "Options", "Quit"]
        self.show_content_warning = True

    def run(self) -> str:
        """Run main menu loop, returns selected action"""
        clock = pygame.time.Clock()

        # First show content warning
        if self.show_content_warning:
            choice = self.show_warning()
            if choice == "exit":
                return "quit"

        # Then show main menu
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
                        option = self.options[self.selected].lower().replace(" ", "_")
                        if option == "quit":
                            return "quit"
                        elif option == "new_game":
                            return "new_game"
                        elif option == "continue":
                            return "continue"
                        elif option == "options":
                            # TODO: Show options menu
                            pass

            self.render()
            pygame.display.flip()

        return "quit"

    def show_warning(self) -> str:
        """Show content warning screen"""
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "continue"
                    elif event.key == pygame.K_ESCAPE:
                        return "exit"

            # Render warning
            self.screen.fill((20, 20, 30))

            # Split warning text into lines
            lines = CONTENT_WARNING.strip().split('\n')
            y = 100

            for line in lines:
                if line.startswith("⚠️"):
                    text = self.font.render(line, True, (255, 200, 50))
                elif line.startswith("-"):
                    text = self.small_font.render(line, True, (200, 200, 200))
                elif "988" in line or "741741" in line:
                    text = self.small_font.render(line, True, (100, 255, 100))
                elif line.strip():
                    text = self.small_font.render(line, True, (255, 255, 255))
                else:
                    text = self.small_font.render(line, True, (255, 255, 255))

                rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
                self.screen.blit(text, rect)
                y += 30

            pygame.display.flip()

        return "exit"

    def render(self):
        """Render main menu"""
        self.screen.fill((20, 20, 30))

        # Title
        title = self.font.render("THE HOLLOW PATH", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        # Subtitle
        subtitle = self.small_font.render(
            "A journey from darkness to light",
            True, (200, 200, 200)
        )
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 190))
        self.screen.blit(subtitle, subtitle_rect)

        # Menu options
        y = 300
        for i, option in enumerate(self.options):
            if i == self.selected:
                color = (255, 255, 100)
                prefix = "> "
            else:
                color = (200, 200, 200)
                prefix = "  "

            text = self.font.render(prefix + option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            self.screen.blit(text, rect)
            y += 50
