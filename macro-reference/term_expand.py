#!/usr/bin/env python3
"""Term-based expansion. Queries many search terms, dedupes, saves scene macros incrementally,
appends to manifest.json as it goes (crash-safe)."""
import json, os, re, time, urllib.parse, urllib.request

API = "https://templates.macrodroid.com/api/templates"
LANG = "en"
PAGE_SIZE = 60
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(OUT, "manifest.json")

TERMS = [
    "gui", "ui", "user interface", "control panel", "popup panel", "floating",
    "media controls", "music player", "volume", "brightness", "quick toggle",
    "toggle panel", "launcher", "app drawer", "icon grid", "switches",
    "settings panel", "control center", "button pad", "keypad", "dashboard",
    "web page", "html", "custom ui", "scene builder", "tap targets",
    "game menu", "mod menu", "cheat menu", "hud", "health bar",
    "spotify", "youtube", "player overlay", "shell", "terminal",
    "clipboard", "calculator", "clock overlay", "floating clock",
    "status bar", "notification panel", "drawer", "quick tile",
]


def fetch(url, timeout=90):
    req = urllib.request.Request(url, headers={"User-Agent": "macro-reference-collector/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def extract_inner(m):
    return m["macro"] if isinstance(m, dict) and "macro" in m and isinstance(m["macro"], dict) else m


def scene_actions(macro):
    out = []
    for i, a in enumerate(macro.get("m_actionList") or []):
        if isinstance(a, dict):
            cls = a.get("m_classType") or ""
            if "sceneDescription" in a or "Scene" in cls or "scene" in cls.lower():
                out.append((i, a))
    return out


def slugify(name):
    s = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower()
    return s[:50] or "macro"


def main():
    man = json.load(open(MAN))
    seen = {r["id"] for r in man}
    added = 0
    for term in TERMS:
        url = f"{API}?deviceLanguage={LANG}&start=0&pageSize={PAGE_SIZE}&searchTerm={urllib.parse.quote(term)}"
        try:
            items = fetch(url)
        except Exception as e:
            print(f"[warn] {term!r}: {e}")
            time.sleep(2)
            continue
        chunk = []
        for t in items:
            tid = t.get("id")
            if not tid or tid in seen or not t.get("json"):
                continue
            try:
                macro = extract_inner(json.loads(urllib.parse.unquote(t["json"])))
            except Exception:
                continue
            sa = scene_actions(macro)
            if not sa:
                continue
            name = t.get("name") or f"template_{tid}"
            fname = f"{tid}__{slugify(name)}.macro"
            with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
                json.dump(macro, f, ensure_ascii=False, indent=1)
            chunk.append({
                "id": tid, "name": name, "file": fname,
                "url": f"{API}/{tid}?deviceLanguage=en",
                "viewUrl": f"https://templates.macrodroid.com/view/{tid}",
                "sceneActionCount": len(sa),
                "sceneActionIndexes": [i for i, _ in sa],
                "description": (t.get("description") or "")[:200],
                "source": f"term:{term}",
            })
            seen.add(tid)
            added += 1
            print(f"[save] {fname} ({len(sa)}) via {term!r}", flush=True)
        if chunk:
            man.extend(chunk)
            with open(MAN, "w", encoding="utf-8") as f:
                json.dump(man, f, ensure_ascii=False, indent=1)
        print(f"[term] {term!r}: {len(items)} results, total added {added}", flush=True)
        time.sleep(0.8)
    print(f"DONE added={added} total={len(seen)}")


if __name__ == "__main__":
    main()