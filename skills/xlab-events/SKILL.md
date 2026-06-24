---
name: xlab-events
description: Orchestrate XLAB event proposals, creative concepts, and RFP responses. Trigger whenever the user mentions an event brief, poptávka, RFP, nabídka na event, event concept, conference proposal, brand activation, experiential project, or immersive installation brief. Also trigger for analyzing incoming briefs, preparing brief cards, or discussing event strategy. This skill coordinates xlab-pricing (kalkulace), xlab-proposal (PPTX), xlab-content (brand voice), and xlab-brand (visual identity) into cohesive event deliverables.
---

# XLAB Events Skill

Orchestrator for the complete event proposal lifecycle — from brief intake through creative concept to final deliverables.

## When to Use

Trigger this skill when:
- An event brief, RFP, or poptávka arrives (any format: email, PDF, PPTX, verbal description)
- The user asks to create a proposal, nabídka, or concept for an event project
- The user wants to analyze a brief or prepare an internal brief card
- The user needs help with event strategy, dramaturgy, or spatial design
- The user asks about event types, proposal structure, or XLAB methodology

## Skill Dependencies

This skill orchestrates but does NOT replace:
- **xlab-pricing** → kalkulace / Excel pricing
- **xlab-proposal** → PPTX proposal generation
- **xlab-content** → brand voice and product portfolio text
- **xlab-brand** → visual identity, colors, logos

**External dependencies:**
- **Notion MCP** → Reference Library (primary source for signals, case studies, past projects). Fallback: local `references/` files.

## Core Workflow

```
BRIEF IN → INTAKE & ANALYSIS → ROUTING → CONCEPT / PROPOSAL → REVIEW → OUTPUT
```

### Phase 1: Intake & Brief Deconstruction

When a brief arrives, Claude performs structured analysis. Read `references/intake-checklist.md` for the complete intake framework.

**Step 1 — Extract facts** (what the brief explicitly states):
- Client, event name, date(s), location
- Audience (who, how many, profile)
- Budget (stated or implied range)
- Key requirements and deliverables
- Evaluation criteria (if RFP)
- Timeline and deadlines

**Step 2 — Gap analysis** (what the brief does NOT say but should):
- Creative latitude: how open is the client?
- Decision-maker profile: procurement vs. marketing vs. C-level?
- Competitive context: who else is pitching?
- Technical specifics missing (venue, AV, logistics)
- Success metrics not defined

**Step 3 — Brief Card** (structured summary for internal use):
Present the brief card to the user for confirmation before proceeding. The brief card is the single source of truth for all downstream work.

```
PROJECT:        [name]
CLIENT:         [name + segment]
TYPE:           [see event-types.md]
CREATIVE SCOPE: [standard / enhanced / full creative]
DATE:           [date(s)]
LOCATION:       [venue / city / TBD]
AUDIENCE:       [count + profile]
BUDGET:         [amount + currency]
LANGUAGE:       [CZ / EN / bilingual]
KEY MESSAGE:    [core communication objective]
XLAB TECH:      [mapping / hologram / avatar / LED / interactive / dome / other]
DEADLINE:       [proposal submission date]
GAPS:           [list of missing information]
```

### Phase 2: Routing

Based on the brief card, determine the output strategy. Read `references/event-types.md` for type definitions.

**Output types:**
1. **Full proposal** (PPTX + optional kalkulace) — for formal RFPs and competitive pitches
2. **Creative concept** (document or PPTX) — for open briefs where the idea is the pitch
3. **Technical solution** (document) — for installation/immersive projects where specs matter
4. **Quick response** (email/document) — for initial interest, rough estimate, or qualification round
5. **RFP questionnaire** — for structured RFP responses (fill-in format)

**Routing logic:**
- Formal RFP with scoring criteria → Full proposal + pricing
- Open creative brief → Creative concept + rough budget range
- Installation/immersive brief → Technical solution + creative concept + detailed pricing
- SAP-style agency RFP → RFP questionnaire + company presentation + pricing sheet
- Quick inquiry or sizing request → Quick response

### Phase 3: Concept & Proposal Generation

Read `references/proposal-structure.md` for the complete proposal framework.
Read `references/dramaturgy-framework.md` for creative methodology.

**Key principles (always apply):**

1. **Start from audience.** The first question is always "what should the attendee feel/know/do?" Technology choices follow from the answer.

2. **One throughline.** Every XLAB proposal has a single creative concept that ties everything together — a coherent experience narrative.

3. **Show understanding before showing ideas.** The proposal must prove XLAB understood the brief before presenting the creative solution. The ratio is roughly: 20% understanding, 60% solution, 20% proof (team + references + budget).

4. **Technology serves narrative.** XLAB's competitive advantage is tech expertise. Proposals lead with the experience and reveal the technology as enabler.

5. **Be specific.** Replace "cutting-edge technology" with "4× 15,000 lm laser projectors with automated calibration." Replace "engaging experience" with "visitors draw their own creatures on touchscreens; these appear in the dome projection 3 minutes later."

6. **Attendee journey is mandatory.** Every proposal must include a clear journey map — what happens from arrival to departure, step by step.

7. **Visualize whenever possible.** Moodboards, spatial diagrams, zone layouts, and run-of-show timelines are not optional extras — they are how XLAB sells.

### Phase 4: Delegation to Other Skills

When generating deliverables, delegate to the appropriate skills:

**For PPTX proposals:**
→ Use `xlab-proposal` skill for branded presentation output
→ Pass: project name, client, slide content structure

**For pricing/kalkulace:**
→ Use `xlab-pricing` skill for Excel pricing output
→ Pass: scope items, durations, team composition, equipment list

**For text content:**
→ Use `xlab-content` skill for brand voice compliance
→ Proposals are typically in English; internal concepts may be in Czech

**For visual identity:**
→ Use `xlab-brand` skill for logos, colors, typography

## Reference Sources — Notion First, Local Fallback

### Primary Source: Notion Reference Library (MCP)

When looking for references, case studies, or past project patterns, **always search Notion Reference Library first** via the Notion MCP connector.

**Database:** Reference Library (data source `collection://e7e6a68e-5255-4a2c-8843-99842ab49771`)

**How to search:**
- Use `Notion:notion-search` with `data_source_url: "collection://e7e6a68e-5255-4a2c-8843-99842ab49771"` and a relevant query
- Filter by Track (T1–T4), Technologie, Tagy, or free-text search
- For full content (case study body, transferable patterns), fetch individual pages with `Notion:notion-fetch`

**What's in Notion:**
- Signal cards (Typ = Signal) — short captures of industry projects, trends, technologies
- Case studies (Typ = Case Study) — detailed breakdowns with transferable patterns
- XLAB internal projects (Zdroj = Internal) — past XLAB proposals and projects with transferable patterns
- External references (Zdroj = External) — industry benchmarks and inspiration

**Search strategy by use case:**
| Need | Search approach |
|------|----------------|
| References for a conference proposal | Search by Track = "T1 Conferences" |
| Brand activation inspiration | Search by Track = "T2 Activations" |
| Immersive installation patterns | Search by Track = "T3 Culture & Art" |
| AI/digital technology references | Search by Track = "T4 AI & Digital" |
| Specific technology (e.g. projection mapping) | Search by Technologie tag |
| XLAB's own past work | Search by Zdroj = "Internal" |
| Deep production breakdowns | Search for Case Studies with Case Study Level = "Deep" |

### Fallback: Local Reference Files

If Notion MCP is unavailable (no connection, timeout, or tool not loaded), fall back to local curated files. These contain a baseline of references but are not actively maintained — Notion is the living source.

**Local files (read as needed, do NOT read all at once):**

| File | Read when... |
|------|-------------|
| `references/intake-checklist.md` | Analyzing a new brief or preparing a brief card |
| `references/event-types.md` | Classifying an event or selecting proposal approach |
| `references/proposal-structure.md` | Writing a proposal or structuring deliverables |
| `references/dramaturgy-framework.md` | Developing creative concepts or spatial design |
| `references/engagement-architecture.md` | Designing attendee engagement across touchpoints |
| `references/xlab-past-projects.md` | **Fallback only.** XLAB past project patterns — primary source is now Notion (Zdroj = Internal) |
| `references/curated-conferences.md` | **Fallback only.** T1 conference references — primary source is now Notion (Track = T1) |
| `references/curated-activations.md` | **Fallback only.** T2 activation references — primary source is now Notion (Track = T2) |
| `references/curated-culture-art.md` | **Fallback only.** T3 culture & art references — primary source is now Notion (Track = T3) |
| `references/curated-ai-digital.md` | **Fallback only.** T4 AI & digital references — primary source is now Notion (Track = T4) |
| `references/case-studies/*.md` | **Fallback only.** Deep case studies — primary source is now Notion (Case Study Level = Deep) |
| `preferences.md` | Checking accumulated creative preferences (local only, not in Notion) |

## Creative Principles

1. **Reference = orientation.** Extract principles from references and transform them into something original.
2. **Creative freedom is the default.** Past work sets the quality floor. The ceiling is open.
3. **Preferences accumulate, with room to break.** The `preferences.md` file captures patterns but Claude should break them when the brief demands it.
4. **Match creative intensity to brief scope.** A standard conference does not need a tech-art manifesto. A flagship experiential launch does.
5. **XLAB always proposes a creative concept.** Even for "standard" events, there is a throughline idea. XLAB does not deliver "just production."
6. **International awareness, local execution.** Reference global best practices (Expo pavilions, major brand activations, immersive art installations) but ground proposals in practical reality.

### Using References in Proposals

The Notion Reference Library (and fallback curated files) contain real-world signal cards and case studies — recent projects, technologies, and trends from the event and immersive technology industry. Use them to:

- **Ground proposals in reality.** When proposing a concept, search Notion for similar real-world projects that validate the approach. Example: "Interactive projection mapping on a product reveal" → search Notion by Track T2 + Technologie "projection mapping".
- **Find technology benchmarks.** When specifying tech, search for what was used on comparable projects. Example: "Real-time generative content" → search for case studies mentioning Notch, Disguise, or Unreal Engine.
- **Learn from XLAB's own work.** Search Notion by Zdroj = "Internal" to find transferable patterns from past XLAB projects.
- **Support pricing conversations.** Reference industry benchmarks to contextualize XLAB pricing.
- **Inspire creative concepts.** Search by Track T3 for artistic patterns that could translate to an event concept.

Do NOT quote signal cards verbatim in proposals. Extract the principle, adapt it to the brief, and present it as XLAB thinking.

## Language & Tone

### Language Selection
- Proposals for international / corporate clients → **English**
- Internal concepts and Czech clients → **Czech** (unless specified)

### Writing Mode — Two Distinct Registers

Claude must actively determine which register applies. If unclear, ask the user.

**Register 1: Communication (xlab-content rules apply strictly)**
Applies to: website text, social media, press releases, company descriptions, product descriptions, formal emails.
→ Full xlab-content voice rules. Factual, precise, no superlatives.

**Register 2: Creative (xlab-content rules are relaxed)**
Applies to: creative concepts, dramaturgical scripts, experience narratives, concept naming, spatial storytelling, pitch decks where the idea is being sold.
→ Language can be atmospheric, evocative, sensory. Metaphor and imagery are welcome.
→ The goal is to make the reader FEEL the experience — sensory, atmospheric, immersive language.
→ xlab-content's Communication Mode rules (banned phrases, no pathos, etc.) do NOT apply here.
→ The only constants: no exclamation marks, no emoji, no aggressive marketing tone, calm confidence.

**How to decide:** If the text describes what XLAB does → Register 1. If the text imagines what an experience could feel like → Register 2. When a proposal contains both (e.g., "About XLAB" section + "Creative Concept" section), switch registers between sections.

### Absolute Writing Rule: No Negative Framing

XLAB text never defines itself by what it is NOT. Always state what something IS.

**Banned patterns:**
- "X, not Y" / "X, nikoli Y"
- "This is not X, this is Y"
- "We don't do X — we do Y"
- "Unlike X, we..."
- "It's not about X, it's about Y"
- Any construction where the primary rhetorical device is contrast against a negative

**Instead:** State the positive directly. Let the quality speak for itself.

Bad: "The tunnel is not a corridor — it is a dramaturgical transition."
Good: "The tunnel functions as a dramaturgical transition between two experiential phases."

Bad: "XLAB does not deliver just production. We deliver experience design."
Good: "XLAB delivers experience design — from concept through production to on-site execution."

Bad: "This is not a technology demo. This is an emotional journey."
Good: "The installation is designed as an emotional journey, with technology serving the narrative."

This rule applies in BOTH registers — communication and creative. Zero exceptions.

## Important Rules

- **Holobox and Avatar are ALWAYS separate line items** in pricing (Holobox 20k CZK, Avatar 10k CZK Standard).
- **Creative/intellectual work uses Set/celek** (qty default 1) — never expose day counts to clients.
- **Team members are named** with roles and relevant references in proposals.
- **XLAB often partners** with other companies (New Wave, Event Arena, WOW Factor Hungary, etc.) — reflect this when the scope exceeds pure tech/content.
- **Never commit to specific dates or prices** in concepts — use "subject to confirmation" or "to be detailed in final proposal."
