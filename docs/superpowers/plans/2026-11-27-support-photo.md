# Potence photo STeaMi — plan de réalisation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Une potence imprimée en 3D (OpenSCAD paramétrable) qui tient la tête de la caméra de document à 110 mm au-dessus d'une carte STeaMi posée à plat, pour des photos du wiki au cadrage identique.

**Architecture:** Un fichier de paramètres, un contour de carte généré depuis le Gerber, des modules OpenSCAD par partie (tête, carte, potence) et un fichier d'entrée qui choisit la pièce à produire (`piece = "gabarit" | "potence" | "cale" | "controle_champ"`). Les invariants géométriques sont des `assert()` OpenSCAD. Les tests pytest lancent `openscad` en ligne de commande et vérifient les STL produits.

**Tech Stack:** OpenSCAD 2021.01 (paquet Debian/Ubuntu `openscad`), Python 3 + pytest (sans autre dépendance), `ffmpeg` pour les captures de `/dev/video4`.

**Spec:** `docs/superpowers/specs/2026-11-27-support-photo-design.md`

## Global Constraints

- Tout se trouve dans `support-photo/` du dépôt `steamicc/steami-tools`, sur la branche `feat/support-photo`. Une issue et une PR sur `steamicc/steami-tools`.
- Textes (README, commentaires, messages de commit) en français. Commits au format conventionnel (`feat(support-photo): …`), sans ligne d'attribution.
- Unités en millimètres. Repère : origine sur l'axe optique, au niveau du **dessus du circuit** de la carte (z = 0). +X va de l'objectif vers la patte de la tête, donc vers le montant. +Z va vers le haut.
- Hauteur nominale : 110 mm entre la face vitrée de l'objectif et le dessus du circuit. La potence est dessinée pour 107 mm sans cale (`marge_cale = 3`), et la cale de 3 mm donne la hauteur nominale.
- Socle : il remplit tout le champ (au moins 150 × 115 mm, centré sur l'axe optique), et sa face supérieure sert de fond aux photos. Impression en filament gris mat.
- La carte est centrée sous l'objectif : centre de la boîte englobante du contour sur l'axe optique. Le paramètre `decalage_carte` permet de recentrer l'écran.
- La carte repose par les bords du circuit sur un rebord, au-dessus d'un creux qui loge 8,4 mm de composants (support CR2032). Rien ne s'appuie sur la pile.
- La tête repose à plat, côté objectif, dans une empreinte. La patte est fixée par une vis M5 et un écrou M5 captif, et bloquée en rotation par l'empreinte.
- Aucune partie de la pièce au-dessus de z = 0,01 ne doit entrer dans le champ de la caméra.

## Review Focus

1. **Cotes de la tête prises sur photo (±1,5 mm)** : la tête doit entrer dans l'empreinte sans jeu excessif. Couvert par le gabarit d'essai (tâche 3) avant toute impression longue.
2. **Pièce visible dans l'image** : le montant, les renforts ou le plateau ne doivent pas entrer dans le champ. Testé par `controle_champ` (tâche 4).
3. **Carte penchée** : la carte ne doit pas reposer sur son support de pile. Couvert par un `assert` sur la profondeur du creux (tâche 4).
4. **Vis trop courte ou écrou mal placé** : la vis doit traverser la patte, la cale et l'écrou avec au moins 1 mm de dépassement. Couvert par un `assert` (tâches 3 et 5).
5. **Câble USB-C ou fil de batterie qui force sur la carte** : les passages sont placés d'après les relevés de la tâche 1 et vérifiés sur la vraie carte (tâche 6).

---

### Task 1: Issue, outils et relevés manquants

**Files:**
- Create: `support-photo/releves.md`

**Interfaces:**
- Produces: les valeurs mesurées, reprises telles quelles dans `parametres.scad` (tâche 3) : `capteur_rotation`, `usb_angle`, `usb_largeur`, `fil_batterie_angle`, `batterie` (L × l × e), `fil_batterie_longueur`, `patte_epaisseur`, `patte_decalage`.

- [ ] **Step 1 : Créer l'issue** sur `steamicc/steami-tools`, avec pour titre « Potence imprimée pour photographier la carte STeaMi » et dans le corps un lien vers la spec. Noter son numéro.
- [ ] **Step 2 : Demander à l'utilisateur d'installer OpenSCAD** (`sudo apt install openscad`, ce qui demande son mot de passe), puis vérifier :
  Run : `openscad --version`
  Expected : `OpenSCAD version 2021.01`
- [ ] **Step 3 : Déterminer le sens du capteur.** Demander à l'utilisateur de poser la tête, objectif vers le bas, sur deux cales d'environ 10 cm, avec la patte orientée vers une pièce de monnaie posée sur la table. Capturer :
  `ffmpeg -hide_banner -loglevel error -f v4l2 -input_format mjpeg -video_size 3264x2448 -i /dev/video4 -vf "select=gte(n\,60),format=yuvj420p" -frames:v 1 -y capteur.jpg`
  Si la pièce apparaît sur un **petit** côté de l'image, alors `capteur_rotation = 0` (le grand côté de l'image suit X). Si elle apparaît sur un **grand** côté, alors `capteur_rotation = 90`. Noter aussi de quel côté elle apparaît : le côté opposé est celui où sortira le câble USB-C, loin du montant.
- [ ] **Step 4 : Relever la position du connecteur USB-C.** Repère : centre du demi-cercle du contour = origine du Gerber, axe +Y du Gerber vers le bout arrondi. Sur la capture `regle-full.jpg` (règle et carte, 23,2 px/mm, dans le scratchpad de la session de conception), ou sur une nouvelle capture prise avec la carte à plat et la règle, mesurer l'angle du câble par rapport à l'axe +Y (environ 23° sur la capture de conception) et la largeur de la fiche. Noter `usb_angle` (en degrés, sens trigonométrique, vu de dessus) et `usb_largeur` (largeur de la fiche + 2 mm).
- [ ] **Step 5 : Relever, avec l'utilisateur,** les dimensions de la LiPo, la longueur du fil, l'angle par lequel le fil sort sous la carte (`fil_batterie_angle`, même repère), l'épaisseur de la patte (environ 9 mm) et le côté de son décalage (environ 2,5 mm, du côté gauche vu côté boutons, patte en haut).
- [ ] **Step 6 : Écrire `support-photo/releves.md`** : un tableau valeur, source, date, avec les valeurs de la spec rappelées et les nouvelles.
- [ ] **Step 7 : Commit** `docs(support-photo): relevés de la tête, de la carte et du capteur`

### Task 2: Contour de la carte depuis le Gerber

**Files:**
- Create: `support-photo/donnees/STeaMi.GKO` (copie de `steamicc/steami-reference-design`, `Manufacturing/GERBER/STeaMi.GKO`)
- Create: `support-photo/donnees/LICENCE-reference-design.txt` (texte BSD-2-Clause du dépôt source, avec sa provenance)
- Create: `support-photo/outils/gerber_contour.py`
- Create: `support-photo/scad/carte_contour.scad` (généré, commité)
- Test: `support-photo/tests/test_gerber_contour.py`

**Interfaces:**
- Produces: `lire_segments(chemin: Path) -> list[Segment]`, `contour_exterieur(segments) -> list[tuple[float, float]]` (boucle fermée, sens trigonométrique, points tous les 0,2 mm au plus sur les arcs), `ecrire_scad(points, chemin: Path)`. Le fichier `carte_contour.scad` définit `carte_contour = [[x, y], …];` dans le repère Gerber (mm) et `carte_bbox = [[xmin, ymin], [xmax, ymax]];`.
- CLI : `python3 support-photo/outils/gerber_contour.py support-photo/donnees/STeaMi.GKO support-photo/scad/carte_contour.scad`

- [ ] **Step 1 : Écrire les tests**
  - `test_bbox` : la boîte englobante de `contour_exterieur` vaut X [-30,55 ; 30,55], Y [-61,08 ; 30,65] (à ±0,05).
  - `test_boucle_fermee` : premier point = dernier point à 0,01 près.
  - `test_trous_exclus` : aucun point du contour ne tombe à |x| < 10 et -20 < y < -5 (zone des découpes internes, autour de (0 ; -15)).
  - `test_aire` : l'aire (formule du lacet) est comprise entre 4500 et 5600 mm² et positive (sens trigonométrique).
- [ ] **Step 2 : Lancer les tests et vérifier qu'ils échouent.** Run : `pytest support-photo/tests/test_gerber_contour.py -v`. Expected : erreur d'import.
- [ ] **Step 3 : Implémenter.** Analyseur RS-274X minimal : `%FSLAX44Y44*%` et `%MOMM*%` (échelle 1e-4 mm), `G01`/`G02`/`G03` modaux, `G75` (arcs multi-quadrants, centre = point courant + I/J), `D01`/`D02`, en ignorant les régions `G36`/`G37`. Prendre tous les tracés quel que soit le diamètre d'outil. Chaîner les segments par extrémités (tolérance 0,01 mm) en boucles fermées, et garder celle dont l'aire absolue est la plus grande.
- [ ] **Step 4 : Lancer les tests et vérifier qu'ils passent**, puis générer `carte_contour.scad` avec la CLI.
- [ ] **Step 5 : Commit** `feat(support-photo): contour de la carte tiré du Gerber`

### Task 3: Paramètres, empreinte de la tête et gabarit d'essai

**Files:**
- Create: `support-photo/scad/parametres.scad`
- Create: `support-photo/scad/tete.scad`
- Create: `support-photo/potence.scad` (point d'entrée)
- Create: `support-photo/tests/openscad.py` (aides de test)
- Test: `support-photo/tests/test_gabarit.py`

**Interfaces:**
- Consumes : les valeurs de `releves.md` (tâche 1).
- Produces :
  - `parametres.scad`, avec ces noms exacts (valeurs de la spec, ou de `releves.md` quand elles sont plus précises) : `objectif_carte = 110; marge_cale = 3;` `tete_longueur = 111; tete_largeur = 55; tete_epaisseur = 19.5; tete_rayon = 27.5; objectif_depuis_bout = 26;` `anneau_diametre = 52; anneau_saillie = 7;` `patte_largeur = 18; patte_longueur = 45; patte_epaisseur = 9; patte_decalage = 2.5; trou_depuis_bout = 12; trou_diametre = 5.5;` `jeu_tete = 0.5; plateau_epaisseur = 5; bord_hauteur = 6; bord_epaisseur = 2.4;` `ecrou_plats = 8; ecrou_epaisseur = 4; jeu_ecrou = 0.3; vis_longueur = 20;` `ouverture_anneau = anneau_diametre + 3;` ainsi que les valeurs de la tâche 1.
  - Grandeurs dérivées (dans `parametres.scad`) : `z_objectif = objectif_carte - marge_cale` (107), `z_appui_tete = z_objectif + anneau_saillie` (face du corps côté objectif), `x_trou` = distance objectif → trou dans l'axe (= `tete_longueur - objectif_depuis_bout + patte_longueur - trou_depuis_bout`, ≈ 118, à comparer aux 117 mesurés).
  - `tete.scad` : `module empreinte_tete()` (plateau, bords, ouverture de l'anneau, plot de la patte avec trou et logement d'écrou), placée dans le repère global (objectif à l'origine en XY, face d'appui à `z_appui_tete`).
  - `potence.scad` : `piece = "gabarit";` sélectionne la pièce, et `include` les fichiers de `scad/`.
  - `tests/openscad.py` : `rendre(piece: str, **params) -> Path` (lance `openscad -o <tmp>.stl -D piece="…" [-D cle=valeur…] support-photo/potence.scad`, lève une exception si le code de retour est non nul ou si stderr contient `ERROR` ou `Assertion`), `bbox(stl: Path) -> tuple[tuple[float, float, float], tuple[float, float, float]]` (lecture des lignes `vertex` du STL ASCII), `est_vide(piece: str) -> bool` (vrai si OpenSCAD signale un objet vide).

- [ ] **Step 1 : Écrire les tests**
  - `test_gabarit_se_rend` : `rendre("gabarit")` ne lève pas d'exception.
  - `test_gabarit_couvre_la_tete` : l'étendue XY du gabarit couvre au moins `[-26.5, 130.5] × [-28, 28]`, c'est-à-dire le corps et la patte avec le jeu.
  - `test_gabarit_mince` : la hauteur Z du gabarit est ≤ `plateau_epaisseur + patte_hauteur_plot + 1`, où `patte_hauteur_plot = tete_epaisseur - patte_epaisseur` (≈ 10,5).
  - `test_assert_vis` : `rendre("gabarit", vis_longueur=12)` lève une exception, puisque l'assert de longueur de vis échoue.
- [ ] **Step 2 : Lancer les tests et vérifier qu'ils échouent.** Run : `pytest support-photo/tests/test_gabarit.py -v`
- [ ] **Step 3 : Implémenter `empreinte_tete()`.** Contour du corps : rectangle de `tete_largeur` × (`tete_longueur - tete_rayon`) prolongé par un demi-cercle de rayon `tete_rayon`, centré sur l'objectif. L'empreinte est ce contour décalé de `jeu_tete`, avec des bords de `bord_hauteur` sur tout le tour, sauf une ouverture de 12 mm au bout de la patte pour le câble. La patte est décalée de `patte_decalage` en Y. Le plot sous la patte fait `tete_epaisseur - patte_epaisseur` de haut. Logement d'écrou hexagonal (`ecrou_plats + jeu_ecrou`) ouvert par-dessous, à une profondeur telle que la vis dépasse de l'écrou d'au moins 1 mm. `assert(vis_longueur >= patte_epaisseur + <épaisseur vissée jusqu'au bas de l'écrou> + 1)`. Pour `piece = "gabarit"`, produire seulement l'empreinte et le plot, posés à plat (translatés à z = 0).
- [ ] **Step 4 : Lancer les tests et vérifier qu'ils passent.**
- [ ] **Step 5 : Exporter `support-photo/stl/gabarit.stl`.** Commit `feat(support-photo): empreinte de la tête et gabarit d'essai`.
- [ ] **Step 6 : Point d'arrêt avec l'utilisateur.** Il imprime le gabarit et essaie la tête, la vis M5 × 20 et l'écrou. Corriger les cotes de `parametres.scad` et `releves.md` d'après son retour, puis réimprimer jusqu'à ce que la tête entre sans forcer et sans jeu visible. Commit des corrections.

### Task 4: Potence complète (socle, cuvette, montant, plateau)

**Files:**
- Create: `support-photo/scad/carte.scad`
- Create: `support-photo/scad/potence_corps.scad`
- Modify: `support-photo/potence.scad` (nouvelles valeurs de `piece`)
- Modify: `support-photo/scad/parametres.scad`
- Test: `support-photo/tests/test_potence.py`

**Interfaces:**
- Consumes : `carte_contour`, `carte_bbox` (tâche 2) ; `empreinte_tete()`, `z_objectif`, `z_appui_tete`, `x_trou`, `rendre`, `bbox`, `est_vide` (tâche 3).
- Produces :
  - Paramètres : `pcb_epaisseur = 1.6; carte_dessous = 8.4; jeu_carte = 0.3; rebord = 2.5; fond_epaisseur = 3; socle_min = [150, 115]; champ_carte = [130, 98]; marge_champ = 3; decalage_carte = [0, 0];`
  - `carte.scad` : `module carte_placee()` place `carte_contour` centré sur l'axe optique (centre de `carte_bbox` + `decalage_carte`), le grand côté suivant le grand côté de l'image selon `capteur_rotation`, et le bout arrondi à l'opposé du montant. `module cuvette()` : creux au contour de la carte décalé de `jeu_carte`, sur `pcb_epaisseur` de profondeur, puis creux intérieur décalé de `-rebord`, sur `carte_dessous + 1` de profondeur. S'y ajoutent deux encoches pour les doigts sur les grands côtés, les passages USB-C (`usb_angle`, `usb_largeur`, débouchant au bord du socle) et le fil de batterie (`fil_batterie_angle`, vers la poche de batterie).
  - `potence_corps.scad` : `module potence()` = socle (face supérieure à z = 0, au moins `socle_min` autour de l'axe), moins `cuvette()` et la poche de batterie (hors champ, côté montant), plus le montant (sous le plot de la patte, au-delà de x = `champ_carte.x/2 + marge_champ` quand `capteur_rotation = 0`), plus un renfort triangulaire hors champ et `empreinte_tete()`.
  - `module champ()` : pyramide de sommet `[0, 0, z_objectif]` et de base le rectangle `champ_carte` à z = 0, agrandi de `marge_champ`, orienté selon `capteur_rotation`. La pyramide est prolongée jusqu'à z = 0,01, pour exclure la face du socle qui sert de fond.
  - Valeurs de `piece` : `"potence"`, et `"controle_champ"` = `intersection() { potence(); champ(); }`.
  - Assertions : profondeur sous le rebord ≥ `carte_dessous + 0.5` ; socle ≥ `socle_min` ; montant hors champ.

- [ ] **Step 1 : Écrire les tests**
  - `test_potence_se_rend` : `rendre("potence")` ne lève pas d'exception.
  - `test_socle_couvre_le_champ` : l'étendue XY du STL contient `[-75, 75] × [-57.5, 57.5]`.
  - `test_hauteur` : la boîte englobante en Z va de `-(pcb_epaisseur + carte_dessous + 1 + fond_epaisseur)` (à ±0,5) jusqu'à au moins `z_appui_tete + bord_hauteur`.
  - `test_rien_dans_le_champ` : `est_vide("controle_champ")` est vrai.
  - `test_rien_dans_le_champ_tourne` : `est_vide("controle_champ")` avec `capteur_rotation=90` est vrai aussi.
  - `test_creux_trop_court` : `rendre("potence", carte_dessous=20)` lève une exception, parce que l'assert de profondeur échoue avec le fond imposé. Ce test vérifie que l'assert est bien câblé.
- [ ] **Step 2 : Lancer les tests et vérifier qu'ils échouent.** Run : `pytest support-photo/tests/test_potence.py -v`
- [ ] **Step 3 : Implémenter** `carte.scad`, `potence_corps.scad` et les nouvelles valeurs de `piece`. Pour que la pièce s'imprime sans supports, le plateau en porte-à-faux s'appuie sur le montant et sur un renfort à 45°.
- [ ] **Step 4 : Lancer tous les tests et vérifier qu'ils passent.** Run : `pytest support-photo/tests -v`
- [ ] **Step 5 : Exporter `support-photo/stl/potence.stl`.** Commit `feat(support-photo): potence complète avec cuvette et socle`.

### Task 5: Cales, README et PR

**Files:**
- Create: `support-photo/scad/cale.scad`
- Create: `support-photo/README.md`
- Modify: `support-photo/potence.scad`
- Modify: `index.html` (lien vers le README sur GitHub, dans la liste existante)
- Test: `support-photo/tests/test_cale.py`

**Interfaces:**
- Consumes : `empreinte_tete()` et les paramètres de la tête (tâche 3).
- Produces : `module cale(e)` = une plaque au contour intérieur de l'empreinte (sans l'ouverture de l'anneau) plus une rondelle Ø 10 / Ø 5,5 pour la patte, toutes deux d'épaisseur `e`, posées à plat. `piece = "cale"` et `cale_epaisseur = 3;`.

- [ ] **Step 1 : Écrire les tests**
  - `test_cale` : pour `e` dans {1, 2, 3, 4, 5}, la hauteur Z de `rendre("cale", cale_epaisseur=e)` vaut `e` (±0,01).
  - `test_vis_avec_cale_max` : `rendre("potence", cale_epaisseur=5)` ne lève pas d'exception, avec `vis_longueur` réglée pour que la vis traverse encore l'écrou avec la cale de 5 mm. Si elle ne suffit pas, passer à 25 mm et l'indiquer dans le README.
- [ ] **Step 2 : Lancer les tests et vérifier qu'ils échouent.**
- [ ] **Step 3 : Implémenter `cale(e)`.** L'assert de vis tient compte de `cale_epaisseur`.
- [ ] **Step 4 : Lancer tous les tests et vérifier qu'ils passent.** Exporter `stl/cale-1.stl` à `stl/cale-5.stl`.
- [ ] **Step 5 : Écrire `README.md`** au ton neutre (infinitif), avec un sommaire : rôle de la pièce, matériel (vis M5 × 20 ou × 25, écrou M5, filament gris mat), impression (orientation, supports), montage, réglage de la hauteur avec les cales, régénération du contour et des STL, lancement des tests.
- [ ] **Step 6 : Commit** `feat(support-photo): cales de hauteur et documentation`. Pousser la branche, puis ouvrir la PR (« Closes #<issue> ») avec un résumé et la liste des tests. Ne pas la fusionner : c'est l'utilisateur qui fusionne.

### Task 6: Essai réel et réglage

**Files:**
- Modify: `support-photo/scad/parametres.scad`, `support-photo/releves.md`, `support-photo/README.md` (selon les résultats)

- [ ] **Step 1 : L'utilisateur imprime** la potence en gris mat et la cale de 3 mm, puis monte la tête et pose une carte allumée.
- [ ] **Step 2 : Capturer** avec la commande de la tâche 1 (step 3), avec 60 images de chauffe et l'exposition automatique.
- [ ] **Step 3 : Vérifier sur l'image :**
  - la carte est entière et centrée ;
  - aucun bord de pièce ni de table n'est visible ;
  - l'échelle au plan de la carte vaut environ 25,1 px/mm (23,2 × 119/110), à mesurer avec la règle posée sur la carte ;
  - aucun câble ne soulève la carte ;
  - la carte est bien à plat : l'échelle est la même aux deux bouts de la règle (à 1 % près) ;
  - le reflet de l'anneau lumineux sur l'écran est acceptable.
- [ ] **Step 4 : Corriger.** La hauteur se corrige par la cale (1 à 5 mm). Pour une erreur de plus de 2 mm, corriger `objectif_carte` ou `marge_cale`. Mettre à jour `releves.md` et le README (reflet, cale retenue).
- [ ] **Step 5 : Commit et push** des corrections sur la PR `fix(support-photo): réglages après le premier essai`.
