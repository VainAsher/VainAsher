"""
Input controls configuration for The Hollow Path.
"""
import pygame

CONTROLS = {
    # Movement
    "move_left": pygame.K_a,
    "move_right": pygame.K_d,
    "jump": pygame.K_SPACE,
    "crouch": pygame.K_s,
    "dash": pygame.K_LSHIFT,

    # Advanced Movement
    "shadow_dash": pygame.K_q,
    "grapple": pygame.K_e,

    # Combat
    "attack": "MOUSE_LEFT",
    "shuriken": "MOUSE_RIGHT",

    # Companion
    "call_companion": pygame.K_c,

    # Consumables
    "consumable_1": pygame.K_1,
    "consumable_2": pygame.K_2,
    "consumable_3": pygame.K_3,
    "consumable_4": pygame.K_4,
    "radial_menu": pygame.K_TAB,

    # Menus
    "memories": pygame.K_i,
    "journey": pygame.K_m,
    "growth": pygame.K_g,
    "pause": pygame.K_ESCAPE,

    # Menu Navigation
    "menu_up": pygame.K_w,
    "menu_down": pygame.K_s,
    "menu_left": pygame.K_a,
    "menu_right": pygame.K_d,
    "menu_confirm": pygame.K_RETURN,
    "menu_cancel": pygame.K_ESCAPE,

    # Debug
    "debug_hitboxes": pygame.K_F1,
    "debug_fps": pygame.K_F2,
    "debug_godmode": pygame.K_F3,
    "debug_noclip": pygame.K_F4,
    "debug_spawn_enemy": pygame.K_F5,
    "debug_unlock_all": pygame.K_F6,
    "debug_teleport": pygame.K_F7,
    "debug_reload": pygame.K_F8
}
