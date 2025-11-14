"""
Progression tracking system for The Hollow Path.
Tracks player progress, achievements, and completion.
"""
from typing import List, Set
import time


class ProgressionTracker:
    """Tracks player progression through the game"""

    def __init__(self):
        # Time tracking
        self.playtime = 0.0  # Total playtime in seconds
        self.session_start = time.time()

        # Deaths
        self.deaths = 0

        # Regions
        self.current_region = "the_depths"
        self.regions_visited: Set[str] = {"the_depths"}
        self.regions_completed: Set[str] = set()

        # Abilities unlocked
        self.abilities_unlocked: Set[str] = set()

        # Bosses defeated
        self.bosses_defeated: Set[str] = set()

        # Rooms explored
        self.rooms_explored: Set[int] = set()
        self.total_rooms = 150

        # NPCs met
        self.npcs_met: Set[str] = set()

        # Endings achieved
        self.beacon_path_complete = False
        self.archive_path_complete = False
        self.true_ending_achieved = False

        # Statistics
        self.enemies_defeated = 0
        self.damage_taken = 0.0
        self.damage_dealt = 0.0
        self.distance_traveled = 0.0

    def update_playtime(self):
        """Update total playtime"""
        current_time = time.time()
        self.playtime += current_time - self.session_start
        self.session_start = current_time

    def visit_region(self, region_name: str):
        """Mark a region as visited"""
        self.current_region = region_name
        self.regions_visited.add(region_name)

    def complete_region(self, region_name: str):
        """Mark a region as completed"""
        self.regions_completed.add(region_name)

    def unlock_ability(self, ability_name: str):
        """Track ability unlock"""
        self.abilities_unlocked.add(ability_name)

    def defeat_boss(self, boss_id: str):
        """Track boss defeat"""
        self.bosses_defeated.add(boss_id)

    def explore_room(self, room_id: int):
        """Mark a room as explored"""
        self.rooms_explored.add(room_id)

    def meet_npc(self, npc_id: str):
        """Track NPC encounter"""
        self.npcs_met.add(npc_id)

    def player_died(self):
        """Increment death counter"""
        self.deaths += 1

    def enemy_defeated(self):
        """Increment enemy defeat counter"""
        self.enemies_defeated += 1

    def track_damage_taken(self, amount: float):
        """Track damage taken"""
        self.damage_taken += amount

    def track_damage_dealt(self, amount: float):
        """Track damage dealt"""
        self.damage_dealt += amount

    def calculate_completion(self) -> float:
        """
        Calculate overall game completion percentage.

        Returns:
            float: Completion percentage (0-100)
        """
        total_score = 0.0
        max_score = 0.0

        # Regions (30 points)
        total_score += len(self.regions_completed) * (30 / 7)
        max_score += 30

        # Abilities (20 points)
        total_score += len(self.abilities_unlocked) * (20 / 8)
        max_score += 20

        # Bosses (15 points)
        total_score += len(self.bosses_defeated) * (15 / 2)
        max_score += 15

        # Rooms explored (20 points)
        total_score += (len(self.rooms_explored) / self.total_rooms) * 20
        max_score += 20

        # NPCs (10 points)
        total_score += len(self.npcs_met) * (10 / 5)
        max_score += 10

        # Endings (5 points)
        if self.beacon_path_complete or self.archive_path_complete:
            total_score += 2.5
        if self.true_ending_achieved:
            total_score += 2.5
        max_score += 5

        return (total_score / max_score) * 100 if max_score > 0 else 0

    def get_playtime_formatted(self) -> str:
        """Get playtime as formatted string"""
        hours = int(self.playtime // 3600)
        minutes = int((self.playtime % 3600) // 60)
        seconds = int(self.playtime % 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def get_stats_summary(self) -> dict:
        """Get summary of player statistics"""
        return {
            "playtime": self.get_playtime_formatted(),
            "completion": f"{self.calculate_completion():.1f}%",
            "deaths": self.deaths,
            "regions_completed": f"{len(self.regions_completed)}/7",
            "abilities_unlocked": f"{len(self.abilities_unlocked)}/8",
            "bosses_defeated": f"{len(self.bosses_defeated)}/2",
            "rooms_explored": f"{len(self.rooms_explored)}/{self.total_rooms}",
            "npcs_met": f"{len(self.npcs_met)}/5",
            "enemies_defeated": self.enemies_defeated,
        }
