"""
World generation settings for The Hollow Path.
Defines regions, generation parameters, and ability gating.
"""

# World Generation
WORLD_GENERATION = {
    "algorithm": "BSP",
    "seed_based": True,
    "total_rooms": 150,
    "world_width": 50,
    "world_height": 50,
    "room_min_size": 5,
    "room_max_size": 12,
    "hallway_width": 2
}

# Region Definitions
REGIONS = {
    "the_depths": {
        "depth_range": (0, 20),
        "room_count": 20,
        "color_palette": "grayscale",
        "enemy_types": ["shadow_self"],
        "save_point_density": 0.1,
        "special_rooms": {
            "ability_room": 1,
            "safe_rooms": 2
        }
    },
    "courtroom_maze": {
        "depth_range": (21, 40),
        "room_count": 30,
        "color_palette": "cold_whites",
        "enemy_types": ["gatekeeper", "echo"],
        "save_point_density": 0.15,
        "special_rooms": {
            "boss_room": 1,
            "ability_room": 1,
            "safe_rooms": 3
        },
        "mechanics": {
            "closing_doors": True,
            "timed_platforms": True,
            "ability_lock_zones": True
        }
    },
    "the_void": {
        "depth_range": (41, 55),
        "room_count": 25,
        "color_palette": "dark_blue",
        "enemy_types": [],
        "save_point_density": 0.05,
        "special_rooms": {
            "ability_room": 1,
            "memory_rooms": 10
        },
        "mechanics": {
            "large_gaps": True,
            "visible_locked_doors": True,
            "distant_sounds": True
        }
    },
    "support_circle": {
        "depth_range": (56, 70),
        "room_count": 15,
        "color_palette": "warm_orange",
        "enemy_types": [],
        "save_point_density": 1.0,
        "special_rooms": {
            "hub_room": 1,
            "npc_rooms": 5,
            "ability_room": 1
        },
        "mechanics": {
            "health_regen": True,
            "fast_travel_hub": True,
            "npc_dialogues": True
        }
    },
    "the_garden": {
        "depth_range": (71, 90),
        "room_count": 25,
        "color_palette": "nature_green",
        "enemy_types": ["shadow_self"],
        "save_point_density": 0.3,
        "special_rooms": {
            "companion_room": 1,
            "ability_room": 1,
            "puzzle_rooms": 5
        }
    },
    "the_bridge": {
        "depth_range": (91, 105),
        "room_count": 15,
        "color_palette": "sunset",
        "enemy_types": [],
        "save_point_density": 0.4,
        "special_rooms": {
            "wedding_room": 1,
            "ability_room": 1,
            "transition_rooms": 5
        }
    },
    "the_watchtower": {
        "depth_range": (106, 150),
        "room_count": 20,
        "color_palette": "bright_sky",
        "enemy_types": ["amalgamation"],
        "save_point_density": 0.5,
        "special_rooms": {
            "final_boss_room": 1,
            "message_rooms": 5,
            "beacon_rooms": 7,
            "ending_room": 1
        }
    }
}

# Ability Gating
ABILITY_GATES = {
    "region_2_entry": ["first_step"],
    "region_3_entry": ["first_step", "wall_climb"],
    "region_4_entry": ["grapple"],
    "region_5_entry": ["dash"],
    "region_6_entry": ["double_jump"],
    "region_7_entry": ["shadow_dash"],
    "void_locked_doors": ["shadow_dash"]
}

# Color Palettes for Regions
COLOR_PALETTES = {
    "grayscale": {
        "background": (30, 30, 35),
        "platform": (60, 60, 65),
        "accent": (80, 80, 90),
        "fog": (40, 40, 45, 128)
    },
    "cold_whites": {
        "background": (200, 200, 210),
        "platform": (180, 180, 190),
        "accent": (150, 150, 160),
        "fog": (220, 220, 230, 64)
    },
    "dark_blue": {
        "background": (10, 15, 30),
        "platform": (20, 25, 50),
        "accent": (30, 40, 80),
        "fog": (15, 20, 40, 192)
    },
    "warm_orange": {
        "background": (80, 50, 30),
        "platform": (120, 80, 50),
        "accent": (200, 120, 60),
        "fog": (100, 60, 30, 32)
    },
    "nature_green": {
        "background": (30, 60, 40),
        "platform": (50, 100, 60),
        "accent": (70, 140, 80),
        "fog": (40, 80, 50, 64)
    },
    "sunset": {
        "background": (100, 60, 80),
        "platform": (150, 90, 110),
        "accent": (200, 120, 140),
        "fog": (120, 70, 90, 48)
    },
    "bright_sky": {
        "background": (135, 206, 235),
        "platform": (100, 150, 200),
        "accent": (70, 120, 180),
        "fog": (160, 220, 255, 32)
    }
}
