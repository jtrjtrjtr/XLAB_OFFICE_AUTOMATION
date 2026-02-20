---
name: xlab-pptx-template
description: XLAB PowerPoint template (XLAB_PPT_ALL.pptx) with branded slide layouts. Use when creating presentations from the XLAB template, or when other skills need cover/closing slides. Contains layouts for cover, content, section dividers, and closing slides.
---

# XLAB PPTX Template Skill

Provides the XLAB_PPT_ALL.pptx master template file for use by other skills and for creating XLAB-branded presentations directly from template layouts.

## When to Use This Skill

Use this skill when the user wants an **XLAB-branded presentation** (internal, non-proposal) where all slides follow the XLAB template. The content is provided by the user (titles, texts, images) and slides are built purely from template layouts.

**Do NOT use for proposals/nabídky** → use `xlab-proposal` skill instead.
**Do NOT use for non-branded presentations** → use the public `pptx` skill instead.

## Template File

Full path: `/mnt/skills/user/xlab-pptx-template/assets/XLAB_PPT_ALL.pptx`

## Slide Dimensions

13.33" × 7.5" (standard PowerPoint widescreen 16:9)

## Themes

The template contains **two parallel sets of layouts**:

- **Layouts 1–15 = BLACK theme** (dark background, white/yellow text) → **default, always use unless user explicitly requests white**
- **Layouts 16–30 = WHITE theme** (white background, dark text, yellow accents decorative only)

Each layout in the black set has an exact white counterpart (+15).

## Layout Reference

| Layout (B/W) | Name | Placeholders | Use case |
|---|---|---|---|
| 1 / 16 | Cover Slide + X Ray | ctrTitle, subTitle | Úvod s X ray paprskem – vždy první slide |
| 2 / 17 | Title + Text | title, body (idx=15) | Klasický textový slide |
| 3 / 18 | Title + Text + IMG | title, body (idx=15), pic (idx=21) | Text vlevo, obrázek vpravo |
| 4 / 19 | Title + Text + 4x IMG | title, body (idx=15), 4× pic | Text + 4 obrázky |
| 5 / 20 | Title + Text + 4x IMG+ | title, body (idx=15), 4× pic | Varianta 4 obrázků |
| 6 / 21 | Title + Text + 2x IMG | title, body (idx=15), 2× pic, extra body (idx=22) | Text + 2 obrázky |
| 7 / 22 | Title + Text + IMG horizontal | title, pic (idx=20), body (idx=15) | Horizontální varianta s obrázkem |
| 8 / 23 | Title + IMG horizontal | title, pic (idx=20) | Pouze titulek + velký obrázek |
| 9 / 24 | Full Screen IMG | pic (idx=20) | Celá plocha obrázek, bez textu |
| 10 / 25 | Title + Text + IMG 4 mask | title, body (idx=15), pic (idx=20) | Obrázek s maskováním |
| 11 / 26 | Gradient Mask | *(žádné placeholdery)* | Dekorativní přechodový slide |
| 12 / 27 | Title Section + Ray Logo | ctrTitle | Sekční dělič s X logem |
| 13 / 28 | Title Section No Ray | ctrTitle | Sekční dělič bez loga |
| 14 / 29 | Cover Slide + No Ray | ctrTitle, subTitle | Alternativní úvod bez X ray paprsku |
| 15 / 30 | Bye Bye Slide | body (idx=16) – kontaktní text | Závěrečný slide – vždy poslední |

## Workflow: Vytvoření prezentace z template

### Krok 1 – Unpack template

```bash
cp /mnt/skills/user/xlab-pptx-template/assets/XLAB_PPT_ALL.pptx /tmp/xlab-work.pptx
python3 /mnt/skills/public/pptx/scripts/office/unpack.py /tmp/xlab-work.pptx /tmp/xlab-unpacked/
```

### Krok 2 – Přidat slidy z layoutů

Pro každý slide prezentace přidej slide z příslušného layoutu pomocí `add_slide.py`:

```bash
# Příklad: cover slide (Layout 1, černé téma)
python3 /mnt/skills/public/pptx/scripts/add_slide.py /tmp/xlab-unpacked/ slideLayout1.xml

# Textový slide (Layout 2)
python3 /mnt/skills/public/pptx/scripts/add_slide.py /tmp/xlab-unpacked/ slideLayout2.xml

# Sekční dělič (Layout 12 – s Ray Logo, DEFAULT pro sekce)
python3 /mnt/skills/public/pptx/scripts/add_slide.py /tmp/xlab-unpacked/ slideLayout12.xml

# Závěrečný slide (Layout 15)
python3 /mnt/skills/public/pptx/scripts/add_slide.py /tmp/xlab-unpacked/ slideLayout15.xml
```

### Krok 3 – Editovat texty v XML

Po přidání slidů edituj placeholder texty přímo v XML. Slidy jsou v `/tmp/xlab-unpacked/ppt/slides/`.

**Vzor – editace title a body placeholderů:**

```python
import re

slide_path = "/tmp/xlab-unpacked/ppt/slides/slide2.xml"
with open(slide_path, "r", encoding="utf-8") as f:
    xml = f.read()

# Nahraď text v title placeholderu (type="title")
# Najdi <p:sp> blok obsahující <p:ph type="title">, pak nahraď <a:t>...</a:t>
xml = re.sub(
    r'(<p:ph type="title"[^>]*/?>.*?<a:t>)[^<]*(</a:t>)',
    r'\1Nový titulek\2',
    xml, flags=re.DOTALL
)

with open(slide_path, "w", encoding="utf-8") as f:
    f.write(xml)
```

**Placeholder typy podle layoutu:**

- `type="ctrTitle"` → hlavní titulek (cover, section slides)
- `type="subTitle" idx="1"` → podtitulek (cover slides)
- `type="title"` → titulek obsahu (content slides)
- `idx="15"` (bez type) → hlavní textový obsah / body
- `idx="16"` → kontaktní text (Bye Bye slide)
- `type="pic"` → obrázkový placeholder

### Krok 4 – Vyčistit a zabalit

```bash
python3 /mnt/skills/public/pptx/scripts/clean.py /tmp/xlab-unpacked/
python3 /mnt/skills/public/pptx/scripts/office/pack.py /tmp/xlab-unpacked/ /home/claude/presentation.pptx \
  --original /mnt/skills/user/xlab-pptx-template/assets/XLAB_PPT_ALL.pptx

cp /home/claude/presentation.pptx /mnt/user-data/outputs/presentation.pptx
```

## Důležitá pravidla

- **Vždy začni Layout 1 (Cover) a konči Layout 15 (Bye Bye)**
- **Výchozí téma je černé (Layouts 1–15)** – bílé použij pouze na explicitní přání
- **Nikdy neupravuj přímo** `/mnt/skills/user/xlab-pptx-template/assets/XLAB_PPT_ALL.pptx` – vždy pracuj na kopii
- Dekorativní prvky (X ray paprsek, zelená linie, loga) jsou součástí layoutů a propíší se automaticky – nekreslíš je ručně
- Layout 11/26 (Gradient Mask) nemá žádné placeholdery – použij ho jako čistě vizuální slide

## Jako závislost pro xlab-proposal skill

`xlab-proposal` skill používá tento template pro extrakci cover a closing slidů. Odkazuje na soubor na výše uvedené cestě.
