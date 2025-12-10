# TACTICAL COMBAT SYSTEM - PHASE 4: UI/UX REQUIREMENTS
*Project KBS - Professional Game Design Documentation*

---

## **1. CORE HUD LAYOUT**

### **Permanent UI Elements** (Always Visible)

```
Screen Layout:
┌─────────────────────────────────────────────────────────────┐
│ [Turn: N]     [Turn Queue: Portraits Row]      [Team Panel] │
│                                                               │
│                                                               │
│                      BATTLEFIELD GRID                         │
│                     (3D Isometric View)                       │
│                                                               │
│ [Current Unit]                            [Hovered Unit]     │
│    Widget                                     Widget          │
│                                                               │
│              [Ability Panel - Grid of Icons]                 │
└─────────────────────────────────────────────────────────────┘
```

---

## **2. IMPLEMENTED UI COMPONENTS** (Current Build - 70%)

### **A. Turn Counter** ✅
**Location:** Top-left corner  
**Content:** "Turn [N]"  
**Updates:** Increments after all units complete turn cycle

### **B. Turn Queue Display** ✅
**Location:** Top center (horizontal row)  
**Content:** Portrait cards for each unit in initiative order  
**Per Card:**
```
┌──────────────┐
│  [Portrait]  │
│  Unit Name   │
│  HP: XX/XX   │
│  Ini: XX     │
└──────────────┘
```
**Behavior:**
- Left-most = next to act
- When unit acts, card removed from queue → moved to "Current Unit" slot
- Queue updates in real-time (wait, initiative changes, summons)

### **C. Current Unit Widget** ✅
**Location:** Bottom-left  
**Content:**
```
┌─────────────────────────┐
│ Effects: [Icon][Icon]   │
│ [Unit Name]             │
│ HP:HP XX/XX  Ini:XX     │
│ ┌─────────────────────┐ │
│ │   Large Portrait    │ │
│ │   (Circular)        │ │
│ └─────────────────────┘ │
└─────────────────────────┘
```
**Updates:** Changes when new unit dequeued

### **D. Hovered Unit Widget** ✅
**Location:** Bottom-right  
**Content:** Same structure as Current Unit Widget  
**Trigger:** Mouse hover over ANY unit on battlefield  
**Behavior:**
- Shows real-time info for hovered unit
- Disappears when mouse leaves unit
- Updates effect panel on re-hover (not live)

### **E. Team Container** ✅
**Location:** Right side (vertical panel)  
**Content:** Simplified unit cards for entire team  
**Per Card:**
```
┌────────┐
│Portrait│
│ HP Bar │
└────────┘
```
**Behavior:**
- Switchable between player team / enemy team
- Quick reference for army status
- [NEEDS SPEC: Toggle button? Tabs? Hotkey?]

### **F. Battlefield Visual Indicators** ✅

#### **Current Unit Highlight**
- **Type:** Blue decal circle under unit
- **Purpose:** Shows whose turn it is at a glance

#### **Target Highlighting**
- **Valid Targets:** Red decal circles
- **Trigger:** Ability selected + hover over valid target
- **Coverage:** All units within reach of selected ability

#### **Friendly Position Indicator**
- **Type:** Yellow decal circles
- **Purpose:** Shows allied unit positions (not targets)
- **Always visible:** For spatial awareness

---

## **3. PLANNED/PARTIAL UI COMPONENTS** (Remaining 30%)

### **A. Ability Panel** ⚙️ *Partially Implemented*
**Location:** Lower bottom (horizontal grid)  
**Layout:** Square icon grid (2-4 rows × 3-6 columns)  
**Per Ability Icon:**
```
┌──────────────┐
│  Ability     │
│   Icon       │
│         [#]  │ ← Charge count (bottom-right)
└──────────────┘
```

**States:**
| State | Visual | Interaction |
|-------|--------|-------------|
| **Available** | Full color | Clickable |
| **Disabled** | Grayscale | Ignored (no click response) |
| **Selected** | Border highlight | Shows targeting overlay |
| **No Charges** | Grayscale + Red "X" | Ignored |

**Hover Behavior:**
- Shows tooltip with ability details (see Tooltip section)

### **B. Effect Panel** ⚙️ *System Exists, Display TBD*
**Location:** 
- Above portrait in Current Unit Widget
- Above portrait in Hovered Unit Widget
- [NOT on battlefield models - too cluttered]

**Layout:** Horizontal icon row (max 10 effects)
```
┌──┐┌──┐┌──┐┌──┐
│♠ ││♣ ││♥ ││♦ │ ← Effect Icons
│2 ││5 ││  ││3 │ ← Duration (bottom-left)
│×3││  ││  ││  │ ← Stack count (top-right, gray)
└──┘└──┘└──┘└──┘
```

**Icon Requirements:**
- Distinct silhouettes (recognizable at small size)
- Color-coded by effect type:
  - Red: Debuffs (damage, stat reduction)
  - Green: Buffs (healing, stat increase)
  - Blue: Control (paralysis, stun)
  - Purple: Transformation effects
  - Yellow: Defensive (wards, shields)

**Hover Behavior:**
- Shows tooltip with effect details (see Tooltip section)

---

## **4. DAMAGE PREVIEW SYSTEM** ✅

### **Trigger Conditions**
```
IF ability selected AND hovering over valid target:
    THEN show preview overlay
```

### **Preview Display**
**Location:** Floating near hovered unit (or in hovered unit widget)  
**Content:**
```
┌─────────────────┐
│ Hit: 75%        │ ← Accuracy percentage
│ Damage: 45      │ ← Expected damage (post-armor)
└─────────────────┘
```

**NOT Included:**
- Damage breakdown (pre-armor, armor reduction, etc.)
- Effect application chance
- Min/max damage range
- Crit chance (doesn't exist)

### **Multi-Target Preview**
**Limitation:** Only hovered target shows preview  
**Rationale:** Prevents UI clutter in AoE scenarios

**Example:**
```
Player selects Fireball (AoE 5 targets)
├─ Hovers over Enemy A → Preview shows
├─ Hovers over Enemy B → Preview updates to Enemy B
└─ Cannot see all 5 previews simultaneously
```

---

## **5. TARGETING & VALIDATION FEEDBACK**

### **Valid Target Indication**
**Visual:** Red decal circle underneath unit  
**Trigger:** Ability selected + target in range  
**Behavior:**
- All valid targets highlighted simultaneously
- Persists while ability remains selected
- Clears when ability deselected or action executed

### **Invalid Target Handling**
**Visual:** No indicator  
**Interaction:** Mouse clicks ignored (no response)  
**Rationale:** Clean UI, no error spam

**Alternative Considered (NOT Implemented):**
- Red "X" cursor over invalid targets
- Tooltip showing "Invalid Target: Out of Range"

### **Area Shape Preview**
**Trigger:** Area ability selected  
**Visual:** Overlays on grid cells showing affected area  
**Colors:**
```
├─ Orange: Primary target cell (player-selected anchor)
├─ Yellow: Secondary affected cells (from area shape)
└─ Updates in real-time as mouse moves
```

**Example - Cross Pattern:**
```
[ ][ ][Y][ ][ ]
[ ][ ][Y][ ][ ]
[Y][Y][O][Y][Y]  ← O = Orange anchor, Y = Yellow affected
[ ][ ][Y][ ][ ]
[ ][ ][Y][ ][ ]
```

### **ClosestEnemies Highlighting**
**Behavior:** Highlights ALL adjacent enemies (not just one)  
**Note:** Contradicts Phase 3 spec (needs clarification)
```
Clarification Needed:
├─ Phase 3 Doc: "ClosestEnemies = always one"
└─ UI Spec: "highlights all valid targets"

Possible Resolution:
├─ Highlights all adjacent
├─ Implementation picks ONE (array order)
└─ Player doesn't control which is chosen
```

### **Salvo Visual Feedback**
**No Extra Display:** Uses default widgets  
**Rationale:** Salvo is queue manipulation, not simultaneous fire  
**Player learns through:** Units firing in rapid sequence

---

## **6. POST-ACTION VISUAL FEEDBACK**

### **Damage Numbers** ❌ *Not Implemented*
**Decision:** No floating damage text  
**Rationale:** 
- Keeps battlefield clean
- Stats update in widgets (sufficient feedback)
- Animation + health bar change conveys success

**Alternative (If Needed Later):**
- Small number briefly appears above unit
- Fades out over 0.5 seconds
- Color-coded by damage type

### **Effect Application Feedback**
**Visual:** VFX particle effect plays once on application  
**Audio:** SFX plays once on application  
**Persistent:** Effect icon appears in effect panel  

**Examples:**
- Poison applied → Green bubbling VFX + hissing sound
- Paralysis applied → Lightning bolt VFX + electric zap
- Buff applied → Golden glow VFX + chime sound

### **Widget Updates** ✅
**Health Changes:**
- HP numbers update immediately in all relevant widgets
- HP bars update (smooth animation vs instant?)
- [NEEDS SPEC: Animation duration? Instant snap?]

**Unit Removal:**
- Dead unit removed from battlefield
- Dead unit removed from queue
- Dead unit grayed out in team container (or removed?)
- Corpse spawns after death animation

**Queue Rearrangement:**
- Turn queue updates when units wait/summon/die
- Smooth slide animation as portraits shift?
- [NEEDS SPEC: Animation or instant update?]

---

## **7. DETAILED INSPECTION SYSTEM**

### **Right-Click Popup** ✅ *Implemented*

**Trigger:** Right-click on any unit  
**Content:** Full stat sheet + ability list  
**Layout:**
```
┌────────────────────────────────────────┐
│ [Unit Portrait]        [Unit Name]     │
│                                        │
│ HP: XXX/XXX    Initiative: XX          │
│ Accuracy: XX%                          │
│                                        │
│ Defense Stats:                         │
│ ├─ Physical Armor: XX%                 │
│ ├─ Fire Armor: XX%                     │
│ ├─ [Other armors...]                   │
│ ├─ Flat Reduction: XX                  │
│ ├─ Immunities: [Icons]                 │
│ └─ Wards: [Icons]                      │
│                                        │
│ Active Effects:                        │
│ └─ [Effect Icons with hover tooltips]  │
│                                        │
│ Abilities:                             │
│ ├─ [Ability Icon] Ability Name         │
│ │  └─ Hover for tooltip                │
│ ├─ [Ability Icon] Ability Name         │
│ └─ ...                                 │
└────────────────────────────────────────┘
```

**Behavior:**
- **Persistent:** Stays open until clicked elsewhere
- **Hoverable:** Can hover over abilities/effects for tooltips
- **Clickthrough:** Clicking outside dismisses popup

**Access Level:**
- **Friendly Units:** Full information
- **Enemy Units:** Full information (no hidden stats)
- **Rationale:** Tactical decision-making requires complete info

---

## **8. TOOLTIP SYSTEM**

### **Ability Tooltips** ⚙️ *System Needed*

**Trigger:** Hover over ability icon (in ability panel OR popup)  
**Content:**
```
┌──────────────────────────────────────┐
│ [Ability Name]                       │
│                                      │
│ [Ability Description]                │
│ Describes what ability does in       │
│ natural language.                    │
│                                      │
│ Damage: [Formula/Range]              │
│ Targets: [Reach Type]                │
│ Charges: [Current/Max or Unlimited]  │
│ Cost: [Turn-ending? Locking?]        │
│                                      │
│ Special: [Unique mechanics]          │
└──────────────────────────────────────┘
```

**Examples:**

**Standard Attack:**
```
┌──────────────────────────────────────┐
│ Standard Attack                      │
│                                      │
│ Attack target with equipped weapon.  │
│                                      │
│ Damage: Weapon-dependent             │
│ Targets: Any Enemy (weapon reach)    │
│ Charges: Unlimited                   │
│ Ends Turn: Yes                       │
└──────────────────────────────────────┘
```

**Fireball (Demon):**
```
┌──────────────────────────────────────┐
│ Fireball                             │
│                                      │
│ Hurl a ball of flame at target and   │
│ surrounding enemies.                 │
│                                      │
│ Damage: 80 Fire (to all targets)    │
│ Targets: Target + Area (cross)       │
│ Charges: 3/5                         │
│ Ends Turn: Yes                       │
│                                      │
│ Special: Applies All-Consuming       │
│ Flame to targets with wards.         │
└──────────────────────────────────────┘
```

**Calculated Values:**
- Show ACTUAL damage (unit's stats applied)
- Not generic formula - player sees real numbers
- Example: "Damage: 80" not "Damage: Base × 1.5"

### **Effect Tooltips** ⚙️ *System Needed*

**Trigger:** Hover over effect icon (in effect panel)  
**Content:**
```
┌──────────────────────────────────────┐
│ [Effect Name]                        │
│                                      │
│ [Effect Description]                 │
│                                      │
│ Duration: [X turns remaining]        │
│ Magnitude: [Numerical value]         │
│ Source: [Unit/Ability that applied]  │
│                                      │
│ [Type-specific stats]                │
└──────────────────────────────────────┘
```

**Examples:**

**Poison:**
```
┌──────────────────────────────────────┐
│ Poison                               │
│                                      │
│ Deals damage at start of each turn.  │
│                                      │
│ Duration: 3 turns                    │
│ Damage/Turn: 15                      │
│ Source: Skeleton Archer              │
└──────────────────────────────────────┘
```

**Attack Buff:**
```
┌──────────────────────────────────────┐
│ Alchemist's Fury                     │
│                                      │
│ Increases attack damage.             │
│                                      │
│ Duration: 5 turns                    │
│ Bonus: +20% Attack                   │
│ Source: Gnome Alchemist              │
└──────────────────────────────────────┘
```

**Paralysis:**
```
┌──────────────────────────────────────┐
│ Paralysis                            │
│                                      │
│ Unit cannot act.                     │
│                                      │
│ Duration: 2 turns                    │
│ Source: Ghost Touch                  │
│                                      │
│ Effect: Turn is skipped entirely.    │
└──────────────────────────────────────┘
```

---

## **9. INFORMATION ARCHITECTURE**

### **Stat Display Priority**

**Always Visible (HUD):**
- Current HP / Max HP
- Initiative value
- Unit name
- Active effect count (icon quantity)

**On Hover (Widget):**
- Current HP / Max HP
- Initiative value
- Unit name
- Effect icons (hoverable)

**On Right-Click (Popup):**
- All core stats
- All defense stats
- All active effects (with details)
- All abilities (with tooltips)
- Weapon information
- Progression data (level, experience)

### **Visibility Rules**

| Information | Player Units | Enemy Units |
|-------------|--------------|-------------|
| HP (current/max) | ✅ Full | ✅ Full |
| Initiative | ✅ Full | ✅ Full |
| Accuracy | ✅ Full | ✅ Full |
| Armor Values | ✅ Full | ✅ Full |
| Immunities | ✅ Full | ✅ Full |
| Wards | ✅ Full | ✅ Full |
| Active Effects | ✅ Full | ✅ Full |
| Abilities | ✅ Full | ✅ Full |
| Weapon Damage | ✅ Full | ✅ Full |

**Design Philosophy:** Complete information transparency  
**Rationale:** Tactical game requires informed decisions

---

## **10. COMBAT LOG & HISTORY** ❌ *Not Planned*

**Decision:** No combat log system  
**Rationale:**
- Focus on real-time decision-making
- Animations + widget updates provide sufficient feedback
- Replay system not needed for turn-based game

**Possible Future Addition:**
- Simple text feed (last 5 actions)
- "Unit X attacked Unit Y for Z damage"
- Scrollable history panel (toggle on/off)

---

## **11. SETTINGS & ACCESSIBILITY** ⚙️ *Not Planned for Dev Phase*

### **Animation Controls** (Future)
- Speed multiplier: 1.0x, 1.5x, 2.0x, 3.0x
- Skip animation hotkey (Space?)
- Auto-battle toggle (AI plays for player)

### **Camera Controls** (Future)
- Fixed isometric view (current)
- Zoom in/out (mouse wheel?)
- Free rotation (Q/E keys?)
- Reset camera (Home key?)

### **Accessibility** (Future)
- Colorblind mode:
  - Damage types use icons + color
  - Decals use patterns + color
  - Team distinction via icon shapes
- Font size scaling
- High contrast mode
- Audio cues for all visual events

---

## **12. UI STATE MACHINE**

### **States & Transitions**

```
┌─────────────────────────────────────────────────────────────┐
│                     TURN START                              │
│  - Current Unit Widget updates                              │
│  - Ability Panel populates                                  │
│  - UI unlocked for player input                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  ABILITY SELECTION                          │
│  - Player clicks ability icon                               │
│  - Targeting overlay activates                              │
│  - Valid targets highlighted                                │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  TARGET SELECTION                           │
│  - Hover shows damage preview                               │
│  - Click confirms target                                    │
│  - OR Right-click to cancel                                 │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   ACTION EXECUTION                          │
│  - UI LOCKS (no input accepted)                             │
│  - Animation plays                                          │
│  - Damage calculated & applied                              │
│  - Widgets update                                           │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     TURN END                                │
│  - Current unit dequeued                                    │
│  - Next unit becomes current                                │
│  - Return to TURN START                                     │
└─────────────────────────────────────────────────────────────┘
```

### **UI Lock States**

| State | Input Allowed | Purpose |
|-------|---------------|---------|
| **Unlocked** | Full player control | Ability selection, targeting |
| **Locked (Animation)** | No input | Prevents double-actions during animation |
| **Locked (Enemy Turn)** | Hover only | Player can inspect but not act |
| **Locked (Game Over)** | No input | Battle resolved |

---

## **13. POLISH & JUICE RECOMMENDATIONS**

### **Screen Shake**
- Light shake on attack impact
- Heavy shake on death/explosion
- Configurable intensity (or disable)

### **Slow Motion**
- Brief slow-mo on critical moments:
  - Killing blow
  - Last unit standing
  - Ultimate ability activation

### **Camera Focus**
- Auto-pan to acting unit when their turn starts
- Smooth camera transition (not instant snap)
- Option to disable auto-pan

### **Sound Design**
- Distinct UI sounds:
  - Click: Different sounds for valid/invalid actions
  - Hover: Subtle highlight sound
  - Turn start: Notification sound
  - Low HP: Warning sound when unit below 25% HP

### **Unit Selection Feedback**
- Clicked ability icon bounces slightly
- Selected unit pulses (in addition to decal)
- Hover over unit scales model up 105%

---

## **14. IMPLEMENTATION PRIORITY**

### **Critical (Must Have for Playable Build):**
1. ✅ Current Unit Widget
2. ✅ Turn Queue Display
3. ✅ Target Highlighting (decals)
4. ⚙️ Ability Panel (functional, needs polish)
5. ⚙️ Effect Panel (system exists, needs UI)
6. ⚙️ Damage Preview (basic numbers)
7. ✅ Right-Click Inspection

### **High Priority (Needed for Beta):**
8. ⚙️ Ability Tooltips
9. ⚙️ Effect Tooltips
10. ⚙️ Area Shape Preview
11. ⚙️ Widget Update Animations (smooth HP bars)
12. ⚙️ Team Container Toggle (switch teams)

### **Medium Priority (Quality of Life):**
13. ❌ Animation Speed Controls
14. ❌ Camera Controls (zoom/rotate)
15. ❌ Auto-battle option
16. ❌ Combat log (simple text feed)

### **Low Priority (Polish):**
17. ❌ Screen shake
18. ❌ Slow motion effects
19. ❌ Advanced camera focus
20. ❌ Accessibility features

---

## **15. OPEN QUESTIONS & CLARIFICATIONS NEEDED**

### **A. Team Container Toggle**
- **Question:** How does player switch between teams?
- **Options:**
  - Tab key toggle?
  - Click on "Team" label?
  - Separate buttons for Player/Enemy?
  - Always show both (split panel)?

### **B. HP Bar Animation**
- **Question:** Should HP changes animate smoothly or snap instantly?
- **Recommendation:** Smooth animation (0.3 seconds) for clarity
- **Alternative:** Instant for fast-paced feel

### **C. Queue Update Animation**
- **Question:** When queue reorders, do portraits slide or snap?
- **Recommendation:** Smooth slide (0.2 seconds) for clarity
- **Alternative:** Instant for performance

### **D. ClosestEnemies Behavior**
- **Conflict:** Phase 3 says "always one", UI spec says "highlights all"
- **Question:** Does ability hit one OR multiple adjacent enemies?
- **Needs Resolution:** Clarify in Phase 3 doc

### **E. Dead Unit Display**
- **Question:** In team container, are dead units:
  - Removed entirely?
  - Grayed out (but visible)?
  - Red "X" overlay?
- **Recommendation:** Grayed out (preserves army composition view)

### **F. Effect Panel Overflow**
- **Question:** If unit has >10 effects, how to display?
- **Options:**
  - Scrollable panel?
  - Show first 10, hide rest?
  - Compress icons (smaller size)?
- **Recommendation:** Compress to smaller icons + tooltip for full list

---

## **16. REFERENCE IMPLEMENTATION GUIDE**

### **Widget Hierarchy (UMG)**

```
BattleHUD (Canvas Panel)
├─ TurnCounter (Text Block)
├─ TurnQueuePanel (Horizontal Box)
│  └─ UnitQueueCard (Widget) × N
│     ├─ Portrait (Image)
│     ├─ NameText (Text Block)
│     ├─ HPText (Text Block)
│     └─ InitiativeText (Text Block)
├─ CurrentUnitWidget (Border)
│  ├─ PortraitImage (Image)
│  ├─ NameText (Text Block)
│  ├─ StatsText (Text Block)
│  └─ EffectPanel (Horizontal Box)
│     └─ EffectIcon (Image) × N
├─ HoveredUnitWidget (Border)
│  └─ [Same structure as CurrentUnitWidget]
├─ TeamContainerPanel (Vertical Box)
│  ├─ TeamLabel (Text Block)
│  └─ SimplifiedUnitCard (Widget) × N
│     ├─ Portrait (Image)
│     └─ HPBar (Progress Bar)
├─ AbilityPanel (Grid Panel)
│  └─ AbilityIcon (Button) × N
│     ├─ IconImage (Image)
│     └─ ChargeText (Text Block)
└─ InspectionPopup (Border) [Visibility: Hidden by default]
   └─ [Detailed stat layout]
```

### **Decal System (Actors)**

```
TargetDecalActor (Blueprint)
├─ DecalComponent
│  ├─ Material: M_Decal_Targeting
│  └─ Size: Matches grid cell
└─ Visibility Logic:
   ├─ Spawn on ability selection
   ├─ Update on mouse move
   └─ Destroy on action execution

Decal Types:
├─ Blue (Current Unit): Persistent, follows unit
├─ Red (Valid Target): Temporary, ability-dependent
└─ Yellow (Friendly Position): Always visible
```

### **Tooltip System (UMG)**

```
TooltipWidget (Border)
├─ Background (Image)
├─ TitleText (Text Block)
├─ DescriptionText (Text Block)
└─ StatsPanel (Vertical Box)
   └─ StatRow (Horizontal Box) × N

Tooltip Manager (C++ Subsystem)
├─ ShowTooltip(Widget, Content)
├─ HideTooltip()
└─ UpdatePosition(MouseLocation)
```

---

## **DOCUMENTATION STATUS**

### **Completed:**
- ✅ Core HUD layout specification
- ✅ Implemented component documentation
- ✅ Planned component specifications
- ✅ Damage preview system
- ✅ Targeting feedback system
- ✅ Visual feedback requirements
- ✅ Inspection system design
- ✅ Tooltip system specifications
- ✅ Information architecture
- ✅ UI state machine
- ✅ Implementation priority guide
- ✅ Reference implementation structure

### **System Documentation Complete:**
- ✅ **Phase 1:** Battle Structure & Flow
- ✅ **Phase 2:** Combat Calculations
- ✅ **Phase 3:** Advanced Mechanics
- ✅ **Phase 4:** UI/UX Requirements

---

## **FINAL RECOMMENDATIONS**

### **For Programmers:**
1. Implement ability tooltips BEFORE beta (critical for usability)
2. Effect panel display is high priority (players need effect visibility)
3. Smooth HP bar animations significantly improve feel
4. Widget update batching prevents performance issues

### **For Artists:**
5. Effect icons must be distinct at 32×32 pixel size
6. Decal materials need clear team distinction (red/blue)
7. UI background should not compete with battlefield visibility
8. Status effect VFX should be brief and impactful (not persistent)

### **For Designers:**
9. Test tooltip verbosity (too much text = ignored)
10. Damage preview accuracy critical for player trust
11. Right-click popup must load instantly (<100ms)
12. Consider colorblind accessibility from start (cheaper than retrofit)

---

*Generated via structured interview + screenshot analysis*  
*Date: 2024*  
*Format: Professional Game Design Documentation*
*Current Implementation: 70% Complete*
