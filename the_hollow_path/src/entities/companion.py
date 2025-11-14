"""
Companion entity for The Hollow Path.
The cat companion that provides light and support.
"""
import pygame
import math
from config.game_balance import COMPANION_LIGHT_RADIUS, COMPANION_DAMAGE_REDUCTION, COMPANION_HEALTH_REGEN
from src.components.animation import AnimationController, Animation
from src.utils.sprite_loader import create_animation_frames


class Companion:
    """
    Cat companion that follows the player.
    Provides light radius, damage reduction, and health regeneration.
    """

    def __init__(self, player):
        self.player = player
        self.pos = player.pos.copy()
        self.velocity = pygame.Vector2(0, 0)

        # State
        self.state = "following"  # following, sitting, called
        self.facing_right = True

        # Following behavior
        self.follow_distance = 50
        self.max_distance = 300
        self.move_speed = 4.0

        # Sitting behavior
        self.sit_timer = 0
        self.sit_threshold = 3.0  # Seconds of player being still

        # Light radius
        self.light_radius = COMPANION_LIGHT_RADIUS

        # Hitbox
        self.hitbox = pygame.Rect(self.pos.x - 12, self.pos.y - 12, 24, 24)

        # Animation
        self.animation = AnimationController()
        self._init_animations()

    def _init_animations(self):
        """Initialize companion animations"""
        # Idle/sitting
        idle_frames = create_animation_frames("companion", 24, 24, 2)
        self.animation.add_animation("idle", Animation(idle_frames, 0.5))

        # Walking
        walk_frames = create_animation_frames("companion", 24, 24, 4)
        self.animation.add_animation("walk", Animation(walk_frames, 0.2))

        # Sitting
        sit_frames = create_animation_frames("companion", 24, 24, 1)
        self.animation.add_animation("sit", Animation(sit_frames, 1.0))

    def update(self, dt: float):
        """Update companion behavior"""
        distance_to_player = (self.player.pos - self.pos).length()

        # Check if player is stationary
        player_moving = abs(self.player.velocity.x) > 0.1 or abs(self.player.velocity.y) > 0.1

        if player_moving:
            self.sit_timer = 0
            if self.state == "sitting":
                self.state = "following"
        else:
            self.sit_timer += dt
            if self.sit_timer >= self.sit_threshold and distance_to_player < 30:
                self.state = "sitting"

        # Update based on state
        if self.state == "following":
            self.follow_player(distance_to_player)
        elif self.state == "called":
            self.move_to_player(distance_to_player)
        elif self.state == "sitting":
            self.velocity = pygame.Vector2(0, 0)

        # Apply movement
        self.pos += self.velocity * dt

        # Update hitbox
        self.hitbox.center = (int(self.pos.x), int(self.pos.y))

        # Update animation
        if self.state == "sitting":
            self.animation.play("sit")
        elif self.velocity.length() > 0.5:
            self.animation.play("walk")
        else:
            self.animation.play("idle")

        self.animation.update(dt)

        # Apply companion benefits to player
        self.apply_benefits(dt, distance_to_player)

    def follow_player(self, distance: float):
        """Follow the player at a distance"""
        if distance > self.follow_distance:
            direction = (self.player.pos - self.pos).normalize()
            self.velocity = direction * self.move_speed
            self.facing_right = direction.x > 0
        else:
            # Slow down when close
            self.velocity *= 0.9

        # Teleport if too far
        if distance > self.max_distance:
            self.pos = self.player.pos.copy()
            self.velocity = pygame.Vector2(0, 0)

    def move_to_player(self, distance: float):
        """Move quickly to player when called"""
        if distance > 20:
            direction = (self.player.pos - self.pos).normalize()
            self.velocity = direction * self.move_speed * 1.5
            self.facing_right = direction.x > 0
        else:
            self.state = "following"
            self.velocity *= 0.9

    def apply_benefits(self, dt: float, distance: float):
        """Apply companion benefits to player"""
        # Benefits only apply when close
        if distance > self.light_radius:
            return

        # Health regeneration when sitting together
        if self.state == "sitting" and distance < 30:
            self.player.will = min(
                self.player.will + COMPANION_HEALTH_REGEN * dt,
                self.player.max_will
            )

    def get_damage_reduction(self, distance: float) -> float:
        """Get damage reduction multiplier based on proximity"""
        if distance < self.light_radius:
            return 1.0 - COMPANION_DAMAGE_REDUCTION
        return 1.0

    def call(self):
        """Call the companion to the player"""
        self.state = "called"
        self.sit_timer = 0

    def render(self, surface: pygame.Surface, camera_offset: tuple = (0, 0)):
        """Render the companion"""
        # Draw light circle
        self.render_light(surface, camera_offset)

        # Get current frame
        frame = self.animation.get_current_frame()

        # Calculate draw position
        draw_x = int(self.pos.x - frame.get_width() // 2 - camera_offset[0])
        draw_y = int(self.pos.y - frame.get_height() // 2 - camera_offset[1])

        # Flip sprite if facing left
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        surface.blit(frame, (draw_x, draw_y))

    def render_light(self, surface: pygame.Surface, camera_offset: tuple):
        """Render the light radius from the companion"""
        # Create a surface for the light
        light_surface = pygame.Surface((self.light_radius * 2, self.light_radius * 2))
        light_surface.set_colorkey((0, 0, 0))

        # Draw gradient light circle
        for i in range(self.light_radius, 0, -5):
            alpha = int(255 * (i / self.light_radius) * 0.3)
            color = (255, 230, 150)  # Warm light color
            # Create temporary surface for this circle
            circle_surf = pygame.Surface((self.light_radius * 2, self.light_radius * 2))
            circle_surf.set_colorkey((0, 0, 0))
            circle_surf.set_alpha(alpha)
            pygame.draw.circle(circle_surf, color,
                             (self.light_radius, self.light_radius), i)
            light_surface.blit(circle_surf, (0, 0))

        # Draw the light surface
        light_x = int(self.pos.x - self.light_radius - camera_offset[0])
        light_y = int(self.pos.y - self.light_radius - camera_offset[1])
        surface.blit(light_surface, (light_x, light_y), special_flags=pygame.BLEND_ADD)
