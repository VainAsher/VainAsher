"""
Inventory system for The Hollow Path.
Manages consumables, memory fragments, and items.
"""
from typing import Dict, List, Optional
from config.game_balance import CONSUMABLES


class Inventory:
    """Player inventory system"""

    def __init__(self, player):
        self.player = player

        # Consumables (quick slots)
        self.consumables: Dict[str, Optional[dict]] = {
            "slot_1": None,
            "slot_2": None,
            "slot_3": None,
            "slot_4": None
        }

        # Currency
        self.hope_fragments = 0

        # Memory Fragments collected
        self.memory_fragments: List[str] = []

        # Key items
        self.key_items: List[str] = []

        # Consumable stacks
        self.consumable_stacks: Dict[str, int] = {}

    def add_consumable(self, consumable_id: str, slot: Optional[str] = None):
        """
        Add a consumable to inventory.

        Args:
            consumable_id: ID of consumable (from CONSUMABLES config)
            slot: Specific slot to add to, or None for first empty
        """
        if consumable_id not in CONSUMABLES:
            return False

        # Add to stack
        max_stack = CONSUMABLES[consumable_id]["max_stack"]
        current = self.consumable_stacks.get(consumable_id, 0)
        if current >= max_stack:
            return False  # Stack full

        self.consumable_stacks[consumable_id] = current + 1

        # Assign to slot if specified or find empty slot
        if slot and slot in self.consumables:
            self.consumables[slot] = {"id": consumable_id, "count": 1}
        else:
            for s in ["slot_1", "slot_2", "slot_3", "slot_4"]:
                if self.consumables[s] is None:
                    self.consumables[s] = {"id": consumable_id, "count": 1}
                    break

        return True

    def use_consumable(self, slot: str):
        """Use a consumable from a slot"""
        if slot not in self.consumables or not self.consumables[slot]:
            return False

        item_data = self.consumables[slot]
        consumable_id = item_data["id"]

        if consumable_id not in CONSUMABLES:
            return False

        # Apply effects
        effect = CONSUMABLES[consumable_id]["effect"]
        if effect:
            self.apply_consumable_effect(effect)

        # Decrease stack
        stack_count = self.consumable_stacks.get(consumable_id, 0)
        if stack_count > 0:
            self.consumable_stacks[consumable_id] = stack_count - 1

        # Remove from slot if no more
        if self.consumable_stacks[consumable_id] <= 0:
            self.consumables[slot] = None

        return True

    def apply_consumable_effect(self, effect: dict):
        """Apply consumable effects to player"""
        if "will" in effect:
            self.player.will = min(
                self.player.will + effect["will"],
                self.player.max_will
            )

        if "strength" in effect:
            self.player.strength = min(
                self.player.strength + effect["strength"],
                self.player.max_strength
            )

        if "damage_mult" in effect:
            duration = effect.get("duration", 30)
            if hasattr(self.player, 'combat'):
                self.player.combat.apply_buff(effect["damage_mult"], duration)

    def add_memory_fragment(self, fragment_id: str):
        """Add a memory fragment to collection"""
        if fragment_id not in self.memory_fragments:
            self.memory_fragments.append(fragment_id)
            return True
        return False

    def has_memory_fragment(self, fragment_id: str) -> bool:
        """Check if player has a memory fragment"""
        return fragment_id in self.memory_fragments

    def add_key_item(self, item_id: str):
        """Add a key item"""
        if item_id not in self.key_items:
            self.key_items.append(item_id)
            return True
        return False

    def has_key_item(self, item_id: str) -> bool:
        """Check if player has a key item"""
        return item_id in self.key_items

    def add_hope_fragments(self, amount: int):
        """Add hope fragments (currency)"""
        self.hope_fragments += amount

    def spend_hope_fragments(self, amount: int) -> bool:
        """Spend hope fragments"""
        if self.hope_fragments >= amount:
            self.hope_fragments -= amount
            return True
        return False

    def get_memory_count(self) -> int:
        """Get total memory fragments collected"""
        return len(self.memory_fragments)

    def get_completion_percentage(self) -> float:
        """Calculate inventory completion percentage"""
        total_memories = 10  # Total memory fragments in game
        total_key_items = 5  # Total key items

        memories_pct = (len(self.memory_fragments) / total_memories) * 50
        items_pct = (len(self.key_items) / total_key_items) * 50

        return memories_pct + items_pct
