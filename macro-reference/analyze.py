#!/usr/bin/env python3
"""
Corpus analysis: study how real scene macros are structured so we can extend the
Scene Builder with the exact fields MacroDroid actually uses.

Outputs macro-reference/ANALYSE.md and macro-reference/analysis_summary.json
"""
import collections
import json
import glob
import os
import re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
magic_counter = 0

# Fields the v19 builder already knows, per component type (from NEW_ITEM_TEMPLATES
# in MacroDroid_Scene_Builder_v19.html). Used to highlight "unknown/new" fields.
KNOWN_COMPONENT_FIELDS = {
    "SceneText": ["type", "guid", "sceneTextConfig"],
    "SceneIcon": ["type", "guid", "sceneIconConfig"],
    "SceneImage": ["type", "guid", "sceneImageConfig"],
    "SceneButton": ["type", "guid", "sceneButtonConfig"],
    "SceneCheckBox": ["type", "guid", "sceneCheckBoxConfig"],
    "SceneSwitch": ["type", "guid", "checkedValue", "sceneSwitchConfig"],
    "SceneSlider": ["type", "guid", "sceneSliderConfig"],
    "SceneVerticalSlider": ["type", "guid", "sceneVerticalSliderConfig"],
    "SceneProgressIndicator": ["type", "guid", "sceneProgressIndicatorConfig"],
    "SceneEditText": ["type", "guid", "enteredText", "lastEnteredText", "sceneEditTextConfig"],
    "SceneDropDownSelection": ["type", "guid", "sceneDropDownConfig"],
    "SceneOptionSelector": ["type", "guid", "sceneOptionSelectorConfig"],
    "SceneDatePicker": ["type", "guid", "sceneDatePickerConfig"],
    "SceneMapView": ["type", "guid", "sceneMapViewConfig"],
    "SceneTimePicker": ["type", "guid", "sceneTimePickerConfig"],
    "SceneWebView": ["type", "guid", "sceneWebViewConfig"],
    "SceneHorizontalDivider": ["type", "guid", "config"],
    "SceneHorizontalLayout": ["type", "guid", "children", "sceneHorizontalLayoutConfig"],
    "SceneVerticalLayout": ["type", "guid", "children", "sceneVerticalLayoutConfig"],
    "SceneGridLayout": ["type", "guid", "children", "sceneGridLayoutConfig"],
    "SceneTableLayout": ["type", "guid", "children", "sceneTableLayoutConfig"],
    "SceneHorizontalPager": ["type", "guid", "sceneHorizontalPagerConfig"],
}

KNOWN_SCENECONFIG_FIELDS = [
    "backgroundColor", "foregroundColor", "blockNextActions", "closeOnBackgroundTouch",
    "contentPadding", "dismissOnBackPress", "dismissOnHomeTaskSwitch", "displayOption",
    "name", "roundedCornerAmount", "showOnLockScreen", "updateValuesOnSceneClose",
]

CONFIG_KEY_BY_TYPE = {
    "SceneText": "sceneTextConfig", "SceneIcon": "sceneIconConfig", "SceneImage": "sceneImageConfig",
    "SceneButton": "sceneButtonConfig", "SceneCheckBox": "sceneCheckBoxConfig", "SceneSwitch": "sceneSwitchConfig",
    "SceneSlider": "sceneSliderConfig", "SceneVerticalSlider": "sceneVerticalSliderConfig",
    "SceneProgressIndicator": "sceneProgressIndicatorConfig", "SceneEditText": "sceneEditTextConfig",
    "SceneDropDownSelection": "sceneDropDownConfig", "SceneOptionSelector": "sceneOptionSelectorConfig",
    "SceneDatePicker": "sceneDatePickerConfig", "SceneMapView": "sceneMapViewConfig",
    "SceneTimePicker": "sceneTimePickerConfig", "SceneWebView": "sceneWebViewConfig",
    "SceneHorizontalPager": "sceneHorizontalPagerConfig",
}


def truncate(v, n=120):
    s = json.dumps(v, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + "…"


def load_macro(path):
    raw = json.load(open(path, encoding="utf-8"))
    if isinstance(raw, dict) and "macro" in raw and isinstance(raw["macro"], dict):
        return raw["macro"]
    return raw


def scene_actions(macro):
    out = []
    for i, a in enumerate(macro.get("m_actionList") or []):
        if isinstance(a, dict) and a.get("sceneDescription"):
            out.append((i, a))
    return out


def walk_items(items, cb):
    for it in items or []:
        if not isinstance(it, dict):
            continue
        cb(it)
        for k in ("children",):
            if isinstance(it.get(k), list):
                walk_items(it[k], cb)
        # horizontal pager tabs
        tabs = (it.get("sceneHorizontalPagerConfig") or {}).get("tabs")
        if isinstance(tabs, list):
            for tab in tabs:
                walk_items((tab or {}).get("children"), cb)


def main():
    macros = {}
    for f in sorted(glob.glob(os.path.join(OUT, "*.macro"))):
        base = os.path.basename(f)
        try:
            m = load_macro(f)
        except Exception as e:
            print("skip", f, e)
            continue
        if not scene_actions(m):
            continue
        macros[base] = m

    disp_counter = collections.Counter()
    scenecfg_counter = collections.Counter()
    unknown_sccfg = collections.Counter()
    unknown_scenecfg = collections.Counter()
    comp_counter = collections.Counter()
    unknown_comp = collections.Counter()
    icondisc = collections.Counter()
    background_counter = collections.Counter()
    var_binding_sites = collections.Counter()
    constraints_types = collections.Counter()
    item_field_samples = {}

    examples = {"displayOption": collections.defaultdict(list), "background": [], "unknown": []}
    scene_cfg_var_summaries = []

    for base, m in macros.items():
        sa = scene_actions(m)
        for idx, action in sa:
            sd = action["sceneDescription"]
            sccfg = sd.get("sceneConfig") or {}
            disp = sccfg.get("displayOption")
            dtype = disp.get("type") if isinstance(disp, dict) else (disp if isinstance(disp, str) else json.dumps(disp))
            disp_counter[str(dtype)] += 1
            if dtype not in examples["displayOption"] or len(examples["displayOption"][dtype]) < 2:
                examples["displayOption"][str(dtype)].append({
                    "file": base, "scene": sccfg.get("name"), "displayOption": disp,
                })
            for k, v in sccfg.items():
                scenecfg_counter[k] += 1
                if k not in KNOWN_SCENECONFIG_FIELDS:
                    unknown_scenecfg[k] += 1
                    if len(unknown_scenecfg) > 0 and (k, base) not in item_field_samples:
                        item_field_samples[f"sceneConfig.{k}"] = (base, sccfg.get("name"), truncate(v, 200))
            bg = sccfg.get("backgroundImage") or sccfg.get("backgroundImageData")
            if bg:
                background_counter["backgroundImage/image"] += 1
            else:
                bgm = sccfg.get("backgroundImageDisplayMode")
                if bgm:
                    background_counter[f"bgImageDisplayMode:{bgm}"] += 1
            if sccfg.get("backgroundImageDisplayMode"):
                bgc = background_counter
                if len(examples["background"]) < 6:
                    examples["background"].append({"file": base, "scene": sccfg.get("name"),
                        "keys": [k for k in sccfg if "ground" in k and k in ("backgroundImage","backgroundImageData","backgroundImageDisplayMode","backgroundColor")],
                        "displayMode": sccfg.get("backgroundImageDisplayMode")})
            # items
            items = ((sd.get("itemList") or {}).get("items")) or []
            for it in items or []:
                pass
            def cb(it):
                global magic_counter
                t = it.get("type")
                comp_counter[t] += 1
                # unknown top-level fields
                known = KNOWN_COMPONENT_FIELDS.get(t)
                if known:
                    for k in it:
                        if k not in known:
                            unknown_comp[(t, k)] += 1
                # record one example per unexpected field
                ctype = it.get("type")
                ck = CONFIG_KEY_BY_TYPE.get(ctype)
                cfg = it.get(ck)
                if cfg:
                    for k, v in cfg.items():
                        if k in ("selectionOptions", "entries", "sceneImageData", "mapMarker", "tabs"):
                            continue
                        s = json.dumps(v, ensure_ascii=False)
                        if "magicText" in s or "[v" in s or "variable" in str(k).lower() or "Variable" in str(k):
                            var_binding_sites[k] += 1
                        magic_counter += s.count("[") - s.count("[]")
                # detect extended button config / click config
                if ctype == "SceneButton":
                    bcfg = it.get("sceneButtonConfig") or {}
                    click = bcfg.get("sceneButtonClickConfig") or bcfg.get("buttonClickConfig")
                    if click:
                        item_field_samples.setdefault("SceneButton.clickConfig", (base, it.get("guid"), truncate(click, 220)))
                if ctype == "SceneSwitch":
                    icondisc[("SceneSwitch.checkedValue" if "checkedValue" in it else "?")] += 1

            walk_items(items, cb)

            # constraint list of the scene action
            for c in action.get("m_constraintList") or []:
                constraints_types[c.get("m_classType")] += 1

    # ---- build markdown ----
    L = []
    L.append("# ANALYSE — corpus des scenes réelles")
    L.append("")
    L.append(f"Macros analysés : `{len(macros)}` (fichiers dans ce dossier, source Template Store + wiki).")
    L.append("")
    L.append("## 1. Composants utilisés")
    L.append("")
    L.append("| type | occurrences |")
    L.append("|---|---|")
    for t, c in comp_counter.most_common():
        L.append(f"| {t} | {c} |")
    L.append("")
    L.append("## 2. displayOption (mode d'affichage)")
    L.append("")
    L.append("| mode | scènes |")
    L.append("|---|---|")
    for t, c in disp_counter.most_common():
        L.append(f"| `{t}` | {c} |")
    L.append("")
    L.append("Exemples réels :")
    for t, exs in examples["displayOption"].items():
        for e in exs:
            L.append(f"- `{t}` — {e['file']} ({e['scene']}) : `{truncate(e['displayOption'], 150)}`")
    L.append("")
    L.append("## 3. Champs sceneConfig utilisés")
    L.append("")
    L.append("| clé | scènes |")
    L.append("|---|---|")
    for k, c in scenecfg_counter.most_common():
        star = " ⚠️ inconnu du builder" if k not in KNOWN_SCENECONFIG_FIELDS else ""
        L.append(f"| `{k}` | {c}{star} |")
    L.append("")
    L.append("### Champs sceneConfig non gérés par le builder v19")
    for k, c in unknown_scenecfg.most_common():
        base, sc, val = item_field_samples.get(f"sceneConfig.{k}", ("", "", ""))
        L.append(f"- `{k}` ×{c} (ex: {base} '{sc}' → {val})")
    L.append("")
    L.append("## 4. Champs de composants non gérés par le builder v19")
    L.append("")
    for (t, k), c in unknown_comp.most_common():
        if c == 0:
            continue
        L.append(f"- `{t}.{k}` ×{c}")
    L.append("")
    L.append("## 5. Bindings variables / magic text")
    L.append("")
    L.append("Sites de binding détectés (clés dont le nom ou la valeur référence une variable) :")
    for k, c in var_binding_sites.most_common(25):
        L.append(f"- `{k}` ×{c}")
    L.append("")
    L.append("## 6. Background")
    L.append("")
    for k, c in background_counter.most_common():
        L.append(f"- {k} ×{c}")
    L.append("")
    L.append("## 7. Constraints de l'action CustomSceneAction")
    L.append("")
    for k, c in constraints_types.most_common():
        L.append(f"- `{k}` ×{c}")
    L.append("")
    L.append("## 8. Boutons / click config")
    L.append("")
    base, guid, v = item_field_samples.get("SceneButton.clickConfig", ("—", "—", "—"))
    L.append(f"Exemple `SceneButton.sceneButtonConfig.buttonClickConfig` ({base} guid={guid}) :")
    L.append(f"```json\n{v}\n```")
    L.append("")

    with open(os.path.join(OUT, "ANALYSE.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    summary = {
        "macros": len(macros),
        "displayOption": dict(disp_counter),
        "sceneConfig_fields": dict(scenecfg_counter),
        "unknown_sceneConfig_fields": dict(unknown_scenecfg),
        "components": dict(comp_counter),
        "unknown_component_fields": {f"{t}.{k}": c for (t, k), c in unknown_comp.items()},
        "variable_binding_keys": dict(var_binding_sites),
        "background": dict(background_counter),
        "constraints": dict(constraints_types),
    }
    with open(os.path.join(OUT, "analysis_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()