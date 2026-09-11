# Feature Integration — Roadmap du Scene Builder (v20.1+)

Analyse approfondie : wiki officiel MacroDroid (pages Magic Text, Custom Scenes, Action:
Display Custom Scene, à jour août 2026), changelogs de l'application (v5.54 → v5.66.9),
fil forum officiel « Scene - Feature Requests » (macrodroidforum, ouvert par MacroDroidDev
le 03/04/2025), et corpus réel `macro-reference/` (71 macros, 148 scènes).

> Ce document est une **liste de travail priorisée** : chaque item comporte la source, le
> besoin, l'implémentation complète (fonctions/structures ciblées dans
> `v20/MacroDroid_Scene_Builder_v20.html`) et la validation. Rien n'est figé : les items
> « App require capture » doivent d'abord être confirmés en exportant un `.macro` de
> référence depuis l'application (le builder ne doit jamais écrire de JSON qu'on n'a pas
> vu produit par MacroDroid).

---

## 0. État des lieux (déjà en place dans v20.1)

Ne pas ré-implémenter. Pour référence des points d'ancrage dans le code :

| Élément | Fonctions (lignes v20.1) |
| --- | --- |
| Éditeurs de tous les types d'éléments | `renderItemProperties` (2168) : Text/Button/Checkbox/Switch/Slider/VerticalSlider/Progress/EditText/Divider/Image/Icon/Spacer + délégués (layouts 2132-2161, MapView/WebView 2155+, DropDown 2141, SelectableList 2144, DatePicker 2148) |
| Scène (nom, block-next-actions, couleurs, fond, lock screen, back/home/touch, padding central) | `renderSceneProperties` (2077) |
| Display mode FullScreen/Dialog/Overlay complet (over status bar, draw over system apps, prevent removal, long-press move, show position, width/height X/Y) | `renderDisplayOptionEditor` (2033) |
| Image de fond STATIC_FILE + display mode | `renderBackgroundEditor` (2058) |
| Bindings variables (typed picker : Local/Global/Special, tous types, visibilité, enabled) | `openTypedVariablePicker` (1837), `openMagicTextPicker` (1828) |
| Variables (créer/renommer/supprimer, incidente de renommage dans les scènes) | `openVariablesPanel` (1887), `renameVariableDialog` (1955) |
| Magic text (catalogue complet ~225 tokens, groupes, numériques, paramétrés) | `MAGIC_TEXT_OPTIONS` (719), `NUMERIC_MAGIC_TOKENS` (1808), validateur (`checkString` 2588) |
| Export macro/BUNDLE/ZIP scènes, PNG, VALIDATE, simulateur, arbre+recherche, multi-sélection/alignement, zoom | voir README.md |
| Constantes réservées (variable booléenne `BUILDER_ALWAYS_FALSE_VAR`) | `ensureBuilderConstantVariables` (2272) |

---

## 1. Priorité P0 — Conformité avec l'application (schema ; à faire en premier)

### P0-1 · Répétition dynamique des conteneurs (array/dictionary) — v5.65.9
- **Source** : changelog app 2026-07-02 (« support for dynamically repeating components in
  scene containers (populated from array/dictionary variable) ») ; wiki Custom Scenes
  (« Containers can repeat their content once per entry of an array/dictionary variable,
  which is ideal for building lists »).
- **Besoin** : pas de brique pour créer une liste dynamique (liste d'items répétée N fois
  selon un array/dictionnaire). C'est LA fonctionnalité la plus demandée côté scènes.
- **Spéc à confirmer** : exporter depuis l'app un `.macro` contenant un
  H/V/Grid/Table Layout avec « repeat content » activé ; noter précisément les clés JSON
  (typiquement un flag type `m_repeat`/`repeat` + un binding `{varName}` de type
  Array/Dictionary, peut-être un suffixe pour l'index de ligne) et le comportement
  d'écriture retour (l'opt. « variable index » pour `{iterator_value}`).
- **Implémentation** :
  1. Ajouter dans `renderHorizontalLayoutProperties`/`renderVerticalLayoutProperties`/
     `renderGridLayoutProperties`/`renderTableLayoutProperties` un groupe « Repeat content »
     : `check` « Repeat once per array/dictionary entry » + `typedVarField` « Array / Dictionary
     variable » (types [4,5]).
  2. Câbler la visibilité du groupe : tags retenus sur les layouts (réutiliser les clés
     issues de la capture P0-1 et conserver l'existant à l'import).
  3. Introspection : `childGroups`/`treeText` (2258) — afficher si un layout est répété
     (badge « ↻ »). Neutre pour le preview tant que la spec app n'est pas confirmée.
  4. Prévention : dans `buildNewMacroDocument`/`buildSceneMacroDoc` (2316+), s'assurer que la
     variable liée au repeat est bien exportée comme variable référencée
     (`usedVariableNamesFor`).
- **Validation** : round-trip corpus (un `.macro` capturé) sans altération + scénario
  « array de 3 → le layout se répète 3 fois » dans la simulation inversée (affichage liste).

### P0-2 · Coins arrondis de scène (dialog/overlay) — v5.54
- **Source** : changelog app 2026-05 (v5.54) ; wiki Display Custom Scene (overlay options).
- **Besoin** : option « Rounded corners » au niveau scène lorsque display mode = Dialog ou
  Overlay.
- **Spéc à confirmer** : capturer un macro avec coins arrondis (clé probablement sur
  `sceneDescription` ou sur l'objet `displayOption` ; vérifier le champ exact, ex.
  `roundedCorners`/`cornerRadius`).
- **Implémentation** : dans `renderSceneProperties` (2077), si `displayOption.type` ∈
  {Dialog, Overlay}, ajouter `field` numérique « Corner radius (px) » + `check` « Rounded
  corners ». Écrire la clé confirmée. Refléter dans le preview `renderPreview` (fond/scène
  avec `border-radius` CSS sur le shell ou le conteneur).
- **Validation** : round-trip + contrôle visuel preview.

### P0-3 · « Scale to fit » et auto-taille du texte (Text) — v5.54
- **Source** : changelog v5.54 (« Text now supports a maximum number of lines and scale to
  fit option ») ; wiki Custom Scenes (« auto-sizing », « Refresh value every second »).
- **État** : le builder gère déjà `maxLines`/`maxLinesEnabled`, `htmlFormatting`,
  `enableAutoRefresh`, `enableSelection` (2176). **Manque** : l'option `scaleToFit`
  (réduire la taille de police pour tenir dans les lignes max).
- **Spéc à confirmer** : nom de champ (probablement `scaleToFit`/`scaleToFitText`) via
  capture.
- **Implémentation** : dans le bloc `SceneText` (2174-2177), après `maxLines`, ajouter
  `check('Scale to fit', c.scaleToFit, v=>c.scaleToFit=v)`. Le garantir :
  `field` Text size et maxLines acceptent déjà magic text (nombre).
- **Validation** : round-trip ; VALIDATE ne signale pas le champ comme inconnu (il ne le
  vérifie pas — ajout d'un token/branche si nécessaire).

### P0-4 · Affichage dynamique des images (URL) et cache — rapport utilisateurs
- **Source** : fil forum (rapport « dynamic image not updated / caching »).
- **Besoin** : côté builder, rien à corriger dans le JSON, mais le preview doit recharger
  l'image d'URL quand celle-ci change : vérifier que `renderPreview` de `SceneImage`
  (2218-2219) force `object.src = uri` avec cache-buster si l'URI a changé (sinon le
  navigateur garde l'ancienne). Ajouter une note d'aide « use a http://… URL and disable
  cache » dans l'éditeur Image.
- **Implémentation** : dans le rendu d'aperçu Image, comparer l'URI précédente et ajouter
  `?t=…` quand `disableCache` est vrai ; documenter dans le champ note.
- **Validation** : manuel (changer l'URI → preview mis à jour sans F5).

### P0-5 · Slider : étiquettes de valeur et saisie exacte
- **Source** : changelog v5.54 (value labels at start/end, step values) ; forum
  (« Allow integer input… exact specific values »).
- **État** : déjà là (2176/2188 : `valuePosition` 0-4, `stepSize`, `valueEditableOnTap`,
  min/max journalière). Aucun travail si la capture de P0-1 le confirme ; sinon ajuster les
  libellés `valuePosition` aux intitulés réels de l'app.

---

## 2. Priorité P1 — Fonctionnalités nouvelles à forte valeur

### P1-1 · Éditeur de `SceneMapView` étendu (état/zoom 2-way, marqueurs avancés)
- **Source** : wiki Display Custom Scene / Custom Scenes (map : markers from array, location
  & zoom bound to variables, two-way pan writes back).
- **État** : `renderMapViewProperties` (2155) gère bind lat/lon/zoom, markersArrayVariable,
  mais plusieurs options restent à finaliser.
- **Implémentation** :
  1. Marqueurs : enrichir le modèle « label/hexColor » en une saisie claire (par ex.
     dictionnaire de correspondance clé→champ, décrit dans une note) et un champ « tapped
     marker → string variable » (déjà amorcé, terminer) + éventuellement « tapped marker →
     int variable (index) ».
  2. Utiliser le typage magique : lat/lon/zoom en `magic:true, magicContext:'number'`
     (activé quand les variables ne sont pas liées — déjà le cas).
  3. Documenter le format des marqueurs dans une fenêtre d'aide contextuelle (le builder est
     hors-ligne → texte statique).
- **Validation** : corpus (1 MapView ou en créer une de référence) ; simulation de tap sur
  marqueur → variable renseignée dans le simulateur.

### P1-2 · Selectable List : peuplement par array/dictionary + multi-sélection → CSV
- **Source** : forum (DropDown : ne veut pas d'array pré-créé ; « output as comma separated
  string ») ; wiki (OptionSelector : single/multi from list of options).
- **État** : `renderSelectableListProperties` (2144) gère options multi-ligne,
  `arrayVariable`, `selectedIndicesVariable` (array) / `selectedIndexVariable` (int).
- **Implémentation** :
  1. Ajouter `typedVarField` « Save selected values (CSV) to String variable » (types [2]) →
     écrire la clé (à confirmer par capture : probable `selectedValuesVariable`).
  2. Peuplement lazy : si `arrayVariable` est posé, afficher un aperçu (n entrées
     prévisualisées) dans le preview via la variable simulée.
- **Validation** : simulation multi-sélection → variable string CSV dans le simulateur.

### P1-3 · DropDown : listes temporaires et saisie dynamique (proposition UX)
- **Source** : forum (temp Array/Dictionary, dynamically typed entry added to variable).
- **Note** : le builder ne peut pas créer de tableau « temporaire » dans l'app (c'est un
  comportement runtime). Proposer plutôt :
  1. Un helper « upgrade array » : convertir une liste multi-ligne (champ commenté) en une
     variable Array locale exportée automatiquement (`ensureBuilderConstantVariables`).
  2. Une option « Allow user to type new entry » → champ booléen (clé à confirmer par
     capture ; sinon différé jusqu'à preuve.
  3. Aide : « uses `{size=Name}` et `{v=Name[i]}` dans le preview ».
- **Priority** : P1 si capture dispo, sinon P4.

### P1-4 · Texte multi-scène : « Refresh value every second » (déjà ok) + « Refresh while scene open » pour Image/WebView
- **Source** : wiki (Text refresh), forum (dynamic image not refreshed).
- **Implémentation** : ajouter `check('Refresh while scene is open', c.enableAutoRefresh, …)`
  aux éléments Image/WebView/MapView s'ils ne l'ont pas (cf. 2216-2220) et documenter le
  comportement preview (pas re-productible hors runtime → juste préserver la clé).
- **Validation** : import sans perte ; VALIDATE silencieux.

### P1-5 · Copie / collage enrichi entre scènes (templates de sous-arbres)
- **Source** : wiki (« Components can be copied and pasted within the designer » ; besoin
  cross-scène) ; pratique.
- **Implémentation** :
  1. `mutate(()=>…)` ; nouvel état `state.clipboard = {item, parentType}` (l'état undo/redo
     existe : `snapshot()` / `pushUndo`). Boutons « Copy subtree » / « Paste » dans
     `renderItemProperties` + raccourcis Ctrl+C/Ctrl+V (les raccourcis existent déjà —
     brancher `clipboard` sur l'existant).
  2. Collage : réassigner un deepClone et le pousser dans le même type de parent
     (layout/table) si compatible, sinon à la racine. Re-câbler `oid`/`idToObject`.
  3. Étendre `state.clipboard` en session uniquement (pas de persistance).
- **Validation** : manuel (copie HLayout avec 3 enfants → collage → même rendu).

### P1-6 · Groupement / dégroupement visuel (alias containers)
- **Source** : forum (grid spanning, alignement L/R impossible sans layout) ; ergonomie.
- **Besoin** : implémenter « column span » pour `SceneGridLayout` :
  `renderGridLayoutProperties` (2135) — ajouter un champ entier « Column span » par enfant
  direct (clé à confirmer par capture : probable `columnSpan`).
- **Validation** : round-trip + alignement preview.

---

## 3. Priorité P2 — Complétude des éditeurs (par composant)

- **P2-1 · SceneSwitch/CheckBox : alignements « Split » et couleurs** — déjà ok (2182/2184) ;
  vérifier l'option app « split alignment » (v5.54) → couvrir `alignment='Split'` dans
  preview (positionnement du contrôle à droite, libellé à gauche).
- **P2-2 · Progress Indicator** — `style` Linear/Circular, `indeterminate`, min/max/current
  (2190). Proposer : valeur magique avec `magic:true, magicContext:'number'` (le wiki dit
  « value can come from a variable via magic text ») → remplacer `field` par `field(...,{magic:true,magicContext:'number'})`.
- **P2-3 · Date/Time Picker** — cross-check des clés (`sceneCalendarConfig` vs
  `sceneDatePickerConfig`) entièrement géré (2148). Option « default date via magic text »
  à capturer.
- **P2-4 · Text Entry** — `inputType` INTEGER/DECIMAL (2192) ✓ ; ajouter « Force capital
  letters » / « Keyboard type » si la capture app le confirme ; `password` ✓.
- **P2-5 · Button** — couvrir « toggle boolean variable » de `renderVariableUpdateEditor`
  (1858) quand `type==='BooleanValue'` + `isToggle` ✓ ; ajouter note « separate Button
  actions when clicked (v5.56) » → `buttonClickConfig.actionBlockName` ✓ ; proposer la
  sélection multi-actions (les per-press individual actions sont App-side).
- **P2-6 · WebView** — éditeur HTML existant (`openWebViewHtmlEditor`) ; ajouter aperçu HTMl
  inline (iframe `srcdoc`) pour valider le contenu embarqué.
- **P2-7 · Icon** — catalogue d'icônes : saisie actuelle par `imageResourceName` (2221) ;
  proposer un mini-picker des icônes standards MacroDroid à partir de la ressource. Les noms
  de ressources venant de l'app (« macro_icon_XX ») peuvent être listés ; sinon rester en
  champ libre + note.
- **P2-8 · Table Layout** — largeurs de colonnes normalisées ✓ (`equalColumnWidths`) ;
  parser aussi `columnWidths` en entrée.

---

## 4. Priorité P3 — Outillage & UX du builder (zéro risque schema)

- **P3-1 · Guides & snapping au déplacement** : dans le preview, afficher des guides
  d'alignement (lignes pointillées) et un léger snap aux bords/centres quand on déplace un
  élément (`dragObject`/`pointermove` preview). Sans stockage : pure UX.
- **P3-2 · Panneau d'inspection « champs non édités »** : le builder préserve certains
  éléments read-only (2225). Lister, pour l'élément sélectionné, les clés présentes dans le
  JSON mais non exposées par l'éditeur (diff clés connues vs `Object.keys(c)`), avec
  possibilité de copier le JSON — aide à l'ajout d'éditeurs manquants.
- **P3-3 · Picker magic-text : libellés FR** (actuellement EN-only). `I18N_FR` translate
  déjà la plupart des labels UI ; étendre les labels des tokens du catalogue
  (`MAGIC_TEXT_OPTIONS` 719-945) via `t()` dans `pickerSection` (1621) ou une table dédiée
  optionnelle.
- **P3-4 · Couleurs : mémorisation du dernier hex / bouton récents** (forum). Améliorer
  `colorField` (1607) : préserver la luminosité, conserver une liste de couleurs récentes
  (localStorage `sb_recent_colors`), champs hex éditables (déjà) avec aperçu.
- **P3-5 · Raccourcis clavier supplémentaires** : dupliquer (Ctrl+D), renommer (F2),
  copier/coller (voir P1-5), verrouillage de sélection (Ctrl+L).
- **P3-6 · Histogramme/météo de schéma** : dans VALIDATE, ajouter info « N clés inconnues
  préservées » pour repérer les futures évolutions schema de l'app.
- **P3-7 · Harness de régression headless** : documenter/déplacer les tests de
  `harness_fr.js`/`p2`/`p6`/`p7` dans `tools/` du repo (actuellement `/tmp/opencode`) et
  ajouter une commande `npm`/`make check` qui extrait le `<script>` (comme
  `builder_v20_check.js`), vérifie la syntaxe (`node --check`) et exécute le round-trip
  corpus. (Note : Node n'est pas installé sur cette machine — cible à documenter.)
- **P3-8 · Fichier d'aide en ligne : catalogues** : intégrer la liste des ~225 tokens dans
  l'aide (sections 6-8 de Help) en table pliable.

---

## 5. Priorité P4 — Idées communauté / long terme (à valider avec le dev MacroDroid)

- **P4-1 · MCP (« Model Context Protocol ») pour l'action scene** (forum #2) : ne concerne
  pas directement le builder ; à noter pour informé « prompt » (`PROMPT`) plutôt que le
  format des scènes.
- **P4-2 · Radio selector** distinct (forum #3) : l'OptionSelector (single) couvre déjà ce
  comportement ; demander/confirmer un composant `SceneRadioGroup` séparé dans l'app si
  pertinent.
- **P4-3 · Sliders avec titre intégré** (forum #3) — propose une clé `title` sur
  `sceneSliderConfig` (capture à faire). Sinon : astuce note « utiliser un SceneText ».
- **P4-4 · Checkboxes peuplées depuis un dictionnaire** (forum #5 : dict → N checkboxes) :
  lié à P0-1 (repeat) — le dictionnaire alimente un layout répété de checkboxes ; mise en
  œuvre dépend de la spec repeat.
- **P4-5 · Renommage de variables côté app** (forum #3) : déjà géré dans le builder
  (`renameVariableDialog`) ; rien à faire ici.
- **P4-6 · « Custom Drawers » (scènes comme tiroirs)** : v5.56+ ; le builder exporte déjà
  des scènes ; documenter la compat Drawer dans l'aide et l'inspector (P3-2).
- **P4-7 · Animations entrée/sortie de composants** : pas encore dans le corpus ; tracker
  les changelogs ; si l'app les ajoute, suivre P3-2 pour les exposer quand les macros
  commencent à les contenir.

---

## 6. Processus recommandé

1. **Capture de référence** : pour chaque item « Spéc à confirmer » (P0-1, P0-2, P0-3,
   P1-2, P1-3, P4-3), créer un macro dans l'app, l'exporter, l'ajouter à
   `macro-reference/` et rédiger `DETAILS.md` + `ANALYSE.md` (round-trip).
2. **Ordre** : P0 puis P1 ; chaque MR = un seul item, avec test round-trip + note
   README.md + bump `BUILD_ID`/version (v20.2, v20.3…).
3. **Zéro invention de schéma** : toute clé écrite doit avoir été vue dans un `.macro`
   produit par l'app (politique actuelle du repo).
4. **MAJ de ce fichier** : cocher/retirer les items à mesure ; les nouveaux retours
   (issues, fil forum, changelogs) s'ajoutent en tête de P0.