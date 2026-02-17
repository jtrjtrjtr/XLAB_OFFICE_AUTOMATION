---
name: xlab-pptx-template
description: XLAB PowerPoint template (XLAB_PPT_ALL.pptx) with branded slide layouts. Use when creating presentations from the XLAB template, or when other skills need cover/closing slides. Contains layouts for cover, content, section dividers, and closing slides.
---

# XLAB PPTX Template Skill

Provides the XLAB_PPT_ALL.pptx master template file for use by other skills and direct presentation creation.

## Template File

Located at: `assets/XLAB_PPT_ALL.pptx`

Full path: `/mnt/skills/user/xlab-pptx-template/assets/XLAB_PPT_ALL.pptx`

## Slide Dimensions

13.33" x 7.5" (standard PowerPoint 16:9, LAYOUT_WIDE in pptxgenjs)

## Key Layouts

| Layout | Name | Use case |
|--------|------|----------|
| Layout 1 | Cover + X Ray | Title slide with X ray light beam graphic |
| Layout 15 | Bye Bye | Closing slide with contact information |

## Usage

### Direct use (template-based editing)

```bash
python /mnt/skills/public/pptx/scripts/office/unpack.py \
  /mnt/skills/user/xlab-pptx-template/assets/XLAB_PPT_ALL.pptx unpacked/
```

Then follow the editing workflow from the pptx skill.

### As dependency for xlab-proposal skill

The xlab-proposal skill uses this template to extract cover and closing slides. It references the template at the path above.

## Notes

- Do not modify the template file directly
- Always work on a copy (unpack to a temp directory)
- The template contains branded graphics (X ray beams, logos) that cannot be recreated programmatically
