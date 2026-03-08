#!/usr/bin/env python3
"""
Create a shell PPTX with cover and closing slides from XLAB_PPT_ALL template.

Usage:
    python3 build_shell.py <output_shell.pptx> [--title "Project Name"] [--client "Client Name"]

Creates a PPTX with:
  - Cover slide from Layout 1 (Cover + X Ray) with title + subtitle placeholders
  - Closing slide from Layout 15 (Bye Bye)
"""
import sys
import os
import re
import shutil
import subprocess

PPTX_SCRIPTS = "/mnt/skills/public/pptx/scripts"
sys.path.insert(0, PPTX_SCRIPTS)
sys.path.insert(0, os.path.join(PPTX_SCRIPTS, "office"))

TEMPLATE_PATH = "/mnt/skills/user/xlab-pptx-template/assets/XLAB_PPT_ALL.pptx"


def _xml_escape(text):
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;"))


COVER_SLIDE_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
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
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="2" name="Title 1"/>
          <p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
          <p:nvPr><p:ph type="ctrTitle"/></p:nvPr>
        </p:nvSpPr>
        <p:spPr/>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p>
            <a:r>
              <a:rPr lang="cs-CZ" dirty="0"/>
              <a:t>{TITLE}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="3" name="Subtitle 2"/>
          <p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
          <p:nvPr><p:ph type="subTitle" idx="1"/></p:nvPr>
        </p:nvSpPr>
        <p:spPr/>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p>
            <a:r>
              <a:rPr lang="cs-CZ" dirty="0"/>
              <a:t>{SUBTITLE}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr>
    <a:masterClrMapping/>
  </p:clrMapOvr>
</p:sld>'''

CLOSING_SLIDE_XML = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
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
</p:sld>'''


def find_layout_by_name(layout_dir, target_name_part):
    for f in sorted(os.listdir(layout_dir)):
        if not f.endswith(".xml"):
            continue
        path = os.path.join(layout_dir, f)
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
        name_match = re.search(r'<p:cSld\s+name="([^"]*)"', content)
        if name_match:
            name = name_match.group(1).lower()
            if target_name_part.lower() in name:
                return f, name_match.group(1)
    return None, None


def build_shell(output_path, title=None, client=None):
    work_dir = "/tmp/shell-build"
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)

    from unpack import unpack
    from pack import pack
    unpack(TEMPLATE_PATH, work_dir)

    slides_dir = os.path.join(work_dir, "ppt", "slides")
    rels_dir = os.path.join(slides_dir, "_rels")
    os.makedirs(slides_dir, exist_ok=True)
    os.makedirs(rels_dir, exist_ok=True)

    layout_dir = os.path.join(work_dir, "ppt", "slideLayouts")
    pres_rels_dir = os.path.join(work_dir, "ppt", "_rels")

    # Find layouts
    cover_layout, cover_name = find_layout_by_name(layout_dir, "cover slide + x ray")
    if not cover_layout:
        cover_layout = "slideLayout1.xml"
        cover_name = "(fallback)"
    print(f"Cover layout: {cover_layout} ({cover_name})")

    closing_layout, closing_name = find_layout_by_name(layout_dir, "bye bye")
    if not closing_layout:
        closing_layout = "slideLayout15.xml"
        closing_name = "(fallback)"
    print(f"Closing layout: {closing_layout} ({closing_name})")

    # Create slide files directly
    cover_xml = COVER_SLIDE_XML.replace(
        "{TITLE}", _xml_escape(title or "NÁZEV PROJEKTU")
    ).replace(
        "{SUBTITLE}", _xml_escape(client or "Klient")
    )
    with open(os.path.join(slides_dir, "slide1.xml"), "w", encoding="utf-8") as f:
        f.write(cover_xml)

    cover_rels = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/{cover_layout}"/>
</Relationships>'''
    with open(os.path.join(rels_dir, "slide1.xml.rels"), "w", encoding="utf-8") as f:
        f.write(cover_rels)

    with open(os.path.join(slides_dir, "slide2.xml"), "w", encoding="utf-8") as f:
        f.write(CLOSING_SLIDE_XML)

    closing_rels = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/{closing_layout}"/>
</Relationships>'''
    with open(os.path.join(rels_dir, "slide2.xml.rels"), "w", encoding="utf-8") as f:
        f.write(closing_rels)

    print(f"Created slide1.xml (cover) + slide2.xml (closing)")

    # Add slide relationships to presentation.xml.rels
    pres_rels_path = os.path.join(pres_rels_dir, "presentation.xml.rels")
    with open(pres_rels_path, "r", encoding="utf-8") as f:
        pres_rels_content = f.read()
    max_rid = max([int(m) for m in re.findall(r'Id="rId(\d+)"', pres_rels_content)], default=0)

    cover_rid = f"rId{max_rid + 1}"
    closing_rid = f"rId{max_rid + 2}"

    new_rels = f'  <Relationship Id="{cover_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>\n  <Relationship Id="{closing_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide2.xml"/>'
    pres_rels_content = pres_rels_content.replace("</Relationships>", new_rels + "\n</Relationships>")
    with open(pres_rels_path, "w", encoding="utf-8") as f:
        f.write(pres_rels_content)

    # Update presentation.xml — add sldIdLst
    pres_path = os.path.join(work_dir, "ppt", "presentation.xml")
    with open(pres_path, "r", encoding="utf-8") as f:
        pres = f.read()

    sld_list = f'''<p:sldIdLst>
    <p:sldId id="256" r:id="{cover_rid}"/>
    <p:sldId id="257" r:id="{closing_rid}"/>
  </p:sldIdLst>'''

    if "<p:sldIdLst>" in pres:
        pres = re.sub(r'<p:sldIdLst>.*?</p:sldIdLst>', sld_list, pres, flags=re.DOTALL)
    elif "<p:sldSz" in pres:
        pres = pres.replace("<p:sldSz", f"{sld_list}\n  <p:sldSz")
    else:
        pres = pres.replace("</p:presentation>", f"  {sld_list}\n</p:presentation>")

    with open(pres_path, "w", encoding="utf-8") as f:
        f.write(pres)

    # Update [Content_Types].xml
    ct_path = os.path.join(work_dir, "[Content_Types].xml")
    with open(ct_path, "r", encoding="utf-8") as f:
        ct = f.read()
    for slide_name in ["slide1.xml", "slide2.xml"]:
        override = f'<Override PartName="/ppt/slides/{slide_name}" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        if override not in ct:
            ct = ct.replace("</Types>", f"  {override}\n</Types>")
    with open(ct_path, "w", encoding="utf-8") as f:
        f.write(ct)

    # Clean and pack
    clean_script = os.path.join(PPTX_SCRIPTS, "clean.py")
    subprocess.run(["python3", clean_script, work_dir], capture_output=True)
    pack(work_dir, output_path, TEMPLATE_PATH)
    print(f"\nShell created: {output_path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build proposal shell from XLAB template")
    parser.add_argument("output", help="Output PPTX path")
    parser.add_argument("--title", help="Project title for cover slide")
    parser.add_argument("--client", help="Client name for cover slide")
    args = parser.parse_args()
    build_shell(args.output, args.title, args.client)
