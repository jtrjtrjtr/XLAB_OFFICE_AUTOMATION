#!/usr/bin/env python3
"""
Notion Queue Writer
Queries Reference Library for Approved + Signal/XLAB Proposal records
and writes their IDs to a Notion page that Cowork VM can read via MCP.

Runs as a cron job BEFORE the Cowork Case Study processing task.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

DATABASE_ID = "72153c9c-a113-4634-a1ec-9654ccb9e216"
QUEUE_PAGE_ID = "32ce8f30-d523-81bb-b26d-f7ee46a841e1"
NOTION_API_VERSION = "2022-06-28"


def load_api_key():
    key = os.environ.get("NOTION_API_KEY")
    if key:
        return key
    key_file = os.path.expanduser("~/.config/notion/api_key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            return f.read().strip()
    print("Error: NOTION_API_KEY not set and ~/.config/notion/api_key not found.", file=sys.stderr)
    sys.exit(1)


def notion_request(method, endpoint, payload=None):
    api_key = load_api_key()
    url = f"https://api.notion.com/v1/{endpoint}"
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(
        url, data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Notion API error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def get_text(props, name):
    prop = props.get(name, {})
    ptype = prop.get("type", "")
    if ptype == "title":
        return "".join(t.get("plain_text", "") for t in prop.get("title", []))
    if ptype == "rich_text":
        return "".join(t.get("plain_text", "") for t in prop.get("rich_text", []))
    if ptype == "select":
        sel = prop.get("select")
        return sel.get("name", "") if sel else ""
    if ptype == "url":
        return prop.get("url") or ""
    return ""


def query_approved_signals():
    filter_payload = {
        "and": [
            {"property": "Status", "select": {"equals": "Approved"}},
            {"or": [
                {"property": "Typ", "select": {"equals": "Signal"}},
                {"property": "Typ", "select": {"equals": "XLAB Proposal"}},
            ]},
        ]
    }
    all_results = []
    start_cursor = None
    while True:
        payload = {"filter": filter_payload, "page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        response = notion_request("POST", f"databases/{DATABASE_ID}/query", payload)
        all_results.extend(response.get("results", []))
        if not response.get("has_more"):
            break
        start_cursor = response.get("next_cursor")
    return all_results


def write_queue_page(records):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if not records:
        content = f"Poslední aktualizace: **{now}**\n---\n## Queue\nŽádné záznamy ke zpracování."
    else:
        lines = [f"Poslední aktualizace: **{now}**"]
        lines.append(f"\nPočet záznamů: **{len(records)}**")
        lines.append("---")
        lines.append("## Queue")
        lines.append("")
        for r in records:
            lines.append(f"- **{r['nazev']}** | ID: `{r['id']}` | Track: {r['track']} | Zdroj: {r['zdroj']} | Zdroj URL: {r['zdroj_url']} | SharePoint: {r['sharepoint_cesta']}")
        content = "\n".join(lines)

    # Update page content via PATCH
    # Notion API doesn't support replace_content directly, so we use the
    # internal API approach: archive all children, then append new ones.
    # Simpler: we use blocks API.

    # First, get existing block children and delete them
    children = notion_request("GET", f"blocks/{QUEUE_PAGE_ID}/children?page_size=100")
    for block in children.get("results", []):
        notion_request("DELETE", f"blocks/{block['id']}")

    # Now append new content as blocks
    blocks = []

    # Header paragraph
    blocks.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {"type": "text", "text": {"content": f"Poslední aktualizace: "}, "annotations": {}},
                {"type": "text", "text": {"content": now}, "annotations": {"bold": True}},
            ]
        }
    })

    blocks.append({"object": "block", "type": "divider", "divider": {}})

    blocks.append({
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Queue"}}]}
    })

    if not records:
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Žádné záznamy ke zpracování."}}]}
        })
    else:
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [
                {"type": "text", "text": {"content": f"Počet záznamů: "}, "annotations": {}},
                {"type": "text", "text": {"content": str(len(records))}, "annotations": {"bold": True}},
            ]}
        })

        for r in records:
            text_parts = [
                {"type": "text", "text": {"content": r["nazev"]}, "annotations": {"bold": True}},
                {"type": "text", "text": {"content": f"\nID: {r['id']}"}},
                {"type": "text", "text": {"content": f"\nTrack: {r['track']} | Typ: {r['typ']} | Zdroj: {r['zdroj']}"}},
            ]
            if r["zdroj_url"]:
                text_parts.append({"type": "text", "text": {"content": f"\nZdroj URL: {r['zdroj_url']}"}})
            if r["sharepoint_cesta"]:
                text_parts.append({"type": "text", "text": {"content": f"\nSharePoint: {r['sharepoint_cesta']}"}})

            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": text_parts}
            })

    # Append blocks in batches of 100 (API limit)
    for i in range(0, len(blocks), 100):
        batch = blocks[i:i+100]
        notion_request("PATCH", f"blocks/{QUEUE_PAGE_ID}/children", {"children": batch})

    print(f"[{now}] Queue updated: {len(records)} record(s)")


def main():
    results = query_approved_signals()
    records = []
    for page in results:
        props = page.get("properties", {})
        records.append({
            "id": page["id"],
            "nazev": get_text(props, "Název"),
            "typ": get_text(props, "Typ"),
            "track": get_text(props, "Track"),
            "zdroj": get_text(props, "Zdroj"),
            "zdroj_url": get_text(props, "Zdroj URL"),
            "sharepoint_cesta": get_text(props, "SharePoint cesta"),
        })
    write_queue_page(records)


if __name__ == "__main__":
    main()
