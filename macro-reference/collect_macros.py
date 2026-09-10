#!/usr/bin/env python3
"""
Corpus collector for MacroDroid scene macros.
Sources: the public Template Store API (templates.macrodroid.com).

- Queries the list/search API with several terms likely to surface scene macros.
- Decodes the embedded macro JSON embedded in the "json" field.
- Keeps macros that contain at least one CustomSceneAction (sceneDescription).
- Saves them as standalone .macro files (same format MacroDroid exports / wiki hosts)
  and writes a manifest describing each macro.

Usage: python3 collect_macros.py  (writes into macro-reference/)
"""

import json
import os
import re
import time
import urllib.parse
import urllib.request

API = "https://templates.macrodroid.com/api/templates"
LANG = "en"
PAGE_SIZE = 60
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))

SEARCH_TERMS = [
    "scene",
    "custom scene",
    "customscene",
    "overlay",
    "dialog",
    "popup",
    "menu",
    "dashboard",
    "hud",
    "launcher",
    "quick settings",
    "control center",
    "widget",
]


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "macro-reference-collector/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def find_scene_actions(macro):
    """Return list of (index, action) for CustomScene actions in a macro's action list."""
    found = []
    acts = macro.get("m_actionList") or []
    for i, a in enumerate(acts):
        if isinstance(a, dict):
            cls = a.get("m_classType") or a.get("actionClassType") or ""
            if "sceneDescription" in a or "Scene" in cls or "scene" in cls.lower():
                found.append((i, a))
    return found


def extract_inner_macro(raw_macro):
    """Template store embeds the inner macro directly; .macro files use {macroExportVersion, macro}."""
    if isinstance(raw_macro, dict) and "macro" in raw_macro and isinstance(raw_macro["macro"], dict):
        return raw_macro["macro"]
    return raw_macro


def slugify(name):
    s = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower()
    return s[:50] or "macro"


def main():
    seen = {}
    order = []

    for term in SEARCH_TERMS:
        url = f"{API}?deviceLanguage={LANG}&start=0&pageSize={PAGE_SIZE}&searchTerm={urllib.parse.quote(term)}"
        try:
            items = fetch(url)
        except Exception as e:
            print(f"[warn] search term {term!r} failed: {e}")
            time.sleep(2)
            continue
        for t in items:
            tid = t.get("id")
            if not tid or tid in seen:
                continue
            jf = t.get("json")
            if not jf:
                continue
            try:
                macro = extract_inner_macro(json.loads(urllib.parse.unquote(jf)))
            except Exception:
                continue
            scene_actions = find_scene_actions(macro)
            if scene_actions:
                seen[tid] = (t, macro, scene_actions)
                order.append(tid)
        print(f"[ok] term {term!r}: {len(items)} results, {len(seen)} scene macros so far")
        time.sleep(1)

    manifest = []
    os.makedirs(OUT, exist_ok=True)
    for tid in order:
        t, macro, scene_actions = seen[tid]
        name = t.get("name") or f"template_{tid}"
        fname = f"{tid}__{slugify(name)}.macro"
        path = os.path.join(OUT, fname)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(macro, f, ensure_ascii=False, indent=1)
        manifest.append({
            "id": tid,
            "name": name,
            "file": fname,
            "url": f"https://templates.macrodroid.com/api/templates/{tid}?deviceLanguage=en",
            "viewUrl": f"https://templates.macrodroid.com/view/{tid}",
            "sceneActionCount": len(scene_actions),
            "sceneActionIndexes": [i for i, _ in scene_actions],
            "description": (t.get("description") or "")[:200],
        })
        print(f"[save] {fname} ({len(scene_actions)} scene actions)")

    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(f"\nDone. {len(order)} scene macros saved to {OUT}")


if __name__ == "__main__":
    main()