"""
Movement component for The Hollow Path.
Handles player movement abilities and mechanics.
"""
import pygame
from config.game_balance import *
import config.runtime_settings as runtime


class MovementComponent:
    """Handles all player movement abilities"""

    def __init__(self, entity):
        self.entity = entity

        # Jump state
        self.jumps_remaining = 0
        self.max_jumps = 1  # Increases with double_jump ability
        self.coyote_timer = 0
        self.jump_buffer_timer = 0

        # Dash state
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.is_dashing = False
        self.dash_direction = pygame.Vector2(1, 0)

        # Shadow dash state
        self.shadow_dash_timer = 0
        self.is_shadow_dashing = False
        self.phasing = False  # Can pass through enemies/hazards

        # Wall mechanics
        self.wall_slide_timer = 0
        self.can_wall_jump = False

        # Grapple state
        self.grapple_active = False
        self.grapple_point = None
        self.grapple_cooldown_timer = 0

        # Down smash state
        self.is_down_smashing = False

    def update(self, dt: float):
        """Update all timers"""
        # Coyote time (grace period for jumping after leaving ground)
        if self.coyote_timer > 0:
            self.coyote_timer -= dt

        # Jump buffer (remember jump press briefly)
        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= dt

        # Dash timers
        if self.dash_timer > 0:
            self.dash_timer -= dt
        else:
            self.is_dashing = False

        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= dt

        # Shadow dash timers
        if self.shadow_dash_timer > 0:
            self.shadow_dash_timer -= dt
        else:
            self.is_shadow_dashing = False
            self.phasing = False

        # Grapple cooldown
        if self.grapple_cooldown_timer > 0:
            self.grapple_cooldown_timer -= dt

    def can_jump(self) -> bool:
        """Check if entity can jump"""
        # Can jump if on ground or in coyote time
        if self.entity.on_ground or self.coyote_timer > 0:
            return True

        # Or if we have jumps remaining (double jump, etc.)
        if self.jumps_remaining > 0:
            return True

        return False

    def jump(self):
        """Execute a jump"""
        if not self.can_jump():
            return

        # First jump (from ground) uses full force
        if self.entity.on_ground or self.coyote_timer > 0:
            self.entity.velocity.y = JUMP_FORCE
            self.jumps_remaining = self.max_jumps - 1
        # Additional jumps (double jump, etc.)
        else:
            self.entity.velocity.y = DOUBLE_JUMP_FORCE
            self.jumps_remaining -= 1

        self.coyote_timer = 0
        self.jump_buffer_timer = 0

    def wall_jump(self):
        """Execute a wall jump"""
        if not self.entity.on_wall:
            return

        # Jump away from wall
        direction = -1 if self.entity.wall_direction == 1 else 1
        self.entity.velocity.x = WALL_JUMP_X_FORCE * direction
        self.entity.velocity.y = WALL_JUMP_Y_FORCE

        # Reset jumps
        self.jumps_remaining = self.max_jumps
        self.can_wall_jump = False  # Reset until touching wall again

    def start_dash(self, direction: pygame.Vector2):
        """Start a dash - provides speed boost"""
        if self.dash_cooldown_timer > 0:
            return

        self.is_dashing = True
        self.dash_timer = runtime.get_dash_duration()
        self.dash_cooldown_timer = DASH_COOLDOWN
        self.dash_direction = direction.normalize() if direction.length() > 0 else pygame.Vector2(1, 0)

        # Store direction, don't set velocity directly
        # Velocity will be modified in player movement handling

        # Invulnerability during dash
        if DASH_INVULNERABLE:
            self.entity.invulnerable = True

    def start_shadow_dash(self, direction: pygame.Vector2):
        """Start a shadow dash (can pass through obstacles)"""
        if self.dash_cooldown_timer > 0:
            return

        self.is_shadow_dashing = True
        self.shadow_dash_timer = runtime.get_shadow_dash_duration()
        self.dash_cooldown_timer = SHADOW_DASH_COOLDOWN
        self.phasing = True
        self.dash_direction = direction.normalize() if direction.length() > 0 else pygame.Vector2(1, 0)

        # Store direction, don't set velocity directly
        self.entity.invulnerable = True

    def get_dash_speed_multiplier(self) -> float:
        """Get current dash speed multiplier"""
        if self.is_shadow_dashing:
            return runtime.get_shadow_dash_speed_mult()  # Shadow dash is faster
        elif self.is_dashing:
            return runtime.get_dash_speed_mult()  # Regular dash
        return 1.0  # Normal speed

    def start_down_smash(self):
        """Start a down smash attack while in air"""
        if self.entity.on_ground:
            return

        self.is_down_smashing = True
        self.entity.velocity.x = 0
        self.entity.velocity.y = DOWN_SMASH_FORCE

    def start_grapple(self, target_point: pygame.Vector2, tilemap=None):
        """Start grappling to a point"""
        if self.grapple_cooldown_timer > 0:
            return

        # If tilemap provided, find nearest grapple_point tile
        if tilemap:
            nearest_grapple = None
            nearest_dist = GRAPPLE_RANGE

            # Search area around target
            search_rect = pygame.Rect(
                target_point.x - GRAPPLE_RANGE,
                target_point.y - GRAPPLE_RANGE,
                GRAPPLE_RANGE * 2,
                GRAPPLE_RANGE * 2
            )

            tiles = tilemap.get_tiles_in_rect(search_rect)
            for tile in tiles:
                if tile.tile_type == "grapple_point":
                    tile_center = pygame.Vector2(
                        tile.rect.centerx,
                        tile.rect.centery
                    )
                    dist = (tile_center - self.entity.pos).length()
                    if dist < nearest_dist:
                        nearest_dist = dist
                        nearest_grapple = tile_center

            if nearest_grapple:
                self.grapple_active = True
                self.grapple_point = nearest_grapple
                self.grapple_cooldown_timer = GRAPPLE_COOLDOWN
                print(f"Grappling to point at {nearest_grapple}")
            else:
                print("No grapple point in range!")
        else:
            # Fallback: grapple to target directly
            distance = (target_point - self.entity.pos).length()
            if distance > GRAPPLE_RANGE:
                return

            self.grapple_active = True
            self.grapple_point = target_point
            self.grapple_cooldown_timer = GRAPPLE_COOLDOWN

    def update_grapple(self, dt: float):
        """Update grapple physics"""
        if not self.grapple_active or not self.grapple_point:
            return

        # Pull toward grapple point
        direction = (self.grapple_point - self.entity.pos).normalize()
        self.entity.velocity = direction * PULL_SPEED

        # Release when close enough
        distance = (self.grapple_point - self.entity.pos).length()
        if distance < 20:
            self.release_grapple()

    def release_grapple(self):
        """Release grapple"""
        self.grapple_active = False
        self.grapple_point = None

    def on_landed(self):
        """Called when entity lands on ground"""
        self.jumps_remaining = self.max_jumps
        self.is_down_smashing = False
        self.coyote_timer = COYOTE_TIME

    def on_left_ground(self):
        """Called when entity leaves ground"""
        if not self.is_dashing and not self.is_shadow_dashing:
            self.coyote_timer = COYOTE_TIME
