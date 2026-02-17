#!/usr/bin/env python3
"""
Merge XLAB proposal: shell (cover+closing) + content slides → final PPTX.

Usage:
    python3 merge_proposal.py <shell.pptx> <content.pptx> <output.pptx>

The shell.pptx contains cover (slide 1) and closing (last slide).
The content.pptx contains all generated content slides.
Result: cover + all content slides + closing.
"""
import sys
import os
import shutil
import re
import glob

# Add public pptx skill scripts to path
PPTX_SCRIPTS = "/mnt/skills/public/pptx/scripts"
sys.path.insert(0, PPTX_SCRIPTS)
sys.path.insert(0, os.path.join(PPTX_SCRIPTS, "office"))

from unpack import unpack
from pack import pack


def get_slide_ids(pres_xml_path):
    """Extract slide IDs and relationships from presentation.xml"""
    with open(pres_xml_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Find all sldId entries
    pattern = r'<p:sldId\s+id="(\d+)"\s+r:id="(rId\d+)"\s*/>'
    return re.findall(pattern, content)


def get_slide_path_from_rel(rels_path, rid):
    """Get slide file path from relationship ID"""
    with open(rels_path, "r", encoding="utf-8") as f:
        content = f.read()
    pattern = rf'<Relationship\s+Id="{rid}"[^>]*Target="([^"]+)"'
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None


def merge(shell_pptx, content_pptx, output_pptx):
    shell_dir = "/tmp/merge-shell"
    content_dir = "/tmp/merge-content"
    merged_dir = "/tmp/merge-output"

    # Clean up
    for d in [shell_dir, content_dir, merged_dir]:
        if os.path.exists(d):
            shutil.rmtree(d)

    # Unpack both
    unpack(shell_pptx, shell_dir)
    unpack(content_pptx, content_dir)

    # Start with shell as base
    shutil.copytree(shell_dir, merged_dir)

    # Get shell slide info
    shell_pres = os.path.join(merged_dir, "ppt", "presentation.xml")
    shell_rels = os.path.join(merged_dir, "ppt", "_rels", "presentation.xml.rels")
    shell_slides = get_slide_ids(shell_pres)

    # Get content slide info
    content_pres = os.path.join(content_dir, "ppt", "presentation.xml")
    content_rels = os.path.join(content_dir, "ppt", "_rels", "presentation.xml.rels")
    content_slides = get_slide_ids(content_pres)

    # Find max slide number and max ID in shell
    existing_slides = glob.glob(os.path.join(merged_dir, "ppt", "slides", "slide*.xml"))
    max_slide_num = max([int(re.search(r'slide(\d+)', s).group(1)) for s in existing_slides])
    max_id = max([int(sid) for sid, _ in shell_slides]) if shell_slides else 256
    max_rid_num = 0
    with open(shell_rels, "r", encoding="utf-8") as f:
        for m in re.finditer(r'Id="rId(\d+)"', f.read()):
            max_rid_num = max(max_rid_num, int(m.group(1)))

    # Copy content slides into merged directory
    new_slide_entries = []
    for i, (cid, crid) in enumerate(content_slides):
        # Get source slide path
        content_slide_rel_path = get_slide_path_from_rel(content_rels, crid)
        if not content_slide_rel_path:
            continue

        content_slide_name = os.path.basename(content_slide_rel_path)
        content_slide_path = os.path.join(content_dir, "ppt", "slides", content_slide_name)

        if not os.path.exists(content_slide_path):
            continue

        # New slide number and IDs
        new_num = max_slide_num + 1 + i
        new_id = max_id + 1 + i
        new_rid_num = max_rid_num + 1 + i
        new_rid = f"rId{new_rid_num}"
        new_slide_name = f"slide{new_num}.xml"

        # Copy slide XML
        shutil.copy2(
            content_slide_path,
            os.path.join(merged_dir, "ppt", "slides", new_slide_name)
        )

        # Copy slide rels if exists
        content_slide_rels = os.path.join(
            content_dir, "ppt", "slides", "_rels", f"{content_slide_name}.rels"
        )
        merged_slide_rels_dir = os.path.join(merged_dir, "ppt", "slides", "_rels")
        os.makedirs(merged_slide_rels_dir, exist_ok=True)

        if os.path.exists(content_slide_rels):
            shutil.copy2(
                content_slide_rels,
                os.path.join(merged_slide_rels_dir, f"{new_slide_name}.rels")
            )

        # Copy media files referenced by this slide
        if os.path.exists(content_slide_rels):
            with open(content_slide_rels, "r", encoding="utf-8") as f:
                rels_content = f.read()
            media_refs = re.findall(r'Target="\.\./(media/[^"]+)"', rels_content)
            for media_ref in media_refs:
                src_media = os.path.join(content_dir, "ppt", media_ref)
                dst_media = os.path.join(merged_dir, "ppt", media_ref)
                os.makedirs(os.path.dirname(dst_media), exist_ok=True)
                if os.path.exists(src_media) and not os.path.exists(dst_media):
                    shutil.copy2(src_media, dst_media)

        # Add relationship to presentation.xml.rels
        new_rel = f'<Relationship Id="{new_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/{new_slide_name}"/>'
        with open(shell_rels, "r", encoding="utf-8") as f:
            rels = f.read()
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

    # Update presentation.xml: insert content slides between cover and closing
    with open(shell_pres, "r", encoding="utf-8") as f:
        pres_content = f.read()

    # Find sldIdLst
    sld_list_match = re.search(r'(<p:sldIdLst>)(.*?)(</p:sldIdLst>)', pres_content, re.DOTALL)
    if sld_list_match:
        existing_entries = re.findall(r'<p:sldId[^/]*/>', sld_list_match.group(2))

        if len(existing_entries) >= 2:
            # Cover = first, Closing = last
            cover = existing_entries[0]
            closing = existing_entries[-1]
            new_list = f"<p:sldIdLst>\n    {cover}\n"
            for entry in new_slide_entries:
                new_list += f"    {entry}\n"
            new_list += f"    {closing}\n  </p:sldIdLst>"
        else:
            # Just append content before closing
            new_list = "<p:sldIdLst>\n"
            for entry in existing_entries:
                new_list += f"    {entry}\n"
            for entry in new_slide_entries:
                new_list += f"    {entry}\n"
            new_list += "  </p:sldIdLst>"

        pres_content = pres_content[:sld_list_match.start()] + new_list + pres_content[sld_list_match.end():]

        with open(shell_pres, "w", encoding="utf-8") as f:
            f.write(pres_content)

    # Pack
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
