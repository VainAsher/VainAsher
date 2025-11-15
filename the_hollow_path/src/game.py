"""
Main game class for The Hollow Path.
Handles game loop, state management, and coordination of all systems.
"""
import pygame
from config import settings, controls
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.entities.companion import Companion
from src.world.tilemap import create_test_level
from src.systems.camera import Camera
from src.systems.audio import AudioManager
from src.ui.hud import HUD
from src.ui.death_screen import DeathScreen
from src.ui.pause_menu import PauseMenu
from src.ui.help_screen import HelpScreen
from src.ui.options_menu import OptionsMenu
from src.utils.debug import debug
from src.utils.save_system import SaveSystem
from src.components.combat import Projectile


class Game:
    """Main game controller"""

    def __init__(self, screen: pygame.Surface, new_game: bool = True, load_slot: int = None):
        self.screen = screen
        self.running = True
        self.paused = False
        self.clock = pygame.time.Clock()

        # Game state
        self.state = "playing"  # playing, paused, dead, help, options

        # Systems
        self.camera = Camera()
        self.hud = HUD()
        self.audio_manager = AudioManager()

        # UI Menus
        self.death_screen = DeathScreen(screen)
        self.pause_menu = PauseMenu(screen)
        self.help_screen = HelpScreen(screen)
        self.options_menu = OptionsMenu(screen, self.audio_manager)

        # Statistics
        self.deaths = 0

        # World
        self.tilemap = create_test_level()

        # Entities
        # Spawn player at start of test level (x=10 tiles * 32 = 320px, y=18 tiles * 32 = 576px)
        self.player = Player(320, 550)
        self.camera.set_target(self.player)
        self.enemies = []
        self.projectiles = []
        self.companion = None

        # Input state
        self.keys = {}
        self.mouse_pos = (0, 0)
        self.keys_pressed = set()

        # Load game if specified
        if load_slot is not None and not new_game:
            self.load_game(load_slot)
        elif new_game:
            self.start_new_game()

        # Spawn some test enemies
        self.spawn_test_enemies()

    def start_new_game(self):
        """Initialize a new game"""
        # Unlock first ability
        self.player.unlock_ability("first_step")
        # Could show intro cutscene here

    def spawn_test_enemies(self):
        """Spawn test enemies in different test sections"""
        # Section 1: Starting area - Shadow Self
        self.enemies.append(Enemy(400, 550, "shadow_self"))

        # Section 3: Wall climb area - Gatekeeper
        self.enemies.append(Enemy(1750, 280, "gatekeeper"))

        # Section 4: Dash course - Echo
        self.enemies.append(Enemy(2250, 550, "echo"))

        # Section 9: Combat arena - Multiple enemies
        self.enemies.append(Enemy(4500, 620, "shadow_self"))
        self.enemies.append(Enemy(4600, 620, "shadow_self"))
        self.enemies.append(Enemy(4550, 620, "gatekeeper"))

    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000.0  # Delta time in seconds

            self.handle_events()

            if not self.paused:
                self.update(dt)

            self.render()

    def handle_events(self):
        """Handle pygame events"""
        self.keys_pressed = set()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.keys[event.key] = True
                self.keys_pressed.add(event.key)

                # Pause
                if event.key == controls.CONTROLS["pause"]:
                    self.toggle_pause()

                # Debug controls
                if event.key == controls.CONTROLS["debug_hitboxes"]:
                    debug.toggle_hitboxes()
                elif event.key == controls.CONTROLS["debug_fps"]:
                    debug.toggle_fps()
                elif event.key == controls.CONTROLS["debug_godmode"]:
                    debug.toggle_godmode()
                elif event.key == controls.CONTROLS["debug_unlock_all"]:
                    self.debug_unlock_all_abilities()

            elif event.type == pygame.KEYUP:
                self.keys[event.key] = False

            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                # Convert to world coordinates
                world_pos = self.camera.screen_to_world(pygame.Vector2(*event.pos))
                self.mouse_pos = (world_pos.x, world_pos.y)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.keys["MOUSE_LEFT"] = True
                    self.keys_pressed.add("MOUSE_LEFT")
                elif event.button == 3:  # Right click
                    self.keys["MOUSE_RIGHT"] = True
                    self.keys_pressed.add("MOUSE_RIGHT")

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.keys["MOUSE_LEFT"] = False
                elif event.button == 3:
                    self.keys["MOUSE_RIGHT"] = False

    def get_inputs(self) -> dict:
        """Convert raw input to game inputs"""
        inputs = {}

        # Movement
        inputs["move_left"] = self.keys.get(controls.CONTROLS["move_left"], False)
        inputs["move_right"] = self.keys.get(controls.CONTROLS["move_right"], False)
        inputs["jump"] = self.keys.get(controls.CONTROLS["jump"], False)
        inputs["jump_pressed"] = controls.CONTROLS["jump"] in self.keys_pressed
        inputs["crouch"] = self.keys.get(controls.CONTROLS["crouch"], False)

        # Abilities
        inputs["dash_pressed"] = controls.CONTROLS["dash"] in self.keys_pressed
        inputs["shadow_dash_pressed"] = controls.CONTROLS["shadow_dash"] in self.keys_pressed
        inputs["grapple_pressed"] = controls.CONTROLS["grapple"] in self.keys_pressed

        # Combat
        inputs["attack_pressed"] = "MOUSE_LEFT" in self.keys_pressed
        inputs["shuriken_pressed"] = "MOUSE_RIGHT" in self.keys_pressed

        # Other
        inputs["mouse_pos"] = self.mouse_pos

        # Consumables
        for i in range(1, 5):
            key = controls.CONTROLS[f"consumable_{i}"]
            inputs[f"consumable_{i}"] = key in self.keys_pressed

        return inputs

    def update(self, dt: float):
        """Update game state"""
        inputs = self.get_inputs()

        # Update player
        self.player.update(dt, inputs, self.tilemap)

        # Update camera
        self.camera.update(dt)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(dt, self.player, self.tilemap)
            if enemy.dead:
                self.enemies.remove(enemy)

        # Update companion
        if self.companion:
            self.companion.update(dt)

        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update(dt)
            if not projectile.active:
                self.projectiles.remove(projectile)

        # Check combat collisions
        self.check_combat_collisions()

        # Check for pickups
        self.check_pickups()

        # Check for player death
        if self.player.state == "dead":
            self.handle_player_death()

        # God mode
        if debug.godmode:
            self.player.invulnerable = True
            self.player.will = self.player.max_will

    def check_combat_collisions(self):
        """Check for combat-related collisions"""
        # Player attacks hitting enemies
        if self.player.combat.attack_hitbox:
            for enemy in self.enemies:
                if enemy.hitbox.colliderect(self.player.combat.attack_hitbox):
                    damage = self.player.combat.get_melee_damage()
                    knockback_dir = (enemy.pos - self.player.pos).normalize()
                    knockback = knockback_dir * 5
                    enemy.take_damage(damage, knockback)
            self.player.combat.attack_hitbox = None

        # Projectiles hitting enemies
        for projectile in self.projectiles:
            if not projectile.active:
                continue
            for enemy in self.enemies:
                if enemy.hitbox.colliderect(projectile.hitbox):
                    enemy.take_damage(projectile.damage)
                    projectile.hit()

        # Enemies hitting player
        for enemy in self.enemies:
            if enemy.hitbox.colliderect(self.player.hitbox):
                if enemy.ai.state == "attack" and not self.player.invulnerable:
                    knockback_dir = (self.player.pos - enemy.pos).normalize()
                    knockback = knockback_dir * 5
                    self.player.take_damage(enemy.damage, knockback)

    def check_pickups(self):
        """Check for player collecting pickups (consumables, abilities, etc.)"""
        # Get tiles player is touching
        tiles = self.tilemap.get_tiles_in_rect(self.player.hitbox)

        for tile in tiles:
            if tile.tile_type == "consumable":
                # Add consumable to first empty slot
                for i in range(1, 5):
                    slot = f"slot_{i}"
                    if not self.player.consumables[slot]:
                        self.player.consumables[slot] = "Health Potion"
                        print(f"Collected Health Potion (Slot {i})")
                        # Remove tile
                        self.tilemap.remove_tile(tile.x, tile.y)
                        break

            elif tile.tile_type == "ability_pickup":
                # Unlock all abilities for testing (in real game, would unlock specific ones)
                abilities_to_unlock = ["first_step", "wall_climb", "double_jump",
                                      "dash", "shadow_dash", "grapple", "down_smash"]
                for ability in abilities_to_unlock:
                    if not self.player.abilities[ability]:
                        self.player.unlock_ability(ability)
                        print(f"Ability unlocked: {ability}")
                        # Remove tile
                        self.tilemap.remove_tile(tile.x, tile.y)
                        return  # Only unlock one set per pickup

    def handle_player_death(self):
        """Handle player death - show death screen and handle restart"""
        self.deaths += 1
        self.state = "dead"

        # Show death screen
        choice = self.death_screen.run(self.deaths)

        if choice == "restart":
            # Respawn player at starting position
            self.player.pos = pygame.Vector2(320, 550)
            self.player.velocity = pygame.Vector2(0, 0)
            self.player.will = self.player.max_will
            self.player.strength = self.player.max_strength
            self.player.state = "idle"
            self.player.invulnerable = False

            # Respawn enemies
            self.enemies.clear()
            self.spawn_test_enemies()

            # Resume game
            self.state = "playing"
        elif choice == "quit":
            # Return to main menu
            self.running = False

    def toggle_pause(self):
        """Toggle pause state and show pause menu"""
        if self.state == "dead":
            return

        self.paused = True
        self.state = "paused"

        # Show pause menu - loop until we get resume or quit
        while self.state == "paused":
            choice = self.pause_menu.run()

            if choice == "resume":
                self.paused = False
                self.state = "playing"
                break
            elif choice == "controls":
                self.help_screen.run()
                # Loop back to pause menu
            elif choice == "options":
                self.options_menu.run()
                # Loop back to pause menu
            elif choice == "quit":
                # Return to main menu
                self.running = False
                self.state = "playing"  # Prevent further updates
                break

    def debug_unlock_all_abilities(self):
        """Debug: Unlock all abilities"""
        for ability in self.player.abilities:
            self.player.unlock_ability(ability)
        print("All abilities unlocked!")

    def save_game(self, slot: int):
        """Save the game"""
        # Create a simple progress tracker
        class Progress:
            playtime = 0
            deaths = 0
            completion = 0
            regions_completed = []

        SaveSystem.save_game(slot, self.player, self.tilemap, Progress())

    def load_game(self, slot: int):
        """Load a saved game"""
        save_data = SaveSystem.load_game(slot)
        if save_data:
            # Restore player state
            player_data = save_data.get("player", {})
            pos = player_data.get("position", {"x": 640, "y": 400})
            self.player.pos = pygame.Vector2(pos["x"], pos["y"])
            self.player.will = player_data.get("will", 10)
            self.player.max_will = player_data.get("max_will", 10)
            self.player.abilities = player_data.get("abilities", {})
            # Restore more state as needed

    def render(self):
        """Render everything"""
        # Clear screen
        self.screen.fill((20, 20, 30))

        # Get camera offset
        camera_offset = self.camera.get_offset()

        # Render tilemap
        self.tilemap.render(self.screen, camera_offset)

        # Render enemies
        for enemy in self.enemies:
            enemy.render(self.screen, camera_offset)

        # Render projectiles
        for projectile in self.projectiles:
            screen_pos = projectile.pos - pygame.Vector2(*camera_offset)
            pygame.draw.circle(self.screen, (255, 255, 0),
                             (int(screen_pos.x), int(screen_pos.y)), 4)

        # Render companion
        if self.companion:
            self.companion.render(self.screen, camera_offset)

        # Render player
        self.player.render(self.screen, camera_offset)

        # Render HUD
        self.hud.render(self.screen, self.player)

        # Render debug info
        debug.draw_fps(self.screen, self.clock)
        if debug.show_hitboxes:
            # Draw player hitbox
            draw_rect = self.player.hitbox.copy()
            draw_rect.x -= camera_offset[0]
            draw_rect.y -= camera_offset[1]
            pygame.draw.rect(self.screen, (0, 255, 0), draw_rect, 2)

            # Draw enemy hitboxes
            for enemy in self.enemies:
                draw_rect = enemy.hitbox.copy()
                draw_rect.x -= camera_offset[0]
                draw_rect.y -= camera_offset[1]
                pygame.draw.rect(self.screen, (255, 0, 0), draw_rect, 2)

        pygame.display.flip()
