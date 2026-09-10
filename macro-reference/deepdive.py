#!/usr/bin/env python3
"""Deep-dive: extract representative, complete structures for the interaction-model questions."""
import collections
import json
import glob
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def load_macro(path):
    raw = json.load(open(path, encoding="utf-8"))
    return raw["macro"] if isinstance(raw, dict) and "macro" in raw else raw


def scenes():
    out = []
    for f in sorted(glob.glob(os.path.join(OUT, "*.macro"))):
        try:
            m = load_macro(f)
        except Exception:
            continue
        for i, a in enumerate(m.get("m_actionList") or []):
            if isinstance(a, dict) and a.get("sceneDescription"):
                out.append((os.path.basename(f), m, i, a))
    return out


def walk(items, cb):
    for it in items or []:
        if not isinstance(it, dict):
            continue
        cb(it)
        for ch in (it.get("children") or []):
            walk([ch], cb)
        for tab in ((it.get("sceneHorizontalPagerConfig") or {}).get("tabs") or []):
            walk((tab or {}).get("children"), cb)


def trunc(v, n=300):
    s = json.dumps(v, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + "…"


def main():
    all_scenes = scenes()
    print(f"total scenes: {len(all_scenes)}")
    L = []
    A = L.append

    # ---- 1. Overlay full config ----
    A("# DETAILS — structures réelles (interaction app ↔ scène)")
    A("")
    A("## Overlay — structure complète")
    A("")
    shown = set()
    seen = collections.Counter()
    for base, m, i, a in all_scenes:
        do = (a["sceneDescription"].get("sceneConfig") or {}).get("displayOption") or {}
        if isinstance(do, dict) and do.get("type") == "Overlay":
            key = tuple(sorted(do.keys()))
            if seen[key] < 1 and key not in shown:
                shown.add(key)
                A(f"```json\n{json.dumps(do, indent=1, ensure_ascii=False)}\n```")
                A(f"*— {base}, scène '{a['sceneDescription']['sceneConfig'].get('name')}'*")
                A("")
            seen[key] += 1
    A(f"Overlay total: {sum(seen.values())}")
    A("")

    # ---- 2. Variable binding structures ----
    A("## Structures de binding de variables")
    A("")
    bind_examples = {
        "variableToUpdate": {},
        "variableUpdateValue": {},
        "visibilityVariable": {},
        "booleanVariable": {},
        "stringVariable": {},
        "numberVariable": {},
        "dictionaryVariable": {},
        "bindToVariable": {},
    }
    for base, m, i, a in all_scenes:
        sd = a["sceneDescription"]
        items = (sd.get("itemList") or {}).get("items") or []
        def cb(it):
            ctype = it.get("type")
            ck = {
                "SceneText": "sceneTextConfig", "SceneButton": "sceneButtonConfig",
                "SceneSwitch": "sceneSwitchConfig", "SceneSlider": "sceneSliderConfig",
                "SceneDropDownSelection": "sceneDropDownConfig", "SceneMapView": "sceneMapViewConfig",
                "SceneImage": "sceneImageConfig", "SceneEditText": "sceneEditTextConfig",
                "SceneCheckBox": "sceneCheckBoxConfig",
            }.get(ctype)
            cfg = it.get(ck) or {}
            for k in bind_examples:
                if k in cfg:
                    if k not in bind_examples[k]:
                        bind_examples[k][k] = {"file": base, "scene": (sd.get("sceneConfig") or {}).get("name"), "value": trunc(cfg[k], 260)}
        walk(items, cb)
    for k, ex in bind_examples.items():
        A(f"### `{k}`")
        A("")
        if ex:
            e = ex[k]
            A(f"Exemple ({e['file']}, scène '{e['scene']}') :")
            A(f"```json\n{e['value']}\n```")
        else:
            A("(aucun exemple dans le corpus)")
        A("")

    # ---- 3. Background full ----
    A("## Background — structure complète (cases avec image)")
    A("")
    for base, m, i, a in all_scenes:
        cfg = (a["sceneDescription"].get("sceneConfig") or {})
        if cfg.get("backgroundImage"):
            A(f"### {base} — '{cfg.get('name')}'")
            A("")
            A(f"```json\n{json.dumps({'backgroundImage': cfg['backgroundImage'], 'backgroundImageDisplayMode': cfg.get('backgroundImageDisplayMode')}, indent=1, ensure_ascii=False)}\n```")
            A("")

    # ---- 4. SceneSpacer ----
    A("## SceneSpacer (composant inconnu du builder)")
    A("")
    for base, m, i, a in all_scenes:
        items = (a["sceneDescription"].get("itemList") or {}).get("items") or []
        def cb(it):
            if it.get("type") == "SceneSpacer":
                A(f"```json\n{json.dumps(it, indent=1, ensure_ascii=False)}\n```")
                A(f"*— {base}*")
                A("")
        walk(items, cb)
        break

    # ---- 5. Button click config full + variable TYPES ----
    A("## ButtonClickConfig — structure complète")
    A("")
    count = 0
    for base, m, i, a in all_scenes:
        if count >= 3:
            break
        items = (a["sceneDescription"].get("itemList") or {}).get("items") or []
        def cb(it):
            nonlocal count
            if it.get("type") == "SceneButton" and count < 3:
                bc = it.get("sceneButtonConfig") or {}
                cl = bc.get("buttonClickConfig") or bc.get("sceneButtonClickConfig")
                if cl:
                    A(f"### {base} — guid {it.get('guid')}")
                    A("")
                    A(f"```json\n{json.dumps(cl, indent=1, ensure_ascii=False)[:900]}\n```")
                    A("")
                    count += 1
        walk(items, cb)

    # ---- 6. guid / iconRes semantics ----
    A("## GUID & iconRes")
    A("")
    guid_vals = collections.Counter()
    iconres_vals = collections.Counter()
    uniqueids = collections.Counter()
    for base, m, i, a in all_scenes:
        items = (a["sceneDescription"].get("itemList") or {}).get("items") or []
        def cb(it):
            g = it.get("guid")
            if g is not None:
                guid_vals["0" if g == 0 else ("neg" if g < 0 else "pos")] += 1
            ir = it.get("iconRes")
            if ir is not None:
                iconres_vals["0" if ir == 0 else "nonzero"] += 1
            uid = it.get("uniqueId")
            if uid is not None:
                uniqueids["0" if uid == 0 else ("id-like" if isinstance(uid, int) else "string")] += 1
        walk(items, cb)
    A(f"`guid` distribution : {dict(guid_vals)}")
    A(f"`iconRes` distribution : {dict(iconres_vals)}")
    A(f"`uniqueId` distribution : {dict(uniqueids)}")
    A("")

    # ---- 7. SceneText auto-refresh & magic text fields ----
    A("## SceneText — champs avancés (auto refresh / magic text)")
    A("")
    seen_kt = set()
    for base, m, i, a in all_scenes:
        items = (a["sceneDescription"].get("itemList") or {}).get("items") or []
        def cb(it):
            if it.get("type") == "SceneText":
                cfg = it.get("sceneTextConfig") or {}
                k = tuple(sorted(cfg.keys()))[2:13]
                if k not in seen_kt:
                    seen_kt.add(k)
                    A(f"```json\n{json.dumps(cfg, indent=1, ensure_ascii=False)[:700]}\n```")
                    A(f"*— {base}*")
                    A("")
        walk(items, cb)
        if len(seen_kt) >= 3:
            break

    # ---- 8. localVariables present in the scene macros ----
    A("## Variables locales dans les macros à scène")
    A("")
    lv_counts = []
    for base, m, i, a in all_scenes:
        lv = m.get("localVariables") or []
        names = [v.get("m_name") for v in lv if isinstance(v, dict)]
        lv_counts.append((base, len(names), names[:8]))
    for base, n, names in lv_counts[:12]:
        A(f"- {base} : {n} vars — {names}")
    A("")

    with open(os.path.join(OUT, "DETAILS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("wrote DETAILS.md", len(L), "lines")


if __name__ == "__main__":
    main()