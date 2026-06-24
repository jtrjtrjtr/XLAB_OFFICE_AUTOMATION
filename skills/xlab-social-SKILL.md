---
name: xlab-social
description: >
  Generate social media content for XLAB's Instagram and LinkedIn company page.
  Produces bilingual (CZ + EN) post packages including captions, cover text suggestions,
  visual direction, and hashtags — all following XLAB brand voice.
  Use this skill whenever the user mentions social media posts, Instagram, LinkedIn,
  posting about an event, sharing a project on socials, writing a caption,
  or preparing content for XLAB's social channels. Also trigger when the user
  describes a completed event or project and wants to communicate it externally.
  Always use together with xlab-content (brand voice) and xlab-brand (visual identity).
---

# XLAB Social Media Skill

Generate ready-to-publish social media content for XLAB's Instagram and LinkedIn (company page).

Every output is bilingual — Czech and English versions are always generated together.

## Dependencies

This skill builds on two other XLAB skills. Read them before generating content:
- **xlab-content** → brand voice rules, tone, word replacements, product portfolio descriptions
- **xlab-brand** → colors, typography, logo placement rules for visual direction

## When to Use

Trigger when the user:
- Wants to post about a completed XLAB event, project, or installation
- Asks for Instagram or LinkedIn content
- Says "napiš post", "připrav příspěvek", "social media", "IG post", "LinkedIn post"
- Describes an event/project and wants to share it externally
- Asks for captions, hashtags, or cover text suggestions

## Input Processing

The user will typically provide a brief about an event or project. Extract these elements:

| Element | Why it matters |
|---------|---------------|
| What happened | Core of the post — the event, installation, technology used |
| Client / brand | Tagging, context (some clients prefer to remain unnamed — ask if unclear) |
| Location + date | Adds specificity and credibility |
| Scale / numbers | Audience size, screen count, projection area — concrete facts carry more weight than adjectives |
| XLAB's role | What exactly did XLAB do — concept, production, content, technology, all of it |
| Visual assets available | Photos, video, BTS — determines format recommendations |

If the user's brief is thin (missing several elements), ask one focused follow-up question rather than a long list. Prioritize: what happened, what technology, and what visual assets exist.

## Output Structure

For every request, produce this complete package:

---

### 1. INSTAGRAM

#### 1a. Caption (CZ)

The Czech Instagram caption. Structure:

- **Opening line** — one sentence that says what the post is about. Start with a fact or context. This line appears in the feed preview, so it must work standalone.
- **Body** — 2–4 sentences expanding on what happened, what technology was used, what XLAB's role was. Include at least one concrete fact (number, technology name, dimension). Keep total caption between 150–400 characters for best engagement — longer is acceptable if the content justifies it.
- **Closing** — optional. If there's a natural closing thought, include it. If the body says everything, end there.
- **Hashtags** — on a separate line after a line break. See Hashtag Strategy below.

#### 1b. Caption (EN)

English version. Not a translation — rewrite for an international audience. The structure mirrors CZ but the phrasing should feel native. English captions can be slightly more concise.

#### 1c. Cover Text Suggestion

Short text for the first image of the post (the cover that appears in the grid). Constraints:
- Maximum 6–8 words (ideally fewer)
- Must be readable at small grid size
- Typically: event name, or a short descriptor of what's shown
- Provide both CZ and EN variants
- Include visual direction: recommend which XLAB brand theme (black/white), text placement (center, bottom-left), and whether the text overlays a photo or sits on a solid background

#### 1d. Format & Visual Recommendation

- Recommend format: single image (1:1 or 4:5), carousel, or Reel
- Describe what the ideal visual would show — be specific: "wide shot of the facade with mapping active, audience visible in foreground"
- If carousel: suggest slide sequence (e.g., "1. wide shot of mapping, 2. detail of content on facade, 3. BTS of projection setup, 4. audience reaction")

---

### 2. LINKEDIN

#### 2a. Post Text (CZ)

LinkedIn posts from XLAB's company page have a different character than Instagram. They provide more context and professional framing.

Structure:
- **Opening line** — the hook that appears before "...zobrazit více". Make it count — one specific, interesting sentence.
- **Context** — what was the project, who was the client (if public), what was the challenge or brief
- **What XLAB did** — specific role, technologies, approach. This is where the professional audience wants detail. Name the technologies: Disguise, Notch, Resolume, LED volume, projection mapping — whatever applies.
- **Result or impact** — audience size, client feedback (if available), a concrete outcome
- **Closing** — a forward-looking sentence or acknowledgment of the team/partners.

Length: 800–1500 characters (sweet spot for company page engagement). Can go longer for complex projects.

LinkedIn posts carry hashtags only when the user specifically requests them. If included: 3–5 maximum at the very end, separated by a line break.

#### 2b. Post Text (EN)

English version for LinkedIn. Same structure, rewritten for international professional audience.

#### 2c. Visual Recommendation

- Recommend: single image, carousel (document post), or video
- LinkedIn favors landscape (16:9) or square (1:1) images
- Describe the ideal visual — same specificity as Instagram recommendation
- For carousels: LinkedIn uses PDF/document uploads, so suggest slide content

---

## Voice Rules (Quick Reference)

These are derived from xlab-content. Apply them to every caption and post:

- **Lead with facts.** "Projection mapping on a 40-metre facade" says more than any adjective.
- **Use concrete language.** Name the technology, the scale, the material. Specifics build credibility.
- **Write in direct positive statements.** Every sentence says what something is or does. Contrastive constructions ("X, not Y") are banned from all XLAB text.
- **Keep the tone calm and confident.** XLAB communicates through the quality of the work.
- **Let numbers speak.** "12 projectors, 3000 m² of projection surface" is more persuasive than evaluation.
- **Start with a fact.** First sentence says what the post is about.
- **Czech specifics:** Use "videomapping". Use "imerzivní".
- **English specifics:** Use "projection mapping". Use "immersive".

## Hashtag Strategy

### Core hashtags (always include)

```
#XLAB #XLABRealtime
```

### Category hashtags (pick 2–3 based on content)

| Category | CZ/Neutral hashtags | EN hashtags |
|----------|-------------------|-------------|
| Projection mapping | #videomapping #projectionmapping #mappingshow | #projectionmapping #videomapping |
| Events & production | #eventproduction #stagedesign #showdesign | #eventtech #liveevents #eventproduction |
| Holographic | #hologram #holobox #holographic | #hologram #holographic #holographicdisplay |
| Digital avatars | #digitalavatar #AIavatar | #digitalavatar #AIavatar #virtualassistant |
| Immersive | #immersive #immersiveexperience | #immersive #immersiveexperience #immersiveart |
| Interactive | #interactiveinstallation #interactiveart | #interactiveinstallation #interactiveart |
| LED / visual tech | #LEDwall #visualtechnology | #LEDwall #LEDdisplay #visualtechnology |

### Contextual hashtags (pick 2–4 based on specifics)

Add hashtags relevant to:
- **Location:** #Prague #Brno #Praha (for Czech events), city/country for international
- **Client industry:** #automotive #pharma #tech #FMCG — only if the client is publicly named
- **Event type:** #conference #gala #festival #productlaunch #exhibition
- **Technology:** #Disguise #Notch #Resolume #TouchDesigner #Unreal — if specific tools are notable

### Total hashtag count

- **Instagram:** 8–15 hashtags (core + category + contextual)
- **LinkedIn:** 0 by default. If requested: 3–5 maximum, at the end.

## Platform-Specific Notes

### Instagram

- XLAB posts from the company account @xlab.cz (verify current handle with user if unsure)
- Grid aesthetic matters — cover images should be visually consistent
- Carousel posts get higher reach than single images — recommend carousel when multiple strong visuals exist
- Reels get highest reach — recommend when video footage exists
- Tag client accounts when relationship is public (ask user if unsure)
- Location tag: always recommend adding it

### LinkedIn (Company Page)

- Company page posts have lower organic reach than personal profiles — the text must earn clicks on "...zobrazit více"
- First line is critical: it must be specific and interesting enough to expand
- Professional audience expects: what technology, what challenge, what result
- Tagging the client company increases reach — recommend it when appropriate
- Employee reshares are the primary reach amplifier — note this to the user when relevant

## Example Output

Below is a condensed example to illustrate tone and structure. Real outputs should be fuller.

**Input:** "Dělali jsme videomapping na fasádu Rudolfina pro Českou filharmonii, 25. výročí sezóny. 6 projektorů, celá přední fasáda. Máme fotky i video."

**Instagram CZ:**
```
Videomapping na fasádě Rudolfina pro Českou filharmonii – 25 let koncertní sezóny.

Šest projektorů, celá přední fasáda proměněná pohyblivým obrazem a hudbou.
Obsah jsme navrhli tak, aby respektoval neoklasicistní architekturu budovy
a zároveň ji dal do pohybu.

#XLAB #XLABRealtime #videomapping #projectionmapping
#mappingshow #Prague #Praha #CeskaFilharmonie
```

**Instagram EN:**
```
Projection mapping on the Rudolfinum facade for the Czech Philharmonic –
marking 25 years of the concert season.

Six projectors, the entire front facade transformed with moving image and music.
Content designed to respect the neoclassical architecture while setting it in motion.

#XLAB #XLABRealtime #projectionmapping #videomapping
#mappingshow #Prague #CzechPhilharmonic #architecturalmapping
```

**Cover text CZ:** RUDOLFINUM — 25 LET
**Cover text EN:** RUDOLFINUM — 25 YEARS
**Visual direction:** Black theme, text centered lower third, overlaying a wide shot of the active mapping. White uppercase text, yellow accent line above.

**Format:** Carousel (1. wide facade shot with mapping active, 2. detail of animated content, 3. projection setup / BTS, 4. audience perspective). Also recommend a Reel cut from the video footage.

**LinkedIn CZ:**
```
Videomapping na Rudolfinu – šest projektorů, celá přední fasáda, příležitost
oslavit 25 let koncertní sezóny České filharmonie.

Neoklasicistní architektura Rudolfina má přísný řád – sloupy, římsy, symetrie.
Obsah jsme navrhli tak, aby tento řád respektoval a pracoval s ním. Animace
sleduje geometrii budovy, reaguje na její proporce a postupně ji uvádí do pohybu.

Technika: 6× projektor 20 000 lm, edge blending, 3D kalibrační systém přizpůsobený
členité fasádě. Realizace proběhla v jedné noci včetně montáže, kalibrace a živého
vysílání.
```

**LinkedIn EN:**
```
Projection mapping on the Rudolfinum — six projectors across the entire front
facade, celebrating 25 years of the Czech Philharmonic concert season.

The Rudolfinum's neoclassical architecture follows a strict order — columns,
cornices, symmetry. We designed the content to respect and work within that order.
Animation follows the geometry of the building, responds to its proportions,
and gradually sets it in motion.

Setup: 6× 20,000 lm projectors, edge blending, 3D calibration system adapted
to the articulated facade. The entire production — rigging, calibration,
and live show — was completed in a single night.
```

## Checklist Before Output

Run this internally before presenting the output to the user:

1. Does every caption start with a fact?
2. Does every sentence say what something is or does? (Zero contrastive "X, not Y" constructions.)
3. Is at least one concrete number or technical detail included?
4. Are CZ and EN versions independent rewrites (not translations)?
5. Is the cover text ≤ 8 words?
6. Are hashtags correctly split (core + category + contextual)?
7. Is the visual recommendation specific?
8. Does the LinkedIn opening line work as a standalone hook?
9. Punctuation: periods and em dashes only.
10. Would someone outside the industry understand what the post is about?
