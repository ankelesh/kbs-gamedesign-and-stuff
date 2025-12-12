# TACTICAL COMBAT SYSTEM - PHASE 3: ADVANCED MECHANICS
*Project KBS - Game Design Documentation*

---

## **1. INITIATIVE SYSTEM - COMPLETE MECHANICS**

### **Base Initiative Resolution**

```
Turn Order Priority:
1. Higher Initiative value goes first
2. If tied → Attacker team goes first
3. If same team → Higher BASE initiative stat (ignore buffs)
4. If still tied → Implementation-dependent (sorting algorithm)

Example:
├─ Attacker Unit A: Initiative 50
├─ Defender Unit B: Initiative 50
└─ Resolution: Unit A acts first (attacker priority)

Example (Same Team):
├─ Attacker Unit A: Initiative 50 (base 40 + buff)
├─ Attacker Unit B: Initiative 50 (base 50)
└─ Resolution: Unit B acts first (higher base stat)
```

### **Wait Mechanic - Deep Dive**

#### **Initiative Negation**
```
Mechanism: Initiative value inverted to negative
Formula: WaitedInitiative = -(CurrentInitiative)

Example:
├─ Unit with Initiative 50 waits
├─ New effective initiative: -50
└─ Moves to end of queue (all positive values > negative)

Wait Queue Sorting:
├─ Positive initiatives processed first (50, 45, 40...)
├─ Then negative initiatives in descending order (-10, -30, -50...)
└─ Higher negative = acted later (-10 goes before -50)
```

#### **Multiple Units Waiting**
```
Process: Inserted one-by-one with queue resort each time

Example Timeline:
Turn 1: Queue = [50, 45, 40, 35]
├─ Unit(50) acts normally
├─ Unit(45) waits → Queue resorts to [40, 35, -45]
├─ Unit(40) waits → Queue resorts to [35, -40, -45]
└─ Unit(35) acts normally → Then Unit(-40) → Then Unit(-45)
```

#### **Wait Restrictions**
```
Self-Locking: After using Wait, ability locks for that turn
├─ Unit cannot Wait → still in queue → Wait again
└─ Wait becomes available again next turn

No Value Reroll:
├─ Initiative value is NOT recalculated when waiting
├─ Uses the EFFECTIVE value at time of wait
└─ Buffs/debuffs applied before wait persist in negative value
```

### **Initiative Modification During Combat**

#### **Mid-Turn Modifications**
```
Quemin Chain Example: Defend grants +20 Initiative
├─ Effect applies AFTER Defend action resolves (turn ended)
├─ Does NOT reshuffle current turn queue
└─ Takes effect on NEXT turn's queue generation

Timing:
Turn N: Unit Defends → Gains +20 Initiative buff
Turn N+1: New queue generated → Unit sorted with modified initiative
```

#### **Initiative Gain Triggers Queue Resort**
```
Trigger Conditions:
├─ Long-duration buff applied mid-battle on unit who still can act

Behavior:
├─ Queue immediately resorts with new values
├─ Already-acted units remain marked as acted
└─ Current unit will still end it's turn normally (resorted queue will be popped normally)
```

---

## **2. MULTI-TARGET & AREA ABILITIES**

### **Target Reach Types - Complete Specification**

| Reach Type               | # Targets             | Selection Rule        | Notes                                        |
|--------------------------|-----------------------|-----------------------|----------------------------------------------|
| **AnyEnemy**             | 1                     | Manual                | Standard single-target                       |
| **ClosestEnemies**       | 1                     | Manual (adjacent only)| Standard close-combat                        |
| **AllEnemies**           | All living enemies    | Automatic.            | Implementation order from team container     |
| **Area**                 | Shape                 | Manual (anchor point) | DataAsset defines shape                      |
| **AnyFriendly**          | 1                     | Manual                | Support abilities                            |
| **AllFriendlies**        | All living allies     | Automatic             | Buff/heal abilities                          |
| **EmptyCell**            | 0 (position)          | Manual                | Summon/movement abilities                   |
| **EmptyCellOrFriendly**  | 0 or 1                | Manual                | Swap/teleport abilities                      |

### **Area Shape System**

```cpp
FAreaShape Definition:
├─ RelativeCells: Array of FIntPoint offsets from anchor
├─ bAffectsAllLayers: Hit ground + air simultaneously?
└─ Anchor: Player-selected target cell

Example - Cross Pattern:
RelativeCells = [
    (0, 0),   // Center
    (-1, 0),  // Left
    (1, 0),   // Right
    (0, -1),  // Up
    (0, 1)    // Down
]

Example - Line (3 cells forward):
RelativeCells = [(0, 1), (0, 2), (0, 3)]
```

### **Multi-Target Hit Resolution**

#### **Damage Application Order**
```
Process: Implementation-dependent (team container array order)

Pseudo-Code:
1. Collect all valid targets in array
2. FOR EACH target IN array:
   ├─ Calculate damage
   ├─ Apply damage
   ├─ Check death
   └─ If dead → Emit UnitDied signal
3. Grid orchestrator handles corpse spawning AFTER all hits

Important: Corpses spawn AFTER all damage is resolved
├─ AoE hits 3 units, kills all 3
├─ All damage applied first
└─ Then 3 corpses spawn simultaneously
```

#### **Effect Application**
```
Timing: All effects applied simultaneously
Order: Implementation-dependent (array iteration order)
Deduplication: Standard effect stacking rules apply

Example - AoE Poison:
├─ Hits 5 targets
├─ All 5 get poison effect (from same DataAsset)
├─ If target already has poison from THIS DataAsset → refresh/replace
└─ If target has poison from DIFFERENT DataAsset → both stack
```

## **3. ANIMATION & TIMING SYSTEM**

### **Animation Architecture**

#### **Blocking vs Non-Blocking Categories**

**BLOCKING Animations** (combat waits for completion):
```
Attack Animations:
├─ Weapon swing/thrust
├─ Projectile travel
├─ Spell cast visuals
└─ Ultimate ability sequences

Death Animations:
├─ Unit collapse/fade
├─ Corpse spawn
└─ Provides dramatic weight + clarity


Movement Animations:
├─ Unit(s) move simultaneously in target cells
```

**NON-BLOCKING Animations** (overlap/parallel):
```
Hit Reactions:
├─ Quick flinch/stagger
├─ Damage number popups (if implemented)
└─ Maintains combat pace

Passive Visuals:
├─ Status effect particles
```

### **Turn Execution Timeline**

```
PLAYER PHASE:
├─ Player gets control over unit (UI and highlighting activates)
├─ Player selects action (UI active)
├─ Player selects target (UI active)
└─ Confirms selection

EXECUTION PHASE:
├─ UI locks (no further input)
├─ Action validation runs
├─ Animation launches (BLOCKING)
│  ├─ Attack animation plays
│  ├─ Projectile travels (if ranged)
│  └─ Impact occurs
├─ Damage calculation executes
├─ Hit reaction plays (NON-BLOCKING)
├─ Effects apply
├─ Death check
│  └─ If dead: Death animation plays (BLOCKING)
└─ Turn end triggers

QUEUE ADVANCE:
├─ Next unit dequeued
└─ Return to PLAYER PHASE
```

### **Animation Speed Controls**

```
Base Speed: 1.0x (cinematic, default)
Optional Speeds: 1.5x, 2x, 3x
Implemented later
```


## **4. COMPLEX INTERACTION SCENARIOS**

### **Scenario A: Phylactery Management**

```
Phylactery Assignment:
├─ Costs: NO ACTION (free ability use)
├─ Timing: Can be used during Lich's turn
└─ Limit: ONE phylactery total (no spares)

Case 1: Phylactery Holder Dies
├─ Phylactery destroyed
├─ Lich DOES NOT die immediately
├─ Lich's "Revival" passive ability locks
└─ If Lich dies → Permanent death (no revive)

Case 2: Lich not using assignment
├─ Gains HP buff
├─ Gains ONE guaranteed revival (other effect)
├─ Second death → Permanent death

Case 3: Second Reassignment
├─ NOT POSSIBLE
├─ Once assigned, phylactery cannot be moved
└─ Lasts entire battle

Revival Mechanics:
├─ Trigger: Lich HP reaches 0 with valid phylactery
├─ Effect: Revive at 50% HP immidiately
├─ Position: Same cell
└─ Phylactery consumed after revival
```

### **Scenario B: Ghost Derealization Timing**

```
Key Constraint: Ghost can ONLY derealize on own turn

Case: Enemy casts AoE "AllEnemies"
├─ Enemy's turn → Selects ability
├─ Target validation: Polls team container for living enemies
├─ Ghost is ON battlefield during enemy turn
└─ Ghost is valid target → Gets hit

Invalid Scenario (Ghost already derealized):
├─ Ghost used Derealize on previous turn
├─ Ghost not on battlefield
├─ Enemy casts AoE
├─ Target validation: Ghost not in team container
└─ Ghost not hit

Timing Diagram:
Turn 1: Ghost derealizes (leaves battlefield)
Turn 2: Enemy casts AoE → Ghost not valid target
Turn 3: Ghost can reappear on own turn
```

### **Scenario C: Borrowed Time + Multi-Hit**

```
"Living on Borrowed Time" Mechanic:
├─ Passive ability triggers on lethal damage
├─ BLOCKS death handler
├─ Unit survives at negative HP
└─ Death only checked on turn END

Multi-Hit Resolution:
Attack 1:
├─ Devourer at 100 HP
├─ Takes 150 damage → Now -50 HP
├─ Borrowed Time triggers → Blocks death
└─ Devourer survives (still at -50 HP)

Devourer's Next Attack (before turn ends):
├─ Attacks enemy, deals 60 damage
├─ Vampirism: Heals 30 HP (50% of damage)
├─ HP: -50 + 30 = -20 HP
└─ Still alive (turn hasn't ended)

Counterattack (same turn):
├─ Devourer at -20 HP
├─ Takes 40 damage → Now -60 HP
└─ Still survives (turn hasn't ended)

Turn End Check:
├─ Borrowed Time passive triggers
├─ Checks HP: -60 HP
├─ HP < 0 → Death handler executes
└─ Devourer dies

Survival Condition:
├─ Must heal above 0 HP before turn ends
└─ Multiple attacks CAN be survived if healing between
```

## **5. ABILITY CHARGE SYSTEMS - ADVANCED**

### **Salvo Initiative Manipulation**

```
Mechanism: Best roll distribution

Detailed Example:
Initial State:
├─ Musketeer A: Initiative 45 (rolled)
├─ Musketeer B: Initiative 50 (rolled) ← Best
├─ Musketeer C: Initiative 47 (rolled)
└─ All are identical unit type

Trigger: Musketeer B acts (Initiative 50)
Process:
1. Identify all identical units who haven't acted
2. Set ALL their initiatives to own
3. Queue processes remaining units

Result Queue:
├─ [50, 50, 50] → All Musketeers fire in sequence
└─ Overrides original initiative spread

Important: Not true simultaneity
├─ Still sequential execution
├─ Each attack resolves fully before next
└─ Allows for tactical targeting changes
```

### **Reload Mechanics - Timing**

```
Standard Reload:
├─ Costs: Full turn (ends turn immediately)
├─ Effect: Restores charges to max
└─ Vulnerable: Unit cannot defend while reloading, effectively skipping turn

Engineer-Assisted Reload:
├─ Engineer's Action: Target ally unit
├─ Cost: Engineer's full turn
├─ Effect: Target's charges restored
├─ Target: Can act normally on their turn
└─ Tactical: Allows high-value units to maintain DPS

Restriction:
├─ Cannot reload self + attack same turn
```

### **Demonic Charge Transfer**

```
Demonomancer Actions:
1. Drain Charges
   ├─ Target: Allied unit with demonic charges
   ├─ Effect: Removes X charges, stores in Demonomancer
   └─ Cost: Does NOT end turn (stackable). Locks itself (1 charge per turn)

2. Transfer Charges
   ├─ Source: Demonomancer's stored charges
   ├─ Target: Allied unit with demonic weapon
   ├─ Effect: Adds X charges to target from Demonomancer supply
   └─ Cost: Does NOT end turn (stackable). Locks itself (1 charge per turn)

3. Consume for Spell
   ├─ Source: Demonomancer's stored charges
   ├─ Effect: Cast spell using charges as resource
   └─ Cost: Ends turn (spell casting)

Example Flow:
Turn N:
├─ Drain 2 charges from Sniper A
├─ Transfer 2 charges to Flamethrower
└─ Cast spell using 1 remaining charge (ends turn)
```

## **6. DEATH & REPLACEMENT MECHANICS**

### **Corpse Spawn Timing**

```
Death Trigger: Unit HP reaches 0
Process:
1. UnitDied signal emits
2. Death animation plays (BLOCKING)
3. Signal reaches Grid orchestrator
4. Orchestrator spawns corpse entity
5. Corpse placed at death location

Multi-Death Scenario:
├─ AoE kills 3 units simultaneously
├─ All 3 emit UnitDied signals
├─ All 3 death animations play (parallel)
└─ All 3 corpses spawn after animations complete

Corpse Properties:
├─ Position: Exact death location (air units drop to ground)
├─ Stacking: Multiple corpses per cell allowed
├─ Selection: Most recent corpse prioritized
└─ Collision: Does NOT block movement/targeting
```

### **Tactical Retreat - Detailed Rules**

#### **Quemin Retreat**
```
Trigger: Unit would take fatal damage (HP → 0)

Conditions Check:
├─ NOT Paralyzed ✓
├─ NOT Petrified ✓
├─ NOT Grounded ✓
└─ All conditions must pass

Effect:
├─ Unit removed from battlefield (not corpse) to "fled" container
├─ Hp not restored
└─ Returns after battle (if squad survives), i.e. restores hp to alive state

Squad Survival Requirement:
├─ At least ONE unit must flee naturally (not die)
├─ Fled units count toward survival
└─ All units dead = Squad eliminated

Failed Retreat:
├─ If conditions not met → Unit dies normally
└─ Corpse spawns instead of flee
```

#### **League Dragon's Pride**
```
Trigger: Dragon unit takes fatal damage

Process:
1. Prevent death
2. Dragon executes final AoE attack on ALL enemies
3. Dragon flees battlefield
4. Counts as "fled" for victory

Exclusion: Dracoliches do NOT have this ability
└─ They die normally (undead limitation)
```

### **Engineer Revival - Mech Restoration**

```
Normal Case: Mech destroyed
├─ Mech lost permanently
├─ No corpse (mechanical)
└─ Must replace via hiring

Special Case: Max-level Engineer
├─ Can controllably destroy mech
├─ Timing: Any engineer turn
├─ Result: Mech restored at 1 HP after battle, but destroyed immidiately
```


## **7. EDGE CASE RESOLUTION MATRIX**

### **Effect + Status Condition Interactions**

| Condition         | Can Move? | Can Attack? | Takes DoT? | Notes                                 |
|-------------------|-----------|-------------|------------|---------------------------------------|
| **Paralysis**     | ✗         | ✗           | ✓          | Turn completely skipped               |
| **Petrification** | ✗         | ✗           | ✓          | All armor → 30%, vulnerable           |
| **Seduction**     | ✓         | ✓           | ✓          | Removes wards/blocks, extends effects |
| **Transformation**| ✓         | ✓           | ✓          | Only basic melee attack               |
| **Borrowed Time** | ✓         | ✓           | ✓          | Can survive at negative HP            |


### **Simultaneous Effect Resolution**

**Case: Seduction + Poison + Paralysis**
```
Application Order (same frame):
1. Paralysis applied → Unit's next turn skipped (triggers still processed)
2. Seduction applied → Extends Paralysis by 1 turn
3. Poison applied → Will proc on unit's (skipped) turn

Result:
├─ Turn 1: Unit paralyzed (skips turn) and poisoned
├─ Turn 2: Still paralyzed (Seduction extended). Poison procs
├─ Turn 3: Paralysis expires, Poison procs
└─ Seduction extends ALL effects, not just itself
```

## **8. IMPLEMENTATION NOTES**

### **Queue Management Best Practices**

```
Turn Queue Structure:
├─ Maintain sorted array of active units
├─ Resort triggers:
│  ├─ Unit waits (insert with negative initiative)
│  ├─ Unit gains/loses initiative mid-battle
│  └─ New unit spawns (demon breakout, summon)
└─ Already-acted flags persist through resorts

Implementation:
├─ Mark units as "acted" to make rebuilds
├─ Clear "acted" flags when all units have acted
└─ Rebuild queue for new turn cycle
```

### **Effect Manager Architecture**

```
Per-Unit Effect Array:
├─ Store effects in ActiveEffects TArray
├─ Deduplicate by effect_stack_id getter
├─ Process on turn start (OnTurnStart hook), turn end (OnTurnEnd) and any other triggers
└─ Remove expired effects after processing (effect returns expiration state on trigger)

Effect Stacking Logic:
IF new effect added:
    FOR EACH existing effect:
        IF effect.get_stack_id() == new_effect.get_stack_id():
            Replace existing effect
            EXIT
    ELSE:
        Add new effect to array
```
