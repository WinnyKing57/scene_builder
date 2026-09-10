# macro-reference — corpus de scènes MacroDroid réelles

Corpus de **fichiers `.macro`** contenant des **Custom Scenes**, récupéré pour comprendre la
structure réelle des scènes et la façon dont MacroDroid échange avec elles avant d'étendre le
**Scene Builder** (v19 → v20).

## Contenu

| Élément | Détail |
|---|---|
| **70 macros** | 68 via l'API Template Store (`templates.macrodroid.com`), 1 tuto wiki (`Quick_Actions_Menu.macro`), 1 cible de référence (`Infinite_Clipboard_23587.macro`). |
| **~141 scènes** | 63 FullScreen · 53 Dialog · 25 Overlay |
| ~10,7 Mo | 69 fichiers ± + ANALYSE.md, DETAILS.md, analysis_summary.json, manifest.json |
| Manifest | `manifest.json` : id, nom, fichier, URL (API + page), nombre d'actions de scène. |

Sources principales : Template Store (templates.macrodroid.com) et wiki. Les attachments du
forum (macrodroidforum.com) sont en **403 sans compte**, mais les fils y pointent presque
toujours vers le Template Store (`macrodroidlink.com/macrostore?id=…`).

### Scripts (reproductibles)
- `collect_macros.py` — recherche ciblée (mots-clés scène/overlay/menu…) + détection
  `sceneDescription`, sauvegarde les `.macro`.
- `expand_collection.py` — IDs repérés sur le forum + balayage paginé.
- `term_expand.py` — balayage par nombreux termes (crash-safe, manifest incrémental).
- `analyze.py` → `ANALYSE.md` + `analysis_summary.json` (statistiques agrégées).
- `deepdive.py` → `DETAILS.md` (structures complètes représentatives).

## Format d'un fichier `.macro`

Deux formes existent :

```jsonc
// 1) Export MacroDroid (wiki / app) :
{ "macroExportVersion": 1,
  "macro": { "m_GUID": 0, "m_name": "…", "m_actionList": [ … ], "localVariables": [ … ],
             "globalVariables" : non inclus pour .macro, "exportedActionBlocks": [ … ], … } }

// 2) Store (champ "json" décodé) : directement l'objet `macro` interne (pas de wrapper).
```

Le builder v19 attend la **forme 1** (`{globalVariables, macro:{…}, macroExportVersion}`) :
les fichiers `*.macro` de ce dossier contiennent l'objet interne du store — **il faut les
re-wrap** avant de les importer dans le builder (utile pour les tests de round-trip).

## Où vivent les scènes

Dans `macro.m_actionList[]`, chaque action a :
```jsonc
{ "m_classType": "CustomSceneAction",
  "sceneDescription": { "itemList": { "items": [ … ] }, "sceneConfig": { … } },
  "m_constraintList": [ … ], "m_comment": …, "m_SIGUID": 0, "disableLogging": false }
```

## Modèle d'interaction app ↔ scène (ce que le builder doit reproduire/préserver)

### sceneConfig (toutes les scènes)
- `backgroundColor`, `foregroundColor`, `name`, `blockNextActions`, `dismissOnBackPress`,
  `updateValuesOnSceneClose`, `dismissOnHomeTaskSwitch`, `closeOnBackgroundTouch`,
  `contentPadding`, `roundedCornerAmount`, `showOnLockScreen` — déjà connus du builder.
- **`displayOption`** (objet) :
  - `{"type":"FullScreen", "nameRes": 2132021408}`
  - `{"type":"Dialog", "closeOnOutsideTouch": false, "nameRes": …}`
  - `{"type":"Overlay", drawOverSystemApps, preventRemovalByBin, showPositionOnMove,
    longPressToMove, overlayStatusBar, widthOption, widthValue, heightOption, heightValue,
    xValue, yValue, nameRes}` — valeurs en **% sous forme de chaînes** (ex. `"100"`, `"50"`).
  - `nameRes` : id de ressource interne (champ opaque) → **préserver**, générer pour les nouvelles scènes.
- **`backgroundImageDisplayMode`** — `"CENTER_CROP"` (97 scènes), même sans image. Autre
  valeur possible ? (surtout présent avec fond couleur). Non géré par v19.

### Background image (4 cas)
```jsonc
"backgroundImage": { "type": "STATIC_FILE",
                     "imageUri": "content://com.android.externalstorage.documents/document/…",
                     "useAllFilesAccess": false },
"backgroundImageDisplayMode": "CENTER_CROP"
```
Types possibles à sécuriser : `STATIC_FILE` (imageUri), vraisemblablement `THIRD_PARTY_APP`,
`GIPHY`, `/EMBEDDED_BASE64` selon les items (à vérifier pour SceneImage).

### Bindings de variables (cœur de l'interaction)
Chaque composant peut **lire** (afficher) et/ou **écrire** une variable, via des
objets `{"varName": "…"}` et des descripteurs « Set Variable » `{"type": …}` :
- `variableUpdateValue` (affichage/déclencheur) : `None` | `StringValue{label}` |
  `IntValue{label}` | `IntIncrement{}` | `IntDecrement{}` | `BooleanValue{isToggle,label}` |
  `ExpressionValue{label}` (magic text, ex. `"{lv=cont[0]}-ceiling(sin({lv=cont[0]}))"`).
- `variableToUpdate` / `stringVariable` / `booleanVariable` / `numberVariable` /
  `arrayVariable` / `dictionaryVariable` / `keyOutputVariable` — cibles d'écriture
  `varName` (+ `dictionaryKeys.keys[]` pour le tirage dict/array).
- `visibilityVariable {varName}` — affiche/masque l'item (sur beaucoup de composants).
- `enabledVariable`, `bindToVariable` (SceneSlider), `onlySetVariableWhenValueChanged`.

→ Pour une **nouvelle scène sans macro parente**, ces `varName` doivent être **collectés
et déclarés** dans `macro.localVariables` à l'export (le builder v19 ne le fait pas :
l'inventaire est vide).

### Composants & gaps vs builder v19
- Types présents : SceneText, Button, Switch, CheckBox, Slider, ProgressIndicator,
  EditText, DropDownSelection, OptionSelector, Date/TimePicker, WebView, MapView
  (absent du corpus), Image, Icon, Divider, layouts H/V/Grid/Table/Pager, **SceneSpacer**.
- **SceneSpacer** : `{type, sceneSpacerConfig:{heightDp,widthDp}, guid, iconRes, …}` — absent du builder.
- **SceneDatePicker** réel : `sceneCalendarConfig` (pas `sceneDatePickerConfig`) + `dictionaryVariable` → à prendre en compte.
- **Champs quasi-systématiques, inconnus du builder** (à préserver, pas à réécrire) :
  `guid` (toujours **négatif** en réel, ex. `-7634687123121573313` — jamais 0), `iconRes`
  (id de ressource), `lastRefreshValue` (cache d'évaluation), `iconResId`, `uniqueId`.
  → le builder doit **générer des guid négatifs** pour ses nouveaux items (pas `0`), et ne
  jamais détruire `iconRes`/`lastRefreshValue` à l'édition.
- **Boutons** : `sceneButtonConfig.buttonClickConfig` (présent dans les 375 boutons) =
  `{"actionBlockData": {actionBlockGuid, actionBlockName, inputVarsMap, inputDictionaryMap,
  outputVarsMap, outputDictionaryMap}, "closeScene": false}`. Autres formes possibles :
  action directe, set variable → à inventorier (ex. macro YouTube : fermeture de scène).

### Échanges au runtime (sémantique à refléter dans l'aide/preview)
- `blockNextActions` → la macro attend la fermeture de la scène.
- `updateValuesOnSceneClose` → relecture des magic text à la fermeture.
- `closeOnOutsideTouch` / `closeOnBackgroundTouch` / `dismissOnBackPress` / `longPressToMove`.
- Magic text partout (ex. `textSize: "{lv=FontSizes[1]}"`, `text: "♾️+Infinite+Clipboard+📋"`).

## Voir aussi
- `ANALYSE.md` — stats agrégées (composants, displayOption, champs, bindings, constraints).
- `DETAILS.md` — structures JSON complètes représentatives (Overlay, bindings, background, clicks).
- `analysis_summary.json` — données brutes pour le builder.
- `archive/MacroDroid_Scene_Builder_v19.html` — l'app à étendre.