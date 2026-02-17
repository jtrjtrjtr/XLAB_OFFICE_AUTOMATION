---
name: xlab-brand
description: Apply XLAB brand identity to presentations, documents, HTML, artifacts, and visual outputs. Trigger for any XLAB-branded materials including proposals, pitch decks, and client-facing content.
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
| Mid Gray | `#4a4a4a` | Captions, dividers, overlines on white theme |
| Dark Gray | `#1a1a1a` | Secondary dark background, card fills |
| Light Gray | `#888888` | Secondary/body text |

**Yellow rules**: Use for headings, icons, buttons, light beam elements, overlines on dark backgrounds. Never as a background fill or gradient. **Never use yellow for text on white or light backgrounds** — yellow text lacks contrast and is poorly readable on light surfaces. On white/light backgrounds, yellow is permitted ONLY for decorative lines and accents (horizontal rules, vertical bars, top-of-card lines). Use XLAB Black or Mid Gray for text on light backgrounds instead.

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

**IMPORTANT — Aspect ratio:** The X symbol is a landscape rectangle, NOT a square. Aspect ratio is approximately 1.6 : 1. Always maintain this ratio when embedding. Never stretch or compress the symbol into a square.

#### Assets

All brand assets are encoded as base64 inside `scripts/extract_assets.py`. This prevents image format corruption during skill upload.

**IMPORTANT — Before using any assets, always run the extraction script first:**

```python
import subprocess
subprocess.run(["python3", "/mnt/skills/user/xlab-brand/scripts/extract_assets.py", "/tmp/xlab-assets"], check=True)
```

This creates the following files in `/tmp/xlab-assets/`:

| Asset | File | Aspect ratio | Use case |
|-------|------|--------------|----------|
| X symbol (white) | `x_symbol_white.png` | ~1.6:1 | On black/dark backgrounds |
| X symbol (black) | `x_symbol_black.png` | ~1.6:1 | On white/light backgrounds |
| XLAB logo (white) | `x_logo_white.png` | ~5.6:1 | Full XLAB wordmark, dark backgrounds |
| XLAB logo (black) | `x_logo_black.png` | ~5.6:1 | Full XLAB wordmark, light backgrounds |

All extracted files are **PNG with transparent background (RGBA)** — they work correctly on any background color.

**How to access assets in code:**

```python
import subprocess, os

# Step 1: Extract assets (always do this first)
ASSETS_DIR = "/tmp/xlab-assets"
subprocess.run([
    "python3",
    "/mnt/skills/user/xlab-brand/scripts/extract_assets.py",
    ASSETS_DIR
], check=True)

# Step 2: Use asset paths
x_symbol_white = os.path.join(ASSETS_DIR, "x_symbol_white.png")
x_symbol_black = os.path.join(ASSETS_DIR, "x_symbol_black.png")
x_logo_white = os.path.join(ASSETS_DIR, "x_logo_white.png")
x_logo_black = os.path.join(ASSETS_DIR, "x_logo_black.png")
```

For HTML artifacts, read the extracted file and embed as base64 data URI:

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

- **PPTX**: Use `slide.addImage({ path: "<extracted_path>", x: 12.5, y: 6.9, w: 0.48, h: 0.30 })` for a bottom-right placement on a 13.33"×7.5" slide
- **HTML**: Read the extracted asset file, convert to base64, and embed as `<img src="data:image/png;base64,..." style="aspect-ratio: 1056/662;">`
- Do not attempt to recreate the symbol with SVG — always use the provided PNG assets
- **Never set equal width and height** — the symbol is a rectangle, not a square

## Theme Variants

### BLACK theme (default)

| Role | Color |
|------|-------|
| Background | `#000000` |
| Primary text | `#F8F7F2` |
| Cards / panels | `#1a1a1a` |
| Accent (overlines, icons, numbers, card titles) | `#E3E829` |
| Secondary text | `#888888` |
| X symbol | white variant |
| Logo | white variant |

### WHITE theme

| Role | Color |
|------|-------|
| Background | `#F8F7F2` |
| Primary text | `#1a1a1a` |
| Cards / panels | `#EBEBEB` |
| Decorative lines only | `#E3E829` |
| Overlines, card titles, accent text | `#4a4a4a` |
| Secondary text | `#666666` |
| X symbol | black variant |
| Logo | black variant |

**WHITE theme yellow restriction:** Yellow (#E3E829) is used ONLY for decorative elements — horizontal lines, vertical bars, top-of-card accent lines. Never for text, icons, numbers, or any content that needs to be read. Use dark gray (#4a4a4a) or black (#1a1a1a) instead.

## Layout Rules

### Presentations (PPTX)

Key points:
- Slide size: 13.33" × 7.5" (standard PowerPoint 16:9)
- Black or white background depending on chosen theme
- X symbol bottom-right on every slide **except the cover/title slide**
- Page number bottom-left on every slide
- Footer area: page number (left), X symbol (right) — keep minimal, no full-width bars
- Centered composition for title/cover slides

Content slide header pattern (consistent across all content slides):
- **Overline**: small text (10pt), bold, UPPERCASE — yellow on black theme, mid gray on white theme
- **Title**: large text (32pt), bold — white on black theme, near-black on white theme
- **Accent line**: yellow horizontal line (2" wide, 0.04" thick) below title

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
    --light-gray: #888888;
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

All brand assets are encoded in `scripts/extract_assets.py` as base64 to prevent format corruption during skill upload. Always extract before use. No external dependencies or network access required.
