# DETAILS — structures réelles (interaction app ↔ scène)

## Overlay — structure complète

```json
{
 "type": "Overlay",
 "drawOverSystemApps": false,
 "heightOption": 1,
 "heightValue": "100",
 "longPressToMove": false,
 "overlayStatusBar": true,
 "preventRemovalByBin": true,
 "showPositionOnMove": false,
 "widthOption": 0,
 "widthValue": "100",
 "xValue": "50",
 "yValue": "50",
 "nameRes": 2132021908
}
```
*— 15180__youtube_skip_ads.macro, scène 'Spinner+2'*

```json
{
 "type": "Overlay",
 "drawOverSystemApps": false,
 "heightOption": 1,
 "heightValue": "73",
 "longPressToMove": true,
 "overlayStatusBar": false,
 "preventRemovalByBin": false,
 "widthOption": 1,
 "widthValue": "75",
 "xValue": "100",
 "yValue": "0",
 "nameRes": 2132021409
}
```
*— 25011__macrodroid_voice_assistant_r2d2.macro, scène 'radarPopUp+2'*

```json
{
 "type": "Overlay",
 "heightOption": 1,
 "heightValue": "30",
 "longPressToMove": true,
 "overlayStatusBar": true,
 "preventRemovalByBin": false,
 "widthOption": 1,
 "widthValue": "100",
 "xValue": "100",
 "yValue": "0",
 "nameRes": 2132021428
}
```
*— 26440__youtube_popup_window.macro, scène 'youTubePopUp+2'*

Overlay total: 19

## Structures de binding de variables

### `variableToUpdate`

Exemple (19708__handycalculator.macro, scène 'NumKbd+2') :
```json
{"varName": "Button"}
```

### `variableUpdateValue`

Exemple (19708__handycalculator.macro, scène 'NumKbd+2') :
```json
{"type": "None"}
```

### `visibilityVariable`

Exemple (23587__infinite_clipboard.macro, scène 'infiniteClipboardPopup+2') :
```json
{"varName": "shwPgBtton938"}
```

### `booleanVariable`

Exemple (23587__infinite_clipboard.macro, scène 'infiniteClipboardPopup+2') :
```json
{"varName": "pausLggr268"}
```

### `stringVariable`

Exemple (19708__handycalculator.macro, scène 'NumKbd+2') :
```json
{"varName": "Expression"}
```

### `numberVariable`

Exemple (23587__infinite_clipboard.macro, scène 'infiniteClipboardPopup+2') :
```json
{"varName": "fntSzInt738"}
```

### `dictionaryVariable`

(aucun exemple dans le corpus)

### `bindToVariable`

Exemple (30447__adb_scripts_gui_on_off_switches.macro, scène 'ADB+Scripts+2') :
```json
true
```

## Background — structure complète (cases avec image)

### 29446__fbi_security.macro — 'FBI++2'

```json
{
 "backgroundImage": {
  "imageUri": "content://com.android.externalstorage.documents/document/primary%3AAIRetouch_20260317_042858744.png",
  "type": "STATIC_FILE",
  "useAllFilesAccess": false
 },
 "backgroundImageDisplayMode": "CENTER_CROP"
}
```

### 30447__adb_scripts_gui_on_off_switches.macro — 'ADB+Scripts+2'

```json
{
 "backgroundImage": {
  "imageUri": "content://ru.zdevs.zarchiver.external/storage/emulated/0/Pictures/100PINT/Pins/8fc76279253716167586df446571b731.jpg",
  "type": "STATIC_FILE",
  "useAllFilesAccess": false
 },
 "backgroundImageDisplayMode": "CENTER_CROP"
}
```

### 30978__fahhh.macro — 'cat_meme+2'

```json
{
 "backgroundImage": {
  "imageUri": "content://com.android.providers.downloads.documents/document/msf%3A25241",
  "type": "STATIC_FILE",
  "useAllFilesAccess": false
 },
 "backgroundImageDisplayMode": "CENTER_CROP"
}
```

## SceneSpacer (composant inconnu du builder)

## ButtonClickConfig — structure complète

### 19708__handycalculator.macro — guid -7634687123121573313

```json
{
 "actionBlockData": {
  "actionBlockGuid": -7600351054461526861,
  "actionBlockName": "NumKbd",
  "inputDictionaryMap": {},
  "inputVarsMap": {
   "Kpressed": "1",
   "InputStr": "{lv=Expression}"
  },
  "outputDictionaryMap": {},
  "outputVarsMap": {
   "OutputStr": "Dsply"
  }
 },
 "closeScene": false
}
```

### 19708__handycalculator.macro — guid -7993875981405281671

```json
{
 "actionBlockData": {
  "actionBlockGuid": -7600351054461526861,
  "actionBlockName": "NumKbd",
  "inputDictionaryMap": {},
  "inputVarsMap": {
   "Kpressed": "2",
   "InputStr": "{lv=Expression}"
  },
  "outputDictionaryMap": {},
  "outputVarsMap": {
   "OutputStr": "Dsply"
  }
 },
 "closeScene": false
}
```

### 19708__handycalculator.macro — guid -4736563928815094930

```json
{
 "actionBlockData": {
  "actionBlockGuid": -7600351054461526861,
  "actionBlockName": "NumKbd",
  "inputDictionaryMap": {},
  "inputVarsMap": {
   "Kpressed": "3",
   "InputStr": "{lv=Expression}"
  },
  "outputDictionaryMap": {},
  "outputVarsMap": {
   "OutputStr": "Dsply"
  }
 },
 "closeScene": false
}
```

## GUID & iconRes

`guid` distribution : {'neg': 1560}
`iconRes` distribution : {'nonzero': 1560}
`uniqueId` distribution : {'id-like': 155}

## SceneText — champs avancés (auto refresh / magic text)

```json
{
 "autoSizeText": false,
 "closeSceneOnPress": false,
 "enableAutoRefresh": false,
 "enableSelection": false,
 "htmlFormatting": false,
 "isBold": false,
 "isItalic": false,
 "maxLines": "3",
 "maxLinesEnabled": false,
 "padding": "8",
 "text": "Skipping+Ads",
 "textAlignment": "Center",
 "textColor": -1,
 "textSize": "20"
}
```
*— 15180__youtube_skip_ads.macro*

```json
{
 "autoSizeText": false,
 "enableAutoRefresh": false,
 "enableSelection": false,
 "fontFamily": "Roboto+(System)",
 "htmlFormatting": false,
 "isBold": false,
 "isItalic": false,
 "maxLinesEnabled": false,
 "text": "Please+wait!",
 "textAlignment": "Center",
 "textColor": -16777216,
 "textSize": "20"
}
```
*— 23155__park_suite_classic_menu.macro*

```json
{
 "autoSizeText": false,
 "enableAutoRefresh": false,
 "enableSelection": false,
 "htmlFormatting": false,
 "isBold": false,
 "isItalic": false,
 "maxLines": "3",
 "maxLinesEnabled": false,
 "text": "♾️+Infinite+Clipboard+📋",
 "textAlignment": "Center",
 "textColor": -1,
 "textSize": "20"
}
```
*— 23587__infinite_clipboard.macro*

```json
{
 "autoSizeText": false,
 "enableAutoRefresh": false,
 "enableSelection": false,
 "htmlFormatting": false,
 "isBold": false,
 "isItalic": false,
 "maxLines": "3",
 "maxLinesEnabled": false,
 "text": "",
 "textAlignment": "Start",
 "textColor": -1,
 "textSize": "10",
 "visibilityVariable": {
  "varName": "shwSpcr841"
 }
}
```
*— 23587__infinite_clipboard.macro*

## Variables locales dans les macros à scène

- 15180__youtube_skip_ads.macro : 1 vars — ['current_vol_music']
- 19708__handycalculator.macro : 18 vars — ['Button', 'Compatibility', 'Expression', 'Henabled', 'History', 'LastExpr', 'Result', 'Rounding']
- 23155__park_suite_classic_menu.macro : 15 vars — ['Geocoding_Homecountry', 'Geocoding_Language', 'Geocoding_AdditionalInfo', 'file_path', 'parking', 'parking_confirm', 'parking_select', 'parking_showmap']
- 23587__infinite_clipboard.macro : 70 vars — ['slctedItm2x345', 'notCntntStrng482', 'pindNotArry537', 'pindNotStrng824', 'pindNotArry2x372', 'notCntntArry835', 'pindNotEntry837', 'nwNotEntryIndx472']
- 23713__categories_for_macrodroid_drawer_macro_launcher.macro : 34 vars — ['sceneIndicator', 'selectedItem', 'macroListString', 'newListOrder', 'updatedCatList', 'selectableItemsJSON', 'buildNewDict', 'categories']
- 23713__categories_for_macrodroid_drawer_macro_launcher.macro : 34 vars — ['sceneIndicator', 'selectedItem', 'macroListString', 'newListOrder', 'updatedCatList', 'selectableItemsJSON', 'buildNewDict', 'categories']
- 23713__categories_for_macrodroid_drawer_macro_launcher.macro : 34 vars — ['sceneIndicator', 'selectedItem', 'macroListString', 'newListOrder', 'updatedCatList', 'selectableItemsJSON', 'buildNewDict', 'categories']
- 25011__macrodroid_voice_assistant_r2d2.macro : 43 vars — ['input', 'content', 'loopCount', 'macroList', 'currentNotVolume', 'musicPath', 'videoPath', 'smsMessage']
- 25011__macrodroid_voice_assistant_r2d2.macro : 43 vars — ['input', 'content', 'loopCount', 'macroList', 'currentNotVolume', 'musicPath', 'videoPath', 'smsMessage']
- 25011__macrodroid_voice_assistant_r2d2.macro : 43 vars — ['input', 'content', 'loopCount', 'macroList', 'currentNotVolume', 'musicPath', 'videoPath', 'smsMessage']
- 25184__realtime_password_generator_demo_for_custom_scene.macro : 7 vars — ['result', 'use_uppercase', 'use_lowercase', 'use_numbers', 'use_symbols', 'password_length', 'random']
- 25190__rae_ai_custom_scene_demo.macro : 1 vars — ['contents']
