# TACTICAL COMBAT SYSTEM - PHASE 1 DOCUMENTATION
*Project KBS - Professional Game Design Documentation*

---

## **1. SYSTEM OVERVIEW**

**Purpose:** Resolve turn-based tactical battles between two squads on a hex/square grid battlefield with initiative-driven turn order.

**Scope Boundaries:**
- **Starts:** When strategic map encounter triggers battle
- **Ends:** When one team has zero active units (any number of fled / off-fielded is accepted)
- **Not Included:** Strategic map movement, unit recruitment, hero inventory management outside battle

**Core Pillars:**
- Initiative-based sequential turns (not simultaneous)
- Action system (abilities define turn-ending behavior)
- Terrain and global buffs affect combat calculations
- Corpse persistence for necromancy/spell targeting

## **2. BATTLE INITIALIZATION SEQUENCE**

```
TRIGGER: Strategic encounter → Battle Start
│
├─ STEP 1: Unit Conversion & Spawn
│  ├─ Convert strategic representations to tactical pawns (AUnit)
│  ├─ Instantiate full visual/audio/delegate connections 
│  └─ Place units on battlefield (predetermined positions)
│
├─ STEP 2: Terrain Metadata Application
│  ├─ [Some terrain has specific effect, not listed in general buffs]
│  ├─ Example: Territory Initiative Buff: +10% initiative for owner team
│  └─ [Other terrain types apply their buffs]
│
├─ STEP 3: Global Map Buff Processing
│  ├─ Apply pre-battle buffs/debuffs from strategic layer
│  └─ Modifiers persist until battle end (not dispellable)
│
├─ STEP 4: Initiative Queue Population
│  ├─ Calculate final initiative values (modified stat + roll)
│  ├─ Sort units descending (highest initiative first)
│  └─ Create turn order queue
│
└─ STEP 5: First Turn Begins
   └─ Dequeue first unit → Enter Unit Turn Loop
```

## **3. CORE COMBAT LOOP** *(The Main Cycle)*

```
┌──────────────────────────────────────────────────────────────┐
│                    COMBAT ACTIVE                             │
│  Condition: At least one unit per team not dead or off-field │
└──────────────────────────────────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   DEQUEUE NEXT UNIT   │
              │ (Highest initiative)  │──┐
              └───────────────────────┘  │
                          │              │
                          ▼              │
              ┌───────────────────────┐  │
              │    UNIT TURN START    │  │
              │  ► Unit Turn Loop     │  │ 
              └───────────────────────┘  │
                          │              │
                          ▼              │
              ┌───────────────────────┐  │
              │    TURN ENDS          │  │
              │  (Ability executed)   │  │
              └───────────────────────┘  │
                          │              │
                          ▼              │
              ┌───────────────────────┐  │
              │  CHECK VICTORY        │  │
              │  One team eliminated? │  │
              └───────────────────────┘  │
                  │YES          │NO      │
                  ▼             └────────┘
         ┌──────────────┐    (Loop continues)
         │ BATTLE ENDS  │
         │ ► Resolution │
         └──────────────┘
```

---

## **4. UNIT TURN LOOP** *(Sub-loop called each turn)*

```
ENTRY: Unit dequeued from initiative queue
│
├─ PHASE A: Turn Setup
│  ├─ Select default action (first in unit's action list)
│  ├─ Highlight action in UI
│  ├─ Update UI (portrait, stats, frames, team containers)
│  └─ Process on turn start trigger for unit (ticks dependent effects and abilities)
│
├─ PHASE B: Targeting & Validation
│  ├─ Targeting component scans battlefield
│  ├─ Mark valid target cells for current action
│  └─ Enable UI interaction
│
├─ PHASE C: Player Decision Loop ◄─────┐
│  │                                   │
│  ├─ OPTION 1: Change Action          │
│  │  ├─ Player clicks different ability button
│  │  ├─ Check ability availability     │
│  │  ├─ Check if ability can insta-execute (self-targeted), if yes: goto Execute Action
│  │  ├─ Update target markers          │
│  │  └─ Return to Decision Loop ───────┘
│  │
│  ├─ OPTION 2: Inspect Battlefield
│  │  ├─ Right-click enemy units (view stats)
│  │  ├─ No state change                │
│  │  └─ Return to Decision Loop ───────┘
│  │
│  ├─ OPTION 3: Execute Action
│  │  ├─ Player clicks valid target cell
│  │  ├─ Execute ability logic
│  │  ├─ Play animations/VFX/SFX
│  │  ├─ Apply damage/effects/state changes
│  │  └─ Check action flags:
│  │      ├─ "Ends Turn"? → Exit to Turn End
│  │      ├─ "Locks Picking"? → Limit subsequent choices
│  │      ├─ "Locks self"? -> Disable UI button
│  │
│  └─ OPTION 4: Special Actions (default for everyone)
│     ├─ MOVE: Swaps unit with target cell's content -> turn end for default impl
│     ├─ WAIT: Re-insert to queue (initiative × -1) → Turn End for default impl
│     ├─ DEFEND: Apply 50% damage reduction → Turn End for default impl
│     └─ FLEE: Move to "off-field" container → Turn End
│
└─ PHASE D: Turn End
   ├─ Remove unit from active turn state
   ├─ Trigger "On Turn End" effects
   └─ Return to Core Combat Loop
```

---

## **5. ACTION SYSTEM MECHANICS**

### **Action Parameters** *(Every ability has these getters, implementation differs)*

| Getter                   | Values     | Effect |
|--------------------------|------------|--------|
| **Ends Turn**            | True/False | If True, turn ends immediately after execution |
| **Locks Picking**        | True/False | If True, prevents selecting other abilities this turn |
| **Re-pickable**          | True/False | If False, cannot be selected again this turn |

### **Action Types & Behaviors:**
 - (Examples, spreadsheet: )
 - inner calc = parameter is implementation-dependent and can be calculated depending on specific calc
 - inner calc example: double attack has attack counter, which resets in on turn start trigger and decreases on execution

| Action Type        | Ends Turn | Locks Picking | Re-pickable | Notes                                         |
|--------------------|-----------|---------------|-------------|-----------------------------------------------|
| **Auto-Attack**    | ✓         | —             |           — | Default action, uses weapon specs             | 
| **Double Attack**  | inner calc| ✓             | inner calc  | Player picks two targets sequentially         |
| **Movement**       | ✓         | ✗             | ✗           | Ground: 1 cell, Air: any cell, Layer change: any cell |
| **Use Consumable** | ✗         | ✗             | ✗           | Max 2 per battle, executes + removes from list|
| **Wait**           | ✓         | —             | —           | Re-queues with initiative × (-1)              |
| **Defend**         | ✓         | —             | —           | +50% damage reduction until next turn start   |
| **Flee**           | ✓         | —             | —           | Unit moved to "retreated" container           |
| **Self-Heal**      | ✓         | —             | —           | No targeting required, instant execute        |
| **Spell/Ability**  | inner calc| inner calc    | inner calc  | Inherits from attack subtypes                 |

---

## **6. VICTORY/DEFEAT RESOLUTION**

```
CHECK TRIGGER: After every turn end
│
├─ COUNT ACTIVE UNITS
│  ├─ Team A: Living units on battlefield, not in off-field container
│  └─ Team B: Living units on battlefield, not in off-field container
│
├─ IF Team A = 0 AND Team B > 0
│  └─ Team B Wins → Team A Resolution
│
├─ IF Team B = 0 AND Team A > 0
│  └─ Team A Wins → Team B Resolution
│
└─ IF Both Teams > 0
   └─ Continue Combat Loop

LOSER RESOLUTION:
├─ IF all units DIED (no retreated units)
│  └─ Hero + Squad ELIMINATED (permanent loss)
│
└─ IF any units RETREATED
   └─ Squad SURVIVES, strategic unit representation gains 'dead' flag
```

---

## **7. CORPSE SYSTEM**

```
TRIGGER: Unit HP reaches 0
│
├─ CREATE CORPSE ENTITY
│  ├─ Position: Death location (air units fall to ground)
│  ├─ Collision: No (does not block movement)
│  ├─ Stacking: Yes (multiple corpses per cell)
│  └─ Selection priority: Most recent corpse
│
└─ CORPSE USAGE
   └─ Valid target for specific spells (resurrection, necromancy)
```

