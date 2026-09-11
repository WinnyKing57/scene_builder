# Feature Integration — Roadmap du Scene Builder (v20.1+)

> Dossier de travail : `docs/` (le corpus brut reste dans `macro-reference/`).
> Analyse approfondie : wiki officiel MacroDroid (Magic Text, Custom Scenes, Action:
> Display Custom Scene, MacroDroid Drawer), changelogs de l'application (v5.54 → v5.66.x),
> fil forum officiel « Scene - Feature Requests » (toutes pages #1–#237 lues),
 et corpus réel `macro-reference/` (71 macros, 140 scènes).

> **Politique du repo — zéro invention de schéma** : toute clé JSON écrite doit avoir été
> vue dans un `.macro` produit par l'app. Les § marqués « ✅ corpus » sont vérifiés ; les §
> marqués « ⚠️ capture » exigent d'abord d'exporter un `.macro` de référence depuis l'app.

---

## 1. État des lieux — ce que le builder v20.1 fait déjà

Points d'ancrage (lignes v20.1) :

| Index | Fonctions |
|---|---|
| Picker magic text menu complet (~225 tokens, groupes, numériques, paramétrés) | `MAGIC_TEXT_OPTIONS` (719), `NUMERIC_MAGIC_TOKENS` (1808), `checkString` (2588) |
| Pickers variables typés (Local/Global/Special, tous types) | `openMagicTextPicker` (1828), `openTypedVariablePicker` (1837) |
| Éditeur « Set Variable on press » (BooleanValue/toggle, Int±, StringValue, ExpressionValue, dict/array) | `renderVariableUpdateEditor` (1858) |
| Gestion variables + renommage propagé | `openVariablesPanel` (1887), `renameVariableDialog` (1955) |
| Display mode FullScreen/Dialog/Overlay complet (incl. nameRes, width/height option 0/1/2 = match/percent/wrap, X/Y %, flags overlay) | `renderDisplayOptionEditor` (2033) |
| Fond : couleur + image STATIC_FILE + display mode CENTER_CROP/FILL_BOUNDS | `renderBackgroundEditor` (2058) |
| Scène : name, blockNextActions, couleurs, lock screen, close on back/home/touch, padding, update-on-close | `renderSceneProperties` (2077) |
| Layouts H/V/Grid/Table + colonnes normalisées (%) + **repetition dynamique (UI)** | `renderHorizontalLayoutProperties` (2158), `renderVerticalLayoutProperties` (2132), `renderGridLayoutProperties` (2135), `renderTableLayoutProperties` (2138), `renderColumnWidths` (2120), `renderRepeatProperties` (2126) |
| Pager/Tabs (tabs, scrollable, defaultTabIndex, visibility/enabled par onglet) | `renderTabLayoutProperties` (2161) |
| DropDown (type `useKeys`, output string, output key, only-set-on-change) | `renderDropDownProperties` (2141) |
| Selectable List / OptionSelector (options, multiSelect, array source) | `renderSelectableListProperties` (2144) |
| DatePicker standard + calendrier (`sceneCalendarConfig`/`sceneDatePickerConfig` + convertisseur) | `renderDatePickerProperties` (2148), `pickDatePickerConfig` (2147) |
| MapView (bind lat/lon/zoom, markers array, tapped-marker) | `renderMapViewProperties` (2155) |
| Tous les composants restants | `renderItemProperties` (2168) |
| Export macro/BUNDLE/ZIP/PNG, VALIDATE, preview, simulateur, multi-sélection/alignement, recherche | README.md |
| Constante réservée (booléen `BUILDER_ALWAYS_FALSE_VAR`) | `ensureBuilderConstantVariables` (2272), `buildNewMacroDocument` (2316) |

---

## 2. Chronologie des versions scène (app) — sources du backlog

| Version (date) | Apports scenes |
|---|---|
| **v5.54** (juin 2025) | Horizontal Divider ; slider « clic sur la valeur → saisie » ; Password Text Entry ; split alignment Switch/Checkbox ; **coins arrondis scène (dialog/overlay)** ; labels valeur slider début/fin/aucun ; step size slider ; Text size en magic text ; Text HTML ; Text max lines + **scale to fit** ; visibilité liée à une variable booléenne (tous items) ; Switch couleurs texte/on/off séparées ; Button toggle booléen |
| **v5.54.9** (juin 2025) | Option de transparence ; scènes sur écran de verrouillage |
| **v5.63.11** (avril 2026) | **MacroDroid Drawer multi-scènes** ; trigger « Custom Scene Shown/Dismissed » ; **Scene Button/Icon/Image → actions individuelles au clic** ; Camera In Use, Mic Recording, Shizuku Stopped, App Enabled/Disabled |
| **v5.65.9** (juillet 2026) | **Répétition dynamique des composants dans les conteneurs (array/dictionary)** ; Remote Control ; Webhook 2-way ; push macro depuis le Template Store web |
| **v5.66.x** (2026-08/09) | Bug « scale-to-fit + HTML » rapporté (#230) ; demandes WebView URL→variable (#234) |

---

## 3. P0 — Conformité schema (priorité absolue)

### P0-1 · ❗ Correction : OptionSelector / Selectable List — variables de sortie ⚠️
- **Corpus (source de vérité)** : les OptionSelector réels n'ont **jamais** `selectedIndexVariable`
  ni `selectedIndicesVariable` (0 occurrence). Les clés réelles sont :
  `arrayVariable`, `keyOutputVariable`, `multiSelect`, `onlySetVariableWhenValueChanged`,
  `showBorder`, `borderColor`, `useKeys`.
- **Builder actuel** : `renderSelectableListProperties` (2144) écrit et initialise
  `selectedIndicesVariable` (array) / `selectedIndexVariable` (int) — schéma **non validé**.
- **Action** : (1) capturer un `.macro` avec OptionSelector en single ET en multi ;
  (2) corriger les champs de sortie selon le corpus ;
  (3) ajouter les éditeurs manquants : `showBorder`, `borderColor`,
  `onlySetVariableWhenValueChanged` ; (4) traiter `keyOutputVariable` en sortie (string).
- **Impact** : sans correction, la variable choisie par l'utilisateur peut ne jamais être
  écrite par l'app.

### P0-2 · Coins arrondis de scène — `sceneConfig.roundedCornerAmount` ✅ corpus
- **Corpus** : `roundedCornerAmount` présent sur **117/140 scènes** (ex. `8`) — le builder a la
  valeur par défaut (`roundedCornerAmount:0`, ligne 1222) mais **aucun éditeur**.
- **Action** : dans `renderSceneProperties` (2077-2090), après les couleurs, ajouter
  `field('Rounded corners (dp)', c.roundedCornerAmount??0, v=>c.roundedCornerAmount=v, {type:'number',number:true,min:0,max:100})`.
  Refléter en CSS sur le preview (shell Dialog/Overlay → `border-radius`).
- **Validation** : round-trip corpus (aucun `.macro` altéré) + preview visuel.

### P0-3 · « Scale to fit » texte — `sceneTextConfig.autoSizeText` ✅ corpus
- **Corpus** : `autoSizeText` dans la quasi-totalité des SceneText (ex. `false`) ; changelog v5.54
  (« scale to fit ») ; demande forum #24 (Endercraft) précisément cette option.
- **Builder** : `autoSizeText` présent dans la valeur par défaut (ligne 1227) mais **pas d'éditeur**.
- **Action** : dans le bloc SceneText (2173-2177), après « Limit number of lines »,
  `check('Scale to fit', !!c.autoSizeText, v=>c.autoSizeText=v)`.
  ⚠️ Bug connu app (forum #230, juil. 2026) : « scale to fit » + `htmlFormatting` = le HTML
  ne se rend pas → côté UI : désactiver `htmlFormatting` quand `autoSizeText` est coché.
- **Validation** : round-trip + VALIDATE silencieux + note dans l'aide.

### P0-4 · Répétition dynamique des conteneurs — UI existante mais **schéma ⚠️ capture**
- **Source** : changelog v5.65.9 ; wiki Custom Scenes (« Containers can repeat their content
  once per entry of an array/dictionary variable »).
- **Builder** : `renderRepeatProperties` (2126-2130) existe et propose
  `repeatConfig.{isEnabled,dataSource}` — mais **0 occurrence dans le corpus** et aucune doc
  JSON publique : le nom des clés est **inventé**.
- **Action bloquée** : exporter depuis l'app (v5.65.9+) un `.macro` avec un layout en
  « repeat » ; relever les clés exactes (flag, source, éventuel compteur d'itération pour le
  magic text `{iterator_value}`) ; mettre à jour `renderRepeatProperties` + `checkString`
  + l'aide. Tant que ce n'est pas fait : garder l'UI mais l'étiqueter « expérimentale ».
- **Sémantique attendue** : on répète un *template d'enfant* par entrée array/dict ; le magic
  text de l'itérateur s'utilise dans le template (voir `{size=Name}` / `{v=Name[i]}`).

### P0-5 · WebView — clés « extensions » riskées ⚠️ capture
- **Corpus (Schema Vrai)** : `closeSceneOnPress, enableJavaScript, enableSwipeNavigation,
  height, url, variableUpdateValue, visibilityVariable, width`.
- **Builder** : édite aussi `darkMode` et `retainState` — **absents du corpus** (capturer pour
  vérifier). Idem les champs EditText étendus (`inputType`, `forceNumericalKeyboard`,
  `showBorder`, `showBackground`, `textSizeString`, `isPassword`) et Image par ressource.

### P0-6 · MapView — schéma quasi entièrement inventé ⚠️ capture
- **Corpus** : **aucun** SceneMapView (0/140) → tous les champs actuels
  (`bindLocationToVariables`, `latitudeVariable`, `longitudeVariable`, `zoomVariable`,
  `markersArrayVariable`, `tappedMarkerVariable`, `showMyLocation`, `showCompass`, `mapType`)
  sont **non vérifiés**. Avant d'encourager leur usage : capturer un `.macro` avec MapView.

### P0-7 · Affichage dynamique des images + cache (rapports #21/#23)
- **Source** : forum #21/#23 — l'app **copie en cache interne** l'image (URL ou fichier) et ne
  la rafraîchit pas ; base64 énorme → crash.
- **Builder** : côté JSON rien à corriger. Vérifier le preview Image (option
  `disableCache` déjà éditable) : recharger `object.src` quand l'URI change + cache-buster de
  *preview uniquement* (ne pas écrire ce paramètre dans le JSON). Documenter l'astuce
  `disableCache` dans l'éditeur Image.
- **Validation** : manuel (changer l'URI → preview mis à jour sans F5).

---

## 4. P1 — Fonctionnalités à forte valeur (schéma sûr ou déjà exigé)

### P1-1 · WebView : URL → variable, actions contexte, JS → variable (#222, #234)
- **Demandes forum** : lier l'URL courante du WebView à une variable string (navigation =
  mise à jour) ; menu contextuel sur liens/images ; **intercepter les valeurs « mdOutput »
  du JS vers une variable locale** (analogue à Action JavaScript).
- **Builder** : pour l'éditeur WebView (2214-2215) → ajouter un champ « Bind current URL to
  String variable » (⚠️ schema à capturer — sinon expliciter en note) et un aperçu HTML
  inline (`iframe.srcdoc`) pour le preview. La partie JS→variable relève surtout de l'app ;
  la documenter en P4.
- **Validation** : preview + round-trip.

### P1-2 · Slider/Progress : valeur en temps réel et affichages (#56, #58)
- **Demandes** : « set variable en temps réel pendant le slider » (#56) ;
  « cacher la ligne et le point, garder la saisie numérique » (#58).
- **Builder** : le preview peut lire la valeur simulée en direct (déjà fait pour les
  `IntValue`/`BooleanValue`). Proposer : option `hideSlider` (⚠️ capture) sinon note.
  Vérifier labels start/end/none (`valuePosition` 0-4 ✅) et step (`stepSize` ✅).

### P1-3 · Groupement et colonne « span » sur GridLayout (forum #35-list)
- **Source** : demandes communautaires (étiquettes d'icônes en grille #47, rangement).
- **Builder** : `renderGridLayoutProperties` (2135) a `itemsPerRow`/`rowHeight` ✅. Un enfant
  direct « column span » n'existe pas dans le corpus → **P4** tant que l'app ne l'émet pas.

### P1-4 · Copier/coller de sous-arbres entre scènes
- Voir P3-3 (implémentation 100 % côté builder, aucun risque schema).

### P1-5 · Long-press sur les éléments cliquables (#235)
- **Demande** : déclencher une action/macro par appui-long sur un bouton (comme les floating
  texts). Pas de clé schema → **P4 / à remonter au dev**, mais le builder peut déjà préserver
  une future clé sans la modifier (aucune action nécessaire).

---

## 5. P2 — Complétude des éditeurs (clés corpus vs éditeurs)

Croisement corpus ↔ `renderItemProperties` (2168-2226) :

| Composant | Clés réelles (corpus) | Manque dans le builder v20.1 |
|---|---|---|
| SceneText | autoSizeText, closeSceneOnPress, enableAutoRefresh, enableSelection, htmlFormatting, isBold, isItalic, maxLines, maxLinesEnabled, padding, text, textAlignment, textColor, textSize, variableUpdateValue (+fontFamily) | **« Scale to fit » (P0-3)** ; `closeSceneOnPress` déjà via `renderButtonClickConfig` ✅ |
| SceneButton | buttonClickConfig, buttonColor, closeSceneOnPress, htmlFormatting, padding, text, textColor, textSize, variableToUpdate, variableUpdateValue | — (editeur complet, toggle booléen ✅) |
| SceneSwitch | alignment, isChecked, text, textColor, textSize, textStart (+ `checkedValue` au niveau item) | `checkedValue` ⚠️ (capturer pour comprendre l'usage) ; Switch vertical (#227) → P4 |
| SceneCheckBox | alignment, booleanVariable, isChecked, padding, text, textColor, textSize, textStart | — |
| SceneSlider | alignment, current, max, min, numberVariable, padding, sliderColor, stepSize, textColor, textSize, valuePosition, visibilityVariable, widthPercent (+bindToVariable, fontFamily) | — (magic text sur min/max/current/step ✅, fontFamily ✅) |
| SceneVerticalSlider | (absent du corpus) | épingler le schéma actuel ⚠️ |
| SceneProgressIndicator | current, indeterminate, max, min, size, style, thickness, trackColor | — (éditeur complet 2190 ✅) |
| SceneEditText | hintText, isBold, isItalic, populateWithValue, singleLineOnly, stringVariable, textColor, textSize (+enteredText/lastEnteredText runtime) | épingler les clés étendues ⚠️ (P0-5) |
| SceneDropDownSelection | onlySetVariableWhenValueChanged, padding, showHeading, text, textColor, textSize, useKeys (+arrayVariable, stringOutputVariable, keyOutputVariable) | — (éditeur complet ✅) |
| SceneOptionSelector | arrayVariable, borderColor, keyOutputVariable, multiSelect, onlySetVariableWhenValueChanged, padding, showBorder, textColor, textSize, useKeys | **output + showBorder/borderColor (P0-1)** |
| SceneIcon | alignment, closeSceneOnPress, size, tintColor, tintEnabled, variableUpdateValue (sceneIconData : imageResourceId, imageResourceName, imageUri, manualMode) | mini-picker de ressources (P3.5) |
| SceneImage | alignment, closeSceneOnPress, height, sceneImageData, variableUpdateValue, width | mode ressource/URL de l'image ⚠️ → P4 |
| SceneHorizontalDivider | config : dividerColor, dividerHeight, padding, verticalPadding | — (éditeur ✅ ; transparence OK) |
| SceneSpacer | heightDp, widthDp | — |
| SceneWebView | closeSceneOnPress, enableJavaScript, enableSwipeNavigation, height, url, variableUpdateValue, visibilityVariable, width | darkMode/retainState ⚠️ (P0-5) |
| SceneDatePicker | sceneCalendarConfig + dictionaryVariable | — (convertisseur ✅) |
| SceneTimePicker | sceneTimePickerConfig (dictionaryVariable, useAmPm…) | à recenser ⚠️ |
| SceneHorizontalLayout | alignment, visibilityVariable | height/width (#226) → P4 |
| SceneVerticalLayout | alignment, heightPercent, widthPercent | — |
| SceneGridLayout | itemsPerRow, rowHeight | column span → P4 |
| SceneTableLayout | columnWidths, numColumns, rowHeight, showTableBorders, tableBorderColor | — (colonnes % préservées ✅) |
| SceneHorizontalPager | heightPercentage, tabs, useScrollableTabs | — (éditeur ✅) |
| Champs item | guid, iconRes, iconResId, lastRefreshValue, uniqueId, id | générer guid négatif + préserver ces clés (fait ? à vérifier) |

### Annexes corpus (fin du doc) : clés sceneConfig, displayOption, inventaire des bindings.

---

## 6. P3 — Outillage & UX du builder (zéro risque schema)

- **P3-1 · Guides & snapping** au déplacement dans le preview (alignements visuels).
- **P3-2 · Inspecteur « champs non éditables »** : pour l'élément sélectionné, diff
  `Object.keys(c) ∩ {clés inconnues de l'éditeur}` → révéler les futures clés app et les
  ajouter à ce fichier (P0-5 à P0-6 utilisent ça).
- **P3-3 · Copier/coller sous-arbre entre scènes** : `state.clipboard`, boutons Copy/Paste dans
  `renderItemProperties`, Ctrl+C/Ctrl+V ; reassociation `oid`/`idToObject`.
- **P3-4 · Libellés FR du picker magic text** : table de traduction optionnelle pour
  `MAGIC_TEXT_OPTIONS` (719-945) via `t()` (labels EN actuellement).
- **P3-5 · Couleurs** : mémoriser la luminosité + liste des récents (forum #35-list) ;
  `localStorage['sb_recent_colors']` autour de `colorField`.
- **P3-6 · Raccourcis clavier** : dupliquer (Ctrl+D), renommer (F2), verrouiller (Ctrl+L).
- **P3-7 · Harness de régression** : mettre `harness_fr/p2/p6/p7.js` dans le repo (ex.
  `tools/`) + commande `make check` (extraction du `<script>`, `node --check`, round-trip).
  (⚠️ Node n'est pas installé sur cette machine — à documenter/cible.)
- **P3-8 · Aide en ligne** : tables pliables du catalogue magic text dans Help (sections 6-8).

---

## 7. P4 — Demandes communautaires non couvertes (à remonter au dev MacroDroid)

À **relayer** au dev (aucun impact builder tant que le schéma n'existe pas) :
- Animations d'ouverture/fermeture (fade) (#27) ; animations des composants (#29).
- Widget persistant d'une scène sur l'écran d'accueil (#48, #60).
- Scène « calendar/clock » avec planification (#30).
- Orientation verticale pour Text/Icon/Image/Progress (#32 ; le VerticalSlider existe ✅).
- Boîte d'affichage lecture seule (résultat) (#33/34).
- Mode vertical pour Switch/Checkbox en « radio » (#227, #35-rapport « Radio »).
- Couleur/transparence par variable (#41, #55).
- Vibration des éléments cliquables (#46).
- Étiquettes sous les icônes en grille (#47) — astuce actuelle : texte sous la grille.
- Fermeture par tap hors scène pour Overlay (#49-51 — `closeOnBackgroundTouch` exposé, à
  vérifier sur Overlay), empilement FullScreen + Dialog (#52), sauvegarde de position
  Overlay (#53), hide du tracé/bout du slider (#58), menus repliables (#59).
- Hauteur Overlay « based on contents » + « max % » (#233 — l'option `Wrap content` (2)
  existe déjà) ; arrangement horizontal des variables de l'action (#236) ;
  switch « cancel scene » (#237).
- MCP (fil forum #2) ; QML/Scenes V2 (#232); « histogramme Status Dot » (#231).
- WebView : JS→variable (#222, voir P1-1) ; menu contextuel sur liens/images (#234).
- Déplacement des `.md` du corpus : déjà fait (docs/).

---

## 8. Demandes forum → statut (mapping posts)

| Post | Demande | Statut |
|---|---|---|
| #21/#23 | image dynamique/cache, base64 crash | bug app → P0-7 (builder neutre) |
| #24 | texte single-line scale down | ✅ v5.54 = `autoSizeText` → **P0-3 éditeur** |
| #25 | taille de texte par entier | ✅ magic text (builder ✅) |
| #26 / #45 | possible action item sans variable | ✅ v5.63 (actions individuelles, builder `actionField`+`buttonClickConfig`) |
| #27 | coins arrondis nom : fond/overlay + fade | ✅ v5.54 `roundedCornerAmount` → **P0-2** ; fade → P4 |
| #29 | animation floating text / « if-not-confirmed » | P4 (branching déjà dispo via If/else) |
| #30 | widget horloge/planificateur | P4 |
| #32 | vertical Text/Icon/Image/Slider/Progress | VerticalSlider ✅ ; reste → P4 |
| #33/#34 | boîte résultat lecture seule | astuce Text+magic ; feature → P4 |
| #35-list | dropdown temp. array, saisie dynamique, multi-select CSV, separator, radio, slider title, mémoriser luminosité, rename propagé, Text Entry STR/INT | Séparateur ✅v5.54 ; rename ✅ builder ; STR/INT ✅v5.54 ; le reste → P4 (dropdown multi : voir OptionSelector `multiSelect` ✅ corpus) |
| #40 | sliders verticaux, step, position valeur, CSS | ✅ v5.54 (CSS via HTML) |
| #41/#55 | couleur/transparence par variable | P4 |
| #42 | swipe entre scènes | P4 |
| #44 | texte de switch cliquable | P4 |
| #46 | vibration cliquables | P4 |
| #47 | étiquettes icônes grille | P4 |
| #49/#51 | close-on-outside pour Overlay | `closeOnBackgroundTouch` exposé (2087) — à vérifier sur Overlay |
| #52 | empilement FullScreen+Dialog | P4 |
| #53 | sauvegarde position Overlay | P4 |
| #56 | slider temps réel + lock screen | lock ✅v5.54.9 (`showOnLockScreen`) ; temps réel → P4 |
| #58 | hide ligne/point slider | P4 |
| #59 | menus repliables | P4 |
| #60 | widget home screen | P4 |
| #64 | « Pin item to screen » (rester visible) | P4 |
| #65 | image de fond personnalisée (galerie) | ✅ v5.54 `backgroundImage` + builder P0-7 |
| #66 | postMessage WebView ↔ threads | P4 / P1-1 |
| #68 | retour haptic sur boutons/icônes | P4 |
| #71 | Text Entry hauteur fixe + scroll | P4 |
| #78 | magic text pour couleurs (theme switch) | P4 |
| #79/#82 | bind visibility à FALSE (inverser) | ✅ builder (inverser bool) ; P4 |
| #85 | Overlay scrollbars, Dialog pas de position x/y | P4 (limitations connues) |
| #86 | type scène « Panel » (swipe drawer-like) | P4 (app) |
| #87/#93 | Text Entry ne se rafraîchit pas à la modification de variable | ✅ v5.55 (bug fix app) |
| #90 | taille texte < 6pt (placeholder fin) | P4 |
| #91 | scène par-dessus scène (overlay multi) | P4 (app) |
| #92 | swap icône pour état enabled/disabled | P4 |
| #94 | rayon coins bouton scène | P4 |
| #95 | texte à nb lignes max + scrollbar | P4 |
| #96/#98 | WebView JS → variable MacroDroid | P4 / P1-1 |
| #101/#103/#110 | design bouton (bordures, icône+texte) | P4 |
| #109/#113 | Text Entry entrée entier (clavier numpad) | P4 |
| #115 | couleurs supportent variables | P4 |
| #116 | Overlay bugs (back key, move, delete) + Dialog largeur/hauteur | P4 |
| #117 | layout drop-down, tabs verticaux, taille bouton, animations, séparateur | P4 |
| #118/#120 | Text Entry : format, min-max, couleur hint, transparent, marges, taille texte/padding | P4 |
| #121 | masquer titres tab Layout | P4 |
| #122 | confirmation suppression tab | P4 (UX) |
| #123 | cancel dans tab Layout n'annule pas les edits | bug app |
| #124 | long-press move par défaut + autosave | P4 |
| #125 | bouton Home continue macro (régression) + choix behavior | bug app → P4 |
| #126/#180 | bind enabled à boolean ; opérateurs logiques visibility | P4 |
| #127 | bind visibility par tab individuel | P4 |
| #128 | colonnes grid ajustables | P4 |
| #129 | magic text pour row height | P4 |
| #130 | trigger scene show/hide | P4 (app) |
| #131 | row height horizontal layout | P4 |
| #132 | type Bubble, gradients, shapes | P4 (app) |
| #133/#137/#138/#139 | close scene on press sur switch/dropdown/slider/checkbox | P4 |
| #135 | opérateurs logiques (AND/OR/NOT) pour visibility | P4 |
| #141 | scène HTML/CSS/JS + bridge variables (Winny57) | P4 / P1-1 |
| #142 | rotation écran lock screen | P4 |
| #143 | min-max variables, secondes time picker | P4 |
| #144 | date picker sélection directe mois | P4 |
| #145 | composants riches style termux-dialog | P4 (app) |
| #146 | radio buttons | P4 |
| #149 | floating text tue scène d'un autre macro | bug app |
| #150/#155 | chemin image dynamique + crash lecture photos | P0-7 / bug app |
| #152/#181 | bouton définit plusieurs variables | P4 |
| #153 | transparence Activity mode | P4 |
| #156/#158 | taille widgets %, zones gestuelles | P4 |
| #159/#163 | selectable list en grille/horizontale | P4 |
| #160 | édition calendrier dans scène | P4 |
| #161 | état actif/inactif par boolean | P4 |
| #166 | selectable list : recherche, séparateurs, select-all | P4 |
| #171 | copier éléments entre scènes | ✅ builder (déjà dispo) |
| #172 | widgets Android custom dans scènes | P4 (app) |
| #173 | bordure dropdown, reflow table | P4 |
| #174 | drag-drop dans table layout | P4 |
| #175 | margin entre éléments | P4 |
| #178 | UI dynamique depuis array/dictionary | P4 |
| #179 | action Block depuis bouton | P4 (app) |
| #186 | stocker index en integer (pas string) | P4 |
| #187 | séparateurs selectable list | P4 |
| #188 | tab+table overlap (sélection impossible) | bug éditeur |
| #189 | couleur bouton toggle au press | P4 |
| #190/#192/#193/#194 | switch tab programmatique, tab par défaut, tab actif variable | P4 |
| #195 | bouton dans selectable list, taille texte bouton | P4 |
| #196 | slider decimal, multi-boolean visibility | P4 |
| #197 | slider vertical overlay | P4 |
| #198 | WebView editor scroll-to-bottom | bug éditeur |
| #202/#204 | edge-to-edge padding | ✅ v5.64 |
| #209 | background color sur texte | P4 |
| #210 | WebView HTML scene avec variables | P4 / P1-1 |
| #211 | SVG pour icônes/images | P4 |
| #212 | boutons dynamiques depuis array | P4 |
| #213/#216 | bordure texte, input désactivé non gris | P4 |
| #217 | magic text dans sélecteurs couleur | P4 |
| #218 | bouton Home exit + variable résultat | P4 (app) |
| #219/#220 | conditions sur éléments scène (AND/OR) | P4 |
| #222 | JS webview → variable | P4 / P1-1 (interception) |
| #224 | reset « variable to modify » = None | retour app UX → P4 |
| #226 | height/width sur HorizontalLayout | P4 (non dans le corpus) |
| #227 | boutons clear/search dans Text Entry ; options scène pour Drawer ; radio checkbox ; switch vertical | P4 |
| #228 | Table 4 colonnes « by design ? » | retour app |
| #229 | toggle visibilité mot de passe (Text Entry) | P4 |
| #230 | bug scale-to-fit + HTML | connue app → **note P0-3** |
| #231 | status-dot overlay | P4 |
| #233 | height overlay « based on contents » + max % | partiel ✅ (`Wrap content`(2)) ; max% → P4 |
| #234 | URL webview→var, menu contextuel liens/images | P4 / P1-1 |
| #235 | appui long bouton → action | P4 |
| #236 | disposition horizontale des variables (action) | P4 |
| #237 | switch « cancel scene » | P4 |

---

## 9. Processus recommandé

1. **Capture de référence** (bloquante pour ⚠️) : `.macro` v5.65.9 avec repeat ; OptionSelector
   single+multi avec sorties ; WebView darkMode/retainState ; Image ressource ; Text Entry
   `inputType`/`isPassword` ; MapView ; TimePicker. Les déposer dans `macro-reference/` et
   régénérer `docs/corpus_ANALYSE.md` / `docs/corpus_DETAILS.md`.
2. **Ordre** : P0-1 → P0-2 → P0-3 → P0-4 (après capture) → P1 ; un item = un commit, avec
   round-trip corpus + note README.md + bump `BUILD_ID`/version (v20.2, v20.3…).
3. **Idées clés** : ne jamais détruire les clés inconnues à l'import (comportement actuel) ;
   `VALIDATE` ne doit signaler que ce que l'app refuse.
4. **Maintenance de ce fichier** : cocher/retirer les items faits ; entrées forum/changelogs
   nouvelles en tête de P0. Toutes les pages forum (1–12) sont maintenant épluchées.

---

## 10. Annexes — données corpus vérifiées (140 scènes)

### sceneConfig (clés)
`backgroundColor, backgroundImage, backgroundImageDisplayMode (CENTER_CROP ×97, FILL_BOUNDS),
blockNextActions, closeOnBackgroundTouch, contentPadding, dismissOnBackPress,
dismissOnHomeTaskSwitch, displayOption, foregroundColor, name, roundedCornerAmount (×117),
showOnLockScreen, updateValuesOnSceneClose`

### displayOption (objets réels)
- `{"type":"FullScreen","nameRes":2132021408}`
- `{"type":"Dialog","closeOnOutsideTouch":false,"nameRes":2132021906}`
- `{"type":"Overlay", drawOverSystemApps, preventRemovalByBin, showPositionOnMove,
  longPressToMove, overlayStatusBar, widthOption, widthValue, heightOption, heightValue,
  xValue, yValue, nameRes}` — valeurs en **% sous forme de chaînes** (`"100"`, `"50"`).

### Inventaire des bindings (clés + volume)
`variableUpdateValue ×587, variableToUpdate ×290, visibilityVariable ×243,
booleanVariable ×143, stringVariable ×121, numberVariable ×41, arrayVariable ×27,
stringOutputVariable ×23, keyOutputVariable ×22, onlySetVariableWhenValueChanged ×16,
bindToVariable ×9, enabledVariable ×5, dictionaryVariable ×3`

> ⚠️ **Aucun `selectedIndicesVariable`/`selectedIndexVariable`** — voir P0-1.

### Composants — clés par type
`SceneText`: autoSizeText, closeSceneOnPress, enableAutoRefresh, enableSelection,
htmlFormatting, isBold, isItalic, maxLines, maxLinesEnabled, padding, text, textAlignment,
textColor, textSize, variableUpdateValue · `SceneButton`: buttonClickConfig, buttonColor,
closeSceneOnPress, htmlFormatting, padding, text, textColor, textSize, variableToUpdate,
variableUpdateValue · `SceneSwitch`: alignment, isChecked, text, textColor, textSize,
textStart · `SceneCheckBox`: alignment, booleanVariable, isChecked, padding, text, textColor,
textSize, textStart · `SceneSlider`: alignment, bindToVariable, current, max, min,
numberVariable, padding, sliderColor, stepSize, textColor, textSize, valuePosition,
visibilityVariable, widthPercent · `SceneProgressIndicator`: current, indeterminate, max,
min, size, style, thickness, trackColor · `SceneEditText`: hintText, isBold, isItalic,
populateWithValue, singleLineOnly, stringVariable, textColor, textSize · 
`SceneDropDownSelection`: onlySetVariableWhenValueChanged, padding, showHeading, text,
textColor, textSize, useKeys (+ arrayVariable, stringOutputVariable, keyOutputVariable) ·
`SceneOptionSelector`: arrayVariable, borderColor, keyOutputVariable, multiSelect,
onlySetVariableWhenValueChanged, padding, showBorder, textColor, textSize, useKeys ·
`SceneIcon`: alignment, closeSceneOnPress, size, tintColor, tintEnabled, variableUpdateValue
(+ sceneIconData: imageResourceId, imageResourceName, imageUri, manualMode) · `SceneImage`:
alignment, closeSceneOnPress, height, sceneImageData, variableUpdateValue, width ·
`SceneWebView`: closeSceneOnPress, enableJavaScript, enableSwipeNavigation, height, url,
variableUpdateValue, visibilityVariable, width · `SceneHorizontalDivider` (clé `config`):
dividerColor, dividerHeight, padding, verticalPadding · `SceneSpacer`: heightDp, widthDp ·
`SceneHorizontalLayout`: alignment, visibilityVariable · `SceneVerticalLayout`: alignment,
heightPercent, widthPercent · `SceneGridLayout`: itemsPerRow, rowHeight ·
`SceneTableLayout`: columnWidths, numColumns, rowHeight, showTableBorders, tableBorderColor ·
`SceneHorizontalPager`: heightPercentage, tabs, useScrollableTabs

### Champs item systématiques (préserver / générer)
`guid` (toujours négatif en réel, ex. −7634687123121573313, jamais 0), `iconRes`,
`iconResId`, `lastRefreshValue`, `uniqueId`, `id`, `checkedValue` (Switch, usage ⚠️).

---

## 11. Sources

- Wiki MacroDroid : Magic Text, Custom Scenes, Action: Display Custom Scene, MacroDroid
  Drawer, Control flow: Repeat actions (`macrodroidforum.com/wiki/index.php/…`).
- Changelogs : ReleaseAPK v5.54 (juin 2025) complet ; apkfab v5.63.11 ; Aptoide v5.65.9 ;
  4pda compile-play 5.54→5.65.9.
- Forum : « Scene - Feature Requests » (thr. 9894, 12 pages) — **toutes pages lues** (#1–#237) ;
  « Visual ideas for user scenes » (thr. 10029, par Winny57).
- Corpus : `macro-reference/` (71 macros, 140 scènes de `sceneDescription`) +
  `docs/corpus_ANALYSE.md`, `docs/corpus_DETAILS.md`, `analysis_summary.json`.