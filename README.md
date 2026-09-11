# MacroDroid Scene Builder (v20.3 · FR/EN/ES/DE/IT)

A single-file, offline, zero-dependency browser tool for building and editing **MacroDroid Scenes** (the JSON `sceneDescription` embedded in `CustomSceneAction` actions).

**Main file** — `v20/MacroDroid_Scene_Builder_v20.html` (self-contained HTML; JS + CSS inline, no network, no build step). The header reports `BUILDER_VERSION='v20.3'`, `BUILD_ID`, and `WORKSPACE_SCHEMA=1`. A ready-to-share copy is packaged as `v20/MacroDroid_Scene_Builder_v20.zip`.

**Repository layout**

```
README.md
LICENSE                                MIT License (WinnyKing57, 2026)
.github/                               issue & PR templates (see docs/CONTRIBUTING.md)
v19/MacroDroid_Scene_Builder_v19.zip   original forum release (kept unchanged for reference)
v20/MacroDroid_Scene_Builder_v20.html  current source of truth (build v20.3, edit this file)
v20/MacroDroid_Scene_Builder_v20.zip   v20.3 ready-to-share copy
macro-reference/                       real-scene corpus + collection/analysis scripts
docs/                                  research: feature_integration.md (roadmap), corpus_ANALYSE.md, corpus_DETAILS.md, CONTRIBUTING.md
```
- **Language**: **EN / FR / ES / DE / IT** via toolbar `langSelect` (EN is the source language, FR/ES/DE/IT are full localised copies); choice is persisted in `localStorage['sb_lang']`.
- **Theme**: Light / Dark via toolbar `themeSelect`; choice is persisted in `localStorage['sb_theme']` and applied before first paint (no flash).
- **Use**: open the `.html` directly in Chrome/Edge/Firefox (a Chromium browser is recommended for `showOpenFilePicker`/`showSaveFilePicker` support).

## Features

- **New Scene / Import** — create a Scene from scratch, or `OPEN` any `.macro` created on the phone and pick a Scene to work on.
- **Visual editor** — palette (drag & drop or double-click), tree, live preview, property editor, undo/redo, move/duplicate/delete (context menu), keyboard shortcuts.
- **Scene config** — FullScreen / Dialog / Overlay display mode (incl. nameRes identifier), background colour, background image (URI / STATIC_FILE access / display mode), content padding, sizing, orientation, scrolling, fonts.
- **Variables (new in v20)** — local & global variable manager (`VARIABLES` panel): add/rename/delete, view and edit current value, duplicate-name guard; usage tracking, reference rename and reference removal on delete.
  - **Set Variable on press** — bind a variable to buttons / images / icons / text (`{0..5}` typed bindings incl. Boolean / Integer / Decimal / String / Dictionary / Array with element key), and set a *New value*: `BooleanValue`, `IntValue`, `IntIncrement`, `IntDecrement`, `StringValue`, `ExpressionValue`.
- **Spacer (new in v20)** — `SceneSpacer` with height/width in dp.
- **Date picker (new in v20)** — calendar + standard `SceneDatePicker`, with a one-click converter between `sceneCalendarConfig` and `sceneDatePickerConfig`.
- **Close scene when touched** — `buttonClickConfig` toggle on buttons/images/icons/text (plus read-only `actionBlockName` note).
- **Save** — saves the whole opened macro (all Scenes + remaining logic), or `SAVE MACRO AS`.
- **Export Scene as macro** — minimal standalone `.macro` (`EmptyTrigger` + one `CustomSceneAction`) for direct MacroDroid testing; the Scene's referenced variables are automatically added as local/global variables.
- **Bundle (new in v20)** — `BUNDLE` downloads `<scene>_bundle.zip` containing the standalone `<scene>.macro` + `README.txt` (no-compression ZIP writer implemented inline).
- **PNG preview export (new in v20)** — `PNG` renders the current Scene preview (as displayed, zoom included) to a PNG: DOM tree cloned, computed styles inlined, serialized through an SVG `foreignObject` to `<canvas>`, then downloaded as `<scene>_preview.png`.
- **Integrity check (new in v20)** — `VALIDATE` scans the Scene for missing referenced variables, magic-text errors (unbalanced braces, empty/unknown tokens), duplicate non-zero GUIDs, Table column widths not totaling 100 %, out-of-range width/height percents and negative padding, with a severity report (errors/warnings/info) and a *COPY REPORT* action.
- **Multi-scene ZIP export (new in v20)** — `ZIP SCENES` exports every Scene of the macro as an individual standalone `.macro` (`scenes/01_Name.macro`) plus a PNG preview per Scene, the full original macro (import mode) and a `README.txt`, all in `<name>_scenes.zip`.
- **Tree search (new in v20)** — filter field above the tree: matches labels/types or any descendant; matching subtrees are auto-expanded and hits highlighted.
- **Selection & alignment (new in v20)** — Shift/Ctrl click selects several elements (tree + preview); the Properties panel then offers Align lefts/centers/rights, Equalize widths/heights/text size (per element, using each type's supported keys), and Distribute along a `SceneHorizontalLayout` row.
- **Preview zoom (new in v20)** — 50 %–400 % (`zoom` property, Chromium) via −/+/select in the toolbar.
- **Interaction simulation (new in v20)** — `Simulation` toggle: clicking pressable elements applies their Set-Variable (`BooleanValue`/toggle, `IntValue`, `IntIncrement`, `IntDecrement`, `StringValue`, `ExpressionValue`) or bound `booleanVariable` to the real variable objects, cycles dropdown/option rows, and flashes close-scene actions — without modifying the Scene (no undo, no dirty flag).
- **PROMPT** — copies LLM instructions + current `sceneDescription` JSON (see Help section 6; pairing with `macrodroid-llm-schema.yaml` and optional target `.macro`).
- **Help (translated)** — 8 sections in FR/EN, incl. bundle, LLM usage and Tools (PNG / VALIDATE / ZIP SCENES / zoom / simulation / selection & alignment).
- **MacroDroid system variables (new in v20.1)** — full official magic-text catalogue (~225 entries from the MacroDroid Wiki reference, cross-checked against the `macro-reference/` corpus) in the magic-text picker ("…" button): battery & power, location, Wi-Fi SSID, connectivity, volumes, device/system, memory & storage, date/time, macro context, trigger-specific tokens, plus parameterised utilities (`{size=Name}`, `{stopwatch=Name}`, `{setting_system=key}`, `{fbutton_x=Name}`…). Numeric-only tokens are offered for numeric fields; `VALIDATE` recognises the whole catalogue and the parameterised forms.
- **Autosave workspace** — the working Scene is persisted to IndexedDB and restored on reload; schema-versioned (`WS1`). **Snapshots (new in v20.2)** keep the 15 most recent workspace copies (IndexedDB), restorable from the start dialog or via `SNAPSHOTS`.
- **Languages (new in v20.2)** — toolbar language selector now offers **FR / ES / DE / IT** in addition to EN (the source language); the whole UI, magic-text group labels, variables panel and help are translated.
- **Validator click-through (new in v20.2)** — each `VALIDATE` report line that concerns a Scene element is clickable and jumps to that element: it is selected, the tree scrolls to its row and the preview highlights it.
- **Accessible text contrast (new in v20.2)** — `VALIDATE` now also reports elements whose text colour vs. background (or button) colour falls under the WCAG threshold (4.5:1 normal, 3:1 large text).
- **Drag & drop .macro (new in v20.2)** — drop a `.macro` / `.json` file anywhere on the Builder to open it.
- **Reusable snippets (new in v20.2)** — right-click an element in the preview → *Save as snippet* (a name is asked) stores it in `localStorage['sb_snippets']`; the toolbar `SNIPPETS` button lists saved snippets and inserts a deep copy (new GUID / icon resource) into the selected layout.
- **Magic-text everywhere & translated search (new in v20.3)** — the Progress Indicator now accepts magic text for `Min`, `Max` and `Value` (e.g. `{battery}` for a dynamic battery indicator); the magic-text picker is fully searchable, and its ~220 labels plus 34 group titles are translated into the active language (type *« heure »* to find the hour tokens in FR, *« ora »* in IT, etc.).
- **Structured property editor (new in v20.3)** — element properties are now grouped under readable sub-section headers (*Content / Style / Behaviour / Layout / Range…*, all translated) so fields no longer pile up on each other.
- **Feature roadmap (new)** — `docs/feature_integration.md` : prioritised research-based backlog (P0–P4) grounded in the MacroDroid wiki, app changelogs, the official forum « Scene - Feature Requests » thread and the `macro-reference/` corpus (component schema fields per type, binding inventory, display-option structures).

## Variable model

- New-macro mode keeps its own `draftVars { local, global }`; imported macros read variables from `macroJson`.
- Variables with MacroDroid value shapes: booleans (`m_type 0` + `m_booleanValue`), integers (`1` + `m_intValue`), decimals (`3` + `m_decimalValue`), strings, dictionaries/arrays (`4/5` + `dictionary:{entries,isArray,variableType,type}`).
- `buildNewMacroDocument()` exports only variables actually referenced by the Scene (`usedVariableNames()` via `{lv=Name}`/`{v=Name}` magic tokens and `object.varName` bindings).

## Testing

DOM-stub harnesses (Node, no browser required) live in `/tmp/opencode` during development:

- `harness_fr.js` — P0/P1 regression: i18n EN/FR, displayOption + background image editors.
- `harness_p2.js` — P2–P5: variable manager add/rename/delete/value, Set-variable editor, Spacer, DatePicker calendar conversion, ZIP structure (local header, central directory, EOCD), referenced-variable export, help FR, preview duplicate via dblclick.
- `harness_p6.js` — corpus round-trip: loads every file in `macro-reference/` (70 scene-using macros, 148 Scenes): `macroJson` unchanged after load, no crash, no real `sceneHash` collisions.
- `harness_p7.js` — P7 features: `buildSceneMacroDoc`/`usedVariableNamesFor` (referenced-variable export per Scene), validator checks (missing var, table widths, duplicate GUIDs, magic-text), simulation of `IntIncrement`/toggle, multi-element alignment ops, zoom clamping/steps, PNG-capture safety under DOM-less stubs.

Re-generate `/tmp/opencode/builder_v20_check.js` from the `.html` `<script>` before running.

## Known limitations

- Element types without a full property editor are preserved on save (read-only notice in the property panel).
- Copy operations are limited by the browser clipboard quota; above it, use `EXPORT SCENE AS MACRO` + file hand-off to an LLM.
- Font changes must be made in MacroDroid on the phone; the preview uses Roboto preference.

## License

Distributed under the **MIT License** — see `LICENSE`. To contribute (branches + pull requests,
merge on `main` by the owner), see `docs/CONTRIBUTING.md`.