"""
Physics component for The Hollow Path.
Handles gravity, collision, and movement physics.
"""
import pygame
from config.game_balance import *


class PhysicsComponent:
    """Physics simulation for entities"""

    def __init__(self, entity):
        self.entity = entity
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.on_ground = False
        self.on_wall = False
        self.wall_direction = 0  # -1 for left, 1 for right
        self.affected_by_gravity = True

    def apply_gravity(self, dt: float):
        """Apply gravity to the entity"""
        if not self.affected_by_gravity:
            return

        if not self.on_ground:
            self.velocity.y += GRAVITY
            if self.velocity.y > MAX_FALL_SPEED:
                self.velocity.y = MAX_FALL_SPEED

    def apply_friction(self, dt: float):
        """Apply friction based on ground state"""
        if self.on_ground:
            self.velocity.x *= FRICTION
        else:
            self.velocity.x *= AIR_FRICTION

    def update(self, dt: float):
        """Update physics simulation"""
        # Apply acceleration
        self.velocity += self.acceleration * dt

        # Apply gravity
        self.apply_gravity(dt)

        # Apply friction
        self.apply_friction(dt)

        # Update position
        self.entity.pos += self.velocity

        # Reset acceleration
        self.acceleration = pygame.Vector2(0, 0)

    def add_force(self, force: pygame.Vector2):
        """Add a force to the entity"""
        self.acceleration += force

    def set_velocity(self, velocity: pygame.Vector2):
        """Set velocity directly"""
        self.velocity = velocity

    def check_collision(self, tilemap):
        """
        Check and resolve collisions with tilemap.
        Updates on_ground and on_wall states.
        """
        # This will be implemented when we create the tilemap system
        pass


class Collision:
    """Collision detection utilities"""

    @staticmethod
    def rect_collision(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
        """Check if two rectangles collide"""
        return rect1.colliderect(rect2)

    @staticmethod
    def point_in_rect(point: tuple, rect: pygame.Rect) -> bool:
        """Check if a point is inside a rectangle"""
        return rect.collidepoint(point)

    @staticmethod
    def circle_collision(pos1: pygame.Vector2, radius1: float,
                        pos2: pygame.Vector2, radius2: float) -> bool:
        """Check if two circles collide"""
        distance = (pos2 - pos1).length()
        return distance < (radius1 + radius2)

    @staticmethod
    def resolve_collision(entity_rect: pygame.Rect, tile_rect: pygame.Rect,
                         velocity: pygame.Vector2) -> pygame.Vector2:
        """
        Resolve collision and return adjusted velocity.

        Args:
            entity_rect: Entity's hitbox
            tile_rect: Tile's hitbox
            velocity: Current velocity

        Returns:
            Adjusted velocity after collision
        """
        new_velocity = velocity.copy()

        # Calculate overlap on each axis
        overlap_x = min(entity_rect.right - tile_rect.left,
                       tile_rect.right - entity_rect.left)
        overlap_y = min(entity_rect.bottom - tile_rect.top,
                       tile_rect.bottom - entity_rect.top)

        # Resolve on the axis with less overlap
        if overlap_x < overlap_y:
            # Horizontal collision
            if velocity.x > 0:  # Moving right
                entity_rect.right = tile_rect.left
                new_velocity.x = 0
            elif velocity.x < 0:  # Moving left
                entity_rect.left = tile_rect.right
                new_velocity.x = 0
        else:
            # Vertical collision
            if velocity.y > 0:  # Moving down
                entity_rect.bottom = tile_rect.top
                new_velocity.y = 0
            elif velocity.y < 0:  # Moving up
                entity_rect.top = tile_rect.bottom
                new_velocity.y = 0

        return new_velocity
