"""
Runtime settings that can be modified during gameplay.
These values override the defaults in game_balance.py
"""

# Audio Settings
music_volume = 0.7
sfx_volume = 0.8
fullscreen = False

# Player Mechanics Multipliers
player_speed_multiplier = 1.0
jump_force_multiplier = 1.0
dash_speed_multiplier = 1.0
shadow_dash_speed_multiplier = 1.0
dash_duration_multiplier = 1.0
shadow_dash_duration_multiplier = 1.0

# Difficulty Settings
difficulty_multiplier = 1.0  # Affects enemy health and damage
# 0.5 = Easy, 1.0 = Normal, 1.5 = Hard, 2.0 = Very Hard


def get_player_speed():
    """Get modified player speed"""
    from config.game_balance import PLAYER_SPEED
    return PLAYER_SPEED * player_speed_multiplier


def get_jump_force():
    """Get modified jump force"""
    from config.game_balance import JUMP_FORCE
    return JUMP_FORCE * jump_force_multiplier


def get_dash_speed_mult():
    """Get modified dash speed multiplier"""
    from config.game_balance import DASH_SPEED_MULTIPLIER
    return DASH_SPEED_MULTIPLIER * dash_speed_multiplier


def get_shadow_dash_speed_mult():
    """Get modified shadow dash speed multiplier"""
    from config.game_balance import SHADOW_DASH_SPEED_MULTIPLIER
    return SHADOW_DASH_SPEED_MULTIPLIER * shadow_dash_speed_multiplier


def get_dash_duration():
    """Get modified dash duration"""
    from config.game_balance import DASH_DURATION
    return DASH_DURATION * dash_duration_multiplier


def get_shadow_dash_duration():
    """Get modified shadow dash duration"""
    from config.game_balance import SHADOW_DASH_DURATION
    return SHADOW_DASH_DURATION * shadow_dash_duration_multiplier


def reset_to_defaults():
    """Reset all settings to default values"""
    global player_speed_multiplier, jump_force_multiplier
    global dash_speed_multiplier, shadow_dash_speed_multiplier
    global dash_duration_multiplier, shadow_dash_duration_multiplier
    global difficulty_multiplier

    player_speed_multiplier = 1.0
    jump_force_multiplier = 1.0
    dash_speed_multiplier = 1.0
    shadow_dash_speed_multiplier = 1.0
    dash_duration_multiplier = 1.0
    shadow_dash_duration_multiplier = 1.0
    difficulty_multiplier = 1.0
