# Relevés pour la potence photo

Valeurs utilisées dans `scad/parametres.scad`. Repère de la potence :
origine sur l'axe optique au niveau du dessus du circuit de la carte, +X de
l'objectif vers la patte de la tête (vers le montant), +Z vers le haut.
Repère du Gerber : centre du bout arrondi de la carte à l'origine, +Y vers le
bout arrondi, vu de dessus.

| Valeur | Mesure | Source | Date |
|---|---|---|---|
| Champ de la caméra | 140,6 × 105,4 mm, objectif à ~120 mm de la table (23,2 px/mm à 3264 × 2448) | capture d'une règle, graduations analysées | 2026-11-27 |
| Corps de la tête | ~111 × 55 mm, bout arrondi rayon ~27,5 mm | photos dessus et dessous avec règle | 2026-11-27 |
| Épaisseur du corps | ~22,5 mm (`tete_epaisseur`) ; une 1re estimation donnait 19,5 mm | 2e photo de profil, règle posée sur la tête (21,9 px/mm) | 2026-11-27 |
| Objectif | dans l'axe, à ~26 mm du bout arrondi, ~85 mm du bord côté patte | photo du dessous | 2026-11-27 |
| Anneau lumineux | Ø ~52 mm, dépasse de ~7 mm sous le corps | photos dessous et profil | 2026-11-27 |
| Patte | ~18 × 45 mm, affleure la face des boutons ; ~7,5 mm d'épaisseur à l'endroit du trou (`patte_epaisseur`), ~16,7 mm sur les 23 premiers mm depuis le corps, où passe le câble (`fenetre_patte`) | 2e photo de profil avec règle | 2026-11-27 |
| Décalage de la patte | ~2,5 mm vers la gauche, vu côté boutons patte en haut (`patte_decalage = 2.5`, vers +Y du repère de la potence) | photos dessus et dessous | 2026-11-27 |
| Trou de la patte | Ø ~5,5 mm, lamé Ø ~10 mm, centre à ~12 mm du bout | photo du dessus | 2026-11-27 |
| Vis d'origine | M5 × 12, tête cylindrique fendue Ø ~8,5–9 mm | photo avec règle | 2026-11-27 |
| Sens du capteur | grand côté de l'image perpendiculaire à l'axe de la tête : `capteur_rotation = 90` (le grand côté du champ suit Y) | capture avec une gomme posée côté patte : elle apparaît sur un grand côté | 2026-11-27 |
| Carte dans l'image | bout arrondi vers −Y, connecteur micro:bit vers +Y (Gerber tourné de 180°) | choix : même sens que les captures actuelles | 2026-11-27 |
| Fiche USB-C | à ~16° de l'axe +Y du Gerber, vers −X du Gerber (`usb_angle = 16`) ; passage de 14 mm (`usb_largeur`) | capture règle + carte | 2026-11-27 |
| Fil de batterie | sort sous la carte, côté connecteur micro:bit ; longueur 13 cm | captures et utilisateur | 2026-11-27 |
| Batterie LiPo | ~40 × 20 × 10 mm (`batterie = [40, 20, 10]`) | utilisateur | 2026-11-27 |
| Épaisseur de la carte (V1c) | 10 mm au total : support d'écran 6 mm dessus, circuit 1,6 mm, buzzer 3 mm dessous (composant le plus épais) | utilisateur | 2026-11-27 |
| Dessous de la V1b | deux connecteurs Grove au bord, de part et d'autre de la partie ronde (Gerber : 14 < \|x\| < 34, −21 < y < −3) ; prise USB-C sous le circuit | photo du dessous | 2026-11-27 |
| Hauteur objectif → carte | 116 mm jusqu'au dessus du circuit (objectif à 120 mm de la table, circuit de la V1c posée à 10 − 6 = 4 mm) | utilisateur + calcul | 2026-11-27 |
