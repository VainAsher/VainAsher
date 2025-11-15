"""
Options menu for The Hollow Path.
Allows adjusting volume and display settings.
"""
import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class OptionsMenu:
    """Options menu for game settings"""

    def __init__(self, screen: pygame.Surface, audio_manager=None):
        self.screen = screen
        self.audio_manager = audio_manager
        self.font_title = pygame.font.Font(None, 52)
        self.font_option = pygame.font.Font(None, 38)
        self.font_text = pygame.font.Font(None, 28)
        self.selected = 0

        # Settings
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.fullscreen = False

        # Load current settings from audio manager if available
        if audio_manager:
            self.music_volume = audio_manager.music_volume
            self.sfx_volume = audio_manager.sfx_volume

        self.options = [
            "Music Volume",
            "SFX Volume",
            "Fullscreen",
            "Back"
        ]

    def run(self) -> bool:
        """
        Show options menu and wait for user to finish.

        Returns:
            bool: True if settings were changed
        """
        clock = pygame.time.Clock()
        settings_changed = False

        running = True
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.adjust_setting(-1):
                            settings_changed = True
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if self.adjust_setting(1):
                            settings_changed = True
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.selected == len(self.options) - 1:  # Back
                            running = False
                        elif self.selected == 2:  # Fullscreen toggle
                            self.fullscreen = not self.fullscreen
                            settings_changed = True
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            self.render()

        return settings_changed

    def adjust_setting(self, direction: int) -> bool:
        """
        Adjust the selected setting.

        Args:
            direction: -1 for decrease, 1 for increase

        Returns:
            bool: True if setting was changed
        """
        if self.selected == 0:  # Music Volume
            self.music_volume = max(0.0, min(1.0, self.music_volume + direction * 0.1))
            if self.audio_manager:
                self.audio_manager.set_music_volume(self.music_volume)
            return True
        elif self.selected == 1:  # SFX Volume
            self.sfx_volume = max(0.0, min(1.0, self.sfx_volume + direction * 0.1))
            if self.audio_manager:
                self.audio_manager.set_sfx_volume(self.sfx_volume)
            return True
        elif self.selected == 2:  # Fullscreen
            if direction != 0:
                self.fullscreen = not self.fullscreen
                return True
        return False

    def render(self):
        """Render options menu"""
        self.screen.fill((20, 20, 30))

        # Title
        title = self.font_title.render("OPTIONS", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)

        # Options
        y = 200
        for i, option in enumerate(self.options):
            is_selected = i == self.selected

            # Option name
            color = (255, 255, 100) if is_selected else (200, 200, 200)
            prefix = "> " if is_selected else "  "
            text = self.font_option.render(prefix + option, True, color)
            self.screen.blit(text, (200, y))

            # Option value
            if i == 0:  # Music Volume
                value_text = f"{int(self.music_volume * 100)}%"
                self.draw_slider(700, y + 5, self.music_volume, is_selected)
                value = self.font_text.render(value_text, True, color)
                self.screen.blit(value, (900, y + 5))
            elif i == 1:  # SFX Volume
                value_text = f"{int(self.sfx_volume * 100)}%"
                self.draw_slider(700, y + 5, self.sfx_volume, is_selected)
                value = self.font_text.render(value_text, True, color)
                self.screen.blit(value, (900, y + 5))
            elif i == 2:  # Fullscreen
                value_text = "ON" if self.fullscreen else "OFF"
                value = self.font_text.render(value_text, True, color)
                self.screen.blit(value, (700, y + 5))

            y += 80

        # Controls hint
        hint = "Arrow Keys / WASD to navigate, Left/Right to adjust, Enter to confirm"
        hint_text = self.font_text.render(hint, True, (150, 150, 150))
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint_text, hint_rect)

        pygame.display.flip()

    def draw_slider(self, x: int, y: int, value: float, selected: bool):
        """Draw a slider bar for volume control"""
        slider_width = 150
        slider_height = 20

        # Background
        pygame.draw.rect(self.screen, (60, 60, 70), (x, y, slider_width, slider_height))

        # Fill
        fill_width = int(slider_width * value)
        color = (255, 255, 100) if selected else (100, 150, 255)
        pygame.draw.rect(self.screen, color, (x, y, fill_width, slider_height))

        # Border
        border_color = (255, 255, 255) if selected else (150, 150, 150)
        pygame.draw.rect(self.screen, border_color, (x, y, slider_width, slider_height), 2)
