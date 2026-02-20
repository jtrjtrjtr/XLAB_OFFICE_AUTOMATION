---
name: xlab-pricing
description: Generate XLAB event pricing calculations. Two modes — Standard (reads bundled ceník XLSX) and Freeform (custom prices without ceník). Outputs branded Excel with Kalkulace + Summary sheets. Use when user asks for kalkulace, cenová nabídka, pricing, cost estimate, or budget.
---

# XLAB Pricing Skill

Generate professional event pricing calculations as branded Excel files.

## When to Use

Trigger when the user asks for:
- **kalkulace**, **cenová kalkulace**, **pricing**, **cost estimate**, **budget**
- **kolik by stálo...**, **nacenit**, **připravit ceny**
- Any request to price an XLAB event, conference, activation, or project

**Skill routing:**
- Pricing/kalkulace → **this skill** (xlab-pricing)
- Proposal/nabídka PPTX → `xlab-proposal` skill
- General presentation → `xlab-pptx-template` or public `pptx` skill

## Two Modes

### Standard Mode (default)
Uses bundled ceník `SKILL_DIR/data/XLAB_Centralni_Cenik_v5.xlsx` for automatic price lookup. Ceník auto-detection priority:
1. User upload in current conversation (if newer version uploaded)
2. Bundled ceník in `SKILL_DIR/data/`
3. Skill installation path `/mnt/skills/user/xlab-pricing/data/`

### Freeform Mode
For non-standard projects that don't fit XLAB's ceník templates. Triggered when:
- User says: "kalkulace bez ceníku", "vlastní ceny", "freeform", "nestandardní projekt"
- Input JSON has `"freeform": true` in metadata
- User provides all prices directly

In freeform mode, every item must include `unit_price_sell` (and optionally `unit_price_cost`). The same Excel design is generated — just without automatic ceník lookup.

**Example freeform input:**
```json
{
  "metadata": {
    "client": "BMW", "event": "Custom Installation",
    "date": "2026-06-01", "freeform": true
  },
  "items": [
    {"name": "Custom LED Wall", "category": "Hardware", "unit_price_sell": 85000, "unit_price_cost": 52000, "quantity": 1, "days": 3, "unit": "set"},
    {"name": "Installation Crew", "category": "Labour", "unit_price_sell": 800, "unit_price_cost": 450, "quantity": 18, "days": 3, "unit": "h"}
  ]
}
```

## Architecture

```
User describes event
  ├─ Standard → Claude maps to ceník items → calculate.py → generate_excel.py → Excel
  └─ Freeform → Claude builds items with custom prices → calculate.py --freeform → generate_excel.py → Excel
```

## Data Sources

### Ceník XLSX v5 (bundled in SKILL_DIR/data/)

Columns: A=Položka, B=Popis (client description), C=Jednotka, D=Nákladová, E=Snížená, F=Standard, G=Premium, H=Poznámka (internal)

6 sheets:
- **Lidé** — 38+ roles (hourly rates)
- **Technika** — 30+ items (daily/set rates)
- **Produkce & Logistika** — 44+ items
- **Pravidla** — pricing rules
- **Alokační šablony** — 7 event type templates
- **Sestavy** — 16 typical assemblies

### Updating the Ceník
To update prices: download this skill ZIP → unzip → edit `data/XLAB_Centralni_Cenik_v5.xlsx` in Excel → save → re-zip → re-upload skill. No script changes needed for price updates.

## File Naming Convention

Output files follow: `CE_{JobNr}_{Klient}_{Projekt}_v01.xlsx`

Before generating, ask the user for:
- **Job Nr.** (if known)
- **Klient** (client name)
- **Projekt** (project/event name)

If not provided, use placeholders: `CE_JobNr_Klient_Projekt_v01.xlsx`

## Workflow

### Step 1: Understand the Brief

Extract from user's description:

| Parameter | Example | Default |
|-----------|---------|---------|
| **Event type** | konference, gala, aktivace | — (required) |
| **Duration** | 1 den, 2 dny | 1 den |
| **Tier** | standard, snížená, premium | Standard |
| **Scale** | 50 lidí, velká | infer from type |
| **Special needs** | streaming, LED, avatar | none |
| **Client** | VISA, Coca Cola | — (ask) |
| **Event name** | Winter Meeting 2026 | — (ask) |
| **Job Nr.** | 2026-042 | — (ask) |
| **Date** | 15.3.2026 | today |
| **Freeform?** | bez ceníku, vlastní ceny | false |

### Step 2: Select Template & Items (Standard Mode)

Match event to closest **Alokační šablona**:

| Template | Keywords |
|----------|----------|
| Press Conference | tiskovka, TK, press |
| Střední Event | event, akce, středně velká |
| Gala / Winter Meeting | gala, večírek, ples |
| Mezinárodní aktivace | F1, international, aktivace |
| Konference (Ventuz) | konference, conference, Ventuz |
| HoloboX | holobox, hologram, avatar |
| Dealer Meeting | dealer meeting, full service |

### Step 3: Build Item List

**On-site production — CRITICAL RULE:**
All personnel rates in ceník are **hourly**. For on-site roles:
- Default: `quantity = persons × 9` (standard day), `unit = "h"`, `days = N`
- Stage Hands: e.g. 4 persons × 9h = `quantity = 36`, `unit = "h"`
- Use `"persons": N` in input JSON — calculate.py converts automatically
- Alternative (on request): `"use_daily": true` to use daily rates instead

**Tech progression** (baked into effective_days):
- 2 dny = 1.5× cena
- 3 dny = 2× cena
- 5 dní = 3× cena

### Step 4: Run Calculation

```bash
# Standard mode (ceník auto-detected):
python3 SKILL_DIR/scripts/calculate.py \
  --input /tmp/calc_input.json \
  --output /tmp/calc_result.json

# With specific ceník:
python3 SKILL_DIR/scripts/calculate.py \
  --cenik /path/to/cenik.xlsx \
  --input /tmp/calc_input.json \
  --output /tmp/calc_result.json

# Freeform mode:
python3 SKILL_DIR/scripts/calculate.py \
  --freeform \
  --input /tmp/calc_input.json \
  --output /tmp/calc_result.json
```

### Step 5: Generate Excel

```bash
python3 SKILL_DIR/scripts/generate_excel.py \
  --input /tmp/calc_result.json \
  --output /mnt/user-data/outputs/CE_JobNr_Klient_Projekt_v01.xlsx
```

Assets (logos) are auto-detected from `SKILL_DIR/assets/`.

## Excel Design Specification

### Layout
- **R1**: empty (logo space)
- **R2-R4**: Logo left + meta right (Klient/Projekt/Job Nr. in E-H)
- **R5**: Title "Cenová kalkulace" (16pt bold navy) + Datum
- **R7**: Table headers — charcoal (#333333) fill, white text
  - B "Položka" + C "Popis": LEFT aligned
  - D-H: CENTER aligned
  - K-O: Orange internal headers
- **R8+**: Data rows grouped by category

### Columns
| Col | Width | Content |
|-----|-------|---------|
| A | 3.0 | Spacer |
| B | 31.3 | Položka |
| C | 19.5 | Popis (client description) |
| D | 11.0 | Cena/jed. (NO fill) |
| E | 7.0 | Mn. (warm accent fill) |
| F | 9.0 | Jednotka (no fill) |
| G | 5.0 | Dní (warm accent fill) |
| H | 11.5 | Celkem CZK |
| I | 1.5 | Separator |
| K-O | varies | Internal (orange theme) |

### Color Palette — Grayscale + Warm Gray-Yellow
| Name | Hex | Usage |
|------|-----|-------|
| CHARCOAL | #333333 | Primary text, table header fill |
| LIGHT_TXT | #888888 | Notes, popis |
| WARM_1 | #F7F3EC | Editable cells (E, G columns only) |
| WARM_2 | #EDE7DC | Internal category headers (K-O) |
| WARM_3 | #E3DDD2 | Subtotal row fills |
| WARM_BIG | #BFB8AD | Category headers A-H + CELKEM row A-H |
| WARM_4 | #D4CEC3 | Internal CELKEM fill (K-O) |
| NAVY | #1F4E79 | Title "Cenová kalkulace" only |
| ORANGE | #CC6600 | Internal section (headers, text, editable) |
| GREEN | #2E7D32 | Profit display |

### Data Row Styling
- All cells: **vertical-center** alignment
- Font: Helvetica Light 10pt, color #333333
- D column: no background fill
- E, G columns: WARM_1 (#F7F3EC) fill
- Popis (C): 9pt italic #888888, wrap text, v-center

### Category Headers
- Merge A-H, fill WARM_BIG (#BFB8AD)
- Font: Helvetica Light 10pt bold #333333
- Internal K-O: fill WARM_2 (#EDE7DC)

### Subtotals
- Label: "Celkem {category}", merge A-G, right-aligned
- Fill: WARM_3 (#E3DDD2) across A-O
- Font: bold #333333

### Summary Section
- MEZISOUČET: bold, right-aligned
- Sleva z techniky: % editable in F (WARM_1 fill)
- Agency fee: % editable in F (WARM_1 fill)
- CELKEM bez DPH: 12pt bold, left-aligned, WARM_BIG fill A-H, WARM_4 fill K-O

### Footer
- X icon at A{row}
- Contact: M/E/W labels (8pt) in C, values in D
- Company: IČO, DIČ, BANKA in E-F
- Address: XLAB s.r.o. / Výstaviště 67 / 170 00 Praha 7 in H
- Internal summary: K-O (Celkové náklady, Celkový zisk, Celková marže)

### Summary Sheet
- Title: "Cenová kalkulace — souhrn" (16pt bold navy)
- Meta: Client — Event
- Table: Category | Celkem CZK (with formulas referencing Kalkulace sheet)
- Alternating WARM_1 accent on rows
- CELKEM bez DPH row: WARM_4 fill
- Designed for copy-paste into PPTX proposals

### Print Area
- Kalkulace: A1:H{total+6}, landscape, fit to width
- Summary: A1:C{total+2}

## Pricing Rules

### Tiers
| Tier | Multiplier |
|------|-----------|
| Nákladová | varies (internal cost) |
| Snížená/Partner | Standard × 0.80 |
| Standard | 100% |
| Premium | Standard × 1.20 |

### Other Rules
- EUR = Standard ÷ 25
- Rounding: ≥200 CZK → round to 50; <200 → whole numbers
- Max discount: 20%
- Default agency fee: 0% (adjustable)
- Discount applies only to Technika category

## Item Matching Guide (Standard Mode)

### Media Servers
- Simple presentation → **Media Server 4K + režie** (15k)
- Medium with Ventuz → **3D Media Server 2×4K + režie** (35k)
- Large multi-screen → **3D Media Server 4×4K + režie** (85k)

### Operators
- Without 3D Media Server → **Video Operator** (1 100/h)
- With 3D Media Server → **3D Media Server Operator** (1 250/h)

### LED Screens
- Small → **LED 3×2,5 m** (20k)
- Medium → **LED 5×3 m** (30k)
- Large → **LED 8×3 m** (40k)

## Error Handling
- **Item not found**: Warn user, ask for clarification
- **Ceník not found**: Auto-detect from bundled data; if truly missing, suggest freeform mode
- **Ambiguous description**: Ask user to clarify
- **Price = 0**: Flag as "individuální — doplnit ručně"

## Language
- Default: **Czech** (item names, headers, labels)
- User communication: follow user's language preference
