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
- **S** - Crouch / Down Smash (in air)
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

## Player Mechanics Guide

### Movement Abilities

#### Wall Jump
- **How to use**: While touching a wall, press SPACE to jump away from it
- **Visual indicator**: When touching a wall, you'll stick briefly - this is your window to wall jump
- **Tips**:
  - You can chain wall jumps between two walls to climb vertical shafts
  - Wall jumping resets your double jump ability
  - The wall kick provides both horizontal and vertical momentum

#### Dash
- **How to use**: Press LEFT SHIFT to dash in the direction you're facing
- **Duration**: 0.4 seconds (default, configurable in options)
- **Speed multiplier**: 2.5x (configurable in options)
- **Features**:
  - Provides invulnerability during dash
  - Can be used in air or on ground
  - Short cooldown between dashes
  - Dash through gaps and over obstacles

#### Shadow Dash
- **How to use**: Press Q to perform an enhanced dash that phases through obstacles
- **Duration**: 0.5 seconds (default, configurable in options)
- **Speed multiplier**: 3.5x (configurable in options)
- **Features**:
  - Phase through purple shadow walls
  - Pass through enemies while phasing
  - Longer duration than regular dash
  - Visual indicator: purple aftereffect while phasing

#### Grapple Hook
- **How to use**: Press E to grapple to yellow grapple points
- **Range**: 400 pixels
- **Visual indicators**:
  - Yellow grapple points pulse when in range
  - Targeting reticle appears on aimable points
  - Crosshair intensity increases as you get closer
- **Tips**:
  - Grapple pulls you toward the point automatically
  - Releases when you get close enough
  - Can be chained between multiple grapple points

#### Down Smash
- **How to use**: While in the air, press S (crouch) to slam downward
- **Features**:
  - Destroys breakable platforms (brown colored tiles)
  - Creates a shockwave on impact
  - Deals damage to enemies in area
- **Visual indicators**:
  - Purple circle shows impact area while falling
  - Breakable tiles highlighted with red X pattern
  - Shows predicted landing location

### Combat System

#### Attack Range Indicators
- **Red outline**: Enemy is in attack range - ready to strike!
- **Red triangle above enemy**: Attack indicator - this enemy can be hit
- **Yellow outline**: Enemy is nearby but not quite in range yet
- **Range**: 40 pixels for sword attacks

### Options Menu Features

Access the options menu via **ESC → Options**. The menu has three categories:

#### Audio & Display
- **Music Volume**: Adjust background music level (0-100%)
- **SFX Volume**: Adjust sound effects volume (0-100%)
- **Fullscreen**: Toggle fullscreen mode

#### Player Mechanics
Fine-tune your gameplay experience:
- **Player Speed** (0.5x - 2.0x): Adjust base movement speed
- **Jump Height** (0.5x - 2.0x): Modify jump force
- **Dash Speed** (0.5x - 3.0x): Change dash speed multiplier
- **Shadow Dash Speed** (0.5x - 3.0x): Adjust shadow dash speed
- **Dash Duration** (0.5x - 3.0x): Lengthen or shorten dash time
- **Shadow Dash Duration** (0.5x - 3.0x): Modify shadow dash duration
- **Reset to Defaults**: Restore all mechanics to default values

#### Difficulty
- **Difficulty Level**: Affects enemy health and damage
  - Easy (0.5x): Half damage and enemy health
  - Normal (1.0x): Balanced experience
  - Hard (1.5x): Increased challenge
  - Very Hard (2.0x): Double damage and enemy health

## Test Level Walkthrough

The test level is designed to introduce each ability systematically. Here's what to expect:

### Section 1: Spawn & Basic Jump (Start)
**Location**: Starting area
**Ability Unlocked**: First Step (Basic Jump)
**Objective**: Practice jumping across platforms
**Collectibles**: 3 consumables (health potions)
**Expected Results**:
- Successfully jump from starting platform to elevated platforms
- Collect consumables by jumping to them
- Learn basic movement and jump timing

### Section 2: Double Jump Test
**Location**: High platforms
**Ability Unlocked**: Double Jump (found at ability pickup)
**Objective**: Reach platforms too high for single jump
**Collectibles**: 1 ability pickup, 1 consumable
**Expected Results**:
- Grab the orange ability pickup to unlock Double Jump
- Press SPACE twice to reach the highest platform
- Notice how double jump gives you extra height and air control

### Section 3: Wall Climb
**Location**: Tall wall section
**Ability Unlocked**: Wall Climb/Jump (found at ability pickup)
**Objective**: Scale vertical walls and navigate narrow shafts
**Collectibles**: 1 ability pickup, 1 consumable
**Expected Results**:
- Slide down walls by touching them while falling
- Press SPACE while on wall to jump away from it
- Chain wall jumps between two walls in the narrow shaft
- Successfully reach the platform at the top

### Section 4: Dash Course
**Location**: Gap with spike pit
**Ability Unlocked**: Dash (found at ability pickup)
**Objective**: Cross the 5-tile gap using dash
**Collectibles**: 1 ability pickup, 1 consumable
**Hazards**: Spike pit (visual indicator)
**Expected Results**:
- Collect the dash ability
- Press LEFT SHIFT to dash across the gap
- Notice the invulnerability during dash
- Land safely on the far platform

### Section 5: Shadow Dash / Phase
**Location**: Purple shadow wall barrier
**Ability Unlocked**: Shadow Dash (found at ability pickup)
**Objective**: Phase through the impassable shadow wall
**Collectibles**: 1 ability pickup, 1 consumable
**Expected Results**:
- Regular dash cannot pass through the purple walls
- Press Q to activate Shadow Dash
- Notice the phasing effect as you pass through the purple shadow walls
- Feel the increased speed and duration compared to regular dash

### Section 6: Grapple Points
**Location**: Open area with yellow grapple anchors
**Ability Unlocked**: Grapple Hook (found at ability pickup)
**Objective**: Use grapple points to cross the gap
**Collectibles**: 1 ability pickup, 1 consumable
**Visual Indicators**: Yellow grapple points with targeting reticle
**Expected Results**:
- Notice yellow grapple points highlighting when in range
- Press E to grapple to the highlighted point
- Get pulled automatically toward the grapple point
- Chain grapples between multiple points to cross the area

### Section 7: Down Smash Test
**Location**: High platform above breakable blocks
**Ability Unlocked**: Down Smash (found at ability pickup)
**Objective**: Break through brown breakable platforms
**Collectibles**: 1 ability pickup, 1 consumable (hidden under breakable block)
**Expected Results**:
- Jump to the high platform and collect the ability
- While in the air, press S to perform Down Smash
- See the purple impact circle and red X indicators on breakable tiles
- Smash through brown breakable platforms
- Reveal the hidden consumable beneath the broken tiles
- Create a shockwave on impact

### Section 8: Crouch Tunnel
**Location**: Low-ceiling passage
**Objective**: Navigate through tight spaces
**Collectibles**: 2 consumables
**Expected Results**:
- Press S while on ground to crouch
- Notice movement speed reduction while crouching
- Successfully navigate under the low ceiling
- Collect consumables in the tunnel

### Section 9: Combat Arena
**Location**: Large open area with obstacles
**Objective**: Practice combat against multiple enemies
**Enemies**: Shadow Self, Gatekeeper
**Collectibles**: 2 consumables, save point
**Expected Results**:
- See red outlines on enemies in attack range
- Use LEFT CLICK to perform sword attacks
- Use RIGHT CLICK to throw shurikens
- Notice attack indicators above targetable enemies
- Combine movement abilities to dodge and reposition
- Use obstacles for cover

### Save Points
Located at:
- Section 1 (Start area)
- Section 4 (Dash course)
- Section 9 (Combat arena)

**Green tiles** indicate save points where progress can be saved.

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
