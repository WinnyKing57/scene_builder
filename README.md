# MacroDroid Scene Builder (v20 · FR/EN)

A single-file, offline, zero-dependency browser tool for building and editing **MacroDroid Scenes** (the JSON `sceneDescription` embedded in `CustomSceneAction` actions).

- **File**: `archive/MacroDroid_Scene_Builder_v19.html` (self-contained HTML; JS + CSS inline, no network, no build step). The header reports `BUILDER_VERSION='v20'`, `BUILD_ID`, and `WORKSPACE_SCHEMA=1`.
- **Language**: bilingual FR (« français ») / EN via toolbar `langSelect`; choice is persisted in `localStorage['sb_lang']`.
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
- **PROMPT** — copies LLM instructions + current `sceneDescription` JSON (see Help section 6; pairing with `macrodroid-llm-schema.yaml` and optional target `.macro`).
- **Help (translated)** — 7 sections in FR/EN, incl. bundle and LLM usage.
- **Autosave workspace** — the working Scene is persisted to IndexedDB and restored on reload; schema-versioned (`WS1`).

## Variable model

- New-macro mode keeps its own `draftVars { local, global }`; imported macros read variables from `macroJson`.
- Variables with MacroDroid value shapes: booleans (`m_type 0` + `m_booleanValue`), integers (`1` + `m_intValue`), decimals (`3` + `m_decimalValue`), strings, dictionaries/arrays (`4/5` + `dictionary:{entries,isArray,variableType,type}`).
- `buildNewMacroDocument()` exports only variables actually referenced by the Scene (`usedVariableNames()` via `{lv=Name}`/`{v=Name}` magic tokens and `object.varName` bindings).

## Testing

DOM-stub harnesses (Node, no browser required) live in `/tmp/opencode` during development:

- `harness_fr.js` — P0/P1 regression: i18n EN/FR, displayOption + background image editors.
- `harness_p2.js` — P2–P5: variable manager add/rename/delete/value, Set-variable editor, Spacer, DatePicker calendar conversion, ZIP structure (local header, central directory, EOCD), referenced-variable export, help FR, preview duplicate via dblclick.
- `harness_p6.js` — corpus round-trip: loads every file in `macro-reference/` (70 scene-using macros, 148 Scenes): `macroJson` unchanged after load, no crash, no real `sceneHash` collisions.

Re-generate `/tmp/opencode/builder_v20_check.js` from the `.html` `<script>` before running.

## Known limitations

- Element types without a full property editor are preserved on save (read-only notice in the property panel).
- Copy operations are limited by the browser clipboard quota; above it, use `EXPORT SCENE AS MACRO` + file hand-off to an LLM.
- Font changes must be made in MacroDroid on the phone; the preview uses Roboto preference.