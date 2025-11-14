"""
Save and load system for The Hollow Path.
Handles game state persistence with backup support.
"""
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any


class SaveSystem:
    """Handles saving and loading game state"""

    SAVE_DIR = "saves/"
    NUM_SLOTS = 3

    @staticmethod
    def save_game(slot: int, player, world, progress) -> bool:
        """
        Save complete game state to a slot.

        Args:
            slot: Save slot number (0-2)
            player: Player entity
            world: World state
            progress: Progress tracker

        Returns:
            bool: True if save successful
        """
        save_data = {
            "timestamp": datetime.now().isoformat(),
            "playtime": getattr(progress, 'playtime', 0),
            "seed": getattr(world, 'seed', 0),

            "player": {
                "position": {"x": player.pos.x, "y": player.pos.y},
                "current_region": getattr(player, 'current_region', 'the_depths'),
                "will": player.will,
                "max_will": player.max_will,
                "strength": player.strength,
                "max_strength": player.max_strength,
                "abilities": player.abilities,
                "facing_right": player.facing_right
            },

            "inventory": {
                "consumables": getattr(player, 'consumables', {}),
                "currency": getattr(player, 'currency', 0),
                "memory_fragments": getattr(player, 'memory_fragments', [])
            },

            "world": {
                "explored_rooms": getattr(world, 'explored_rooms', []),
                "defeated_enemies": getattr(world, 'defeated_enemies', []),
                "defeated_bosses": getattr(world, 'defeated_bosses', []),
                "collected_items": getattr(world, 'collected_items', [])
            },

            "progress": {
                "completion_percent": getattr(progress, 'completion', 0),
                "deaths": getattr(progress, 'deaths', 0),
                "regions_completed": getattr(progress, 'regions_completed', [])
            }
        }

        os.makedirs(SaveSystem.SAVE_DIR, exist_ok=True)

        filename = f"{SaveSystem.SAVE_DIR}save_slot_{slot}.json"
        backup_filename = f"{SaveSystem.SAVE_DIR}save_slot_{slot}.backup.json"

        # Create backup of existing save
        if os.path.exists(filename):
            try:
                os.replace(filename, backup_filename)
            except Exception as e:
                print(f"Warning: Could not create backup: {e}")

        # Save new data
        try:
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=2)
            print(f"Game saved to slot {slot}")
            return True
        except Exception as e:
            print(f"Save failed: {e}")
            # Restore backup if save failed
            if os.path.exists(backup_filename):
                try:
                    os.replace(backup_filename, filename)
                except Exception:
                    pass
            return False

    @staticmethod
    def load_game(slot: int) -> Optional[Dict[str, Any]]:
        """
        Load game state from a slot.

        Args:
            slot: Save slot number (0-2)

        Returns:
            Dict with save data, or None if load failed
        """
        filename = f"{SaveSystem.SAVE_DIR}save_slot_{slot}.json"

        if not os.path.exists(filename):
            return None

        try:
            with open(filename, 'r') as f:
                save_data = json.load(f)
            return save_data
        except Exception as e:
            print(f"Load failed: {e}")
            # Try to load backup
            backup_filename = f"{SaveSystem.SAVE_DIR}save_slot_{slot}.backup.json"
            if os.path.exists(backup_filename):
                try:
                    with open(backup_filename, 'r') as f:
                        return json.load(f)
                except Exception:
                    pass
            return None

    @staticmethod
    def save_exists(slot: int) -> bool:
        """Check if a save exists in a slot."""
        filename = f"{SaveSystem.SAVE_DIR}save_slot_{slot}.json"
        return os.path.exists(filename)

    @staticmethod
    def get_save_info(slot: int) -> Optional[Dict[str, Any]]:
        """Get save file metadata without loading full save."""
        if not SaveSystem.save_exists(slot):
            return None

        try:
            save_data = SaveSystem.load_game(slot)
            if save_data:
                return {
                    "timestamp": save_data.get("timestamp"),
                    "playtime": save_data.get("playtime", 0),
                    "completion": save_data.get("progress", {}).get("completion_percent", 0),
                    "region": save_data.get("player", {}).get("current_region", "Unknown")
                }
        except Exception:
            pass
        return None

    @staticmethod
    def delete_save(slot: int) -> bool:
        """Delete a save slot."""
        filename = f"{SaveSystem.SAVE_DIR}save_slot_{slot}.json"
        backup_filename = f"{SaveSystem.SAVE_DIR}save_slot_{slot}.backup.json"

        success = False
        try:
            if os.path.exists(filename):
                os.remove(filename)
                success = True
            if os.path.exists(backup_filename):
                os.remove(backup_filename)
        except Exception as e:
            print(f"Delete failed: {e}")
            return False

        return success
