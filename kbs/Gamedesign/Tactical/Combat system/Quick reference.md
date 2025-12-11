# QUICK REFERENCE CARDS
*Project KBS - Tactical Combat System*

---

## **CARD 1: COMBAT FORMULA CHEAT SHEET**

### **Damage Calculation (4 Layers)**

```
┌─────────────────────────────────────────────────────────┐
│ STEP 1: ACCURACY CHECK                                  │
├─────────────────────────────────────────────────────────┤
│ HitChance = UnitAccuracy × WeaponMultiplier × 100      │
│ Roll d100                                               │
│ IF Roll > HitChance → MISS (stop here)                 │
└─────────────────────────────────────────────────────────┘
                          │ HIT
                          ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 2: SELECT DAMAGE SOURCE                            │
├─────────────────────────────────────────────────────────┤
│ Choose source with LOWEST target armor                  │
│ (Physical, Fire, Earth, Air, Water, Life, Death, Mind)  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 3: DEFENSE LAYER 1 - IMMUNITY                      │
├─────────────────────────────────────────────────────────┤
│ IF target immune to source → 0 damage (stop)           │
└─────────────────────────────────────────────────────────┘
                          │ NOT IMMUNE
                          ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 4: DEFENSE LAYER 2 - WARD                          │
├─────────────────────────────────────────────────────────┤
│ IF target has ward for source:                          │
│   → 0 damage                                            │
│   → Consume ward (one-time use)                         │
│   → EXCEPTION: All-Consuming Flame (see below)          │
└─────────────────────────────────────────────────────────┘
                          │ NO WARD
                          ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 5: DEFENSE LAYER 3 - PERCENTAGE ARMOR              │
├─────────────────────────────────────────────────────────┤
│ DamageAfterArmor = BaseDamage × (1 - ArmorValue)       │
│ ArmorValue capped at 0.9 (max 90% reduction)           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ STEP 6: DEFENSE LAYER 4 - FLAT REDUCTION                │
├─────────────────────────────────────────────────────────┤
│ FinalDamage = DamageAfterArmor - FlatReduction         │
│ FinalDamage = Max(0, FinalDamage)                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
                    APPLY DAMAGE
```

### **Level-Up Scaling**
```
MaxHealth *= 1.1        (+10% per level)
Accuracy += 0.01        (+1% per level, cap 100%)
WeaponDamage *= 1.1     (+10% per level)
Initiative - NO CHANGE
Armor - NO CHANGE
```

### **Effect Stacking Rules**
```
SAME DataAsset → Replace/Refresh (no stack)
DIFFERENT DataAsset → Stack ADDITIVELY

Example:
Base Attack = 100
Buff A (+20%) + Buff B (+15%) = 100 × 1.35 = 135
NOT: 100 × 1.20 × 1.15 = 138 (no multiplication)
```

### **Special Case: All-Consuming Flame**
```
IF attack blocked by ward:
  → 0 direct damage
  → DoT applied anyway (25% × 2 turns)
  → 10% DoT penetrates fire immunity
```

---

## **CARD 2: FACTION MECHANICS COMPARISON**

| Faction | Primary Mechanic | Replacement System | Unique Features |
|---------|------------------|-------------------|-----------------|
| **Gnomes** | Charge Systems | Replace with XP penalty | • Powder weapons (reloadable)<br>• Demonic charges (limited)<br>• Salvo (initiative sync)<br>• Repair (degenerative)<br>• Demon breakout on mech death |
| **Demons** | Two-Cell Units | Consumption (75% XP transfer) | • All-Consuming Flame<br>• Petrification (30% armor)<br>• Seduction (extends effects)<br>• Transformation to Imp<br>• Heavy flight (limited) |
| **Empire** | Cavalry Focus | Resurrection/Penalty/Training | • Healing (priests only)<br>• Charge actions (attack while moving)<br>• Auxiliary cavalry swap<br>• Stabilization (save at 1 HP) |
| **Resistance** | Corpse Manipulation | Necromancy (1 corpse = 1 unit) | • Shadow Veil (accuracy debuff)<br>• Phylactery (lich revival)<br>• Paralysis (skip turn)<br>• Derealization (teleport/vanish)<br>• Health manipulation |
| **Birdfolk** | Chain Abilities | Tactical Retreat + Training Bonus | • Flight mechanics<br>• Strike on landing (bonus damage)<br>• Chain combos (multi-turn sequences)<br>• Ultimate abilities (6-step unlock)<br>• Effect on takeoff |

### **Faction Strengths Quick Compare**

| Strength | Best Faction | Second Best |
|----------|--------------|-------------|
| **Cavalry** | Empire | Resistance (undead cavalry) |
| **Two-Cell Units** | Demons | - |
| **Magic Damage** | Resistance (Death) | Demons (Fire) |
| **Physical Defense** | Gnomes | Empire |
| **Magic Defense** | Birdfolk | Gnomes |
| **Ranged DPS** | Birdfolk | Gnomes (early) |
| **Melee DPS** | Demons | Birdfolk |
| **Healing** | Empire (only faction) | - |
| **Resurrections** | Resistance | Empire (potions only) |
| **Mobility** | Birdfolk (flight) | Demons (heavy flight) |

---

## **CARD 3: UI COMPONENT STATUS CHECKLIST**

### **✅ IMPLEMENTED (70%)**

| Component | Status | Location | Notes |
|-----------|--------|----------|-------|
| Turn Counter | ✅ | Top-left | Shows turn number |
| Turn Queue | ✅ | Top center | Portrait row, shows initiative |
| Current Unit Widget | ✅ | Bottom-left | HP, Initiative, Portrait, Effects |
| Hovered Unit Widget | ✅ | Bottom-right | Same as Current, hover-triggered |
| Team Container | ✅ | Right side | Simplified cards, switchable |
| Blue Decal (Current) | ✅ | Battlefield | Under active unit |
| Red Decals (Targets) | ✅ | Battlefield | Valid target highlighting |
| Yellow Decals (Friendly) | ✅ | Battlefield | Allied positions |
| Right-Click Popup | ✅ | Overlay | Full unit inspection |
| Damage Preview | ✅ | Near target | Hit% + Final damage |

### **⚙️ PARTIAL (20%)**

| Component | Status | Priority | What's Missing |
|-----------|--------|----------|----------------|
| Ability Panel | ⚙️ | HIGH | Polish, charge display, grayed states |
| Effect Panel | ⚙️ | HIGH | Display above portraits, duration/stacks |
| Ability Tooltips | ⚙️ | HIGH | Hover descriptions with calculated values |
| Effect Tooltips | ⚙️ | HIGH | Duration, magnitude, source info |
| Area Shape Preview | ⚙️ | MEDIUM | Orange/yellow overlay on grid |

### **❌ NOT IMPLEMENTED (10%)**

| Component | Status | Priority | Notes |
|-----------|--------|----------|-------|
| Animation Speed Control | ❌ | LOW | 1x, 1.5x, 2x, 3x toggle |
| Combat Log | ❌ | LOW | Text feed (not planned) |
| Camera Controls | ❌ | LOW | Zoom, rotate (future) |
| Accessibility Options | ❌ | LOW | Colorblind, contrast (future) |

### **Critical Path to Beta:**
1. ⚙️ Effect Panel display
2. ⚙️ Ability Tooltips
3. ⚙️ Effect Tooltips
4. ⚙️ Ability Panel polish
5. ⚙️ Area Shape Preview

---

## **CARD 4: EFFECT PRIORITY & INTERACTION MATRIX**

### **Status Condition Effects**

| Condition | Can Move? | Can Attack? | Can Use Abilities? | Takes Damage? | Takes DoT? |
|-----------|-----------|-------------|-------------------|---------------|------------|
| **Paralysis** | ✗ | ✗ | ✗ | ✓ | ✓ |
| **Petrification** | ✗ | ✗ | ✗ | ✓ (armor→30%) | ✓ |
| **Seduction** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Transformation** | ✓ | ✓ (weak) | ✗ | ✓ | ✓ |
| **Defend Stance** | ✗ | ✗ | ✗ | ✓ (50% reduced) | ✓ |
| **Borrowed Time** | ✓ | ✓ | ✓ | ✓ (can survive <0 HP) | ✓ |
| **Shadow Veil** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Stun** | ✗ | ✗ | ✗ | ✓ | ✓ |

### **Effect Interaction Rules**

#### **Seduction Special Property:**
```
Seduction extends ALL other effects by +1 turn
├─ Paralysis (2 turns) + Seduction → Paralysis (3 turns)
├─ Poison (3 turns) + Seduction → Poison (4 turns)
└─ Applies to ALL effects, not just debuffs
```

#### **Transformation Persistence:**
```
Base Duration: 1 turn
On Expiration: (Accuracy/3)% chance to persist +1 turn
Can Chain: Multiple persistence rolls possible

Example: 90% accuracy = 30% chance per turn
├─ Turn 1: Transform applied
├─ Turn 2: 30% chance → Persists
├─ Turn 3: 30% chance → Persists
└─ Turn 4: 30% chance → Expires
```

#### **Petrification Override:**
```
Petrification sets ALL armor values to 30%
├─ Ignores base armor stats
├─ Ignores buffs/debuffs
└─ Universal 30% for all damage types
```

### **Effect Application Order (Same Frame)**

```
1. All effects applied to ActiveEffects array
2. Deduplicate by DataAsset (replace existing)
3. Process effects in array order (implementation-dependent)

NOTE: Effects don't have inherent priority
└─ Order of application doesn't matter (simultaneous)
```

---

## **CARD 5: TURN EXECUTION FLOWCHART**

### **Simplified Combat Loop**

```
┌──────────────────────────────────────────────┐
│         TURN START                           │
│  • Dequeue next unit from initiative queue   │
│  • Update Current Unit Widget                │
│  • Populate Ability Panel                    │
│  • Remove temporary effects (Defend stance)  │
│  • Process OnTurnStart effects (DoT)         │
│  • UI unlocked                               │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│      PLAYER SELECTS ABILITY                  │
│  • Click ability icon in panel               │
│  • Targeting overlay activates               │
│  • Valid targets highlighted (red decals)    │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│      PLAYER SELECTS TARGET                   │
│  • Hover shows damage preview                │
│  • Click confirms target                     │
│  • UI locks (no more input)                  │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│       ACTION EXECUTION                       │
│  • Animation plays (BLOCKING)                │
│  • Accuracy roll                             │
│  • IF HIT:                                   │
│    ├─ Calculate damage (4 layers)            │
│    ├─ Apply damage                           │
│    ├─ Apply effects                          │
│    └─ Death check                            │
│  • ELSE:                                     │
│    └─ Miss animation                         │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│      WIDGET UPDATES                          │
│  • HP bars update                            │
│  • Effect panels update                      │
│  • Queue updates (if death)                  │
│  • Corpse spawns (if death)                  │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│        TURN END CHECK                        │
│  • Process OnTurnEnd effects                 │
│  • Check ability "Ends Turn" flag            │
│  • IF ends turn → Advance queue              │
│  • ELSE → Return to ability selection        │
└──────────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────────┐
│      VICTORY CHECK                           │
│  • Count active units per team               │
│  • IF one team = 0 → BATTLE ENDS             │
│  • ELSE → Return to TURN START               │
└──────────────────────────────────────────────┘
```

### **Wait Mechanic Flow**

```
Unit selects "Wait" ability
├─ Initiative negated: Value × (-1)
├─ Unit reinserted in queue (at end)
├─ Queue resorts
└─ Turn ends

Example:
Before Wait: [60, 55, 50, 45, 40]
Unit(50) waits: [60, 55, 45, 40, -50]
                                 └─ Goes last
```

### **Salvo Mechanic Flow**

```
Musketeer(50) attacks
├─ Identify all identical units (Musketeers)
├─ Find best initiative among them (50)
├─ Set ALL their initiatives to 50
└─ Queue processes them sequentially

Before: [Musketeer(50), Knight(48), Musketeer(45)]
After:  [Musketeer(50), Musketeer(50), Knight(48)]
        └──────────────┴──────────────┘
         Fire in rapid sequence (not simultaneous)
```

---

## **CARD 6: INITIATIVE SYSTEM QUICK RULES**

### **Initiative Resolution Priority**

```
1. Higher initiative value → Acts first
2. IF TIED → Attacker team goes first
3. IF SAME TEAM → Higher BASE initiative (ignore buffs)
4. IF STILL TIED → Implementation-dependent (sort order)
```

### **Wait Queue Mechanics**

```
Wait Action:
├─ Initiative becomes negative (Value × -1)
├─ Inserted at end of queue
├─ Cannot wait twice in same turn (self-locks)
└─ Value NOT recalculated (persists)

Queue Sorting:
├─ Positive initiatives first (descending)
└─ Negative initiatives last (descending: -10 before -50)
```

### **Mid-Combat Initiative Changes**

```
Birdfolk Chain Ability: +20 Initiative after Defend
├─ Applies AFTER action completes
├─ Does NOT reshuffle current turn queue
└─ Takes effect on NEXT turn

Permanent Initiative Gain (level-up, long buff):
├─ Triggers immediate queue resort
├─ Already-acted units remain marked
└─ Remaining queue reorders
```

---

## **CARD 7: WEAPON & CHARGE SYSTEMS**

### **Gnome Powder Weapons**

```
Charges: 1-4 (varies by weapon)
Reload: Costs full turn, restores all charges
Engineer Assist: Can reload ally (costs Engineer's turn)

Example Flow:
Turn 1: Fire (1 charge spent)
Turn 2: Reload (charges restored) OR Engineer reloads you
Turn 3: Fire again
```

### **Gnome Demonic Charges**

```
Charges: Limited (weapon-specific)
Reload: NOT POSSIBLE
Transfer: YES (via Demonomancer)

Demonomancer Actions (stackable, don't end turn):
├─ Drain charges from unit
├─ Transfer charges to unit
└─ Consume charges for spell (ends turn)

When Exhausted: Weapon unusable
```

### **Salvo System**

```
Trigger: Identical unit attacks
Effect:
├─ Find all identical units (haven't acted)
├─ Set their initiative to attacker's value
└─ They fire in rapid sequence (next in queue)

Benefit:
├─ Bypasses initiative spread
├─ Allows focus fire
└─ Maintains volley timing
```

### **Repair System (Gnomes)**

```
Formula: Restore 20% of CURRENT max HP
Side Effect: Permanently reduce max HP by 20%

Example:
Mech: 1000 max HP, 300 current HP
├─ Repair 1: +60 HP, max → 800 HP
├─ Repair 2: +72 HP, max → 640 HP
└─ Repair 3: +51 HP, max → 512 HP

Degrades with each use
[CLARIFICATION NEEDED: Is there a floor? Can reach 0?]
```

---

## **CARD 8: SPECIAL MECHANICS QUICK REFERENCE**

### **Borrowed Time (Demon T3)**

```
Trigger: Unit takes fatal damage
Effect:
├─ Death handler BLOCKED
├─ Unit survives at negative HP
└─ Death only checked on turn END

Survival:
├─ Must heal above 0 HP before turn ends
├─ Can take unlimited damage while active
└─ Multi-hit attacks can be survived if healing between
```

### **Phylactery (Resistance Liches)**

```
Setup: Lich assigns phylactery to unit (costs no action)
Effects:
├─ Holder gets +% HP buff
├─ Lich can revive once (50% HP, next turn)
└─ If holder dies → Revival disabled

Self-Phylactery:
├─ Lich gets HP buff + 1 revive
└─ Second death = permanent

Limitations:
├─ One phylactery per battle
├─ Cannot reassign mid-battle
└─ Consumed on revival
```

### **Derealization (Resistance Ghosts)**

```
Movement: Instant teleport to any cell (costs turn)
Special:
├─ Can leave battlefield entirely (derealize)
├─ Can return on own turn
└─ Retreat costs no movement (instant from anywhere)

Limitation:
├─ Can only derealize on OWN turn
├─ If all units derealized → Battle LOST
└─ Not valid target while derealized
```

### **Tactical Retreat (Birdfolk)**

```
Trigger: Unit would take fatal damage
Conditions: NOT paralyzed/petrified/grounded
Effect:
├─ Unit flees battlefield (not dead)
├─ Counts as "fled" for victory conditions
└─ Returns after battle if squad survives

Squad Survival:
├─ Requires at least 1 unit to flee naturally
└─ All died (no flees) = Squad eliminated
```

### **Dragon's Pride (Demons)**

```
Trigger: Dragon takes fatal damage
Effect:
├─ Dragon prevented from dying
├─ Makes final AoE attack on ALL enemies
└─ Dragon flees battlefield

Exclusion: Dracoliches don't have this ability
```

---

## **PRINTING INSTRUCTIONS**

### **Recommended Setup:**
1. Print cards 1-8 separately (8 pages)
2. Laminate for durability
3. Keep at desk/workstation
4. Reference during implementation/balancing

### **Digital Use:**
- Keep cards open in second monitor
- Bookmark for quick access
- Share with team via wiki/docs

---

*Quick Reference Cards generated from 105-page documentation*  
*For rapid lookup during development and balancing*