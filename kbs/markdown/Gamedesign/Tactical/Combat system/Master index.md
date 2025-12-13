# TACTICAL COMBAT SYSTEM - MASTER INDEX
*Project KBS - Complete Documentation Package*

---

## **DOCUMENTATION OVERVIEW**

This package contains comprehensive design documentation for Project KBS's tactical combat system. Total documentation: 4 phases + supporting materials.


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
- Action system (abilities define turn-ending behavior)

---

#### **[PHASE 2: COMBAT CALCULATIONS](Phase_2_Combat_Calculations.md)**
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
6. Special Combat Mechanics
7. Progression & Scaling
8. Critical Interactions & Edge Cases

**Key Takeaways:**
- Defense layers process in strict priority order
- Effect stacking is additive (not multiplicative)

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
5. Ability Charge Systems - Advanced
6. Death & Replacement Mechanics
   - Corpse spawn timing
   - Tactical retreat detailed rules (Birdfolk, Demon)
   - Engineer revival (mech restoration)
7. Edge Case Resolution Matrix
8. Implementation Notes
   - Queue management best practices
   - Effect manager architecture
   - Animation state machine

**Key Takeaways:**
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

**Key Takeaways:**
- Complete information transparency (no hidden stats)
- Right-click inspection - primary unit investigation tool

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

#### **[DOCUMENTATION TEMPLATE](Documentation_Template.md)** (This Document, Appendix)
**Purpose:** Reusable structure for documenting other systems

**Contains:**
- Interview methodology
- Loop documentation structure
- Best practices for knowledge extraction
