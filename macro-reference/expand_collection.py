#!/usr/bin/env python3
"""Second sweep: page through ALL templates (recent), plus specifically-checked forum-spotted IDs.

Saves newly discovered scene macros into macro-reference/ and appends to manifest.json.
"""
import json, os, re, time, urllib.parse, urllib.request

API = "https://templates.macrodroid.com/api/templates"
LANG = "en"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(OUT, "manifest.json")

SPECIFIC_IDS = [31806, 31698, 19510, 30243, 31204, 31288, 27640, 29850, 31105, 11667, 6119, 26440, 29059]


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "macro-reference-collector/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def extract_inner_macro(raw):
    if isinstance(raw, dict) and "macro" in raw and isinstance(raw["macro"], dict):
        return raw["macro"]
    return raw


def find_scene_actions(macro):
    found = []
    for i, a in enumerate(macro.get("m_actionList") or []):
        if isinstance(a, dict):
            cls = a.get("m_classType") or a.get("actionClassType") or ""
            if "sceneDescription" in a or "Scene" in cls or "scene" in cls.lower():
                found.append((i, a))
    return found


def slugify(name):
    s = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower()
    return s[:50] or "macro"


def save(tid, t, macro, scene_actions):
    name = t.get("name") or f"template_{tid}"
    fname = f"{tid}__{slugify(name)}.macro"
    path = os.path.join(OUT, fname)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(macro, f, ensure_ascii=False, indent=1)
    rec = {
        "id": tid, "name": name, "file": fname,
        "url": f"https://templates.macrodroid.com/api/templates/{tid}?deviceLanguage=en",
        "viewUrl": f"https://templates.macrodroid.com/view/{tid}",
        "sceneActionCount": len(scene_actions),
        "sceneActionIndexes": [i for i, _ in scene_actions],
        "description": (t.get("description") or "")[:200],
        "source": "sweep",
    }
    print(f"[save] {fname} ({len(scene_actions)} scene actions)")
    return rec


def main():
    seen = {r["id"] for r in json.load(open(MANIFEST_PATH))}
    new_recs = []

    ids_checked = set(SPECIFIC_IDS)
    # 1) specific forum-spotted ids
    for tid in SPECIFIC_IDS:
        if tid in seen:
            continue
        try:
            arr = fetch(f"{API}/{tid}?deviceLanguage={LANG}")
            t = arr[0] if isinstance(arr, list) and arr else arr
        except Exception as e:
            print(f"[warn] id {tid}: {e}")
            continue
        try:
            macro = extract_inner_macro(json.loads(urllib.parse.unquote(t["json"])))
        except Exception as e:
            print(f"[warn] id {tid} json decode: {e}")
            continue
        sa = find_scene_actions(macro)
        if sa:
            rec = save(tid, t, macro, sa)
            new_recs.append(rec)
            seen.add(tid)
        time.sleep(0.5)

    # 2) sweep ALL templates with pagination
    start, page = 0, 80
    while True:
        url = f"{API}?deviceLanguage={LANG}&start={start}&pageSize={page}"
        try:
            items = fetch(url)
        except Exception as e:
            print(f"[warn] sweep start={start}: {e}; stopping")
            break
        if not items:
            break
        for t in items:
            tid = t.get("id")
            if not tid or tid in seen or tid in ids_checked:
                continue
            ids_checked.add(tid)
            jf = t.get("json")
            if not jf:
                continue
            try:
                macro = extract_inner_macro(json.loads(urllib.parse.unquote(jf)))
            except Exception:
                continue
            sa = find_scene_actions(macro)
            if sa:
                rec = save(tid, t, macro, sa)
                new_recs.append(rec)
                seen.add(tid)
        print(f"[page] start={start}: {len(items)} items, {len(new_recs)} new scene macros")
        if len(items) < page:
            break
        start += page
        time.sleep(0.8)

    if new_recs:
        man = json.load(open(MANIFEST_PATH))
        man.extend(new_recs)
        with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
            json.dump(man, f, ensure_ascii=False, indent=1)
    print(f"\nDone. {len(new_recs)} new macros. Total in manifest: {len(seen)}")


if __name__ == "__main__":
    main()