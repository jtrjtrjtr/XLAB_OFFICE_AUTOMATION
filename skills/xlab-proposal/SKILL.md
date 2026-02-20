---
name: xlab-proposal
description: Generate XLAB-branded client proposals as PPTX presentations. Use when the user asks for a proposal, pitch, offer, nabídka, or client-facing presentation for a specific project. Combines cover/closing from XLAB_PPT_ALL template with pptxgenjs-generated content slides. Requires xlab-brand and xlab-pptx-template skills.
---

# XLAB Proposal Skill

Generate professional client proposals as branded PPTX presentations.

## Dependencies

This skill requires two other skills to be active:

- **xlab-brand**: Colors, typography, logo assets, theme definitions
- **xlab-pptx-template**: XLAB_PPT_ALL.pptx template (cover + closing slides)

## When to Use

Trigger when the user asks for a **proposal, pitch deck, nabídka, or offer** for a specific XLAB client project. The user will typically provide project details, scope, pricing, and timeline.

**Skill routing:**
- XLAB proposal/nabídka → **this skill** (xlab-proposal)
- XLAB interní/branded prezentace (ne proposal) → `xlab-pptx-template` skill
- Obecná prezentace bez XLAB brandingu → public `pptx` skill

## Workflow Overview (Cesta C)

The proposal is built by merging template slides with generated content:

```
1. Extract assets from xlab-brand skill
2. Build shell: cover (Layout 1) + closing (Layout 15) from XLAB_PPT_ALL template
3. Generate ONLY content slides with pptxgenjs — NO cover, NO closing
4. Merge: cover + content + closing → final PPTX
```

**⚠️ Kritické pravidlo:** pptxgenjs generuje POUZE content slidy (od slide 2 do předposledního). Cover a closing NIKDY negeneruje pptxgenjs — vždy se berou z template shellu. Porušení způsobí duplicitní slidy po mergi.

## Step-by-Step

### Step 1: Extract Brand Assets

```bash
python3 /mnt/skills/user/xlab-brand/scripts/extract_assets.py /tmp/xlab-assets
```

### Step 2: Build Shell from Template

```bash
# Unpack template
python /mnt/skills/public/pptx/scripts/office/unpack.py \
  /mnt/skills/user/xlab-pptx-template/assets/XLAB_PPT_ALL.pptx /tmp/template-unpacked/

# Create cover from Layout 1 (Cover + X Ray)
python /mnt/skills/public/pptx/scripts/add_slide.py /tmp/template-unpacked/ slideLayout1.xml

# Create closing from Layout 15 (Bye Bye)
python /mnt/skills/public/pptx/scripts/add_slide.py /tmp/template-unpacked/ slideLayout15.xml
```

Then edit `presentation.xml` to keep only cover + closing slides in `<p:sldIdLst>`, clean, and pack:

```bash
python /mnt/skills/public/pptx/scripts/clean.py /tmp/template-unpacked/
python /mnt/skills/public/pptx/scripts/office/pack.py /tmp/template-unpacked/ /tmp/shell.pptx \
  --original /mnt/skills/user/xlab-pptx-template/assets/XLAB_PPT_ALL.pptx
```

Edit cover slide text: replace placeholder title with project name and client name.
Edit closing slide text: update contact details if needed.

### Step 3: Generate Content Slides with pptxgenjs

**⚠️ pptxgenjs generuje POUZE content slidy — NIKDY ne cover ani closing slide. Ty přidá merge z template shellu.**

Create a Node.js script that generates content slides. Use the component library below.

**Critical settings:**

```javascript
const pptxgen = require("pptxgenjs");
let pptx = new pptxgen();

// MUST match template dimensions
pptx.defineLayout({ name: "XLAB", width: 13.33, height: 7.5 });
pptx.layout = "XLAB";
```

### Step 4: Merge Shell + Content

Použij připravený merge script:

```bash
python3 /mnt/skills/user/xlab-proposal/scripts/merge_proposal.py \
  /tmp/shell.pptx \
  /tmp/content.pptx \
  /home/claude/proposal.pptx
```

Script automaticky:
- Injektuje čistý blank layout (`slideLayout31.xml`) do shell PPTX — **zabraňuje layout contamination** (bez toho by se dekorativní prvky Cover layoutu, X ray grafika a zelená linie, propsaly do content slidů)
- Přepíše layout reference content slidů z pptxgenjs na blank layout místo slideLayout1
- Vezme cover (slide 1) ze shell.pptx
- Vloží všechny slidy z content.pptx
- Přidá closing (poslední slide) ze shell.pptx
- Zkopíruje media soubory a aktualizuje relationships
- Odstraní nebo zkopíruje notesSlide reference (pptxgenjs je generuje, ale soubory nemusí existovat)

Copy final output:
```bash
cp /home/claude/proposal.pptx /mnt/user-data/outputs/proposal.pptx
```

## Theme Parameter

The proposal supports two themes:

- `theme: "black"` (default) — black background, white text, yellow accents
- `theme: "white"` — off-white background, dark text, yellow decorative lines only

Theme is set globally for all content slides. Cover and closing always use the template's default styling.

See xlab-brand SKILL.md for complete theme color definitions.

## Proposal Structures

### Compact (6–8 slides)

Use for smaller projects, quick turnarounds, or follow-up proposals.

| # | Section | Component |
|---|---------|-----------|
| 1 | Cover | from template |
| 2 | Kontext / prostor | text-with-image or quote-highlight |
| 3 | Kreativní koncept | 3-column-cards |
| 4 | Technické řešení | detail-with-panel |
| 5 | Harmonogram | timeline |
| 6 | Rozpočet | pricing-simple or pricing-table |
| 7 | Otevřené otázky | checklist |
| 8 | Closing | from template |

### Extended (12+ slides)

Use for larger projects, first-time clients, or complex multi-phase proposals.

| # | Section | Component |
|---|---------|-----------|
| 1 | Cover | from template |
| 2 | Executive summary | quote-highlight |
| 3 | Reference | image-fullbleed (placeholder for user photos) |
| 4 | Porozumění zadání | text-with-image or checklist |
| 5 | Kreativní vize | quote-highlight or big-number |
| 6 | Kreativní koncept — fáze | 3-column-cards |
| 7 | Kreativní koncept — detail | detail-with-panel (1–2 slides) |
| 8 | Technické řešení | detail-with-panel |
| 9 | Volitelná rozšíření | 3-column-cards or checklist |
| 10 | Realizační tým | team |
| 11 | Harmonogram | timeline |
| 12 | Cenové varianty | pricing-table or pricing-simple |
| 13 | Otevřené otázky | checklist |
| 14 | Closing | from template |

## Component Library

All components follow the same header pattern:

```javascript
// Consistent header on every content slide
function addSlideHeader(slide, overline, title, theme) {
  const t = THEMES[theme];
  // Overline
  slide.addText(overline.toUpperCase(), {
    x: 0.8, y: 0.5, w: 5, h: 0.35,
    fontSize: 10, bold: true, color: t.overline, fontFace: "Arial"
  });
  // Title
  slide.addText(title.toUpperCase(), {
    x: 0.8, y: 0.85, w: 10, h: 0.7,
    fontSize: 32, bold: true, color: t.title, fontFace: "Arial"
  });
  // Yellow accent line
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.8, y: 1.6, w: 2.0, h: 0.04, fill: { color: "E3E829" }
  });
}

// Footer on every content slide
function addSlideFooter(slide, pageNum, theme) {
  const t = THEMES[theme];
  slide.addText(String(pageNum), {
    x: 0.5, y: 7.0, w: 0.5, h: 0.3,
    fontSize: 10, color: "888888", fontFace: "Arial"
  });
  slide.addImage({
    path: t.symbolPath,
    x: 12.5, y: 6.9, w: 0.48, h: 0.30
  });
}
```

### Theme Definitions

```javascript
const THEMES = {
  black: {
    bg: "000000",
    title: "F8F7F2",
    overline: "E3E829",
    cardBg: "1A1A1A",
    cardTitle: "E3E829",
    bodyText: "888888",
    accent: "E3E829",
    symbolPath: "/tmp/xlab-assets/x_symbol_white.png",
    logoPath: "/tmp/xlab-assets/x_logo_white.png"
  },
  white: {
    bg: "F8F7F2",
    title: "1A1A1A",
    overline: "4A4A4A",
    cardBg: "EBEBEB",
    cardTitle: "4A4A4A",
    bodyText: "666666",
    accent: "E3E829",  // decorative lines ONLY
    symbolPath: "/tmp/xlab-assets/x_symbol_black.png",
    logoPath: "/tmp/xlab-assets/x_logo_black.png"
  }
};
```

### Components Reference

All coordinates are for 13.33" × 7.5" slides. Content area starts at y: 2.0 (below header).

---

#### 3-column-cards

Three equal cards side by side. Use for phases, steps, comparisons, options.

```javascript
function threeColumnCards(slide, cards, theme) {
  // cards = [{ num: "1", title: "...", desc: "..." }, ...]
  const t = THEMES[theme];
  cards.forEach((card, i) => {
    const cx = 0.8 + i * 3.9;
    // Card background
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: cx, y: 2.0, w: 3.6, h: 4.2,
      fill: { color: t.cardBg }, rectRadius: 0.05
    });
    // Yellow top accent line
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: cx, y: 2.0, w: 3.6, h: 0.04, fill: { color: "E3E829" }
    });
    // Number + Title
    slide.addText(`${card.num}  ${card.title}`, {
      x: cx + 0.3, y: 2.6, w: 3.0, h: 0.35,
      fontSize: 12, bold: true, color: t.cardTitle, fontFace: "Arial"
    });
    // Description
    slide.addText(card.desc, {
      x: cx + 0.3, y: 3.1, w: 3.0, h: 2.5,
      fontSize: 11, color: t.bodyText, fontFace: "Arial", valign: "top"
    });
  });
}
```

---

#### detail-with-panel

Left side: bullet points with icons. Right side: dark/light panel with specs or key info.

```javascript
function detailWithPanel(slide, items, panel, theme) {
  // items = [{ title: "...", desc: "..." }, ...]
  // panel = { title: "...", lines: ["...", "..."] }
  const t = THEMES[theme];

  // Left column items
  items.forEach((item, i) => {
    const iy = 2.2 + i * 1.1;
    // Yellow bullet dot
    slide.addShape(pptx.shapes.OVAL, {
      x: 0.8, y: iy + 0.05, w: 0.15, h: 0.15,
      fill: { color: "E3E829" }
    });
    slide.addText(item.title, {
      x: 1.15, y: iy - 0.05, w: 6, h: 0.35,
      fontSize: 14, bold: true, color: t.title, fontFace: "Arial"
    });
    slide.addText(item.desc, {
      x: 1.15, y: iy + 0.3, w: 6, h: 0.35,
      fontSize: 11, color: t.bodyText, fontFace: "Arial"
    });
  });

  // Right panel
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 8.2, y: 2.0, w: 4.5, h: 4.8,
    fill: { color: t.cardBg }, rectRadius: 0.05
  });
  slide.addText(panel.title, {
    x: 8.5, y: 2.3, w: 3.8, h: 0.4,
    fontSize: 14, bold: true, color: t.cardTitle, fontFace: "Arial"
  });
  // Yellow line under panel title
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 8.5, y: 2.75, w: 1.5, h: 0.03, fill: { color: "E3E829" }
  });
  panel.lines.forEach((line, i) => {
    slide.addText(line, {
      x: 8.5, y: 3.1 + i * 0.45, w: 3.8, h: 0.35,
      fontSize: 11, color: t.bodyText, fontFace: "Arial"
    });
  });
}
```

---

#### text-with-image

Text content on the left, image placeholder on the right.

```javascript
function textWithImage(slide, text, imagePath, theme) {
  // text = { body: "...", bullets: ["...", "..."] }
  const t = THEMES[theme];

  slide.addText(text.body, {
    x: 0.8, y: 2.2, w: 6.0, h: 1.5,
    fontSize: 13, color: t.bodyText, fontFace: "Arial", valign: "top"
  });

  if (text.bullets) {
    const bulletItems = text.bullets.map((b, i) => ({
      text: b,
      options: {
        bullet: true, breakLine: i < text.bullets.length - 1,
        fontSize: 12, color: t.bodyText
      }
    }));
    slide.addText(bulletItems, {
      x: 0.8, y: 3.8, w: 6.0, h: 2.5, fontFace: "Arial", valign: "top"
    });
  }

  if (imagePath) {
    slide.addImage({
      path: imagePath,
      x: 7.5, y: 2.0, w: 5.2, h: 4.8,
      sizing: { type: "cover", w: 5.2, h: 4.8 }
    });
  } else {
    // Placeholder rectangle
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 7.5, y: 2.0, w: 5.2, h: 4.8,
      fill: { color: t.cardBg }
    });
    slide.addText("[ IMAGE ]", {
      x: 7.5, y: 4.0, w: 5.2, h: 0.5,
      fontSize: 14, color: "888888", fontFace: "Arial", align: "center"
    });
  }
}
```

---

#### pricing-table

Three columns for variant pricing. Middle column highlighted.

```javascript
function pricingTable(slide, variants, theme) {
  // variants = [{ name: "...", price: "...", items: ["...", "..."], highlight: false }, ...]
  const t = THEMES[theme];

  variants.forEach((v, i) => {
    const cx = 0.8 + i * 3.9;
    const isHighlight = v.highlight || i === 1;

    // Card
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: cx, y: 2.0, w: 3.6, h: 4.8,
      fill: { color: isHighlight ? (theme === "black" ? "1A1A1A" : "E0E0E0") : t.cardBg }
    });

    // Highlight top bar
    if (isHighlight) {
      slide.addShape(pptx.shapes.RECTANGLE, {
        x: cx, y: 2.0, w: 3.6, h: 0.06, fill: { color: "E3E829" }
      });
    }

    // Variant name
    slide.addText(v.name.toUpperCase(), {
      x: cx + 0.3, y: 2.3, w: 3.0, h: 0.4,
      fontSize: 12, bold: true, color: isHighlight ? "E3E829" : t.cardTitle, fontFace: "Arial"
    });

    // Price
    slide.addText(v.price, {
      x: cx + 0.3, y: 2.8, w: 3.0, h: 0.5,
      fontSize: 24, bold: true, color: t.title, fontFace: "Arial"
    });

    // Divider
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: cx + 0.3, y: 3.4, w: 3.0, h: 0.02, fill: { color: "888888" }
    });

    // Items
    v.items.forEach((item, j) => {
      slide.addText(item, {
        x: cx + 0.3, y: 3.6 + j * 0.4, w: 3.0, h: 0.35,
        fontSize: 11, color: t.bodyText, fontFace: "Arial"
      });
    });
  });
}
```

---

#### pricing-simple

Simple line-item pricing list with total.

```javascript
function pricingSimple(slide, items, total, theme) {
  // items = [{ name: "...", price: "..." }, ...]
  // total = { label: "Celkem", price: "..." }
  const t = THEMES[theme];

  items.forEach((item, i) => {
    const iy = 2.2 + i * 0.7;
    // Divider line
    if (i > 0) {
      slide.addShape(pptx.shapes.RECTANGLE, {
        x: 0.8, y: iy - 0.1, w: 11.0, h: 0.01, fill: { color: "888888" }
      });
    }
    slide.addText(item.name, {
      x: 0.8, y: iy, w: 8.0, h: 0.4,
      fontSize: 14, color: t.title, fontFace: "Arial"
    });
    slide.addText(item.price, {
      x: 8.8, y: iy, w: 3.0, h: 0.4,
      fontSize: 14, bold: true, color: t.title, fontFace: "Arial", align: "right"
    });
  });

  if (total) {
    const ty = 2.2 + items.length * 0.7 + 0.3;
    // Yellow total line
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0.8, y: ty - 0.1, w: 11.0, h: 0.03, fill: { color: "E3E829" }
    });
    slide.addText(total.label, {
      x: 0.8, y: ty + 0.1, w: 8.0, h: 0.5,
      fontSize: 18, bold: true, color: t.title, fontFace: "Arial"
    });
    slide.addText(total.price, {
      x: 8.8, y: ty + 0.1, w: 3.0, h: 0.5,
      fontSize: 18, bold: true, color: "E3E829", fontFace: "Arial", align: "right"
    });
  }
}
```

---

#### checklist

Rows with yellow vertical accent bar + title + description.

```javascript
function checklist(slide, items, theme) {
  // items = [{ title: "...", desc: "..." }, ...]
  const t = THEMES[theme];
  const rowH = Math.min(1.0, 4.5 / items.length);

  items.forEach((item, i) => {
    const iy = 2.1 + i * rowH;
    // Yellow vertical bar
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0.8, y: iy, w: 0.06, h: rowH - 0.3, fill: { color: "E3E829" }
    });
    slide.addText(item.title, {
      x: 1.1, y: iy - 0.05, w: 10, h: 0.35,
      fontSize: 14, bold: true, color: t.title, fontFace: "Arial"
    });
    slide.addText(item.desc, {
      x: 1.1, y: iy + 0.3, w: 10, h: 0.35,
      fontSize: 11, color: t.bodyText, fontFace: "Arial"
    });
  });
}
```

---

#### diagram-with-labels

Large image area on top, three label boxes below.

```javascript
function diagramWithLabels(slide, imagePath, labels, theme) {
  // labels = [{ num: "1", title: "...", desc: "..." }, ...]
  const t = THEMES[theme];

  if (imagePath) {
    slide.addImage({
      path: imagePath,
      x: 0.8, y: 2.0, w: 11.73, h: 3.0,
      sizing: { type: "cover", w: 11.73, h: 3.0 }
    });
  } else {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0.8, y: 2.0, w: 11.73, h: 3.0,
      fill: { color: t.cardBg }
    });
    slide.addText("[ DIAGRAM / IMAGE ]", {
      x: 0.8, y: 3.2, w: 11.73, h: 0.5,
      fontSize: 16, color: "888888", fontFace: "Arial", align: "center"
    });
  }

  labels.forEach((label, i) => {
    const lx = 0.8 + i * 3.9;
    slide.addText(label.num, {
      x: lx, y: 5.3, w: 0.4, h: 0.35,
      fontSize: 14, bold: true, color: "E3E829", fontFace: "Arial"
    });
    slide.addText(label.title, {
      x: lx + 0.4, y: 5.3, w: 3.0, h: 0.35,
      fontSize: 13, bold: true, color: t.title, fontFace: "Arial"
    });
    slide.addText(label.desc, {
      x: lx + 0.4, y: 5.7, w: 3.0, h: 0.8,
      fontSize: 11, color: t.bodyText, fontFace: "Arial", valign: "top"
    });
  });
}
```

---

#### timeline

Horizontal timeline with milestones.

```javascript
function timeline(slide, milestones, theme) {
  // milestones = [{ date: "T+2", label: "...", desc: "..." }, ...]
  const t = THEMES[theme];
  const lineY = 3.8;
  const count = milestones.length;
  const startX = 1.5;
  const endX = 11.8;
  const stepX = (endX - startX) / Math.max(count - 1, 1);

  // Horizontal line
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: startX, y: lineY, w: endX - startX, h: 0.03, fill: { color: "888888" }
  });

  milestones.forEach((m, i) => {
    const mx = startX + i * stepX;
    // Dot
    slide.addShape(pptx.shapes.OVAL, {
      x: mx - 0.1, y: lineY - 0.1, w: 0.22, h: 0.22,
      fill: { color: "E3E829" }
    });
    // Date above
    slide.addText(m.date, {
      x: mx - 0.8, y: lineY - 0.7, w: 1.6, h: 0.4,
      fontSize: 11, bold: true, color: "E3E829", fontFace: "Arial", align: "center"
    });
    // Label below
    slide.addText(m.label, {
      x: mx - 0.8, y: lineY + 0.35, w: 1.6, h: 0.4,
      fontSize: 12, bold: true, color: t.title, fontFace: "Arial", align: "center"
    });
    // Desc
    slide.addText(m.desc || "", {
      x: mx - 0.8, y: lineY + 0.75, w: 1.6, h: 0.8,
      fontSize: 10, color: t.bodyText, fontFace: "Arial", align: "center", valign: "top"
    });
  });
}
```

---

#### big-number

2–3 large stat numbers with labels.

```javascript
function bigNumber(slide, stats, theme) {
  // stats = [{ number: "360°", label: "projekce", desc: "..." }, ...]
  const t = THEMES[theme];
  const count = stats.length;
  const colW = 10.0 / count;

  stats.forEach((stat, i) => {
    const sx = 0.8 + i * colW + (colW - 3.0) / 2;
    // Big number
    slide.addText(stat.number, {
      x: sx, y: 2.5, w: 3.0, h: 1.2,
      fontSize: 54, bold: true, color: "E3E829", fontFace: "Arial", align: "center"
    });
    // Label
    slide.addText(stat.label.toUpperCase(), {
      x: sx, y: 3.7, w: 3.0, h: 0.4,
      fontSize: 14, bold: true, color: t.title, fontFace: "Arial", align: "center"
    });
    // Description
    slide.addText(stat.desc || "", {
      x: sx, y: 4.2, w: 3.0, h: 1.0,
      fontSize: 11, color: t.bodyText, fontFace: "Arial", align: "center", valign: "top"
    });
  });
}
```

---

#### quote-highlight

Large quote with yellow accent bar on the left.

```javascript
function quoteHighlight(slide, quote, attribution, theme) {
  const t = THEMES[theme];
  // Yellow vertical accent
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 1.5, y: 2.5, w: 0.08, h: 3.0, fill: { color: "E3E829" }
  });
  // Quote text
  slide.addText(`„${quote}"`, {
    x: 2.0, y: 2.5, w: 9.0, h: 2.5,
    fontSize: 24, italic: true, color: t.title, fontFace: "Arial", valign: "top"
  });
  // Attribution
  if (attribution) {
    slide.addText(attribution, {
      x: 2.0, y: 5.2, w: 9.0, h: 0.4,
      fontSize: 12, color: t.bodyText, fontFace: "Arial"
    });
  }
}
```

---

#### two-column-text

Two equal text columns.

```javascript
function twoColumnText(slide, left, right, theme) {
  // left = { subtitle: "...", body: "..." }
  // right = { subtitle: "...", body: "..." }
  const t = THEMES[theme];

  [{ col: left, x: 0.8 }, { col: right, x: 6.9 }].forEach(({ col, x }) => {
    slide.addText(col.subtitle, {
      x: x, y: 2.2, w: 5.5, h: 0.4,
      fontSize: 14, bold: true, color: t.cardTitle, fontFace: "Arial"
    });
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: x, y: 2.65, w: 1.2, h: 0.03, fill: { color: "E3E829" }
    });
    slide.addText(col.body, {
      x: x, y: 2.9, w: 5.5, h: 3.5,
      fontSize: 12, color: t.bodyText, fontFace: "Arial", valign: "top"
    });
  });
}
```

---

#### image-fullbleed

Full-slide image with dark gradient overlay and text.

```javascript
function imageFullbleed(slide, imagePath, text, theme) {
  // text = { overline: "...", title: "..." }
  if (imagePath) {
    slide.addImage({
      path: imagePath,
      x: 0, y: 0, w: 13.33, h: 7.5,
      sizing: { type: "cover", w: 13.33, h: 7.5 }
    });
  }
  // Dark overlay gradient (left side)
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 6, h: 7.5,
    fill: { color: "000000", transparency: 40 }
  });
  slide.addText(text.overline.toUpperCase(), {
    x: 0.8, y: 4.5, w: 5, h: 0.35,
    fontSize: 10, bold: true, color: "E3E829", fontFace: "Arial"
  });
  slide.addText(text.title.toUpperCase(), {
    x: 0.8, y: 5.0, w: 5, h: 1.2,
    fontSize: 28, bold: true, color: "F8F7F2", fontFace: "Arial"
  });
}
```

---

#### team

Team member cards with photo placeholder, name, and role.

```javascript
function team(slide, members, theme) {
  // members = [{ name: "...", role: "...", photo: null }, ...]
  const t = THEMES[theme];
  const count = members.length;
  const colW = 11.0 / count;

  members.forEach((m, i) => {
    const mx = 0.8 + i * colW + (colW - 2.0) / 2;
    // Photo placeholder (circle)
    if (m.photo) {
      slide.addImage({
        path: m.photo,
        x: mx, y: 2.3, w: 2.0, h: 2.0,
        rounding: true
      });
    } else {
      slide.addShape(pptx.shapes.OVAL, {
        x: mx, y: 2.3, w: 2.0, h: 2.0,
        fill: { color: t.cardBg }
      });
    }
    // Name
    slide.addText(m.name, {
      x: mx - 0.3, y: 4.6, w: 2.6, h: 0.4,
      fontSize: 14, bold: true, color: t.title, fontFace: "Arial", align: "center"
    });
    // Role
    slide.addText(m.role, {
      x: mx - 0.3, y: 5.0, w: 2.6, h: 0.4,
      fontSize: 11, color: t.bodyText, fontFace: "Arial", align: "center"
    });
  });
}
```

## QA Process

After generating the proposal, ALWAYS:

1. Convert to images for visual inspection:
   ```bash
   python /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf proposal.pptx
   pdftoppm -jpeg -r 150 proposal.pdf slide
   ```

2. Inspect each slide for:
   - Text overflow or cut-off
   - Overlapping elements
   - Correct theme colors
   - X symbol present (except cover)
   - Page numbers correct
   - Cover and closing render properly

3. Fix issues and re-verify.

## Important Notes

- Always use `fontFace: "Arial"` — GT America is not available in the sandbox
- Never use `#` prefix for hex colors in pptxgenjs
- Never reuse option objects across addShape/addText calls (pptxgenjs mutates them)
- Yellow on white theme: ONLY for decorative lines, never for text/icons/numbers
- Cover slide: NEVER add X symbol
- All content slides: ALWAYS add X symbol in footer
- Pricing with yellow total: OK on both themes (yellow line is decorative)
