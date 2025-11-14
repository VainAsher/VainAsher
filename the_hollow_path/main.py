#!/usr/bin/env python3
"""
The Hollow Path
A Metroidvania platformer about struggle, recovery, and hope.

Author: Created for a personal journey
License: MIT
"""

import pygame
import sys
from config import settings
from src.ui.main_menu import MainMenu
from src.game import Game


def main():
    """Entry point for The Hollow Path"""
    # Initialize Pygame
    pygame.init()

    # Create display
    if settings.FULLSCREEN:
        screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT),
            pygame.FULLSCREEN
        )
    else:
        screen = pygame.display.set_mode(
            (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        )

    pygame.display.set_caption("The Hollow Path")

    # Initialize font system
    pygame.font.init()

    # Show main menu
    main_menu = MainMenu(screen)
    choice = main_menu.run()

    # Handle menu choice
    if choice == "new_game":
        game = Game(screen, new_game=True)
        game.run()

    elif choice == "continue":
        # Try to load slot 0
        game = Game(screen, new_game=False, load_slot=0)
        game.run()

    elif choice == "quit":
        pygame.quit()
        sys.exit(0)

    # Cleanup
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
