#!/usr/bin/env python3
"""
Create a shell PPTX with cover and closing slides from XLAB_PPT_ALL template.

Usage:
    python3 build_shell.py <output_shell.pptx> [--title "Project Name"] [--client "Client Name"]

Creates a PPTX with:
  - Cover slide from Layout 1 (Cover + X Ray)
  - Closing slide from Layout 15 (Bye Bye)
"""
import sys
import os
import re
import shutil
import argparse

PPTX_SCRIPTS = "/mnt/skills/public/pptx/scripts"
sys.path.insert(0, PPTX_SCRIPTS)
sys.path.insert(0, os.path.join(PPTX_SCRIPTS, "office"))

TEMPLATE_PATH = "/mnt/skills/user/xlab-pptx-template/assets/XLAB_PPT_ALL.pptx"


def build_shell(output_path, title=None, client=None):
    work_dir = "/tmp/shell-build"
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)

    # Unpack template
    from unpack import unpack
    from pack import pack
    unpack(TEMPLATE_PATH, work_dir)

    # Add cover slide from layout 1
    add_slide_script = os.path.join(PPTX_SCRIPTS, "add_slide.py")

    # Find layout files to determine which layout is "Cover + X Ray" and "Bye Bye"
    # We need to check layout names in the XML
    layout_dir = os.path.join(work_dir, "ppt", "slideLayouts")
    cover_layout = None
    closing_layout = None

    for f in sorted(os.listdir(layout_dir)):
        if not f.endswith(".xml"):
            continue
        path = os.path.join(layout_dir, f)
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
        # Look for layout name
        name_match = re.search(r'<p:cSld\s+name="([^"]*)"', content)
        if name_match:
            name = name_match.group(1)
            if "cover" in name.lower() or "x ray" in name.lower() or "xray" in name.lower():
                cover_layout = f
                print(f"Found cover layout: {f} ({name})")
            if "bye" in name.lower() or "closing" in name.lower() or "end" in name.lower():
                closing_layout = f
                print(f"Found closing layout: {f} ({name})")

    # Fallback to layout numbers if names not found
    if not cover_layout:
        cover_layout = "slideLayout1.xml"
        print(f"Using fallback cover layout: {cover_layout}")
    if not closing_layout:
        # Try layout 15 or the last one
        layouts = sorted([f for f in os.listdir(layout_dir) if f.endswith(".xml")])
        closing_layout = "slideLayout15.xml" if "slideLayout15.xml" in layouts else layouts[-1]
        print(f"Using fallback closing layout: {closing_layout}")

    # Use add_slide.py to create slides from layouts
    import subprocess
    result1 = subprocess.run(
        ["python3", add_slide_script, work_dir, cover_layout],
        capture_output=True, text=True
    )
    print(f"Cover slide: {result1.stdout.strip()}")

    result2 = subprocess.run(
        ["python3", add_slide_script, work_dir, closing_layout],
        capture_output=True, text=True
    )
    print(f"Closing slide: {result2.stdout.strip()}")

    # Parse the sldId entries from add_slide output
    cover_sldid = re.search(r'<p:sldId[^/]*/>', result1.stdout)
    closing_sldid = re.search(r'<p:sldId[^/]*/>', result2.stdout)

    # Update presentation.xml to only contain our two new slides
    pres_path = os.path.join(work_dir, "ppt", "presentation.xml")
    with open(pres_path, "r", encoding="utf-8") as f:
        pres = f.read()

    new_sld_list = "<p:sldIdLst>\n"
    if cover_sldid:
        new_sld_list += f"    {cover_sldid.group()}\n"
    if closing_sldid:
        new_sld_list += f"    {closing_sldid.group()}\n"
    new_sld_list += "  </p:sldIdLst>"

    pres = re.sub(r'<p:sldIdLst>.*?</p:sldIdLst>', new_sld_list, pres, flags=re.DOTALL)

    with open(pres_path, "w", encoding="utf-8") as f:
        f.write(pres)

    # Edit cover slide text if title/client provided
    if title or client:
        slides_dir = os.path.join(work_dir, "ppt", "slides")
        # Find the cover slide (most recently created)
        slides = sorted([f for f in os.listdir(slides_dir) if f.endswith(".xml")])
        # The add_slide creates new slide files — find them
        for slide_file in slides:
            slide_path = os.path.join(slides_dir, slide_file)
            with open(slide_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Look for placeholder text patterns and replace
            if title:
                content = re.sub(
                    r'(<a:t>)(Project Title|NÁZEV PROJEKTU|Click to edit|Klikněte)(</a:t>)',
                    f'\\1{title}\\3',
                    content, flags=re.IGNORECASE
                )
            if client:
                content = re.sub(
                    r'(<a:t>)(Client Name|KLIENT|Subtitle|Podtitul)(</a:t>)',
                    f'\\1{client}\\3',
                    content, flags=re.IGNORECASE
                )
            with open(slide_path, "w", encoding="utf-8") as f:
                f.write(content)

    # Clean and pack
    clean_script = os.path.join(PPTX_SCRIPTS, "clean.py")
    subprocess.run(["python3", clean_script, work_dir], capture_output=True)
    pack(work_dir, output_path, TEMPLATE_PATH)
    print(f"\nShell created: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build proposal shell from XLAB template")
    parser.add_argument("output", help="Output PPTX path")
    parser.add_argument("--title", help="Project title for cover slide")
    parser.add_argument("--client", help="Client name for cover slide")
    args = parser.parse_args()
    build_shell(args.output, args.title, args.client)
