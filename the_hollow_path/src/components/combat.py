"""
Combat component for The Hollow Path.
Handles melee attacks, ranged attacks, and damage.
"""
import pygame
from config.game_balance import *
from typing import List, Optional


class CombatComponent:
    """Handles combat mechanics for entities"""

    def __init__(self, entity):
        self.entity = entity

        # Melee combat
        self.attack_cooldown = 0
        self.is_attacking = False
        self.attack_hitbox = None
        self.combo_stage = 0
        self.combo_timer = 0

        # Ranged combat
        self.shuriken_count = SHURIKEN_COUNT
        self.max_shuriken = SHURIKEN_COUNT
        self.shuriken_reload_timer = 0

        # Damage state
        self.invulnerable = False
        self.invuln_timer = 0
        self.damage_flash_timer = 0

        # Stats
        self.damage_multiplier = 1.0
        self.temp_buff_timer = 0

    def update(self, dt: float):
        """Update combat timers"""
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        if self.combo_timer > 0:
            self.combo_timer -= dt
        else:
            self.combo_stage = 0

        if self.invuln_timer > 0:
            self.invuln_timer -= dt
        else:
            self.invulnerable = False

        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= dt

        if self.shuriken_reload_timer > 0:
            self.shuriken_reload_timer -= dt
        else:
            if self.shuriken_count < self.max_shuriken:
                self.shuriken_count = self.max_shuriken

        if self.temp_buff_timer > 0:
            self.temp_buff_timer -= dt
        else:
            self.damage_multiplier = 1.0

    def melee_attack(self) -> Optional[pygame.Rect]:
        """
        Perform a melee attack.

        Returns:
            pygame.Rect: Hitbox of the attack, or None if can't attack
        """
        if self.attack_cooldown > 0:
            return None

        self.is_attacking = True
        self.attack_cooldown = SWORD_COOLDOWN

        # Advance combo
        self.combo_stage = min(self.combo_stage + 1, MAX_COMBO)
        self.combo_timer = COMBO_WINDOW

        # Create attack hitbox in front of player
        offset = SWORD_RANGE if self.entity.facing_right else -SWORD_RANGE
        attack_x = self.entity.pos.x + offset
        attack_y = self.entity.pos.y

        self.attack_hitbox = pygame.Rect(
            attack_x - SWORD_RANGE // 2,
            attack_y - 20,
            SWORD_RANGE,
            40
        )

        return self.attack_hitbox

    def throw_shuriken(self, direction: pygame.Vector2) -> Optional[dict]:
        """
        Throw a shuriken.

        Args:
            direction: Direction to throw

        Returns:
            dict: Projectile data, or None if can't throw
        """
        if self.shuriken_count <= 0:
            return None

        self.shuriken_count -= 1
        if self.shuriken_count == 0:
            self.shuriken_reload_timer = SHURIKEN_RELOAD_TIME

        # Create projectile data
        projectile = {
            "type": "shuriken",
            "pos": self.entity.pos.copy(),
            "velocity": direction.normalize() * SHURIKEN_SPEED,
            "damage": SHURIKEN_DAMAGE * self.damage_multiplier,
            "lifetime": SHURIKEN_LIFETIME,
            "owner": self.entity
        }

        return projectile

    def take_damage(self, amount: float, knockback: Optional[pygame.Vector2] = None):
        """
        Take damage.

        Args:
            amount: Damage amount
            knockback: Knockback vector (optional)
        """
        if self.invulnerable:
            return

        # Apply damage
        actual_damage = amount
        self.entity.will -= actual_damage

        # Apply knockback
        if knockback:
            self.entity.velocity = knockback

        # Enter invulnerability period
        self.invulnerable = True
        self.invuln_timer = HURT_INVULN_TIME
        self.damage_flash_timer = 0.2

        # Check for death
        if self.entity.will <= 0:
            self.entity.die()

    def apply_buff(self, damage_mult: float, duration: float):
        """
        Apply a temporary damage buff.

        Args:
            damage_mult: Damage multiplier
            duration: Duration in seconds
        """
        self.damage_multiplier = damage_mult
        self.temp_buff_timer = duration

    def get_melee_damage(self) -> float:
        """Get current melee damage (including combo bonus)"""
        base_damage = SWORD_DAMAGE
        combo_bonus = 1.0 + (self.combo_stage - 1) * 0.2
        return base_damage * combo_bonus * self.damage_multiplier

    def should_flash(self) -> bool:
        """Check if entity should flash (damage feedback)"""
        if self.damage_flash_timer > 0:
            # Flash on/off every 0.1 seconds
            return int(self.damage_flash_timer * 10) % 2 == 0
        return False


class Projectile:
    """Projectile entity"""

    def __init__(self, projectile_data: dict):
        self.type = projectile_data["type"]
        self.pos = projectile_data["pos"]
        self.velocity = projectile_data["velocity"]
        self.damage = projectile_data["damage"]
        self.lifetime = projectile_data["lifetime"]
        self.owner = projectile_data.get("owner")
        self.active = True
        self.hitbox = pygame.Rect(self.pos.x - 4, self.pos.y - 4, 8, 8)

    def update(self, dt: float):
        """Update projectile"""
        if not self.active:
            return

        self.pos += self.velocity * dt
        self.hitbox.center = self.pos
        self.lifetime -= dt

        if self.lifetime <= 0:
            self.active = False

    def hit(self):
        """Mark projectile as hit"""
        self.active = False
