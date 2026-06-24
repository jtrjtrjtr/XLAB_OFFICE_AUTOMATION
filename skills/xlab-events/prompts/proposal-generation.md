# Proposal Generation — Prompt Instructions

## Purpose

Instructions for Claude when generating XLAB event proposal content. This file guides the transition from brief card to actual deliverable content.

## Before You Write

1. Confirm the Brief Card is complete and approved by the user
2. Determine event type (→ event-types.md)
3. Select proposal modules (→ proposal-structure.md)
4. Check preferences (→ preferences.md)
5. Check past projects for relevant patterns (→ xlab-past-projects.md)

## Writing Process

### Step 1: Find the Throughline

Before writing any slide or section, define the creative concept in one sentence:

**Template:** "[Concept Name] — [what it is] that [what it does for the attendee/client]."

Examples:
- "Anima Montis — a living forest organism that transforms visitors into microscopic witnesses of nature's hidden infrastructure."
- "Mirror — a reflection across 200 years that connects tradition with the courage to look forward."
- "Inside the Craft — a glass-bottom portal that makes the familiar extraordinary."

If the concept doesn't fit in one sentence, it's not sharp enough.

### Step 2: Build the Journey

Map the attendee experience from arrival to departure. Use the Five-Phase Arc from dramaturgy-framework.md. For each phase, note:

- What the attendee sees / hears / does
- What they feel (emotional state)
- Where they are (spatial position)
- What XLAB technology is active

### Step 3: Write Slide Content

For each selected module, write content following these rules:

**Slide titles:** Action-oriented or concept-driven. Not "About XLAB" but "Who We Are and Why This Brief." Not "Technical Solution" but "How the Experience Works."

**Slide body:** Maximum 5 text elements per slide. If you need more, split into two slides. Every slide should have a clear visual direction note (what image, diagram, or render should accompany the text).

**Speaker notes:** Include talking points that expand on the slide content. The presentation will be presented, not just sent — speaker notes help the presenter.

### Step 4: Build Supporting Materials

Depending on event type, generate:

- **Zone layout / spatial diagram** (description for designer or as SVG/HTML artifact)
- **Run-of-show timeline** (table format)
- **Technology specification** (table format: component, spec, purpose, cost tier)
- **Team matrix** (name placeholder, role, relevant experience)
- **Reference selection** (3–5 projects with 1-line rationale for each)

### Step 5: Pricing Brief

Prepare a pricing brief for the xlab-pricing skill:

```
PRICING BRIEF
Project: [name]
Client: [name]
Mode: [Standard / Freeform]
Currency: [CZK / EUR]

CATEGORIES:
- People: [list roles × days]
- Technology: [list equipment]
- Production & Logistics: [list items]
- Content Production: [list deliverables as Set/celek]
- Travel: [if applicable]

NOTES:
- [any special pricing considerations]
```

## Quality Checklist

Before presenting any proposal content to the user:

- [ ] Does every section connect back to the throughline concept?
- [ ] Is the attendee journey clearly mapped?
- [ ] Does the proposal demonstrate understanding of the brief before presenting solutions?
- [ ] Are technology choices justified by experience needs, not listed for their own sake?
- [ ] Are references relevant to this specific brief?
- [ ] Is the language free of superlatives and negative framing patterns?
- [ ] Is there a clear peak moment identified?
- [ ] Would a reader scanning for 3 seconds per page understand the structure?
- [ ] Are budget and timeline realistic and caveated appropriately?
- [ ] Have Holobox and Avatar been separated (if applicable)?
- [ ] Is creative work priced as Set/celek (not exposed day counts)?
- [ ] **Register check:** Are creative sections (concept, journey, spatial narrative) written in vivid atmospheric language? Are factual sections (team, specs, budget) written in precise communication language?
- [ ] **Negative framing check:** Zero instances of "X, not Y" / "this is not X" / "unlike X" patterns?

## Tone Reference

**Two registers — use both within the same proposal as appropriate:**

**Register 1 — Communication (factual sections: About, Team, Tech specs, Budget):**
"The installation uses four 15,000-lumen laser projectors arranged at floor level, projecting upward onto a grey textile dome surface. Edge blending and automatic calibration produce a single seamless 360° image. The grey surface reduces cross-reflection between projectors and improves contrast in atmospheric dark scenes."

**Register 2 — Creative (concept sections: Creative concept, Journey, Spatial narrative):**
"The visitor enters the tunnel and the world shrinks. LED filaments pulse along the walls like a nerve signal travelling between two hemispheres of a living organism. By the time the dome opens ahead, the visitor is no longer a tourist — they are inside the mountain."

**Never XLAB voice (regardless of register):**
"Our cutting-edge, state-of-the-art projection system delivers a breathtaking, mind-blowing 360° immersive experience that will leave your visitors speechless!"

**Also never XLAB voice (negative framing):**
"The tunnel is not a corridor — it is a dramaturgical transition."
→ Fix: "The tunnel functions as a dramaturgical transition between experiential phases."

## Delegation Checklist

When the content is ready:
- [ ] For PPTX output → hand off to xlab-proposal skill with slide structure
- [ ] For pricing Excel → hand off to xlab-pricing skill with pricing brief
- [ ] For text compliance → validate against xlab-content skill voice rules
- [ ] For visual identity → apply xlab-brand skill colors and assets
