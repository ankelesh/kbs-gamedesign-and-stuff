# TACTICAL COMBAT SYSTEM - PHASE 2: COMBAT CALCULATIONS
*Project KBS - Game Design Documentation*

---

## **1. DAMAGE CALCULATION SYSTEM**

### **Core Damage Formula**

```
PHASE 1: Accuracy Check
├─ HitChance = UnitAccuracy × WeaponAccuracyMultiplier × 100 (clamp 0-100)
├─ Roll d100
└─ If Roll > HitChance → MISS (exit)

PHASE 2: Damage Source Selection
├─ Weapon has multiple damage sources (Physical, Fire, Earth, Air, Water, Mind, Death, Life)
├─ Check target's armor for each source 
└─ SELECT: Source with LOWEST target armor and no immunity/ward, if no such, pick first

PHASE 3: Defense Layer Processing
├─ Layer 1: IMMUNITY CHECK
│  └─ If target immune to selected source → 0 damage (exit)
│
├─ Layer 2: WARD CHECK
│  ├─ If target has ward for selected source → 0 damage
│  └─ Consume ward (mark as consumed in result object)
│
├─ Layer 3: PERCENTAGE ARMOR
│  ├─ DamageAfterArmor = BaseDamage × (1 - ArmorValue)
│  └─ ArmorValue clamp (0-90%)
│
├─ Layer 4: DEFENCE STANCE
│  ├─ if is on: DamageAfterArmor * 0.5
│
└─ Layer 4: FLAT REDUCTION
   ├─ FinalDamage = DamageAfterArmor - FlatReduction
   └─ FinalDamage = clamped (0) if source is not Life

RESULT: FinalDamage applied to target HP
```

### **Damage Types (8 Sources)**

| Damage Source | Common Users                 | Notes                                                  |
|---------------|------------------------------|--------------------------------------------------------|
| **Physical**  | Melee/ranged weapons         | Most common, armour usually hard to stack.             |
| **Fire**      | Demons, Dwarf demon-tech     | Demons resistant/immune to fire                        |
| **Earth**     | Dwarf mages                  | Often has stun/ini reduction and locked to ground layer|
| **Air**       | Empire, quemin mages         | Often single-target high-damage spells                 |
| **Water**     | Dragons                      | Rare source, often is all-units aoe with debuffs.      |
| **Life**      | Any healers                  | Typically healing and buffs, not damage                |
| **Death**     | League mages, poison, debuffs| Most League units are immune to death                  |
| **Mind**      | Demons, Ghosts, spells       | Rarely deals damage, often stuns or debuffs            |

---

## **2. DEFENSE LAYERS (Priority Order)**

### **Layer 1: Immunities**
- **Effect**: 100% damage block, permanent
- **Behavior**: Completely negates damage from source, blocks effect application
- **Examples**: 
  - Demons immune to Fire
  - Ghosts immune to Physical
- **Code**: Checked first, returns 0 damage immediately

### **Layer 2: Wards (One-Time Blocks)**
- **Effect**: 100% damage block, consumed on use
- **Behavior**: Blocks first instance of damage from particular source (or effect from same source)
- **Consumption**: Ward removed after blocking attack or effect
- **Special**: Demon "All-Consuming Flame" bypasses ward consumption (check if ward was spent)
  - If ward spent = apply DoT with 25% of damage (2 turns)
  - If immunity: 10% damage penetrates fire immunity as Life damage (ability level check)
- **Code**: Checked second, consumes ward on block

### **Layer 3: Percentage Armor**
- **Effect**: 0-90% damage reduction per source
- **Cap**: Maximum 90% reduction (0.9 in code)
- **Formula**: `Damage × (1 - ArmorPercentage)`
- **Per-Source**: Each damage type has separate armor value
- **Examples**:
  - 50% Fire armor + 20% Physical armor (independent)

### **Layer 4: Flat Reduction**
- **Effect**: Fixed damage subtraction after percentage armor
- **Timing**: Applied AFTER percentage reduction and defensive stance, so is extremely powerfull when stacked
- **Formula**: `Max(0, DamageAfterArmor - FlatReduction)`
- **Universal**: Applies to all damage sources equally
- **Special**: Is designed to add armoured "in lore" units extra durability vs. weak attacks

### **Defense Calculation Example**

```
Scenario: Demon attacks with Fire weapon
├─ Base Damage: 100 Fire
├─ Target: Has 50% Fire Armor, 10 Flat Reduction, Fire ward
│
├─ Immunity Check: No fire immunity → Continue
├─ Ward Check: Has Fire ward → 0 damage, consume ward
└─ Result: 0 damage dealt, ward removed

Next Attack (ward consumed):
├─ Base Damage: 100 Fire
├─ Immunity: No → Continue
├─ Ward: Already used → Continue
├─ Armor: 100 × (1 - 0.5) = 50 damage
├─ Flat Reduction: 50 - 10 = 40 damage
└─ Result: 40 damage dealt
```

---

## **3. ACCURACY & HIT SYSTEM**

### **Hit Chance Calculation**

```
HitChance = UnitAccuracy × WeaponAccuracyMultiplier × 100
├─ UnitAccuracy: 0.0 - 1.0 (typically 0.65 - 0.95)
├─ WeaponAccuracyMultiplier: Usually 1.0, modified by weapon type
└─ Result: 0-100% (clamped)

Common modifiers:
├─ Shadow Veil (Resistance): Subtracts flat value AFTER calculation (ability-level of calc)
│  └─ clamped (0)
├─ Debuffs: -10 accuracy (applied to modified stats)
└─ Level-Up: +1% accuracy per level (capped at 100%)
```

### **Accuracy Roll**

```
Roll d100 (0.0 - 100.0)
IF Roll ≤ HitChance → HIT
ELSE → MISS
```

### **Miss Consequences**

- No damage dealt
- No effects applied
- Turn still consumed
- Animation plays (miss feedback)

---

## **4. EFFECT SYSTEM**

### **Effect Categories**

#### **A. Damage Over Time (DoT)**
- Examples, spreadsheet ()

| Effect                  | Source | Damage             | Duration | Notes                          |
|-------------------------|--------|--------------------|----------|--------------------------------|
| **All-Consuming Flame** | Life   | dynamic calc (25%) | 2 turns  | Applied by demon's fire attacks|
| **Poison**              | Death  | static calc (value)| Varies   | Standard DoT example           |


**Mechanics:**
- Processed on `OnTurnStart()` (beginning of affected unit's turn)
- Each effect has effect_stack_id (baked in DataAsset). If not unique on unit (by stack id) - override duration, not apply

#### **B. Stat Modifications**
- Two types: additive and override
- Additive calculate and apply themselves
- Override during calculation seeks for other similar override effects, applies only if it's effect is better, recalculates all additive on apply


| Buff Type                | Examples               | Stacking Rule                     | Affects    |
|--------------------------|------------------------|-----------------------------------|------------|
| **Base stat additive**   | Initiative buff (+10)  | Additive from different sources   | Base stat  |
| **Weapon stat additive** | Alchemist buff (*1.75) | Additive from different sources   | Weapon stat|
| **Base stat override**   | Armour buff (40%).     | Overriding stat, latest dominates | Base stat  |
| **Weapon stat override** | Fire buff (Source>fire)| Overriding until battle end.      | Weapon stat| 

**Stacking Formula:**
```
ModifiedStat = BaseStat × (1 + Sum of all modifiers)

Example:
├─ Base damage: 100
├─ Alchemist Buff: +20% (from Effect A)
├─ Hero Aura: +15% (from Effect B)
└─ Final damage: 100 × (1 + 0.20 + 0.15) = 135

NOT: 100 × 1.20 × 1.15 = 138 (multiplicative)
```

**Deduplication:**
- Effects deduplicate per effect_stack_id getter (can be incremental for infinite stacking)


#### **C. Status Conditions**
- Has complex logic and different trigger conditions
- Usually own implementation instead of data-driven approach

| Status               | Effect                               | Duration | Extras       |
|----------------------|--------------------------------------|----------|--------------|
| **Paralysis**        | Skip turn                            | Varies   |              |
| **Petrification**    | All armor → 30%, skip turn           | Varies   |              |
| **Seduction**        | Remove wards/blocks/defense          | 1 turn   |              | 


### **Effect Duration Management**

```
OnTurnStart() Processing:
├─ Decrement RemainingTurns for all effects
├─ Process DoT damage
├─ Trigger effects
└─ Remove effects with RemainingTurns ≤ 0

OnTurnEnd() Processing:
├─ Trigger turn-end effects
└─ No duration decrement (for consistency, if effect has duration, better decrement on start)
```

### **Effect Removal (Dispel)**

**Friendly Dispel** (Common):
- Priest healing often removes debuffs
- Self-cleanse abilities (rare)
- Behavior: removes all non-positive effects by passing through current effects container

**Full Dispel** (Rare):
- High-tier Mage spells
- Behavior: removes all effects from a unit

---

## **5. SPECIAL COMBAT MECHANICS**
(examples)

### **A. Life Drain / Vampirism**

| Unit Type                        | Mechanic                                                   | Notes |
|----------------------------------|------------------------------------------------------------|-------|
| **Demon Devourers T1**           | On unit attacks: self heal (value)                         |       |
| **Demon Devourers T2+**          | On unit attacks: self heal (damage dealt)                  |       |

### **B. Charge Systems**

#### **Powder Weapons (Gnomes)**
```
Charges: 1-4 (varies by weapon)
Reloadable: YES
Reload Cost: Full turn
Engineer Assist: Can reload ally (costs Engineer's turn)

Example Flow:
Turn 1: Fire (1 charge consumed)
Turn 2: Fire (1 charge consumed)
Turn 3: Reload (charges restored)
```

#### **Demonic Charges (Dwarves)**
```
Charges: Limited (varies by weapon)
Reloadable: NO
Transferable: YES (via Demonomancer)

Demonomancer Actions:
├─ Drain charges from unit
├─ Transfer charges to another unit
└─ Spells consume charges

When Exhausted: dependent abilities unusable
```


### **Repair Mechanic (Dwarves)**

```
Healing action, own calculation mechanic (affects also max hp)

Example:
├─ Mech: 100 max HP, 30 current HP
├─ Repair 1: +20 HP (20% of 100), new max = 80 HP
├─ Repair 2: +16 HP (20% of 80), new max = 64 HP
└─ Continues degrading with each use
```

### **E. Demonic Breakout (Dwarves)**

```
Trigger: Mech unit died
Effect:
├─ Spawn demon on mech's position (enemy team)
├─ Demon has "auto-control" effect = actions are done by AI
├─ Demon has "Third side" effect = changes team when friendly team dies
└─ If demon is last survivor: draw (lose for both teams)
```

### **F. Tactical Retreat Systems**

#### **Quemin Retreat**
```
Trigger: Unit dies
Conditions: NOT paralyzed/petrified/grounded
Effect: Unit flees battlefield instead of dying
Squad Survival: Requires at least 1 fled unit with hp > 0
After battle fled units clamp hp to (1..)
```

#### **League "Dragon's Pride"**
```
Trigger: Unit dies
Effect:
├─ Unit flees battlefield instead of dying
├─ Makes final attack before retreat, damaging enemy units
└─ Requires at leas 1 fled unit with hp > 0 for squad to survive, clamps to 1hp if survives.
```

### **G. Chain Ability System (Quemin)**

```
Mechanic: Actions grant bonuses if specific prior action (unit subclass stores history)
Duration: Next action only

Common Chains:
├─ Defend → self-heal (20% HP restore)
├─ Wait → Bonus damage (+50%)
├─ Attack → Ward (physical)
└─ Defend → (Accuracy / initiative buff)

Ultimate Chain Example:
Sequence: Defend → Attack → Wait → Attack → Attack → Flight
Processes on OnUnitAttacks, checks and records sequence history
Reward: Next attack deals 2× damage + stun
```

### **H. Phylactery System (League Liches)**

```
Setup: Lich assigns phylactery to allied unit
Effects:
├─ Holder: +% max HP buff, effect "phylactey holder"
├─ Lich: on unit died: checks battlefield for unit owning phylactery. If found, instant revive (50% hp)
└─ Destruction: If holder dies, effect is wasted and lich can be killed

Self-Phylactery:
├─ Lich gets HP buff + 1 guaranteed revival
└─ Second death is permanent
```

### **I. Derealization (Resistance Ghosts)**

```
Movement: Instant teleport to any cell (costs turn)
Special: Can leave battlefield entirely (go to fled container without lose processing of turns)
Return: can return on any cell from fled container (only action allowed while fled)

Limitation:
├─ Unit is considered fled while derealized. If no other units alive = battle ends.
```

---

## **6. PROGRESSION & SCALING**

### **Unit Level-Up Formula**

```cpp
On Level-Up:
├─ MaxHealth *= 1.1                    // +10% HP
├─ CurrentHealth = MaxHealth × HPRatio // Maintain % HP
├─ Accuracy += 0.01                    // +1% (capped at 1.0)
└─ Weapon Damage *= 1.1                // +10% damage per weapon

```

### **Weapon Scaling**

```
Base Weapon Damage: Set by WeaponDataAsset
Per Level Scaling: +10% damage from base

Example:
├─ Weapon: 50 base damage
├─ Unit Level 1: 50 damage
├─ Unit Level 2: 55 damage (+10%)
```

## **7. CRITICAL INTERACTIONS & EDGE CASES**

### **All-Consuming Flame + Fire Immunity**
```
Scenario: Demon attacks fire-immune target with ward
├─ Ward is skipped
└─ 10% of damage penetrates fire immunity (dealt as life damage)
```

### **Seduction + Transformation Combo**
```
Seduction Effect:
├─ Removes all wards/blocks/defense
├─ Extends ALL effect durations by 1 turn
└─ Transformation duration: 1 turn → 2 turns

Transformation Persistence:
├─ Base duration: 1 turn
├─ On expiration: (Accuracy/3)% chance to persist 1 more turn
└─ Can chain multiple times
```

### **Shadow Veil + Accuracy Caps**
```
Calculation Order:
1. Calculate HitChance = Accuracy × Multiplier × 100
2. Clamp to 100% max
3. Subtract Shadow Veil value
4. Clamp to 10% minimum

Example:
├─ Calculated: 120% → Capped to 100%
├─ Shadow Veil: -30
├─ Result: 70% hit chance

Example (minimum):
├─ Calculated: 50%
├─ Shadow Veil: -50
├─ Before minimum: 0% → Capped to 10%
```

### **Living on Borrowed Time Interaction**
```
First Fatal Damage:
├─ Unit HP: 100 → -50 (survives)
├─ Status: "Borrowed Time" active, suppressing onDeath trigger
└─ Can take unlimited additional damage

Next Attack:
├─ Must deal damage to heal
├─ Check on turn end: if healed above 0 → Survives
├─ If still ≤ 0 → Dies instantly
```

### **Repair Degradation Cap**
```
Question: Can mech be repaired to 0 max HP?
Answer: No
```

---