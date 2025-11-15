"""
Player entity for The Hollow Path.
Main character with all abilities and state management.
"""
import pygame
from config.game_balance import *
from src.components.movement import MovementComponent
from src.components.combat import CombatComponent
from src.components.animation import AnimationController, Animation
from src.utils.sprite_loader import create_animation_frames


class Player:
    """
    Player character with full ability set.

    States: idle, walking, jumping, falling, wall_sliding,
            wall_jumping, dashing, shadow_dashing, crouching,
            down_smashing, grappling, attacking, hurt, dead
    """

    def __init__(self, x: float, y: float):
        # Position & Physics
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.hitbox = pygame.Rect(x - 16, y - 32, 32, 64)

        # State
        self.state = "idle"
        self.facing_right = True
        self.on_ground = False
        self.on_wall = False
        self.wall_direction = 0  # -1 left, 1 right

        # Components
        self.movement = MovementComponent(self)
        self.combat = CombatComponent(self)
        self.animation = AnimationController()

        # Abilities (unlocked through progression)
        self.abilities = {
            "first_step": False,      # Basic jump
            "wall_climb": False,      # Wall slide/jump
            "double_jump": False,     # Air jump
            "dash": False,            # Quick dash
            "shadow_dash": False,     # Phase through obstacles
            "grapple": False,         # Hook to points
            "down_smash": False       # Aerial ground pound
        }

        # Stats (thematic names)
        self.will = STARTING_WILL  # Health
        self.max_will = STARTING_MAX_WILL
        self.strength = STARTING_STRENGTH  # Energy/stamina
        self.max_strength = STARTING_MAX_STRENGTH

        # Consumables
        self.consumables = {
            "slot_1": None,
            "slot_2": None,
            "slot_3": None,
            "slot_4": None
        }
        self.currency = 0  # Hope Fragments
        self.memory_fragments = []

        # Companion reference
        self.companion = None

        # Current region
        self.current_region = "the_depths"

        # Invulnerability
        self.invulnerable = False
        self.invuln_timer = 0

        # Crouching
        self.crouching = False

        # Initialize animations
        self._init_animations()

    def _init_animations(self):
        """Initialize placeholder animations"""
        # Idle animation
        idle_frames = create_animation_frames("player", 32, 64, 2)
        self.animation.add_animation("idle", Animation(idle_frames, 0.5))

        # Walk animation
        walk_frames = create_animation_frames("player", 32, 64, 4)
        self.animation.add_animation("walk", Animation(walk_frames, 0.15))

        # Jump animation
        jump_frames = create_animation_frames("player", 32, 64, 1)
        self.animation.add_animation("jump", Animation(jump_frames, 0.1, loop=False))

        # Fall animation
        fall_frames = create_animation_frames("player", 32, 64, 1)
        self.animation.add_animation("fall", Animation(fall_frames, 0.1))

        # Dash animation
        dash_frames = create_animation_frames("player", 32, 64, 2)
        self.animation.add_animation("dash", Animation(dash_frames, 0.1))

        # Attack animation
        attack_frames = create_animation_frames("player", 32, 64, 3)
        self.animation.add_animation("attack", Animation(attack_frames, 0.1, loop=False))

    def update(self, dt: float, inputs: dict, tilemap=None):
        """Main update loop"""
        # Update components
        self.movement.update(dt)
        self.combat.update(dt)
        self.animation.update(dt)

        # Handle input
        self.handle_input(inputs)

        # Apply physics
        self.apply_physics(dt)

        # Update grapple
        if self.movement.grapple_active:
            self.movement.update_grapple(dt)

        # Update collision state
        if tilemap:
            self.check_collisions(tilemap)

        # Update state
        self.update_state()

        # Update hitbox
        self.hitbox.center = (int(self.pos.x), int(self.pos.y))

        # Update invulnerability
        if self.invuln_timer > 0:
            self.invuln_timer -= dt
        else:
            self.invulnerable = False

    def handle_input(self, inputs: dict):
        """Process player inputs"""
        # Don't process input if dead
        if self.state == "dead":
            return

        # Horizontal movement
        move_x = 0
        if inputs.get("move_left"):
            move_x -= 1
            self.facing_right = False
        if inputs.get("move_right"):
            move_x += 1
            self.facing_right = True

        # Apply movement
        if not self.movement.is_dashing and not self.movement.is_shadow_dashing:
            speed_mult = CROUCH_SPEED_MULT if self.crouching else 1.0
            self.velocity.x += move_x * ACCELERATION * speed_mult

        # Jump
        if inputs.get("jump_pressed"):
            self.movement.jump_buffer_timer = JUMP_BUFFER

        if self.movement.jump_buffer_timer > 0 and self.abilities["first_step"]:
            if self.movement.can_jump():
                self.movement.jump()
                self.movement.jump_buffer_timer = 0

        # Wall jump
        if self.on_wall and inputs.get("jump_pressed") and self.abilities["wall_climb"]:
            self.movement.wall_jump()

        # Crouch
        self.crouching = inputs.get("crouch") and self.on_ground

        # Dash
        if inputs.get("dash_pressed") and self.abilities["dash"]:
            direction = pygame.Vector2(1 if self.facing_right else -1, 0)
            self.movement.start_dash(direction)

        # Shadow Dash
        if inputs.get("shadow_dash_pressed") and self.abilities["shadow_dash"]:
            direction = pygame.Vector2(1 if self.facing_right else -1, 0)
            self.movement.start_shadow_dash(direction)

        # Down Smash
        if not self.on_ground and inputs.get("crouch") and self.abilities["down_smash"]:
            self.movement.start_down_smash()

        # Grapple
        if inputs.get("grapple_pressed") and self.abilities["grapple"]:
            mouse_pos = inputs.get("mouse_pos", self.pos)
            target = pygame.Vector2(mouse_pos[0], mouse_pos[1])
            self.movement.start_grapple(target)

        # Attack
        if inputs.get("attack_pressed"):
            self.combat.melee_attack()

        # Shuriken
        if inputs.get("shuriken_pressed"):
            mouse_pos = inputs.get("mouse_pos", (self.pos.x + 100, self.pos.y))
            direction = pygame.Vector2(mouse_pos[0] - self.pos.x, mouse_pos[1] - self.pos.y)
            self.combat.throw_shuriken(direction)

        # Consumables
        for i in range(1, 5):
            if inputs.get(f"consumable_{i}"):
                self.use_consumable(f"slot_{i}")

    def apply_physics(self, dt: float):
        """Apply gravity and friction"""
        # Gravity (unless grappling)
        if not self.on_ground and not self.movement.grapple_active:
            # Wall slide
            if self.on_wall and self.abilities["wall_climb"] and self.velocity.y > 0:
                self.velocity.y = min(self.velocity.y, WALL_SLIDE_SPEED)
            else:
                self.velocity.y += GRAVITY
                if self.velocity.y > MAX_FALL_SPEED:
                    self.velocity.y = MAX_FALL_SPEED

        # Friction
        if self.on_ground:
            self.velocity.x *= FRICTION
        else:
            self.velocity.x *= AIR_FRICTION

        # Apply speed limit
        max_speed = PLAYER_SPEED
        if abs(self.velocity.x) > max_speed and not self.movement.is_dashing:
            self.velocity.x = max_speed if self.velocity.x > 0 else -max_speed

        # NOTE: Position is now updated in check_collisions() to prevent clipping

    def check_collisions(self, tilemap):
        """
        Check collisions with tilemap using axis-separated collision detection.
        This prevents clipping by moving and checking each axis independently.
        """
        if not tilemap:
            # No tilemap, just apply velocity
            self.pos += self.velocity
            return

        # Skip collision if phasing (shadow dash)
        if self.movement.phasing:
            self.pos += self.velocity
            self.on_ground = False
            self.on_wall = False
            return

        was_on_ground = self.on_ground

        # Reset states
        self.on_ground = False
        self.on_wall = False
        self.wall_direction = 0

        # === HORIZONTAL MOVEMENT AND COLLISION ===
        # Move horizontally first
        self.pos.x += self.velocity.x
        self.hitbox.centerx = int(self.pos.x)

        # Check horizontal collisions
        collision_rects = tilemap.get_collision_rects(self.hitbox)
        for tile_rect in collision_rects:
            if self.hitbox.colliderect(tile_rect):
                # Moving right - push out to the left
                if self.velocity.x > 0:
                    self.hitbox.right = tile_rect.left
                    self.pos.x = self.hitbox.centerx
                    self.velocity.x = 0
                    self.on_wall = True
                    self.wall_direction = 1
                # Moving left - push out to the right
                elif self.velocity.x < 0:
                    self.hitbox.left = tile_rect.right
                    self.pos.x = self.hitbox.centerx
                    self.velocity.x = 0
                    self.on_wall = True
                    self.wall_direction = -1

        # === VERTICAL MOVEMENT AND COLLISION ===
        # Move vertically after horizontal is resolved
        self.pos.y += self.velocity.y
        self.hitbox.centery = int(self.pos.y)

        # Check vertical collisions
        collision_rects = tilemap.get_collision_rects(self.hitbox)
        for tile_rect in collision_rects:
            if self.hitbox.colliderect(tile_rect):
                # Moving down (landing on ground)
                if self.velocity.y > 0:
                    self.hitbox.bottom = tile_rect.top
                    self.pos.y = self.hitbox.centery
                    self.velocity.y = 0
                    self.on_ground = True
                    self.on_wall = False  # On ground takes priority over wall
                # Moving up (hitting ceiling)
                elif self.velocity.y < 0:
                    self.hitbox.top = tile_rect.bottom
                    self.pos.y = self.hitbox.centery
                    self.velocity.y = 0

        # Trigger landing/leaving events
        if not was_on_ground and self.on_ground:
            self.movement.on_landed()
            if self.movement.is_down_smashing:
                self.create_ground_pound_effect()
        elif was_on_ground and not self.on_ground:
            self.movement.on_left_ground()

    def update_state(self):
        """Update animation state"""
        if self.state == "dead":
            return

        if self.movement.is_dashing:
            self.state = "dashing"
            self.animation.play("dash")
        elif self.movement.is_shadow_dashing:
            self.state = "shadow_dashing"
            self.animation.play("dash")
        elif self.combat.is_attacking:
            self.state = "attacking"
            self.animation.play("attack")
        elif not self.on_ground:
            if self.velocity.y < 0:
                self.state = "jumping"
                self.animation.play("jump")
            else:
                self.state = "falling"
                self.animation.play("fall")
        elif abs(self.velocity.x) > 0.5:
            self.state = "walking"
            self.animation.play("walk")
        else:
            self.state = "idle"
            self.animation.play("idle")

    def create_ground_pound_effect(self):
        """Create ground pound shockwave"""
        # Placeholder for particle effect
        pass

    def unlock_ability(self, ability_name: str):
        """Unlock an ability"""
        if ability_name in self.abilities:
            self.abilities[ability_name] = True
            print(f"Ability unlocked: {ability_name}")

            # Update max jumps for double jump
            if ability_name == "double_jump":
                self.movement.max_jumps = 2

    def use_consumable(self, slot: str):
        """Use a consumable from inventory"""
        if slot not in self.consumables or not self.consumables[slot]:
            return

        item = self.consumables[slot]
        # Apply item effects (placeholder)
        print(f"Used: {item}")

    def take_damage(self, amount: float, knockback=None):
        """Take damage"""
        self.combat.take_damage(amount, knockback)

    def die(self):
        """Player death"""
        self.state = "dead"
        self.velocity = pygame.Vector2(0, 0)
        print("Player died")

    def render(self, surface: pygame.Surface, camera_offset: tuple = (0, 0)):
        """Render the player"""
        # Get current frame
        frame = self.animation.get_current_frame()

        # Calculate draw position
        draw_x = int(self.pos.x - frame.get_width() // 2 - camera_offset[0])
        draw_y = int(self.pos.y - frame.get_height() // 2 - camera_offset[1])

        # Flip sprite if facing left
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        # Flash if damaged
        if self.combat.should_flash():
            # Don't draw (creates flashing effect)
            return

        surface.blit(frame, (draw_x, draw_y))
