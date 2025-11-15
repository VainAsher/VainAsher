"""
Options menu for The Hollow Path.
Allows adjusting audio, display, player mechanics, and difficulty settings.
"""
import pygame
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT
import config.runtime_settings as runtime


class OptionsMenu:
    """Comprehensive options menu for game settings"""

    def __init__(self, screen: pygame.Surface, audio_manager=None):
        self.screen = screen
        self.audio_manager = audio_manager
        self.font_title = pygame.font.Font(None, 52)
        self.font_category = pygame.font.Font(None, 42)
        self.font_option = pygame.font.Font(None, 32)
        self.font_text = pygame.font.Font(None, 24)
        self.selected = 0

        # Load current settings from runtime_settings
        self.music_volume = runtime.music_volume
        self.sfx_volume = runtime.sfx_volume
        self.fullscreen = runtime.fullscreen

        # Current category
        self.category = 0  # 0 = Audio/Display, 1 = Player Mechanics, 2 = Difficulty
        self.categories = ["Audio & Display", "Player Mechanics", "Difficulty"]

        # Define options for each category
        self.options_by_category = {
            0: [  # Audio & Display
                "Music Volume",
                "SFX Volume",
                "Fullscreen",
                "Next Category",
            ],
            1: [  # Player Mechanics
                "Player Speed",
                "Jump Height",
                "Dash Speed",
                "Shadow Dash Speed",
                "Dash Duration",
                "Shadow Dash Duration",
                "Reset to Defaults",
                "Next Category",
            ],
            2: [  # Difficulty
                "Difficulty Level",
                "Reset All Settings",
                "Back to Menu",
            ]
        }

    def get_current_options(self):
        """Get options for current category"""
        return self.options_by_category[self.category]

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
                    options = self.get_current_options()

                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected = (self.selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected = (self.selected + 1) % len(options)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.adjust_setting(-1):
                            settings_changed = True
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if self.adjust_setting(1):
                            settings_changed = True
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.handle_enter():
                            settings_changed = True
                            # Check if user wants to exit
                            if self.category == 2 and self.selected == len(options) - 1:
                                running = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            self.render()

        # Save settings to runtime_settings
        self.save_settings()

        return settings_changed

    def adjust_setting(self, direction: int) -> bool:
        """
        Adjust the selected setting.

        Args:
            direction: -1 for decrease, 1 for increase

        Returns:
            bool: True if setting was changed
        """
        options = self.get_current_options()
        option = options[self.selected]

        # Audio & Display Category
        if self.category == 0:
            if option == "Music Volume":
                self.music_volume = max(0.0, min(1.0, self.music_volume + direction * 0.1))
                if self.audio_manager:
                    self.audio_manager.set_music_volume(self.music_volume)
                return True
            elif option == "SFX Volume":
                self.sfx_volume = max(0.0, min(1.0, self.sfx_volume + direction * 0.1))
                if self.audio_manager:
                    self.audio_manager.set_sfx_volume(self.sfx_volume)
                return True
            elif option == "Fullscreen":
                if direction != 0:
                    self.fullscreen = not self.fullscreen
                    return True

        # Player Mechanics Category
        elif self.category == 1:
            if option == "Player Speed":
                runtime.player_speed_multiplier = max(0.5, min(2.0,
                    runtime.player_speed_multiplier + direction * 0.1))
                return True
            elif option == "Jump Height":
                runtime.jump_force_multiplier = max(0.5, min(2.0,
                    runtime.jump_force_multiplier + direction * 0.1))
                return True
            elif option == "Dash Speed":
                runtime.dash_speed_multiplier = max(0.5, min(3.0,
                    runtime.dash_speed_multiplier + direction * 0.1))
                return True
            elif option == "Shadow Dash Speed":
                runtime.shadow_dash_speed_multiplier = max(0.5, min(3.0,
                    runtime.shadow_dash_speed_multiplier + direction * 0.1))
                return True
            elif option == "Dash Duration":
                runtime.dash_duration_multiplier = max(0.5, min(3.0,
                    runtime.dash_duration_multiplier + direction * 0.1))
                return True
            elif option == "Shadow Dash Duration":
                runtime.shadow_dash_duration_multiplier = max(0.5, min(3.0,
                    runtime.shadow_dash_duration_multiplier + direction * 0.1))
                return True

        # Difficulty Category
        elif self.category == 2:
            if option == "Difficulty Level":
                runtime.difficulty_multiplier = max(0.5, min(2.0,
                    runtime.difficulty_multiplier + direction * 0.25))
                return True

        return False

    def handle_enter(self) -> bool:
        """Handle enter key press on current option"""
        options = self.get_current_options()
        option = options[self.selected]

        # Navigation options
        if option == "Next Category":
            self.category = (self.category + 1) % len(self.categories)
            self.selected = 0
            return False
        elif option == "Back to Menu":
            return True

        # Action options
        elif option == "Reset to Defaults":
            runtime.reset_to_defaults()
            return True
        elif option == "Reset All Settings":
            runtime.reset_to_defaults()
            self.music_volume = 0.7
            self.sfx_volume = 0.8
            self.fullscreen = False
            if self.audio_manager:
                self.audio_manager.set_music_volume(self.music_volume)
                self.audio_manager.set_sfx_volume(self.sfx_volume)
            return True
        elif option == "Fullscreen":
            self.fullscreen = not self.fullscreen
            return True

        return False

    def save_settings(self):
        """Save current settings to runtime_settings"""
        runtime.music_volume = self.music_volume
        runtime.sfx_volume = self.sfx_volume
        runtime.fullscreen = self.fullscreen

    def render(self):
        """Render options menu"""
        self.screen.fill((20, 20, 30))

        # Title
        title = self.font_title.render("OPTIONS", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # Category
        category_text = self.font_category.render(
            self.categories[self.category], True, (150, 200, 255))
        category_rect = category_text.get_rect(center=(SCREEN_WIDTH // 2, 110))
        self.screen.blit(category_text, category_rect)

        # Options
        options = self.get_current_options()
        y = 170
        for i, option in enumerate(options):
            is_selected = i == self.selected

            # Option name
            color = (255, 255, 100) if is_selected else (200, 200, 200)
            prefix = "> " if is_selected else "  "
            text = self.font_option.render(prefix + option, True, color)
            self.screen.blit(text, (150, y))

            # Option value
            self.render_option_value(option, 650, y, color, is_selected)

            y += 55

        # Controls hint
        hints = [
            "Arrow Keys / WASD: Navigate",
            "Left/Right: Adjust Values",
            "Enter: Select/Toggle",
            "ESC: Back"
        ]
        hint_y = SCREEN_HEIGHT - 120
        for hint in hints:
            hint_text = self.font_text.render(hint, True, (150, 150, 150))
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, hint_y))
            self.screen.blit(hint_text, hint_rect)
            hint_y += 25

        pygame.display.flip()

    def render_option_value(self, option: str, x: int, y: int, color: tuple, selected: bool):
        """Render the value for a specific option"""
        # Audio & Display
        if option == "Music Volume":
            self.draw_slider(x, y + 5, self.music_volume, selected)
            value_text = f"{int(self.music_volume * 100)}%"
            value = self.font_text.render(value_text, True, color)
            self.screen.blit(value, (x + 200, y + 5))

        elif option == "SFX Volume":
            self.draw_slider(x, y + 5, self.sfx_volume, selected)
            value_text = f"{int(self.sfx_volume * 100)}%"
            value = self.font_text.render(value_text, True, color)
            self.screen.blit(value, (x + 200, y + 5))

        elif option == "Fullscreen":
            value_text = "ON" if self.fullscreen else "OFF"
            value = self.font_text.render(value_text, True, color)
            self.screen.blit(value, (x, y + 5))

        # Player Mechanics
        elif option == "Player Speed":
            self.draw_slider(x, y + 5, (runtime.player_speed_multiplier - 0.5) / 1.5, selected)
            value_text = f"{runtime.player_speed_multiplier:.1f}x"
            value = self.font_text.render(value_text, True, color)
            self.screen.blit(value, (x + 200, y + 5))

        elif option == "Jump Height":
            self.draw_slider(x, y + 5, (runtime.jump_force_multiplier - 0.5) / 1.5, selected)
            value_text = f"{runtime.jump_force_multiplier:.1f}x"
            value = self.font_text.render(value_text, True, color)
            self.screen.blit(value, (x + 200, y + 5))

        elif option == "Dash Speed":
            self.draw_slider(x, y + 5, (runtime.dash_speed_multiplier - 0.5) / 2.5, selected)
            value_text = f"{runtime.dash_speed_multiplier:.1f}x"
            value = self.font_text.render(value_text, True, color)
            self.screen.blit(value, (x + 200, y + 5))

        elif option == "Shadow Dash Speed":
            self.draw_slider(x, y + 5, (runtime.shadow_dash_speed_multiplier - 0.5) / 2.5, selected)
            value_text = f"{runtime.shadow_dash_speed_multiplier:.1f}x"
            value = self.font_text.render(value_text, True, color)
            self.screen.blit(value, (x + 200, y + 5))

        elif option == "Dash Duration":
            self.draw_slider(x, y + 5, (runtime.dash_duration_multiplier - 0.5) / 2.5, selected)
            value_text = f"{runtime.dash_duration_multiplier:.1f}x"
            value = self.font_text.render(value_text, True, color)
            self.screen.blit(value, (x + 200, y + 5))

        elif option == "Shadow Dash Duration":
            self.draw_slider(x, y + 5, (runtime.shadow_dash_duration_multiplier - 0.5) / 2.5, selected)
            value_text = f"{runtime.shadow_dash_duration_multiplier:.1f}x"
            value = self.font_text.render(value_text, True, color)
            self.screen.blit(value, (x + 200, y + 5))

        # Difficulty
        elif option == "Difficulty Level":
            difficulty_value = (runtime.difficulty_multiplier - 0.5) / 1.5
            self.draw_slider(x, y + 5, difficulty_value, selected)

            # Difficulty label
            if runtime.difficulty_multiplier <= 0.75:
                diff_label = "Easy"
            elif runtime.difficulty_multiplier <= 1.25:
                diff_label = "Normal"
            elif runtime.difficulty_multiplier <= 1.75:
                diff_label = "Hard"
            else:
                diff_label = "Very Hard"

            value_text = f"{diff_label} ({runtime.difficulty_multiplier:.2f}x)"
            value = self.font_text.render(value_text, True, color)
            self.screen.blit(value, (x + 200, y + 5))

    def draw_slider(self, x: int, y: int, value: float, selected: bool):
        """Draw a slider bar for value control"""
        slider_width = 150
        slider_height = 20

        # Background
        pygame.draw.rect(self.screen, (60, 60, 70), (x, y, slider_width, slider_height))

        # Fill
        fill_width = int(slider_width * max(0, min(1, value)))
        color = (255, 255, 100) if selected else (100, 150, 255)
        pygame.draw.rect(self.screen, color, (x, y, fill_width, slider_height))

        # Border
        border_color = (255, 255, 255) if selected else (150, 150, 150)
        pygame.draw.rect(self.screen, border_color, (x, y, slider_width, slider_height), 2)
