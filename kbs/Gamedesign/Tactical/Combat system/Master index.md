# TACTICAL COMBAT SYSTEM - MASTER INDEX
*Project KBS - Complete Documentation Package*

---

## **DOCUMENTATION OVERVIEW**

This package contains comprehensive design documentation for Project KBS's tactical combat system. Total documentation: 4 phases + supporting materials.


**Last Updated:** December 2024  

## **TABLE OF CONTENTS**

### **Core Documentation (4 Phases)**

#### **[PHASE 1: BATTLE STRUCTURE & FLOW](Phase_1_Tactical_Combat_System.md)** 
**Purpose:** Defines the high-level battle flow and turn structure

**Contents:**
1. System Overview
   - Purpose & scope boundaries
   - Core pillars
2. Battle Initialization Sequence
   - Unit conversion & spawn
   - Terrain metadata application
   - Global map buff processing
   - Initiative queue population
3. Core Combat Loop
   - Main battle cycle
   - Victory condition checking
4. Unit Turn Loop
   - Turn setup phase
   - Targeting & validation
   - Player decision loop
   - Turn end processing
5. Action System Mechanics
   - Action parameters (Ends Turn, Locks Picking, Re-pickable)
   - Action types & behaviors table
   - Movement mechanics (ground/air/layer change)
6. Victory/Defeat Resolution
   - Active unit counting
   - Loser resolution (death vs retreat)
7. Corpse System
   - Corpse entity creation
   - Stacking & selection rules
   - Spell targeting

**Key Takeaways:**
- Initiative-driven sequential turn order (not simultaneous)
- Action-cost system (abilities define turn-ending behavior)
- Terrain/global buffs affect calculations
- Corpse persistence for necromancy mechanics

---

#### **[PHASE 2: COMBAT CALCULATIONS](Phase_2_Combat_Calculations.md)** (28 pages)
**Purpose:** Documents the mathematical formulas and effect systems

**Contents:**
1. Damage Calculation System
   - Core damage formula (4-layer defense)
   - Accuracy check → Source selection → Defense processing
2. Damage Types (8 Sources)
   - Physical, Fire, Earth, Air, Water, Life, Death, Mind
3. Defense Layers (Priority Order)
   - Layer 1: Immunities (100% block, permanent)
   - Layer 2: Wards (100% block, one-time)
   - Layer 3: Percentage Armor (0-90% reduction per source)
   - Layer 4: Flat Reduction (universal subtraction)
4. Accuracy & Hit System
   - Hit chance calculation
   - Accuracy roll mechanics
   - Miss consequences
5. Effect System
   - Damage Over Time (DoT)
   - Stat Modifications (buffs/debuffs)
   - Status Conditions (paralysis, petrification, etc.)
   - Defensive Effects (shadow veil, defend stance, wards)
   - Effect duration management
   - Effect removal (dispel mechanics)
6. Special Combat Mechanics
   - Life drain / vampirism (5 variants)
   - Charge systems (powder, demonic, salvo)
   - Repair mechanics (degenerative healing)
   - Demonic breakout
   - Tactical retreat systems (Birdfolk, Demon)
   - Chain ability system (Birdfolk)
   - Phylactery system (Resistance Liches)
   - Derealization (Resistance Ghosts)
7. Progression & Scaling
   - Unit level-up formula (+10% HP, +1% accuracy)
   - Weapon scaling (+10% damage per level)
   - Experience & replacement mechanics (all 5 factions)
8. Critical Interactions & Edge Cases
   - All-Consuming Flame + Fire Immunity
   - Seduction + Transformation combo
   - Shadow Veil + Accuracy caps
   - Living on Borrowed Time interaction
   - Repair degradation cap

**Key Takeaways:**
- Defense layers process in strict priority order
- Effect stacking is additive (not multiplicative)
- Each faction has unique replacement mechanics
- Edge cases explicitly documented

---

#### **[PHASE 3: ADVANCED MECHANICS](Phase_3_Advanced_Mechanics.md)** (24 pages)
**Purpose:** Covers timing, animation, and complex interaction scenarios

**Contents:**
1. Initiative System - Complete Mechanics
   - Base initiative resolution (priority rules)
   - Wait mechanic deep dive (initiative negation)
   - Multiple units waiting (queue resort process)
   - Wait restrictions (self-locking, no value reroll)
   - Initiative modification during combat
2. Multi-Target & Area Abilities
   - Target reach types (complete specification table)
   - Area shape system (RelativeCells, bAffectsAllLayers)
   - Multi-target hit resolution order
   - Effect application timing
   - ClosestEnemies specific behavior
3. Animation & Timing System
   - Animation architecture (blocking vs non-blocking)
   - Turn execution timeline
   - Animation speed controls
   - Salvo animation mechanics (sequential, not parallel)
4. Complex Interaction Scenarios
   - Scenario A: Demon Breakout Chain Reaction
   - Scenario B: Phylactery Management
   - Scenario C: Ghost Derealization Timing
   - Scenario D: Living on Borrowed Time + Multi-Hit
5. Ability Charge Systems - Advanced
   - Salvo initiative manipulation
   - Reload mechanics timing
   - Demonic charge transfer
6. Death & Replacement Mechanics
   - Corpse spawn timing
   - Tactical retreat detailed rules (Birdfolk, Demon)
   - Engineer revival (mech restoration)
7. Edge Case Resolution Matrix
   - Effect + status condition interactions (table)
   - Simultaneous effect resolution
   - Priority conflicts
8. Implementation Notes
   - Queue management best practices
   - Effect manager architecture
   - Animation state machine

**Key Takeaways:**
- Salvo is sequential (not simultaneous fire)
- Borrowed Time checks death on turn END only
- Queue resorts on wait OR initiative gain
- Corpses spawn AFTER damage resolution

---

#### **[PHASE 4: UI/UX REQUIREMENTS](Phase_4_UI_UX_Requirements.md)** (32 pages)
**Purpose:** Specifies all visual feedback and player-facing systems

**Contents:**
1. Core HUD Layout
   - Screen layout diagram
2. Implemented UI Components (70% complete)
   - Turn counter ✅
   - Turn queue display ✅
   - Current unit widget ✅
   - Hovered unit widget ✅
   - Team container ✅
   - Battlefield visual indicators ✅
3. Planned/Partial UI Components (30% remaining)
   - Ability panel ⚙️
   - Effect panel ⚙️
4. Damage Preview System ✅
   - Trigger conditions
   - Preview display content
   - Multi-target preview limitations
5. Targeting & Validation Feedback
   - Valid target indication (red decals)
   - Invalid target handling
   - Area shape preview
   - ClosestEnemies highlighting
   - Salvo visual feedback
6. Post-Action Visual Feedback
   - Damage numbers (not implemented)
   - Effect application feedback
   - Widget updates
7. Detailed Inspection System ✅
   - Right-click popup layout
   - Access level (friendly vs enemy)
8. Tooltip System ⚙️
   - Ability tooltips (with examples)
   - Effect tooltips (with examples)
9. Information Architecture
   - Stat display priority
   - Visibility rules (complete transparency)
10. Combat Log & History ❌
    - Not planned
11. Settings & Accessibility ⚙️
    - Animation controls (future)
    - Camera controls (future)
    - Accessibility (future)
12. UI State Machine
    - States & transitions
    - UI lock states
13. Polish & Juice Recommendations
    - Screen shake, slow motion, camera focus, sound design
14. Implementation Priority
    - Critical, High, Medium, Low priority lists
15. Open Questions & Clarifications Needed
    - Team container toggle, HP bar animation, queue update animation, etc.
16. Reference Implementation Guide
    - Widget hierarchy (UMG structure)
    - Decal system (actors)
    - Tooltip system

**Key Takeaways:**
- 70% UI already implemented
- Damage preview shows final damage + hit chance only
- Complete information transparency (no hidden stats)
- Right-click inspection critical for onboarding

---

### **Supporting Materials**

#### **[QUICK REFERENCE CARDS](Quick_Reference_Cards.md)**
**Purpose:** 1-page cheat sheets for rapid lookup

**Contains:**
- Combat Formula Card
- Faction Mechanics Comparison
- UI Component Checklist
- Effect Priority Matrix
- Turn Execution Flowchart

---

#### **[ACTION ITEMS & IMPLEMENTATION GUIDE](Action_Items_Implementation_Guide.md)**
**Purpose:** Actionable task list derived from documentation

**Contains:**
- Clarifications Needed (questions across all phases)
- Implementation Priority (ordered by criticality)
- Feature Status Matrix (exists, partial, missing)
- Estimated Effort Breakdown
- Testing Checklist

---

#### **[DOCUMENTATION TEMPLATE](Documentation_Template.md)** (This Document, Appendix)
**Purpose:** Reusable structure for documenting other systems

**Contains:**
- Interview methodology
- Loop documentation structure
- Best practices for knowledge extraction
- Example: How to document Strategic Map system using this approach

---

## **HOW TO USE THIS DOCUMENTATION**

### **For Programmers:**
1. **Start with Phase 1** - Understand the battle loop
2. **Reference Phase 2** - Implement damage calculations
3. **Check Phase 3** - Handle edge cases and timing
4. **Implement Phase 4** - Build UI according to spec
5. **Use Quick Reference** - Keep combat formula card open while coding
6. **Track Action Items** - Check clarification questions before implementing

### **For Designers:**
1. **Read Phase 1 & 2** - Understand core mechanics
2. **Study Phase 2** - Balance faction mechanics
3. **Reference Quick Reference** - Compare faction capabilities
4. **Use Action Items** - Track design decisions needed

### **For Artists/UI Designers:**
1. **Read Phase 4** - Understand all UI requirements
2. **Reference Quick Reference** - UI component checklist
3. **Check Phase 3** - Animation timing requirements
4. **Use Action Items** - Track asset creation priorities

### **For Onboarding New Team Members:**
1. **Quick Reference Cards** - 30-minute overview
2. **Phase 1** - Understand battle structure
3. **Phase 4** - See what players experience
4. **Phases 2-3** - Deep dive into mechanics

### **For Recruiting Volunteers:**
- Share **Quick Reference Cards** first (low commitment)
- Provide **Phase 1 + Phase 4** for overview (1-hour read)
- Full documentation available for committed contributors

---

## **DOCUMENTATION METHODOLOGY**

This documentation was created using a structured interview process:

### **Process:**
1. **Knowledge Extraction** - Designer answers natural questions
2. **Pattern Recognition** - Identify loops, priorities, edge cases
3. **Formalization** - Convert to professional structure
4. **Validation** - Designer reviews and corrects
5. **Template Extraction** - Capture reusable patterns

### **Why This Works:**
- ✅ Captures implicit knowledge (what's "obvious" to designer)
- ✅ Translates empirical understanding to formal specs
- ✅ Identifies gaps and inconsistencies early
- ✅ Creates onboarding-ready documentation
- ✅ Provides implementation blueprints

### **Key Principles:**
- **Loops over Lists** - Document cycles, not just features
- **Examples over Abstractions** - Show concrete scenarios
- **Priorities over Completeness** - Mark what's critical vs nice-to-have
- **Questions over Assumptions** - Flag ambiguities explicitly

---

## **APPENDIX: DOCUMENTATION TEMPLATE**

### **Template Structure for Other Systems**

Use this structure to document any game system (Strategic Map, Hero Progression, etc.):

```markdown
# [SYSTEM NAME] - PHASE 1: STRUCTURE & FLOW

## 1. SYSTEM OVERVIEW
**Purpose:** [What problem does this system solve?]
**Scope Boundaries:**
- Starts: [Entry condition]
- Ends: [Exit condition]
- Not Included: [Out of scope]
**Core Pillars:** [3-5 key design principles]

## 2. [PRIMARY LOOP NAME]
[ASCII diagram of main cycle]
[Step-by-step breakdown]

## 3. [SUB-LOOP 1]
[Detailed mechanics]

## 4. [SUB-LOOP 2]
[Detailed mechanics]

## 5. [EDGE CASES & INTERACTIONS]
[Complex scenarios]

---

# [SYSTEM NAME] - PHASE 2: CALCULATIONS

## 1. [CORE FORMULA/MECHANIC]
[Mathematical formulas with examples]

## 2. [RESOURCE SYSTEM]
[How resources flow]

## 3. [PROGRESSION SYSTEM]
[Scaling formulas]

## 4. [SPECIAL MECHANICS]
[Unique features]

---

# [SYSTEM NAME] - PHASE 3: ADVANCED MECHANICS

## 1. [TIMING & STATE MANAGEMENT]
[When things happen]

## 2. [COMPLEX INTERACTIONS]
[Scenario walkthroughs]

## 3. [IMPLEMENTATION NOTES]
[Architecture guidance]

---

# [SYSTEM NAME] - PHASE 4: UI/UX REQUIREMENTS

## 1. [INFORMATION DISPLAY]
[What players see]

## 2. [PLAYER INPUTS]
[How players interact]

## 3. [FEEDBACK SYSTEMS]
[Visual/audio response]

## 4. [IMPLEMENTATION GUIDE]
[Widget hierarchy, etc.]
```

### **Interview Question Templates**

**Phase 1 Questions:**
- "Walk me through [system] from start to finish"
- "What happens after [X] completes?"
- "When can this loop exit/repeat?"
- "What decisions does the player make?"

**Phase 2 Questions:**
- "How is [value] calculated?"
- "What affects [resource] gain/loss?"
- "Are there caps/minimums?"
- "How do [A] and [B] interact mathematically?"

**Phase 3 Questions:**
- "What happens if [edge case]?"
- "Can [A] and [B] occur simultaneously?"
- "What's the order of operations?"
- "Are there race conditions?"

**Phase 4 Questions:**
- "What information must players always see?"
- "How do players know [X] succeeded/failed?"
- "What tooltips/details are needed?"
- "How is [state] communicated visually?"

---

## **EXAMPLE: APPLYING TEMPLATE TO STRATEGIC MAP**

### **Strategic Map - Phase 1 Interview Questions:**
1. "Walk me through a turn on the strategic map from start to finish"
2. "When does the player lose/win on the strategic map?"
3. "What actions can a hero take during their turn?"
4. "How does movement work? (action points? free movement?)"
5. "What triggers a battle?"

### **Strategic Map - Phase 2 Interview Questions:**
1. "How are movement points calculated?"
2. "What affects hero vision range?"
3. "How do resources accumulate per turn?"
4. "What's the formula for building construction time?"

### **Strategic Map - Phase 3 Interview Questions:**
1. "What happens if two heroes try to enter the same tile?"
2. "Can you cancel movement mid-path?"
3. "What happens if you lose your last city?"
4. "Can you retreat from a triggered battle?"

### **Strategic Map - Phase 4 Interview Questions:**
1. "What information shows on the strategic map HUD?"
2. "How do players see valid movement tiles?"
3. "What happens visually when you select a hero?"
4. "How are enemy heroes displayed? (fog of war?)"

---

## **VERSION HISTORY**

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 2024 | Initial complete documentation (4 phases) |
| 1.1 | Dec 2024 | Added Master Index + Template + Quick Reference + Action Items |

---

## **FEEDBACK & UPDATES**

This is a living document. When making updates:

1. **Document changes** in Version History
2. **Update Master Index** if structure changes
3. **Regenerate Quick Reference** if formulas change
4. **Update Action Items** as clarifications are resolved

**Suggested Update Triggers:**
- Major mechanic changes (new damage type, new faction)
- Edge cases discovered during implementation
- Playtesting reveals unclear mechanics
- New features added (e.g., combat log, replay system)

---

*Master Index compiled from 4-phase interview-based documentation*  
*Total: 105 pages of professional game design documentation*  
*Ready for implementation, onboarding, and recruitment*