#!/usr/bin/env python3
"""
Merge XLAB proposal: shell (cover+closing) + content slides → final PPTX.

Usage:
    python3 merge_proposal_v2.py <shell.pptx> <content.pptx> <output.pptx>

The shell.pptx contains cover (slide 1) and closing (last slide).
The content.pptx contains all generated content slides.
Result: cover + all content slides + closing.

Fixes:
- Layout contamination: pptxgenjs maps all slides to slideLayout1 (XLAB Cover).
  This script injects a blank BLANK_CONTENT layout and rewrites content slide
  rels to point to it, preventing X ray / connector bleedthrough.
- notesSlide broken rels: strips or copies notes references properly.
"""
import sys
import os
import shutil
import re
import glob

PPTX_SCRIPTS = "/mnt/skills/public/pptx/scripts"
sys.path.insert(0, PPTX_SCRIPTS)
sys.path.insert(0, os.path.join(PPTX_SCRIPTS, "office"))

from unpack import unpack
from pack import pack


BLANK_LAYOUT_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
             xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
             xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
             preserve="1">
  <p:cSld name="BLANK_CONTENT">
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr>
    <a:masterClrMapping/>
  </p:clrMapOvr>
</p:sldLayout>'''


def get_slide_ids(pres_xml_path):
    with open(pres_xml_path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = r'<p:sldId\s+id="(\d+)"\s+r:id="(rId\d+)"\s*/>'
    return re.findall(pattern, content)


def get_slide_path_from_rel(rels_path, rid):
    with open(rels_path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = rf'<Relationship\s+Id="{rid}"[^>]*Target="([^"]+)"'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None


def inject_blank_layout(merged_dir):
    """
    Add a clean blank layout (slideLayout31.xml) to the shell PPTX.
    This prevents content slides from inheriting Cover layout decorations.
    Returns the filename of the injected blank layout.
    """
    blank_name = "slideLayout31.xml"
    layouts_dir = os.path.join(merged_dir, "ppt", "slideLayouts")
    blank_dst = os.path.join(layouts_dir, blank_name)
    blank_rels_dst = os.path.join(layouts_dir, "_rels", f"{blank_name}.rels")

    # Write blank layout XML
    with open(blank_dst, "w", encoding="utf-8") as f:
        f.write(BLANK_LAYOUT_XML)

    # Write layout rels - link to slideMaster1
    blank_rels_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>'''
    os.makedirs(os.path.dirname(blank_rels_dst), exist_ok=True)
    with open(blank_rels_dst, "w", encoding="utf-8") as f:
        f.write(blank_rels_xml)

    # Register in [Content_Types].xml
    ct_path = os.path.join(merged_dir, "[Content_Types].xml")
    with open(ct_path, "r", encoding="utf-8") as f:
        ct = f.read()
    ct_entry = f'<Override PartName="/ppt/slideLayouts/{blank_name}" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
    if ct_entry not in ct:
        ct = ct.replace("</Types>", f"  {ct_entry}\n</Types>")
        with open(ct_path, "w", encoding="utf-8") as f:
            f.write(ct)

    # Register in slideMaster1.xml.rels
    master_rels_path = os.path.join(merged_dir, "ppt", "slideMasters", "_rels", "slideMaster1.xml.rels")
    with open(master_rels_path, "r", encoding="utf-8") as f:
        master_rels = f.read()
    if blank_name not in master_rels:
        rids = [int(m) for m in re.findall(r'Id="rId(\d+)"', master_rels)]
        next_rid = max(rids) + 1 if rids else 1
        new_rel = f'<Relationship Id="rId{next_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/{blank_name}"/>'
        master_rels = master_rels.replace("</Relationships>", f"  {new_rel}\n</Relationships>")
        with open(master_rels_path, "w", encoding="utf-8") as f:
            f.write(master_rels)

        # Register in slideMaster1.xml sldLayoutIdLst
        master_xml_path = os.path.join(merged_dir, "ppt", "slideMasters", "slideMaster1.xml")
        with open(master_xml_path, "r", encoding="utf-8") as f:
            master_xml = f.read()
        # Scan ALL XML files for IDs to avoid global ID conflicts
        all_ids = []
        import glob as _glob
        for xml_file in _glob.glob(os.path.join(merged_dir, "**", "*.xml"), recursive=True):
            try:
                xml_content = open(xml_file).read()
                all_ids.extend(int(x) for x in re.findall(r'id="(\d+)"', xml_content))
            except Exception:
                pass
        next_lid = max(all_ids) + 1 if all_ids else 300
        layout_entry = f'<p:sldLayoutId id="{next_lid}" r:id="rId{next_rid}"/>'
        if "</p:sldLayoutIdLst>" in master_xml:
            master_xml = master_xml.replace(
                "</p:sldLayoutIdLst>",
                f"  {layout_entry}\n  </p:sldLayoutIdLst>"
            )
            with open(master_xml_path, "w", encoding="utf-8") as f:
                f.write(master_xml)

    return blank_name


def rewrite_slide_layout_ref(slide_rels_path, new_layout_name):
    """Rewrite slideLayout reference in a slide's .rels file to point to new_layout_name."""
    with open(slide_rels_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(
        r'(<Relationship[^>]*Type="[^"]*slideLayout"[^>]*Target=")([^"]+)(")',
        rf'\g<1>../slideLayouts/{new_layout_name}\g<3>',
        content
    )
    with open(slide_rels_path, "w", encoding="utf-8") as f:
        f.write(content)


def merge(shell_pptx, content_pptx, output_pptx):
    shell_dir = "/tmp/merge-shell"
    content_dir = "/tmp/merge-content"
    merged_dir = "/tmp/merge-output"

    for d in [shell_dir, content_dir, merged_dir]:
        if os.path.exists(d):
            shutil.rmtree(d)

    unpack(shell_pptx, shell_dir)
    unpack(content_pptx, content_dir)
    shutil.copytree(shell_dir, merged_dir)

    shell_pres = os.path.join(merged_dir, "ppt", "presentation.xml")
    shell_rels = os.path.join(merged_dir, "ppt", "_rels", "presentation.xml.rels")
    shell_slides = get_slide_ids(shell_pres)

    content_pres = os.path.join(content_dir, "ppt", "presentation.xml")
    content_rels_path = os.path.join(content_dir, "ppt", "_rels", "presentation.xml.rels")
    content_slides = get_slide_ids(content_pres)

    existing_slides = glob.glob(os.path.join(merged_dir, "ppt", "slides", "slide*.xml"))
    max_slide_num = max([int(re.search(r'slide(\d+)', s).group(1)) for s in existing_slides]) if existing_slides else 0
    max_id = max([int(sid) for sid, _ in shell_slides]) if shell_slides else 256
    max_rid_num = 0
    with open(shell_rels, "r", encoding="utf-8") as f:
        for m in re.finditer(r'Id="rId(\d+)"', f.read()):
            max_rid_num = max(max_rid_num, int(m.group(1)))

    # ── Inject blank layout to prevent Cover layout contamination ──────────
    blank_layout_name = inject_blank_layout(merged_dir)
    print(f"  Injected blank content layout: {blank_layout_name}")

    merged_slides_dir = os.path.join(merged_dir, "ppt", "slides")
    merged_rels_dir = os.path.join(merged_slides_dir, "_rels")
    os.makedirs(merged_rels_dir, exist_ok=True)

    new_slide_entries = []
    for i, (cid, crid) in enumerate(content_slides):
        content_slide_rel_path = get_slide_path_from_rel(content_rels_path, crid)
        if not content_slide_rel_path:
            continue

        content_slide_name = os.path.basename(content_slide_rel_path)
        content_slide_path = os.path.join(content_dir, "ppt", "slides", content_slide_name)
        if not os.path.exists(content_slide_path):
            continue

        new_num = max_slide_num + 1 + i
        new_id = max_id + 1 + i
        new_rid_num = max_rid_num + 1 + i
        new_rid = f"rId{new_rid_num}"
        new_slide_name = f"slide{new_num}.xml"

        # Copy slide XML
        shutil.copy2(content_slide_path, os.path.join(merged_slides_dir, new_slide_name))

        # Process slide rels
        content_slide_rels = os.path.join(content_dir, "ppt", "slides", "_rels", f"{content_slide_name}.rels")
        dest_rels_path = os.path.join(merged_rels_dir, f"{new_slide_name}.rels")

        if os.path.exists(content_slide_rels):
            with open(content_slide_rels, "r", encoding="utf-8") as f:
                rels_content = f.read()

            # Handle notesSlide references
            notes_refs = re.findall(
                r'<Relationship[^>]*Type="[^"]*notesSlide"[^>]*Target="([^"]+)"[^>]*/>', rels_content
            )
            for notes_ref in notes_refs:
                notes_src = os.path.normpath(
                    os.path.join(content_dir, "ppt", "slides", notes_ref)
                )
                if os.path.exists(notes_src):
                    notes_dst_dir = os.path.join(merged_dir, "ppt", "notesSlides")
                    os.makedirs(notes_dst_dir, exist_ok=True)
                    notes_dst = os.path.join(notes_dst_dir, os.path.basename(notes_ref))
                    if not os.path.exists(notes_dst):
                        shutil.copy2(notes_src, notes_dst)
                else:
                    # Strip broken notesSlide reference
                    rels_content = re.sub(
                        r'\s*<Relationship[^>]*Type="[^"]*notesSlide"[^>]*/>\s*',
                        "\n",
                        rels_content,
                    )

            with open(dest_rels_path, "w", encoding="utf-8") as f:
                f.write(rels_content)

            # ── Fix layout contamination: rewrite slideLayout ref ──────────
            rewrite_slide_layout_ref(dest_rels_path, blank_layout_name)

            # Copy media files
            media_refs = re.findall(r'Target="\.\./(media/[^"]+)"', rels_content)
            for media_ref in media_refs:
                src_media = os.path.join(content_dir, "ppt", media_ref)
                dst_media = os.path.join(merged_dir, "ppt", media_ref)
                os.makedirs(os.path.dirname(dst_media), exist_ok=True)
                if os.path.exists(src_media) and not os.path.exists(dst_media):
                    shutil.copy2(src_media, dst_media)
        else:
            # No rels file — create one pointing to blank layout
            minimal_rels = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/{blank_layout_name}"/>
</Relationships>'''
            with open(dest_rels_path, "w", encoding="utf-8") as f:
                f.write(minimal_rels)

        # Add to presentation.xml.rels
        new_rel = f'<Relationship Id="{new_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/{new_slide_name}"/>'
        with open(shell_rels, "r", encoding="utf-8") as f:
            rels = f.read()
        if f"slides/{new_slide_name}" not in rels:
            rels = rels.replace("</Relationships>", f"  {new_rel}\n</Relationships>")
            with open(shell_rels, "w", encoding="utf-8") as f:
                f.write(rels)

        # Add to Content_Types.xml
        ct_path = os.path.join(merged_dir, "[Content_Types].xml")
        with open(ct_path, "r", encoding="utf-8") as f:
            ct = f.read()
        new_override = f'<Override PartName="/ppt/slides/{new_slide_name}" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        if new_override not in ct:
            ct = ct.replace("</Types>", f"  {new_override}\n</Types>")
            with open(ct_path, "w", encoding="utf-8") as f:
                f.write(ct)

        new_slide_entries.append(f'<p:sldId id="{new_id}" r:id="{new_rid}"/>')

    # Update presentation.xml: cover + content + closing
    with open(shell_pres, "r", encoding="utf-8") as f:
        pres_content = f.read()

    sld_list_match = re.search(r'(<p:sldIdLst>)(.*?)(</p:sldIdLst>)', pres_content, re.DOTALL)
    if sld_list_match:
        existing_entries = re.findall(r'<p:sldId[^/]*/>', sld_list_match.group(2))
        if len(existing_entries) >= 2:
            cover = existing_entries[0]
            closing = existing_entries[-1]
            new_list = f"<p:sldIdLst>\n    {cover}\n"
            for entry in new_slide_entries:
                new_list += f"    {entry}\n"
            new_list += f"    {closing}\n  </p:sldIdLst>"
        else:
            new_list = "<p:sldIdLst>\n"
            for entry in existing_entries:
                new_list += f"    {entry}\n"
            for entry in new_slide_entries:
                new_list += f"    {entry}\n"
            new_list += "  </p:sldIdLst>"
        pres_content = pres_content[:sld_list_match.start()] + new_list + pres_content[sld_list_match.end():]
        with open(shell_pres, "w", encoding="utf-8") as f:
            f.write(pres_content)

    pack(merged_dir, output_pptx, shell_pptx)
    print(f"Merged proposal: {output_pptx}")
    print(f"  Cover: 1 slide from shell")
    print(f"  Content: {len(new_slide_entries)} slides from content")
    print(f"  Closing: 1 slide from shell")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <shell.pptx> <content.pptx> <output.pptx>")
        sys.exit(1)
    merge(sys.argv[1], sys.argv[2], sys.argv[3])
