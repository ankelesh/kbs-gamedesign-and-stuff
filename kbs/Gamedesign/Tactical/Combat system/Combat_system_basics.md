# TACTICAL COMBAT SYSTEM - PHASE 1 DOCUMENTATION
*Project KBS - Professional Game Design Documentation*

---

## **1. SYSTEM OVERVIEW**

**Purpose:** Resolve turn-based tactical battles between two squads on a hex/square grid battlefield with initiative-driven turn order.

**Scope Boundaries:**
- **Starts:** When strategic map encounter triggers battle
- **Ends:** When one team has zero active units (death/flee)
- **Not Included:** Strategic map movement, unit recruitment, hero inventory management outside battle

**Core Pillars:**
- Initiative-based sequential turns (not simultaneous)
- Action-cost system (abilities define turn-ending behavior)
- Terrain and global buffs affect combat calculations
- Corpse persistence for necromancy/spell targeting

---

## **2. BATTLE INITIALIZATION SEQUENCE**

```
TRIGGER: Strategic encounter → Battle Start
│
├─ STEP 1: Unit Conversion & Spawn
│  ├─ Convert strategic representations to tactical pawns
│  ├─ Instantiate full visual/audio/delegate connections
│  └─ Place units on battlefield (predetermined positions)
│
├─ STEP 2: Terrain Metadata Application
│  ├─ City Defense Buff: +20% to all defense stats (HP excluded)
│  ├─ Territory Initiative Buff: +10% initiative for owner team
│  └─ [Other terrain types apply their buffs]
│
├─ STEP 3: Global Map Buff Processing
│  ├─ Apply pre-battle buffs/debuffs from strategic layer
│  └─ Modifiers persist until battle end
│
├─ STEP 4: Initiative Queue Population
│  ├─ Calculate final initiative values (base + buffs)
│  ├─ Sort units descending (highest initiative first)
│  └─ Create turn order queue
│
└─ STEP 5: First Turn Begins
   └─ Dequeue first unit → Enter Unit Turn Loop
```

---

## **3. CORE COMBAT LOOP** *(The Main Cycle)*

```
┌─────────────────────────────────────────────────────────┐
│                    COMBAT ACTIVE                         │
│  Condition: At least one unit per team exists           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   DEQUEUE NEXT UNIT   │
              │ (Highest initiative)  │
              └───────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │    UNIT TURN START    │
              │  ► Unit Turn Loop     │──┐
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
│  └─ Remove temporary effects (e.g., Defend buff expires)
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
│  │  ├─ Update target markers          │
│  │  └─ Return to Decision Loop ───────┘
│  │
│  ├─ OPTION 2: Inspect Battlefield
│  │  ├─ Right-click enemy units (view stats)
│  │  ├─ No state change               │
│  │  └─ Return to Decision Loop ───────┘
│  │
│  ├─ OPTION 3: Execute Action
│  │  ├─ Player clicks valid target cell
│  │  ├─ Quick-apply check: Self-target? Execute immediately
│  │  ├─ Execute ability logic
│  │  ├─ Play animations/VFX/SFX
│  │  ├─ Apply damage/effects/state changes
│  │  └─ Check action flags:
│  │      ├─ "Ends Turn"? → Exit to Turn End
│  │      └─ "Locks Picking"? → Limit subsequent choices
│  │
│  └─ OPTION 4: Special Actions
│     ├─ WAIT: Re-insert to queue (initiative × -1) → Turn End
│     ├─ DEFEND: Apply 50% damage reduction → Turn End
│     └─ FLEE: Move to "retreated" container → Turn End
│
└─ PHASE D: Turn End
   ├─ Remove unit from active turn state
   ├─ Trigger "On Turn End" effects
   ├─ If unit died during turn: Create corpse entity
   └─ Return to Core Combat Loop
```

---

## **5. ACTION SYSTEM MECHANICS**

### **Action Parameters** *(Every ability has these flags)*

| Parameter | Values | Effect |
|-----------|--------|--------|
| **Ends Turn** | True/False | If True, turn ends immediately after execution |
| **Locks Picking** | True/False | If True, prevents selecting other abilities this turn |
| **Re-pickable** | True/False | If False, cannot be selected again this turn |

### **Action Types & Behaviors:**

| Action Type | Ends Turn | Locks Picking | Re-pickable | Notes |
|------------|-----------|---------------|-------------|-------|
| **Auto-Attack** | ✓ | — | — | Default action, uses weapon specs |
| **Double Attack** | After 2nd hit | ✓ | — | Player picks two targets sequentially |
| **Movement** | ✗ | ✗ | ✗ | Ground: 1 cell, Air: any cell, Layer change: any cell |
| **Use Consumable** | ✗ | ✗ | ✗ (self-lock) | Max 2 per battle, executes + removes from list |
| **Wait** | ✓ | — | — | Re-queues with initiative × (-1) |
| **Defend** | ✓ | — | — | +50% damage reduction until next turn start |
| **Flee** | ✓ | — | — | Unit moved to "retreated" container |
| **Self-Heal** | ✓ | — | — | No targeting required, instant execute |
| **Spell/Ability** | Varies | Varies | Varies | Inherits from attack subtypes |

---

## **6. VICTORY/DEFEAT RESOLUTION**

```
CHECK TRIGGER: After every turn end
│
├─ COUNT ACTIVE UNITS
│  ├─ Team A: Living units on battlefield
│  └─ Team B: Living units on battlefield
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
   └─ Squad SURVIVES (can be moved to safety on strategic map)
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

