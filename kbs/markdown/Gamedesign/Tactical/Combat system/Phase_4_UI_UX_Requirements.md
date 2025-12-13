# TACTICAL COMBAT SYSTEM - PHASE 4: UI/UX REQUIREMENTS
*Project KBS - Game Design Documentation*

---

## **1. CORE HUD LAYOUT**

### **Permanent UI Elements** (Always Visible)

```
Screen Layout:
┌───────────────────────────────────────────────────────────────┐
│ [Turn: N]     [Turn Queue: Portraits Row]      [Team Panel]   │
│                                                               │
│                                                               │
│                      BATTLEFIELD GRID                         │
│                     (3D Isometric View)                       │
│                                                               │
│ [Current Unit]                            [Hovered Unit]      │
│    Widget                                     Widget          │
│                                                               │
│              [Ability Panel - Grid of Icons]                  │
└───────────────────────────────────────────────────────────────┘
```

---

## **2. IMPLEMENTED UI COMPONENTS** 

### **A. Turn Counter** ✅
**Location:** Top-left corner  
**Content:** "Turn [N]"  
**Updates:** Increments after all units complete turn cycle

### **B. Turn Queue Display** ✅
**Location:** Top center (horizontal row)  
**Content:** Portrait cards for each unit in initiative order, special "current unit" slot for popped unit  
**Per Card:**
```
┌──────────────┐
│  [Portrait]  │
│  Unit Name   │
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
- Toggle button for switching
- When player's turn = set to player's team, when enemy turn = set to enemy team, when player deals damage - switch to enemy team for animation duraton

### **F. Battlefield Visual Indicators** ✅

#### **Current Unit Highlight**
- **Type:** Blue decal circle under unit
- **Purpose:** Shows whose turn it is at a glance

#### **Target Highlighting**
- **Valid Targets:** Red decal circles
- **Trigger:** Ability selected
- **Coverage:** All units within reach of selected ability

#### **Position indicator**
- **Type:** Yellow decal circles
- **Purpose:** Shows non-hostile targeting (empty cell or friendly unit for special abilities)
- **Coverage:** All units within reach of selected ability

---

## **3. PLANNED/PARTIAL UI COMPONENTS** 

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
| State          | Visual                  | Interaction                   |
|----------------|-------------------------|-------------------------------|
| **Available**  | Full color              | Clickable                     |
| **Disabled**   | Grayscale               | Ignored (no click response)   |
| **Selected**   | Border highlight        | Shows targeting overlay       |
| **No Charges** | Grayscale + Red "X"     | Ignored                       |

**Hover Behavior:**
- Shows tooltip with ability details (see Tooltip section)

### **B. Effect Panel** ⚙️ *System Exists, Display TBD*
**Location:** 
- Above or near portrait in Current Unit Widget
- Above or near portrait in Hovered Unit Widget
- [NOT on battlefield models - too cluttered]

**Layout:** Horizontal icon row (max 10 effects)
```
┌─────┐
│  x3 │ ← Stack count (top-right, gray)
│     │ 
│2    │ ← Duration (bottom-left)
└─────┘
```

**Icon Requirements:**
- Distinct silhouettes (recognizable at small size)
- Color-coded by effect type:
  - Red: negative
  - Green: positive
  - Blue: neutral
  - Purple: Transformation
  - Yellow: stance

**Hover Behavior:**
- Shows tooltip with effect details (see Tooltip section)


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
- HP bars update (instant)

**Unit Removal:**
- Dead unit removed from battlefield
- Dead unit removed from queue
- Dead unit grayed out in team container
- Corpse spawns after death animation

**Queue Rearrangement:**
- Turn queue updates when units wait/summon/die

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
│ ├─ Immunities: [text]                 │
│ └─ Wards: [text]                      │
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

## **8. TOOLTIP SYSTEM**

### **Ability Tooltips** ⚙️ 

**Trigger:** Hover over ability icon (in ability panel OR popup)  
**Content:**
```
┌──────────────────────────────────────┐
│ [Ability Name]                       │
│                                      │
│ [Ability Description]                │
│ Describes what ability does in       │
│ natural language.                    │
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
│ Damage: 80 Fire (to all targets)     │
│ Targets: Target + Area (cross)       │
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
- Actual layout depends of action itself (return formatted text)

### **Effect Tooltips** ⚙️ *System Needed*

**Trigger:** Hover over effect icon (in effect panel)  
**Content:**
```
┌──────────────────────────────────────┐
│ [Effect Name]                        │
│                                      │
│ [Effect Description]                 │
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
- Any unit
- Current HP / Max HP
- Initiative value
- Unit name
- Effect icons (hoverable)

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
│  - Queue shifts                                             │
│  - Team selected unit frame update                          │
│  - Targeting for default ability setted up                  │
│  - UI unlocked for player input                             │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  ABILITY SELECTION                          │
│  - Player clicks ability icon, it is framed, previous not   │
│  - Targeting overlay refreshes                              │
│  - Valid targets highlighted                                │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  TARGET SELECTION                           │
│  - Hover shows damage preview                               │
│  - Click confirms target                                    │
│  - Ability can be changed again                             │
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

| State                  | Input Allowed            | Purpose                                   |
|------------------------|--------------------------|-------------------------------------------|
| **Unlocked**           | Full player control      | Ability selection, targeting              |
| **Locked (Animation)** | No input                 | Prevents double-actions during animation  | 
| **Locked (Game Over)** | No input                 | Battle resolved                           |  


## **13. POLISH & JUICE RECOMMENDATIONS**

### **Sound Design**
- Distinct UI sounds:
  - Click: Different sounds for valid/invalid actions
  - Hover: Subtle highlight sound
  - Turn start: Notification sound
  - Low HP: Warning sound when own unit below 25% HP

### **Unit Selection Feedback**
- Clicked ability icon bounces slightly
- Selected unit pulses (in addition to decal)
- Hover over unit scales model up 105%

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