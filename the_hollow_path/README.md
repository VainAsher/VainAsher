# The Hollow Path

A 2D Metroidvania platformer exploring themes of personal struggle, mental health, and recovery.

## ⚠️ Content Warning

This game contains themes of:
- Depression and mental health challenges
- Loss and separation from loved ones
- Institutional obstacles and legal challenges
- Recovery and hope

**Player discretion advised.**

### Mental Health Resources

If you or someone you know is struggling:
- **988 Suicide & Crisis Lifeline (US)**: Call or Text 988
- **Crisis Text Line**: Text HOME to 741741
- **International**: Visit [findahelpline.com](https://findahelpline.com)

## Story

Navigate a symbolic labyrinth representing the journey from darkness to light. Play as a father separated from his children, battling through depression, legal systems, and loss, finding support in community (Andy's Man Club), new love, and hope for the future.

## Installation

### Requirements
- **Python 3.8 or higher**
- **Ubuntu Linux** (tested on 24.04, works on Proxmox VM)
- **Pygame 2.5+**

### Setup

```bash
cd the_hollow_path
pip install -r requirements.txt
python main.py
```

Or make it executable:

```bash
chmod +x main.py
./main.py
```

## Controls

### Movement
- **A / D** - Move left/right
- **SPACE** - Jump (unlocked: First Step)
- **S** - Crouch
- **LEFT SHIFT** - Dash (unlocked ability)
- **Q** - Shadow Dash (unlocked ability)
- **E** - Grapple Hook (unlocked ability)

### Combat
- **LEFT CLICK** - Sword attack
- **RIGHT CLICK** - Throw shuriken
- **C** - Call companion (after acquiring cat)

### Consumables
- **1 / 2 / 3 / 4** - Quick-use items in slots
- **TAB** - Radial menu (hold)

### Menus
- **I** - Memories (inventory/collectibles)
- **M** - Journey (map)
- **ESC** - Pause menu

### Debug (for development/testing)
- **F1** - Toggle hitbox display
- **F2** - Toggle FPS counter
- **F3** - Toggle god mode
- **F6** - Unlock all abilities

## Gameplay

### Seven Regions

Journey through symbolic regions representing emotional recovery:

1. **The Depths** - Depression, crisis, isolation (grayscale)
2. **The Courtroom Maze** - Legal battles, bureaucracy (cold whites)
3. **The Void** - Loss, separation from children (dark blue, sparse)
4. **The Support Circle** - Andy's Man Club, healing (warm orange, safe hub)
5. **The Garden** - New relationship, partnership (green, companion acquired)
6. **The Bridge** - Wedding, commitment, transition (sunset colors)
7. **The Watchtower** - Hope, future, giving back (bright sky)

### Abilities

Unlock 8 abilities representing personal growth:

- **First Step** - Basic jump (seeking help)
- **Wall Climb** - Persistence through obstacles
- **Double Jump** - Support lifting you higher
- **Dash** - Resilience, pushing through
- **Shadow Dash** - Moving through pain without being trapped
- **Grapple** - Reaching for distant connections (hope)
- **Down Smash** - Using your struggles as strength

### Stats

- **Will** - Health, your emotional resilience
- **Strength** - Energy/stamina for abilities
- **Hope Fragments** - Currency for upgrades

### Features

- **Procedurally Generated Worlds** - Each playthrough creates a unique layout
- **Ability-Gated Progression** - Unlock new areas with new abilities
- **Memory Fragments** - Collectible story pieces (found in The Void)
- **Companion System** - Cat provides light, damage reduction, healing
- **Multiple Endings** - Beacon path, Archive path, or True Ending
- **Save System** - Three save slots with auto-backup

## Development Status

This is a complete, playable prototype featuring:
- ✅ Full player movement with all 8 abilities
- ✅ Combat system (melee + ranged)
- ✅ Enemy AI with multiple types
- ✅ Companion system (cat)
- ✅ Save/Load system
- ✅ Content warning screen
- ✅ HUD and menus
- ✅ Debug tools
- ⏳ Procedural world generation (basic tilemap implemented)
- ⏳ All 7 regions with unique themes (placeholders active)
- ⏳ Narrative system (Memory Fragments, NPCs, cutscenes)
- ⏳ Audio system (music and SFX)
- ⏳ Particle effects

## Architecture

Built with a modular, component-based architecture:
- **Entity-Component System** - Flexible, reusable components
- **State Machines** - Player and enemy behavior
- **Event System** - Decoupled game events
- **Config-Driven** - All tunables in config files
- **Save System** - JSON-based with backup support

## License

MIT License - See LICENSE file for details

## Credits

### Inspiration
- **Andy's Man Club** - Real support group for men's mental health
- Personal experiences with custody battles, depression, and recovery

### Development
- **Engine**: Pygame 2.5+
- **Language**: Python 3.8+
- **Art**: Placeholder colored rectangles (awaiting sprite assets)
- **Music**: Placeholders (awaiting audio assets)

## Contributing

This is a personal project, but feedback and suggestions are welcome.
Please respect the sensitive nature of the themes explored.

## Support

For issues, feedback, or questions:
- Open an issue on the repository
- Remember: This is a game about hope. If you're struggling, please reach out for real help.

---

*"They'll find their way to you. When they're ready, you'll be here."*
