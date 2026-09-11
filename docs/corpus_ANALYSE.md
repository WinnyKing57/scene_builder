# ANALYSE — corpus des scenes réelles

Macros analysés : `70` (fichiers dans ce dossier, source Template Store + wiki).

## 1. Composants utilisés

| type | occurrences |
|---|---|
| SceneText | 548 |
| SceneButton | 375 |
| SceneHorizontalDivider | 132 |
| SceneEditText | 122 |
| SceneSwitch | 118 |
| SceneHorizontalLayout | 108 |
| SceneIcon | 90 |
| SceneGridLayout | 62 |
| SceneSlider | 50 |
| SceneWebView | 49 |
| SceneHorizontalPager | 45 |
| SceneCheckBox | 31 |
| SceneProgressIndicator | 25 |
| SceneDropDownSelection | 25 |
| SceneImage | 13 |
| SceneVerticalLayout | 11 |
| SceneTableLayout | 5 |
| SceneTimePicker | 3 |
| SceneOptionSelector | 2 |
| SceneSpacer | 1 |
| SceneDatePicker | 1 |

## 2. displayOption (mode d'affichage)

| mode | scènes |
|---|---|
| `FullScreen` | 63 |
| `Dialog` | 53 |
| `Overlay` | 25 |

Exemples réels :
- `Overlay` — 15180__youtube_skip_ads.macro (Spinner+2) : `{"type": "Overlay", "drawOverSystemApps": false, "heightOption": 1, "heightValue": "100", "longPressToMove": false, "overlayStatusBar": true, "prevent…`
- `Overlay` — 25011__macrodroid_voice_assistant_r2d2.macro (radarPopUp+2) : `{"type": "Overlay", "drawOverSystemApps": false, "heightOption": 1, "heightValue": "73", "longPressToMove": true, "overlayStatusBar": false, "preventR…`
- `Dialog` — 19708__handycalculator.macro (NumKbd+2) : `{"type": "Dialog", "closeOnOutsideTouch": false, "nameRes": 2132021906}`
- `Dialog` — 23155__park_suite_classic_menu.macro (Wait+2) : `{"type": "Dialog", "closeOnOutsideTouch": false, "nameRes": 2132021407}`
- `FullScreen` — 23587__infinite_clipboard.macro (infiniteClipboardPopup+2) : `{"type": "FullScreen", "nameRes": 2132021408}`
- `FullScreen` — 23713__categories_for_macrodroid_drawer_macro_launcher.macro (selectionMenu+2) : `{"type": "FullScreen", "nameRes": 2132021408}`

## 3. Champs sceneConfig utilisés

| clé | scènes |
|---|---|
| `backgroundColor` | 141 |
| `blockNextActions` | 141 |
| `dismissOnBackPress` | 141 |
| `displayOption` | 141 |
| `foregroundColor` | 141 |
| `name` | 141 |
| `updateValuesOnSceneClose` | 141 |
| `roundedCornerAmount` | 117 |
| `showOnLockScreen` | 115 |
| `backgroundImageDisplayMode` | 97 ⚠️ inconnu du builder |
| `dismissOnHomeTaskSwitch` | 94 |
| `closeOnBackgroundTouch` | 54 |
| `contentPadding` | 23 |
| `backgroundImage` | 4 ⚠️ inconnu du builder |

### Champs sceneConfig non gérés par le builder v19
- `backgroundImageDisplayMode` ×97 (ex: Quick_Actions_Menu_wiki.macro 'Quick Actions' → "CENTER_CROP")
- `backgroundImage` ×4 (ex: 30978__fahhh.macro 'cat_meme+2' → {"imageUri": "content://com.android.providers.downloads.documents/document/msf%3A25241", "type": "STATIC_FILE", "useAllFilesAccess": false})

## 4. Champs de composants non gérés par le builder v19

- `SceneText.iconRes` ×548
- `SceneText.lastRefreshValue` ×510
- `SceneButton.iconRes` ×375
- `SceneButton.lastRefreshValue` ×348
- `SceneHorizontalDivider.iconRes` ×132
- `SceneHorizontalDivider.lastRefreshValue` ×132
- `SceneEditText.iconRes` ×122
- `SceneEditText.lastRefreshValue` ×119
- `SceneSwitch.iconRes` ×118
- `SceneSwitch.lastRefreshValue` ×116
- `SceneHorizontalLayout.iconResId` ×108
- `SceneHorizontalLayout.iconRes` ×108
- `SceneHorizontalLayout.lastRefreshValue` ×105
- `SceneIcon.iconRes` ×90
- `SceneIcon.lastRefreshValue` ×88
- `SceneGridLayout.iconResId` ×62
- `SceneGridLayout.iconRes` ×62
- `SceneText.uniqueId` ×61
- `SceneGridLayout.lastRefreshValue` ×58
- `SceneSlider.iconRes` ×50
- `SceneWebView.iconRes` ×49
- `SceneWebView.lastRefreshValue` ×49
- `SceneHorizontalPager.iconResId` ×45
- `SceneHorizontalPager.iconRes` ×45
- `SceneHorizontalPager.lastRefreshValue` ×45
- `SceneSlider.lastRefreshValue` ×45
- `SceneButton.uniqueId` ×39
- `SceneCheckBox.iconRes` ×31
- `SceneCheckBox.lastRefreshValue` ×26
- `SceneProgressIndicator.iconRes` ×25
- `SceneDropDownSelection.uniqueId` ×25
- `SceneDropDownSelection.iconRes` ×25
- `SceneProgressIndicator.lastRefreshValue` ×21
- `SceneDropDownSelection.lastRefreshValue` ×19
- `SceneImage.iconRes` ×13
- `SceneVerticalLayout.iconResId` ×11
- `SceneVerticalLayout.iconRes` ×11
- `SceneVerticalLayout.lastRefreshValue` ×11
- `SceneImage.uniqueId` ×10
- `SceneIcon.uniqueId` ×10
- `SceneImage.lastRefreshValue` ×10
- `SceneHorizontalLayout.id` ×7
- `SceneHorizontalLayout.uniqueId` ×7
- `SceneSlider.uniqueId` ×6
- `SceneTableLayout.iconResId` ×5
- `SceneTableLayout.iconRes` ×5
- `SceneTableLayout.lastRefreshValue` ×5
- `SceneCheckBox.uniqueId` ×5
- `SceneGridLayout.id` ×4
- `SceneGridLayout.uniqueId` ×4
- `SceneProgressIndicator.uniqueId` ×4
- `SceneEditText.uniqueId` ×3
- `SceneTimePicker.iconRes` ×3
- `SceneTimePicker.lastRefreshValue` ×3
- `SceneSwitch.uniqueId` ×2
- `SceneOptionSelector.uniqueId` ×2
- `SceneOptionSelector.iconRes` ×2
- `SceneOptionSelector.lastRefreshValue` ×2
- `SceneGridLayout.isEditMode` ×1
- `SceneHorizontalLayout.isEditMode` ×1
- `SceneDatePicker.sceneCalendarConfig` ×1
- `SceneDatePicker.iconRes` ×1
- `SceneDatePicker.lastRefreshValue` ×1

## 5. Bindings variables / magic text

Sites de binding détectés (clés dont le nom ou la valeur référence une variable) :
- `variableUpdateValue` ×587
- `variableToUpdate` ×290
- `visibilityVariable` ×243
- `booleanVariable` ×143
- `stringVariable` ×121
- `numberVariable` ×41
- `arrayVariable` ×27
- `stringOutputVariable` ×23
- `keyOutputVariable` ×22
- `onlySetVariableWhenValueChanged` ×16
- `bindToVariable` ×9
- `enabledVariable` ×5
- `dictionaryVariable` ×3
- `text` ×1

## 6. Background

- bgImageDisplayMode:CENTER_CROP ×93
- backgroundImage/image ×4

## 7. Constraints de l'action CustomSceneAction

- `MacroDroidVariableConstraint` ×12
- `TriggerThatInvokedConstraint` ×4
- `CustomSceneConstraint` ×3
- `ScreenOnOffConstraint` ×2
- `DarkThemeConstraint` ×2
- `LogicConstraint` ×1

## 8. Boutons / click config

Exemple `SceneButton.sceneButtonConfig.buttonClickConfig` (19708__handycalculator.macro guid=-7634687123121573313) :
```json
{"actionBlockData": {"actionBlockGuid": -7600351054461526861, "actionBlockName": "NumKbd", "inputDictionaryMap": {}, "inputVarsMap": {"Kpressed": "1", "InputStr": "{lv=Expression}"}, "outputDictionaryMap": {}, "outputVar…
```
