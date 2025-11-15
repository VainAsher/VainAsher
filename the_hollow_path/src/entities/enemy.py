"""
Enemy entity for The Hollow Path.
Base enemy class with AI and combat.
"""
import pygame
from config.game_balance import ENEMY_STATS
from src.components.ai import AIComponent
from src.components.animation import AnimationController, Animation
from src.utils.sprite_loader import create_animation_frames


class Enemy:
    """Base enemy class with AI state machine"""

    def __init__(self, x: float, y: float, enemy_type: str):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.enemy_type = enemy_type

        # Load stats from config
        stats = ENEMY_STATS.get(enemy_type, ENEMY_STATS["shadow_self"])
        self.health = stats["health"]
        self.max_health = stats["health"]
        self.damage = stats["damage"]
        self.speed = stats["speed"]

        # State
        self.state = "patrol"
        self.facing_right = True
        self.on_ground = False
        self.active = True
        self.dead = False

        # Components
        self.ai = AIComponent(self, enemy_type)
        self.animation = AnimationController()

        # Combat
        self.invulnerable = False
        self.invuln_timer = 0
        self.damage_flash_timer = 0

        # Hitbox
        self.hitbox = pygame.Rect(x - 16, y - 16, 32, 32)

        # Initialize animations
        self._init_animations()

    def _init_animations(self):
        """Initialize placeholder animations"""
        # Idle/patrol
        idle_frames = create_animation_frames(self.enemy_type, 32, 32, 2)
        self.animation.add_animation("idle", Animation(idle_frames, 0.5))

        # Chase
        chase_frames = create_animation_frames(self.enemy_type, 32, 32, 4)
        self.animation.add_animation("chase", Animation(chase_frames, 0.2))

        # Attack
        attack_frames = create_animation_frames(self.enemy_type, 32, 32, 3)
        self.animation.add_animation("attack", Animation(attack_frames, 0.15, loop=False))

    def update(self, dt: float, player, tilemap=None):
        """Update enemy"""
        if not self.active or self.dead:
            return

        # Update AI
        self.ai.update(dt, player)
        self.state = self.ai.state

        # Update animation
        if self.state == "attack":
            self.animation.play("attack")
        elif self.state == "chase":
            self.animation.play("chase")
        else:
            self.animation.play("idle")

        self.animation.update(dt)

        # Apply physics
        self.apply_physics(dt, tilemap)

        # Update hitbox
        self.hitbox.center = (int(self.pos.x), int(self.pos.y))

        # Update timers
        if self.invuln_timer > 0:
            self.invuln_timer -= dt
        else:
            self.invulnerable = False

        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= dt

    def apply_physics(self, dt: float, tilemap=None):
        """Apply gravity and friction"""
        # Gravity
        if not self.on_ground:
            self.velocity.y += 0.6  # Gravity
            if self.velocity.y > 15:  # Max fall speed
                self.velocity.y = 15

        # Friction
        if self.on_ground:
            self.velocity.x *= 0.8
        else:
            self.velocity.x *= 0.95

        # Update position
        self.pos += self.velocity

        # Check collisions with tilemap
        if tilemap:
            self.check_collisions(tilemap)
        else:
            # Fallback ground check
            if self.pos.y >= 400:
                self.on_ground = True
                self.pos.y = 400
                self.velocity.y = 0
            else:
                self.on_ground = False

    def check_collisions(self, tilemap):
        """Check collisions with tilemap"""
        self.on_ground = False

        # Get collision rects near enemy
        collision_rects = tilemap.get_collision_rects(self.hitbox)

        # Horizontal collision
        self.hitbox.x = int(self.pos.x - self.hitbox.width // 2)
        for tile_rect in collision_rects:
            if self.hitbox.colliderect(tile_rect):
                # Moving right
                if self.velocity.x > 0:
                    self.hitbox.right = tile_rect.left
                    self.pos.x = self.hitbox.centerx
                    self.velocity.x = 0
                # Moving left
                elif self.velocity.x < 0:
                    self.hitbox.left = tile_rect.right
                    self.pos.x = self.hitbox.centerx
                    self.velocity.x = 0

        # Vertical collision
        self.hitbox.y = int(self.pos.y - self.hitbox.height // 2)
        for tile_rect in collision_rects:
            if self.hitbox.colliderect(tile_rect):
                # Moving down (landing)
                if self.velocity.y > 0:
                    self.hitbox.bottom = tile_rect.top
                    self.pos.y = self.hitbox.centery
                    self.velocity.y = 0
                    self.on_ground = True
                # Moving up (hitting ceiling)
                elif self.velocity.y < 0:
                    self.hitbox.top = tile_rect.bottom
                    self.pos.y = self.hitbox.centery
                    self.velocity.y = 0

    def take_damage(self, amount: float, knockback=None):
        """Take damage from player"""
        if self.invulnerable or self.dead:
            return

        self.health -= amount
        self.damage_flash_timer = 0.2
        self.invulnerable = True
        self.invuln_timer = 0.3

        # Apply knockback
        if knockback:
            self.velocity = knockback

        # Notify AI
        self.ai.on_damaged()

        # Check for death
        if self.health <= 0:
            self.die()

    def die(self):
        """Enemy death"""
        self.dead = True
        self.active = False
        print(f"{self.enemy_type} defeated")
        # Drop items, particles, etc.

    def should_flash(self) -> bool:
        """Check if should flash (damage feedback)"""
        if self.damage_flash_timer > 0:
            return int(self.damage_flash_timer * 10) % 2 == 0
        return False

    def render(self, surface: pygame.Surface, camera_offset: tuple = (0, 0)):
        """Render the enemy"""
        if not self.active:
            return

        # Get current frame
        frame = self.animation.get_current_frame()

        # Calculate draw position
        draw_x = int(self.pos.x - frame.get_width() // 2 - camera_offset[0])
        draw_y = int(self.pos.y - frame.get_height() // 2 - camera_offset[1])

        # Flip sprite if facing left
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        # Flash if damaged
        if self.should_flash():
            return

        surface.blit(frame, (draw_x, draw_y))

        # Draw health bar
        self.render_health_bar(surface, camera_offset)

    def render_health_bar(self, surface: pygame.Surface, camera_offset: tuple):
        """Render enemy health bar"""
        if self.health >= self.max_health:
            return

        bar_width = 32
        bar_height = 4
        bar_x = int(self.pos.x - bar_width // 2 - camera_offset[0])
        bar_y = int(self.pos.y - 24 - camera_offset[1])

        # Background
        pygame.draw.rect(surface, (50, 50, 50),
                        (bar_x, bar_y, bar_width, bar_height))

        # Health
        health_width = int((self.health / self.max_health) * bar_width)
        pygame.draw.rect(surface, (255, 50, 50),
                        (bar_x, bar_y, health_width, bar_height))

        # Border
        pygame.draw.rect(surface, (255, 255, 255),
                        (bar_x, bar_y, bar_width, bar_height), 1)
