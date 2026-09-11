## Résumé

Décrivez brièvement le changement proposé.

## Issue(s) liée(s)

Fix #… / Closes #…

## Changements dans le schéma JSON

Listez les clés **nouvelles** ou **modifiées** et comment vous les avez validées
(ex. présente dans le corpus : `macro-reference/`, `docs/corpus_ANALYSE.md`,
`docs/corpus_DETAILS.md`). Rappel : aucune clé inventée sans preuve d'un `.macro` réel.

## Vérifications effectuées

- [ ] `VALIDATE` sans régression sur les scènes de test
- [ ] Round-trip : re-import d'un `.macro` du corpus sans altération
- [ ] Libellés FR et EN via `t()` (table `I18N_FR`)
- [ ] `v20/MacroDroid_Scene_Builder_v20.zip` régénéré (arcname intact)
- [ ] `BUILDER_VERSION` / `BUILD_ID` / README mis à jour si changement de version

## Notes pour la relecture

Points délicats à vérifier par l'admin, comportements limites éventuels.