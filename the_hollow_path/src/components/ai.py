"""
AI component for The Hollow Path.
Handles enemy behavior patterns and state machines.
"""
import pygame
import random
from typing import Optional
from config.game_balance import ENEMY_STATS


class AIComponent:
    """AI state machine for enemies"""

    def __init__(self, entity, enemy_type: str):
        self.entity = entity
        self.enemy_type = enemy_type

        # Load stats
        stats = ENEMY_STATS.get(enemy_type, {})
        self.behavior = stats.get("behavior", "chase_melee")
        self.detection_radius = stats.get("detection_radius", 200)
        self.attack_range = stats.get("attack_range", 40)
        self.attack_cooldown_time = stats.get("attack_cooldown", 2.0)

        # State
        self.state = "patrol"
        self.target = None

        # Timers
        self.attack_cooldown = 0
        self.state_timer = 0

        # Patrol
        self.patrol_direction = random.choice([-1, 1])
        self.patrol_timer = 0
        self.patrol_change_time = random.uniform(2.0, 4.0)

    def update(self, dt: float, player):
        """Update AI behavior"""
        self.target = player
        self.attack_cooldown -= dt
        self.state_timer -= dt

        # Calculate distance to player
        distance_to_player = (player.pos - self.entity.pos).length()

        # Behavior routing
        if self.behavior == "chase_melee":
            self.chase_melee_behavior(dt, distance_to_player)
        elif self.behavior == "guard_position":
            self.guard_behavior(dt, distance_to_player)
        elif self.behavior == "circle_player":
            self.circle_behavior(dt, distance_to_player)
        elif self.behavior == "pull_player":
            self.pull_behavior(dt, distance_to_player)
        elif self.behavior == "boss_pattern":
            self.boss_behavior(dt, distance_to_player)
        else:
            self.chase_melee_behavior(dt, distance_to_player)

    def chase_melee_behavior(self, dt: float, distance: float):
        """Standard chase and melee attack behavior"""
        if self.state == "patrol":
            self.patrol_movement(dt)
            if distance < self.detection_radius:
                self.state = "chase"

        elif self.state == "chase":
            self.chase_movement()
            if distance < self.attack_range and self.attack_cooldown <= 0:
                self.state = "attack"
                self.state_timer = 0.5
            elif distance > self.detection_radius * 1.5:
                self.state = "patrol"

        elif self.state == "attack":
            self.entity.velocity.x = 0
            if self.state_timer <= 0:
                self.perform_attack()
                self.attack_cooldown = self.attack_cooldown_time
                self.state = "chase"

    def guard_behavior(self, dt: float, distance: float):
        """Guard a position, only engage if player gets close"""
        # Store original position (would need to be set on init)
        if not hasattr(self, 'guard_position'):
            self.guard_position = self.entity.pos.copy()

        if self.state == "patrol":
            # Stay near guard position
            if distance < self.detection_radius:
                self.state = "chase"

        elif self.state == "chase":
            self.chase_movement()
            if distance < self.attack_range and self.attack_cooldown <= 0:
                self.state = "attack"
                self.state_timer = 0.5
            elif distance > self.detection_radius * 2:
                # Return to guard position
                self.state = "return"

        elif self.state == "attack":
            self.entity.velocity.x = 0
            if self.state_timer <= 0:
                self.perform_attack()
                self.attack_cooldown = self.attack_cooldown_time
                self.state = "chase"

        elif self.state == "return":
            # Move back to guard position
            direction = (self.guard_position - self.entity.pos).normalize()
            self.entity.velocity.x = direction.x * self.entity.speed
            if (self.guard_position - self.entity.pos).length() < 20:
                self.state = "patrol"

    def circle_behavior(self, dt: float, distance: float):
        """Circle around the player"""
        if distance < self.detection_radius:
            # Move in a circle around player
            to_player = (self.target.pos - self.entity.pos).normalize()
            # Perpendicular vector for circling
            perpendicular = pygame.Vector2(-to_player.y, to_player.x)

            # Mix of approaching and circling
            if distance > self.attack_range * 1.5:
                move_dir = to_player * 0.7 + perpendicular * 0.3
            else:
                move_dir = perpendicular

            self.entity.velocity = move_dir.normalize() * self.entity.speed
        else:
            self.patrol_movement(dt)

    def pull_behavior(self, dt: float, distance: float):
        """Pull player toward self (like Spiral enemy)"""
        if distance < self.detection_radius:
            # Stay mostly stationary
            self.entity.velocity.x *= 0.9

            # Apply pull force to player
            if self.attack_cooldown <= 0:
                direction = (self.entity.pos - self.target.pos).normalize()
                pull_force = direction * 2.0
                self.target.velocity += pull_force
                self.attack_cooldown = 0.5

    def boss_behavior(self, dt: float, distance: float):
        """Boss pattern behavior (placeholder for custom boss logic)"""
        # Implement specific boss patterns here
        # For now, use aggressive chase behavior
        self.chase_melee_behavior(dt, distance)

    def patrol_movement(self, dt: float):
        """Simple patrol back and forth"""
        self.patrol_timer += dt

        if self.patrol_timer >= self.patrol_change_time:
            self.patrol_direction *= -1
            self.patrol_timer = 0
            self.patrol_change_time = random.uniform(2.0, 4.0)

        self.entity.velocity.x = self.patrol_direction * self.entity.speed * 0.5
        self.entity.facing_right = self.patrol_direction > 0

    def chase_movement(self):
        """Move toward player"""
        if not self.target:
            return

        direction = (self.target.pos - self.entity.pos).normalize()
        self.entity.velocity.x = direction.x * self.entity.speed
        self.entity.facing_right = direction.x > 0

    def perform_attack(self):
        """Perform attack on player"""
        if not self.target:
            return

        # Check if player is in range
        distance = (self.target.pos - self.entity.pos).length()
        if distance < self.attack_range:
            # Deal damage to player
            knockback_dir = (self.target.pos - self.entity.pos).normalize()
            knockback = knockback_dir * 5.0  # Knockback force
            if hasattr(self.target, 'combat'):
                self.target.combat.take_damage(self.entity.damage, knockback)

    def on_damaged(self):
        """Called when entity takes damage"""
        # Interrupt current action
        if self.state == "patrol":
            self.state = "chase"

    def on_player_detected(self):
        """Called when player enters detection range"""
        self.state = "chase"
