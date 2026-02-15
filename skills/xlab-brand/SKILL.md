---
name: xlab-brand
description: Apply XLAB brand identity to any deliverable — presentations (PPTX), documents (DOCX), HTML pages, artifacts, social media graphics, or any visual output. Use this skill whenever the user mentions XLAB, asks for brand-consistent materials, wants to create a presentation/document/page for XLAB, or references XLAB's visual identity. Also trigger when the user says "apply the XLAB theme", "make it on-brand", "use our brand", or asks for event proposals, pitch decks, capabilities presentations, or any client-facing materials for XLAB.
---

# XLAB Brand Skill

Apply XLAB's official brand identity consistently across all deliverables.

## When to use

Trigger this skill for any output that should carry the XLAB brand: slides, documents, HTML pages, React artifacts, social media graphics, email templates, proposals, reports. If it's going to a client or audience and it's for XLAB, use this skill.

## Quick Reference

### Colors

| Name | Hex | Usage |
|------|-----|-------|
| XLAB Black | `#000000` | Primary background |
| XLAB White | `#F8F7F2` | Primary text, logo |
| Neon Greenish Yellow | `#E3E829` | Accent only — headings, icons, buttons, overlines |
| Mid Gray | `#4a4a4a` | Captions, dividers |
| Dark Gray | `#1a1a1a` | Secondary dark background |

**Yellow rules**: Use for headings, icons, buttons, light beam elements, overlines. Never as a background fill or gradient. **Never use yellow for text on white or light backgrounds** — yellow text lacks contrast and is poorly readable on light surfaces. Use XLAB Black for text on light backgrounds instead. Yellow decorative elements (lines, icons, accents) are fine on any background.

### Typography

| Role | Font | Fallback |
|------|------|----------|
| Headlines (H1) | GT America Extended Bold | Helvetica Neue Bold / Arial Bold |
| Subtitles (H2) | GT America Thin | Helvetica Neue Thin / Arial |
| Body text | GT America Medium | Helvetica Neue / Arial |

**Fallback rules:**
- For PPTX/DOCX: Use `Arial` (universally available)
- For HTML: Use CSS font stack `'GT America', 'Helvetica Neue', Helvetica, Arial, sans-serif`

Headlines are always uppercase.

### Brand Symbol (X)

The XLAB "X" symbol is formed by four triangular light beams.

**IMPORTANT — Aspect ratio:** The X symbol is a landscape rectangle, NOT a square. Original pixel dimensions are 1056 × 662 px (aspect ratio approximately 1.6 : 1). Always maintain this ratio when embedding. Never stretch or compress the symbol into a square.

#### Assets (local — bundled with this skill)

All brand assets are stored in the `assets/` directory relative to this skill file.

| Asset | File | Dimensions | Use case |
|-------|------|-----------|----------|
| X symbol (white) | `assets/x_symbol_white.png` | 1056×662 px | On black/dark backgrounds |
| X symbol (black) | `assets/x_symbol_black.png` | 1056×662 px | On white/light backgrounds |
| XLAB logo (white) | `assets/x_logo_white.png` | 1398×248 px | Full XLAB logo, dark backgrounds |
| XLAB logo (black) | `assets/x_logo_black.png` | 1398×248 px | Full XLAB logo, light backgrounds |

**How to access assets in code:**

The assets are located at `/mnt/skills/user/xlab-brand/assets/`. To use them:

```python
# Python — get asset path
import os
SKILL_DIR = "/mnt/skills/user/xlab-brand"
ASSETS_DIR = os.path.join(SKILL_DIR, "assets")

x_symbol_white = os.path.join(ASSETS_DIR, "x_symbol_white.png")
x_symbol_black = os.path.join(ASSETS_DIR, "x_symbol_black.png")
x_logo_white = os.path.join(ASSETS_DIR, "x_logo_white.png")
x_logo_black = os.path.join(ASSETS_DIR, "x_logo_black.png")
```

For HTML artifacts, read the image file and embed as base64 data URI:

```python
import base64
with open(x_symbol_white, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()
    data_uri = f"data:image/png;base64,{b64}"
```

#### Placement rules

- The X symbol goes in the **bottom-right corner** of slides, pages, and social posts
- Choose **white or black** variant based on the slide/page background color
- **NEVER display the X symbol on the first slide (cover/title slide)** of a presentation — the cover slide uses only the text-based XLAB identity
- On all other slides, the X symbol is mandatory in the bottom-right corner
- Minimum size: 30px
- Clear space around symbol: minimum half its height

#### Embedding

**Always respect the 1.6:1 width-to-height ratio.** Example sizes that maintain correct proportions:
- Small (footer/watermark): w: 0.30", h: 0.19"
- Medium: w: 0.48", h: 0.30"
- Large: w: 0.80", h: 0.50"

- **PPTX**: Copy the PNG from the skill assets directory, then use `slide.addImage({ path: "<local_path>", x: 9.35, y: 5.1, w: 0.30, h: 0.19 })` for a small bottom-right placement on a 16:9 slide
- **HTML**: Read the asset file, convert to base64, and embed as `<img src="data:image/png;base64,..." style="aspect-ratio: 1056/662;">`
- Do not attempt to recreate the symbol with SVG — always use the provided PNG assets
- **Never set equal width and height** — the symbol is a rectangle, not a square

## Layout Rules

### Presentations (PPTX)

Key points:
- Black background slides with white text as default
- Yellow for overlines, key numbers, accent text
- X symbol bottom-right on every slide **except the cover/title slide**
- Page number bottom-left on every slide
- Footer area: page number (left), X symbol (right) — keep minimal, no full-width bars
- Centered composition for title/cover slides
- Two-column layouts for content slides (text left, images right)

### Social Media

- Centered composition, centered text alignment
- Brand symbol always bottom-right corner
- Typography must not completely cover photo content

### Documents (DOCX, PDF)

- X symbol top-left (small, subtle) on letterhead
- XLAB logo + contact info at bottom
- Yellow accent for headings and horizontal rules

### HTML / Artifacts

- Use CSS variables for brand colors:
  ```css
  :root {
    --xlab-black: #000000;
    --xlab-white: #F8F7F2;
    --neon-yellow: #E3E829;
    --mid-gray: #4a4a4a;
    --dark-gray: #1a1a1a;
  }
  ```
- Dark theme by default (black bg, white text)

## Forbidden

These rules come from the brand manual and must always be respected:

- No color gradients on backgrounds
- No transparency changes on brand elements
- No rotating, skewing, or distorting the logo or symbol
- No adding slogans or text to the logo
- No colors other than black, white, or yellow on brand elements
- No graphic effects (shadows, glows, outlines) on the logo
- No color filters on photography
- No busy/cluttered photo backgrounds behind brand elements

## Tone of Communication

XLAB's voice is calm, professional, and human. No superlatives, no marketing hype, no exclamation marks, no emoji. Factual, understated confidence. Czech language by default unless specified otherwise.

## Asset References

All brand assets are bundled locally in the `assets/` subdirectory of this skill. No external dependencies or network access required.
