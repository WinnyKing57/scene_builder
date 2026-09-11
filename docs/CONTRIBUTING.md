# Contributing — Guide du contributeur

Merci de vouloir contribuer au **MacroDroid Scene Builder**.
L'outil est un fichier HTML unique, hors-ligne et sans dépendance
(`v20/MacroDroid_Scene_Builder_v20.html`).

## Licence

Le projet est distribué sous **MIT License** (`LICENSE`) : vous pouvez utiliser,
modifier et redistribuer le code librement, sans demander d'autorisation.

## Gestion du dépôt

- **Admin unique** : `WinnyKing57` (propriétaire du dépôt).
- **Contributeurs** : accès **écriture (WRITE)** afin de pouvoir **créer des branches**
  dans le dépôt et les pousser.
- **Branche `main`** : **protection de branche** — personne ne pousse directement
  sur `main` ; toute modification passe par une **Pull Request** revue puis
  **fusionnée par l'admin** (`WinnyKing57`).

> Tant que le dépôt est **privé**, la protection serveur de `main` n'est pas
> activable (limitation GitHub Free). La règle « PR obligatoire » est donc de la
> discipline de chaque contributeur ; elle sera verrouillée côté serveur dès que
> le dépôt passera en **public**.

## Flux de travail

1. Récupérez le dépôt, puis créez une branche : `git checkout -b feat/my-change`.
2. Faites des commits **ciblés**, en anglais ou en français (voir « Style »).
3. Poussez : `git push -u origin feat/my-change`.
4. Ouvrez une **Pull Request** vers `main`.
5. **Validation** : l'admin (`WinnyKing57`) relit la PR puis la fusionne.
   Soyez prêt à ajuster après relecture.

## Règles essentielles du projet

- **Ne jamais inventer de schéma JSON** : toute clé écrite par le builder doit avoir été
  observée dans un `.macro` produit par l'application MacroDroid (voir
  `docs/feature_integration.md`, § « Politique — zéro invention de schéma »).
- **Ne jamais supprimer de clés inconnues** à l'import : préserver, pas réécrire
  (`guid`, `iconRes`, `lastRefreshValue`, clés futures de l'app…).
- La **source de vérité** est `v20/MacroDroid_Scene_Builder_v20.html`.
  Après toute modification : régénérer `v20/MacroDroid_Scene_Builder_v20.zip`
  (arcname `MacroDroid_Scene_Builder_v20.html`) et, s'il y a un changement de version,
  mettre à jour `BUILDER_VERSION`, `BUILD_ID` et le README.
- L'outil doit rester **hors-ligne, sans dépendance, sans réseau**.

## Style

- Recenser d'abord le comportement réel dans : `docs/feature_integration.md`,
  `docs/corpus_ANALYSE.md`, `docs/corpus_DETAILS.md`, `macro-reference/`.
- Suivre le style du code existant (fonctions `renderXxxProperties`, helpers
  `field/check/selectField/typedVarField/colorField`, `mutate()`/`pushUndo` pour toute
  modification, i18n via `t()`).
- Messages de commit concis, à la manière des commits existants (ex. `v20.1 : …`).

## Vérifications avant de proposer une PR

- `VALIDATE` ne signale pas de régression sur vos scènes de test.
- Round-trip : re-import d'un `.macro` du corpus **sans altération**
  (voir `harness_p6.js` — les stubs vivent généralement sous `/tmp/opencode`).
- FR et EN : les nouveaux libellés passent par `t()` et la table `I18N_FR`.

## Questions / sécurité

- Signaler les problèmes (bug, régression, problème de sérialisation) via une **issue**
  (modèle `.github/ISSUE_TEMPLATE/bug_report.md`).
- Ne jamais inclure de secret, token ou informations personnelles dans une PR.
- Pour remonter une faille avant publication : contact direct de l'admin
  (`WinnyKing57`) plutôt qu'une issue publique.