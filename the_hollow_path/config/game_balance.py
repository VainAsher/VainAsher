"""
Game balance configuration for The Hollow Path.
All gameplay parameters and stats are defined here.
"""

# Player Movement
PLAYER_SPEED = 5.0
ACCELERATION = 0.5
FRICTION = 0.8
AIR_FRICTION = 0.95

# Jump System
JUMP_FORCE = -15.0
DOUBLE_JUMP_FORCE = -13.0
GRAVITY = 0.6
MAX_FALL_SPEED = 15.0
COYOTE_TIME = 0.15
JUMP_BUFFER = 0.1

# Wall Mechanics
WALL_SLIDE_SPEED = 2.0
WALL_JUMP_X_FORCE = 8.0
WALL_JUMP_Y_FORCE = -14.0
WALL_STICK_TIME = 0.1

# Dash System
DASH_SPEED = 15.0
DASH_DURATION = 0.4  # Increased from 0.2 to 0.4 for longer dash
DASH_COOLDOWN = 0.5
DASH_INVULNERABLE = True
DASH_SPEED_MULTIPLIER = 2.5  # Configurable speed multiplier

# Shadow Dash
SHADOW_DASH_SPEED = 20.0
SHADOW_DASH_DURATION = 0.5  # Increased from 0.25 to 0.5 for longer phase duration
SHADOW_DASH_COOLDOWN = 2.0
SHADOW_DASH_PHASE = True
SHADOW_DASH_SPEED_MULTIPLIER = 3.5  # Configurable speed multiplier (increased from 3.0)

# Crouch
CROUCH_HEIGHT_MULT = 0.5
CROUCH_SPEED_MULT = 0.4

# Down Smash
DOWN_SMASH_FORCE = 20.0
DOWN_SMASH_DAMAGE = 2.0
GROUND_POUND_RADIUS = 50
BOUNCE_HEIGHT = -10.0

# Grapple Hook
GRAPPLE_RANGE = 400
GRAPPLE_SPEED = 25.0
PULL_SPEED = 12.0
GRAPPLE_COOLDOWN = 0.3

# Combat
SWORD_DAMAGE = 1.0
SWORD_RANGE = 40
SWORD_COOLDOWN = 0.3
COMBO_WINDOW = 0.5
MAX_COMBO = 3

SHURIKEN_DAMAGE = 0.5
SHURIKEN_SPEED = 12.0
SHURIKEN_LIFETIME = 2.0
SHURIKEN_COUNT = 10
SHURIKEN_RELOAD_TIME = 5.0

# Invincibility
HURT_INVULN_TIME = 1.0
KNOCKBACK_FORCE = 5.0

# Companion
COMPANION_LIGHT_RADIUS = 150
COMPANION_DAMAGE_REDUCTION = 0.25
COMPANION_HEALTH_REGEN = 1.0

# Player Stats
STARTING_WILL = 10
STARTING_MAX_WILL = 10
STARTING_STRENGTH = 100
STARTING_MAX_STRENGTH = 100

# Consumables
CONSUMABLES = {
    "moment_of_clarity": {
        "name": "Moment of Clarity",
        "description": "A memory of better times. Restores Will.",
        "effect": {"will": 5},
        "max_stack": 10
    },
    "conversation": {
        "name": "Conversation",
        "description": "Words from a friend. Restores Strength.",
        "effect": {"strength": 30},
        "max_stack": 5
    },
    "letter": {
        "name": "Letter",
        "description": "Words from your children. Temporary boost.",
        "effect": {"damage_mult": 1.5, "duration": 30},
        "max_stack": 3
    },
    "hope_fragment": {
        "name": "Hope Fragment",
        "description": "Currency for upgrades.",
        "effect": None,
        "max_stack": 999
    }
}

# Enemy Stats
ENEMY_STATS = {
    "shadow_self": {
        "health": 3,
        "damage": 1,
        "speed": 3.0,
        "detection_radius": 200,
        "attack_range": 40,
        "attack_cooldown": 2.0,
        "behavior": "chase_melee"
    },
    "gatekeeper": {
        "health": 5,
        "damage": 2,
        "speed": 1.0,
        "detection_radius": 150,
        "attack_range": 50,
        "attack_cooldown": 3.0,
        "behavior": "guard_position"
    },
    "echo": {
        "health": 2,
        "damage": 1,
        "speed": 4.0,
        "detection_radius": 250,
        "attack_range": 30,
        "attack_cooldown": 1.5,
        "behavior": "circle_player",
        "respawn_time": 10.0
    },
    "spiral": {
        "health": 4,
        "damage": 0,
        "speed": 2.0,
        "detection_radius": 300,
        "attack_range": 100,
        "behavior": "pull_player"
    },
    "amalgamation": {
        "health": 50,
        "damage": 3,
        "speed": 2.5,
        "detection_radius": 500,
        "attack_range": 60,
        "attack_cooldown": 1.0,
        "behavior": "boss_pattern",
        "phases": 3
    }
}
