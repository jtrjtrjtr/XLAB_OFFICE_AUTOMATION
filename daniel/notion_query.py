#!/usr/bin/env python3
"""
Notion Database Query Tool
Queries Reference Library for records matching property filters.
Uses the official Notion API (POST /databases/{id}/query) which supports
property-based filtering — unlike Notion MCP which only has semantic search.

Usage:
  export NOTION_API_KEY="ntn_..."
  python3 notion_query.py                    # default: Approved + Signal/XLAB Proposal
  python3 notion_query.py --status New       # custom status filter
  python3 notion_query.py --ids-only         # output only page IDs (for piping)
"""

import json
import os
import sys
import urllib.request
import urllib.error

# Reference Library database ID
DATABASE_ID = "72153c9c-a113-4634-a1ec-9654ccb9e216"

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


def notion_request(endpoint, payload=None):
    api_key = load_api_key()

    url = f"https://api.notion.com/v1/{endpoint}"
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
        },
        method="POST" if payload else "GET",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Notion API error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def get_property_text(props, name):
    prop = props.get(name, {})
    ptype = prop.get("type", "")
    if ptype == "title":
        return "".join(t.get("plain_text", "") for t in prop.get("title", []))
    if ptype == "rich_text":
        return "".join(t.get("plain_text", "") for t in prop.get("rich_text", []))
    if ptype == "select":
        sel = prop.get("select")
        return sel.get("name", "") if sel else ""
    if ptype == "multi_select":
        return ", ".join(o.get("name", "") for o in prop.get("multi_select", []))
    if ptype == "url":
        return prop.get("url") or ""
    if ptype == "number":
        return str(prop.get("number", ""))
    return ""


def query_database(status="Approved", types=None):
    if types is None:
        types = ["Signal", "XLAB Proposal"]

    type_filters = [
        {"property": "Typ", "select": {"equals": t}}
        for t in types
    ]

    filter_payload = {
        "and": [
            {"property": "Status", "select": {"equals": status}},
            {"or": type_filters} if len(type_filters) > 1 else type_filters[0],
        ]
    }

    all_results = []
    start_cursor = None

    while True:
        payload = {"filter": filter_payload, "page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor

        response = notion_request(f"databases/{DATABASE_ID}/query", payload)
        all_results.extend(response.get("results", []))

        if not response.get("has_more"):
            break
        start_cursor = response.get("next_cursor")

    return all_results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Query Notion Reference Library")
    parser.add_argument("--status", default="Approved", help="Status filter (default: Approved)")
    parser.add_argument("--type", nargs="+", default=["Signal", "XLAB Proposal"], help="Typ filter(s)")
    parser.add_argument("--ids-only", action="store_true", help="Output only page IDs")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    results = query_database(status=args.status, types=args.type)

    if args.ids_only:
        for page in results:
            print(page["id"])
        return

    records = []
    for page in results:
        props = page.get("properties", {})
        record = {
            "id": page["id"],
            "url": page.get("url", ""),
            "nazev": get_property_text(props, "Název"),
            "status": get_property_text(props, "Status"),
            "typ": get_property_text(props, "Typ"),
            "track": get_property_text(props, "Track"),
            "zdroj": get_property_text(props, "Zdroj"),
            "zdroj_url": get_property_text(props, "Zdroj URL"),
            "sharepoint_cesta": get_property_text(props, "SharePoint cesta"),
            "klient": get_property_text(props, "Klient"),
            "case_study_level": get_property_text(props, "Case Study Level"),
        }
        records.append(record)

    if args.json:
        print(json.dumps(records, indent=2, ensure_ascii=False))
        return

    print(f"Found {len(records)} record(s) matching Status={args.status}, Typ={args.type}\n")
    if not records:
        print("No records found.")
        return

    for i, r in enumerate(records, 1):
        print(f"  {i}. {r['nazev']}")
        print(f"     ID: {r['id']}")
        print(f"     Track: {r['track']} | Zdroj: {r['zdroj']} | Typ: {r['typ']}")
        if r["zdroj_url"]:
            print(f"     URL: {r['zdroj_url']}")
        if r["sharepoint_cesta"]:
            print(f"     SharePoint: {r['sharepoint_cesta']}")
        print()


if __name__ == "__main__":
    main()
