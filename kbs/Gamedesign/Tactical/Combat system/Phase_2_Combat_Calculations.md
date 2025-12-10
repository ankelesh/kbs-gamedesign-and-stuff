# TACTICAL COMBAT SYSTEM - PHASE 2: COMBAT CALCULATIONS
*Project KBS - Professional Game Design Documentation*

---

## **1. DAMAGE CALCULATION SYSTEM**

### **Core Damage Formula**

```
PHASE 1: Accuracy Check
├─ HitChance = UnitAccuracy × WeaponAccuracyMultiplier × 100
├─ Roll d100
└─ If Roll > HitChance → MISS (exit)

PHASE 2: Damage Source Selection
├─ Weapon has multiple damage sources (Physical, Fire, Earth, etc.)
├─ Check target's armor for each source
└─ SELECT: Source with LOWEST target armor

PHASE 3: Defense Layer Processing
├─ Layer 1: IMMUNITY CHECK
│  └─ If target immune to selected source → 0 damage (exit)
│
├─ Layer 2: WARD CHECK
│  ├─ If target has ward for selected source → 0 damage
│  └─ Consume ward (one-time use)
│
├─ Layer 3: PERCENTAGE ARMOR
│  ├─ DamageAfterArmor = BaseDamage × (1 - ArmorValue)
│  └─ ArmorValue capped at 0.9 (max 90% reduction)
│
└─ Layer 4: FLAT REDUCTION
   ├─ FinalDamage = DamageAfterArmor - FlatReduction
   └─ FinalDamage = Max(0, FinalDamage)

RESULT: FinalDamage applied to target HP
```

### **Damage Types (8 Sources)**

| Damage Source | Common Users | Notes |
|---------------|--------------|-------|
| **Physical** | Melee/ranged weapons | Most common, countered by physical armor |
| **Fire** | Demons, Gnome flamers | Demons resistant/immune to fire |
| **Earth** | - | - |
| **Air** | - | - |
| **Water** | - | - |
| **Life** | - | Typically healing, not damage |
| **Death** | Resistance necromancers | Resistance faction specialty |
| **Mind** | Demons (Seduction) | Bypasses physical defenses |

---

## **2. DEFENSE LAYERS (Priority Order)**

### **Layer 1: Immunities**
- **Effect**: 100% damage block, permanent
- **Behavior**: Completely negates damage from source
- **Examples**: 
  - Demons immune to Fire
  - Ghosts immune to Physical
- **Code**: Checked first, returns 0 damage immediately

### **Layer 2: Wards (One-Time Blocks)**
- **Effect**: 100% damage block, consumed on use
- **Behavior**: Blocks first instance of damage from each source
- **Consumption**: Ward removed after blocking attack
- **Special**: Demon "All-Consuming Flame" bypasses ward consumption
  - Ward blocks damage but leaves DoT (25% of attack, 2 turns)
  - 10% damage penetrates fire immunity
- **Code**: Checked second, consumes ward on block

### **Layer 3: Percentage Armor**
- **Effect**: 0-90% damage reduction per source
- **Cap**: Maximum 90% reduction (0.9 in code)
- **Formula**: `Damage × (1 - ArmorPercentage)`
- **Per-Source**: Each damage type has separate armor value
- **Examples**:
  - 50% Fire armor + 20% Physical armor (independent)
  - Petrification sets ALL armors to 30%

### **Layer 4: Flat Reduction**
- **Effect**: Fixed damage subtraction after percentage armor
- **Timing**: Applied AFTER percentage reduction
- **Formula**: `Max(0, DamageAfterArmor - FlatReduction)`
- **Universal**: Applies to all damage sources equally

### **Defense Calculation Example**

```
Scenario: Demon attacks with Fire weapon
├─ Base Damage: 100 Fire
├─ Target: Has 50% Fire Armor, 10 Flat Reduction
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

Modifiers:
├─ Shadow Veil (Resistance): Subtracts flat value AFTER calculation
│  └─ Applied after clamping to 100%, min 10% final hit chance
├─ Mummy Debuff: -10 accuracy (applied to base accuracy)
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

| Effect | Source | Damage | Duration | Notes |
|--------|--------|--------|----------|-------|
| **All-Consuming Flame** | Demons | 25% of blocked attack | 2 turns | Penetrates wards, 10% through fire immunity |
| **Poison** | Multiple factions | Varies by ability | Varies | Standard DoT |

**Mechanics:**
- Processed on `OnTurnStart()` (beginning of affected unit's turn)
- Multiple DoTs from DIFFERENT DataAssets stack
- Same DataAsset = no stack (replaces/refreshes)

#### **B. Stat Modifications**

| Buff Type | Examples | Stacking Rule |
|-----------|----------|---------------|
| **Attack Buffs** | Alchemist (Gnomes), Priest auras | Additive from different sources |
| **Defense Buffs** | Engineer buffs, terrain bonuses | Additive from different sources |
| **Accuracy Debuffs** | Mummy debuff (-10), Shadow Veil | Additive from different sources |

**Stacking Formula:**
```
ModifiedStat = BaseStat × (1 + Sum of all modifiers)

Example:
├─ Base Attack: 100
├─ Alchemist Buff: +20% (from DataAsset A)
├─ Hero Aura: +15% (from DataAsset B)
└─ Final Attack: 100 × (1 + 0.20 + 0.15) = 135

NOT: 100 × 1.20 × 1.15 = 138 (multiplicative)
```

**Deduplication:**
- Effects deduplicate per **DataAsset**, not per effect type
- Multiple "+20% Attack" buffs stack IF from different DataAssets
- Same DataAsset = only one instance active

#### **C. Status Conditions**

| Status | Effect | Duration | Interactions |
|--------|--------|----------|--------------|
| **Paralysis** | Skip turn | Varies | Prevents Tactical Retreat, blocks flight |
| **Petrification** | All armor → 30% | Varies | Worse than paralysis (takes damage) |
| **Seduction** | Remove wards/blocks/defense | 1 turn | Extends other effect durations by 1 turn |
| **Transformation** | Convert to Imp (weak melee) | 1 turn base | Extended by Seduction, chance to persist |
| **Stun** | Skip turn (physical source) | 1 turn | From Birdfolk ultimate ability |

#### **D. Defensive Effects**

| Effect | Mechanic | Duration |
|--------|----------|----------|
| **Shadow Veil** | Subtract accuracy after cap (min 10%) | Varies |
| **Defend Stance** | 50% damage reduction | Until turn start |
| **Wards** | 100% damage block (one-time) | Until consumed |
| **Chain Ability Bonuses** | Various (damage, regen, wards) | Next action |

### **Effect Duration Management**

```
OnTurnStart() Processing:
├─ Decrement RemainingTurns for all effects
├─ Process DoT damage
├─ Trigger turn-start effects
└─ Remove effects with RemainingTurns ≤ 0

OnTurnEnd() Processing:
├─ Trigger turn-end effects
├─ Apply new effects from abilities
└─ No duration decrement
```

### **Effect Removal (Dispel)**

**Friendly Dispel** (Common):
- Priest healing often removes debuffs
- Self-cleanse abilities (rare)

**Enemy Dispel** (Rare):
- High-tier Mage spells
- Specific counter-abilities

---

## **5. SPECIAL COMBAT MECHANICS**

### **A. Life Drain / Vampirism**

| Unit Type | Mechanic | Notes |
|-----------|----------|-------|
| **Demon Devourers T1** | Restore fixed HP per attack | Doesn't scale with damage |
| **Demon Devourers T2+** | Restore 50% of damage dealt | Scales with damage output |
| **Living on Borrowed Time (T3)** | Can survive at negative HP until next attack | Must heal above 0 or die |
| **Resistance Assassin Hero** | Sacrifice 10% army HP for +15% damage/unit, heal 10% on kill | Army-wide mechanic |

### **B. Charge Systems**

#### **Powder Weapons (Gnomes)**
```
Charges: 1-4 (varies by weapon)
Reloadable: YES
Reload Cost: Full turn
Engineer Assist: Can reload ally (costs Engineer's turn)

Example Flow:
Turn 1: Fire (1 charge consumed)
Turn 2: Reload (charges restored)
Turn 3: Fire (1 charge consumed)
```

#### **Demonic Charges (Gnomes)**
```
Charges: Limited (varies by weapon)
Reloadable: NO
Transferable: YES (via Demonomancer)

Demonomancer Actions:
├─ Drain charges from unit
├─ Transfer charges to another unit
└─ Consume charges for spells

When Exhausted: Weapon/abilities unusable
```

### **C. Salvo Mechanic (Gnomes)**

```
Trigger: Identical unit attacks
Effect: All same-type units who haven't acted fire simultaneously

Example:
├─ 3 Musketeers on battlefield (all Initiative 45-55)
├─ First Musketeer attacks → Triggers salvo
├─ Other 2 Musketeers fire immediately
└─ Bypasses initiative spread
```

### **D. Repair Mechanic (Gnomes)**

```
Formula: Restore 20% of CURRENT max HP
Degenerative: Each repair permanently reduces max HP by 20%

Example:
├─ Mech: 1000 max HP, 300 current HP
├─ Repair 1: +60 HP (20% of 300), new max = 800 HP
├─ Repair 2: +72 HP (20% of 360), new max = 640 HP
└─ Continues degrading with each use
```

### **E. Demonic Breakout (Gnomes)**

```
Trigger: Gnome mech destroyed
Effect:
├─ Spawn aggressive demon on mech's position
├─ Demon attacks all nearby units (friend/foe)
├─ Priority: Last attacker > random target
└─ If demon is last survivor → Defeat for Gnomes
```

### **F. Tactical Retreat Systems**

#### **Birdfolk Retreat**
```
Trigger: Unit would take fatal damage
Conditions: NOT paralyzed/petrified/grounded
Effect: Unit flees battlefield instead of dying
Squad Survival: Requires at least 1 natural flee
```

#### **Demon "Dragon's Pride"**
```
Trigger: Dragon would die
Effect:
├─ Dragon flees battlefield
├─ Makes final AoE attack on all enemies
└─ Does NOT apply to Dracoliches
```

### **G. Chain Ability System (Birdfolk)**

```
Mechanic: Actions grant bonuses if specific prior action
Duration: Next action only

Common Chains:
├─ Defend → Regeneration (20% HP restore)
├─ Wait → Bonus damage (+50%)
├─ Attack → Ward (physical block)
└─ Defend → Accuracy bonus (+20 initiative)

Ultimate Chain Example (T2+ Defenders):
Sequence: Defend → Attack → Wait → Attack → Attack → Flight
Reward: Next attack deals 2× damage + stun
```

### **H. Phylactery System (Resistance Liches)**

```
Setup: Lich assigns phylactery to allied unit
Effects:
├─ Holder: +% max HP buff
├─ Lich: Revive on death (50% HP, next turn)
└─ Destruction: If holder dies, Lich dies permanently

Self-Phylactery:
├─ Lich gets HP buff + 1 guaranteed revive
└─ Second death is permanent
```

### **I. Derealization (Resistance Ghosts)**

```
Movement: Instant teleport to any cell (costs turn)
Special: Can leave battlefield entirely
Retreat: Instant (don't need to be in back row)

Limitation:
├─ If all units derealized (none on battlefield)
└─ Battle is LOST for Resistance
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

NOT Modified:
├─ Initiative (remains static)
├─ Armor percentages (remains static)
└─ Flat damage reduction (remains static)
```

### **Weapon Scaling**

```
Base Weapon Damage: Set by WeaponDataAsset
Per Level Scaling: +10% damage

Example:
├─ Weapon: 50 base damage
├─ Unit Level 1: 50 damage
├─ Unit Level 2: 55 damage (+10%)
├─ Unit Level 3: 60.5 damage (+10%)
└─ Unit Level 5: 73.2 damage (+46.4% total)
```

### **Experience & Replacement Mechanics**

#### **Empire Replacement**
```
Resurrection (Potions): Full restore
Replacement Penalty: Lose (10 × UnitLevel)% of experience difference
Accelerated Training: New unit gains 25% of experience gap per battle
Stabilization: Priest prevents death → unit survives at 1 HP
```

#### **Resistance Necromancy**
```
Cost: 1 enemy corpse
Effect: Revive undead unit
Exclusions: Cannot revive Liches (need phylactery)
```

#### **Demon Consumption**
```
Base Transfer: 75% of accumulated experience
Same Type/Level: Up to 95% transfer
Existing Unit Consumes: Down to 40% transfer
Flexibility: Can redistribute experience across army
```

#### **Gnome Defense Stance**
```
Condition: Unit dies while in Defend stance
Effect: Survives at 1 HP if battle won
Exclusion: Does NOT apply to mechs (permanent loss)
```

#### **Birdfolk Training Bonus**
```
Condition: Unit has less experience than army average
Bonus: +25% of experience gap per battle
```

---

## **7. CRITICAL INTERACTIONS & EDGE CASES**

### **All-Consuming Flame + Fire Immunity**
```
Scenario: Demon attacks fire-immune target with ward
├─ Ward blocks 100% of direct damage
├─ All-Consuming Flame applies DoT anyway (25% × 2 turns)
└─ 10% of DoT penetrates fire immunity
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
├─ Status: "Borrowed Time" active
└─ Can take unlimited additional damage

Next Attack:
├─ Must deal damage to heal
├─ If healed above 0 → Survives
├─ If still ≤ 0 → Dies instantly
```

### **Repair Degradation Cap**
```
Question: Can mech be repaired to 0 max HP?
Answer: [NEEDS CLARIFICATION]

Current: 20% reduction per repair
├─ Repair 1: 100% → 80% max
├─ Repair 2: 80% → 64% max  
├─ Repair 3: 64% → 51.2% max
├─ Repair 4: 51.2% → 40.96% max
└─ Repair 5: 40.96% → 32.77% max
```

---

## **DOCUMENTATION STATUS**

### **Completed:**
- ✅ Damage calculation formula
- ✅ Defense layer system
- ✅ Accuracy & hit mechanics
- ✅ Effect categories & stacking
- ✅ Special combat mechanics
- ✅ Level-up scaling
- ✅ Faction-specific mechanics



