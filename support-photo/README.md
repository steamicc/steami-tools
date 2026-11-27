# Potence photo STeaMi

Potence imprimée en 3D qui tient la tête d'une caméra de document à 116 mm
au-dessus d'une carte STeaMi posée à plat. Chaque photo a ainsi le même
cadrage, et la carte se change en quelques secondes.

## Sommaire

- [Principe](#principe)
- [Matériel](#matériel)
- [Impression](#impression)
- [Montage](#montage)
- [Réglage de la hauteur](#réglage-de-la-hauteur)
- [Prise de vue](#prise-de-vue)
- [Modifier le modèle](#modifier-le-modèle)
- [Tests](#tests)

## Principe

La potence se compose de deux pièces assemblées une fois pour toutes :

- **le bras** (`stl/gabarit.stl`) : une empreinte de la tête de caméra. La
  tête y repose à plat, côté objectif, ce qui garantit son horizontalité.
  L'anneau lumineux passe par l'ouverture ronde. La patte de la tête est vissée
  sur le plot, avec un écrou captif.
- **le pied** (`stl/pied.stl`) : un socle qui remplit tout le champ de la
  caméra et sert de fond aux photos, et un montant qui porte le bras. La carte
  se pose dans une cuvette et repose par les bords du circuit sur un rebord.
  Le creux sous la carte loge les composants du dessous (buzzer de la
  V1c, connecteurs Grove de la V1b). Le
  câble USB-C sort par une rainure. La batterie LiPo se range dans une poche
  hors du champ, et son fil passe par un tunnel.

Le bras sert aussi de **gabarit d'essai** : l'imprimer en premier permet de
vérifier l'ajustement de la tête avant de lancer le pied, plus long à
imprimer. De même, `stl/gabarit-carte.stl` reproduit la cuvette seule (toute la
profondeur du socle, 6 mm autour de la carte) pour vérifier l'ajustement de la
carte.

Les cotes de la tête et de la carte, et leur origine, sont dans
[`releves.md`](releves.md). La conception est décrite dans
[`docs/superpowers/specs/2026-11-27-support-photo-design.md`](../docs/superpowers/specs/2026-11-27-support-photo-design.md).

## Matériel

- 3 vis M5 × 25 à tête cylindrique : une pour la patte, deux pour fixer le bras
  sur le montant ;
- 3 écrous M5 ;
- du filament **gris mat** pour le pied, qui sert de fond aux photos.

## Impression

| Pièce | Fichier | Position | Supports |
|---|---|---|---|
| Bras (gabarit) | `stl/gabarit.stl` | à plat, plateau sur le plateau d'impression | aucun |
| Pied | `stl/pied.stl` | debout, socle sur le plateau d'impression | aucun |
| Essai de la cuvette | `stl/gabarit-carte.stl` | à plat | aucun |
| Cales | `stl/cale-1.stl` à `stl/cale-5.stl` | à plat | aucun |

Les fentes des écrous et le tunnel de la batterie sont des ponts de moins de
9 mm. Le pied mesure environ 190 × 150 × 129 mm.

## Montage

1. Glisser un écrou M5 dans chacune des deux fentes du haut du montant
   (ouvertes vers l'arrière).
2. Poser le bras sur le montant, plot au-dessus du montant, et le fixer avec
   deux vis M5 × 25 par les deux trous lamés du plot.
3. Glisser un écrou M5 dans la fente au bout du plot.
4. Détacher la tête de caméra de son bras articulé. Poser la cale choisie
   dans l'empreinte (voir ci-dessous), puis la tête, objectif vers le bas,
   câble passé par l'ouverture du pont. Poser la rondelle de la cale sur le
   plot, sous la patte.
5. Visser la patte avec la troisième vis M5 × 25, sans forcer : la tête doit
   rester à plat dans l'empreinte.

## Réglage de la hauteur

La potence est dessinée pour 113 mm entre la face vitrée de l'objectif et le
dessus du circuit, sans cale. La **cale de 3 mm** donne la hauteur nominale de
116 mm, celle du cadrage d'origine (objectif à 120 mm de la table, circuit de
la V1c posée à ~4 mm). Les autres cales corrigent dans les deux sens, de 114 à
118 mm. Chaque cale comporte une plaque au contour de la tête et
une rondelle pour la patte, de même épaisseur.

Pour un écart de plus de 2 mm, modifier `objectif_carte` ou `marge_cale` dans
`scad/parametres.scad` et réimprimer.

## Prise de vue

La caméra apparaît comme `/dev/video4` (MJPEG jusqu'à 3264 × 2448). Garder
l'exposition automatique et laisser 60 images de chauffe :

```bash
ffmpeg -f v4l2 -input_format mjpeg -video_size 3264x2448 -i /dev/video4 \
  -vf "select=gte(n\,60),format=yuvj420p" -frames:v 1 -y photo.jpg
```

Le grand côté de l'image suit la carte. Le bout arrondi de la carte apparaît
à droite.

## Modifier le modèle

Le modèle est en OpenSCAD (version 2021.01). L'outil de contour et les tests
sont en Python 3 et demandent numpy, Pillow et pytest.


| Fichier | Rôle |
|---|---|
| `potence.scad` | point d'entrée : la variable `piece` choisit la pièce |
| `scad/parametres.scad` | toutes les cotes, avec leur origine |
| `scad/tete.scad` | empreinte de la tête (bras) |
| `scad/carte.scad` | placement de la carte et cuvette |
| `scad/potence_corps.scad` | pied, assemblage, champ de la caméra |
| `scad/cale.scad` | cales de hauteur |
| `scad/carte_contour.scad` | contour de la carte, généré |

Exporter une pièce :

```bash
openscad -o stl/pied.stl -D 'piece="pied"' potence.scad
openscad -o stl/cale-3.stl -D 'piece="cale"' -D cale_epaisseur=3 potence.scad
```

Des `assert()` arrêtent le rendu si une cote rend la pièce inutilisable : vis
trop courte, creux trop profond pour le socle, socle plus petit que le champ,
montant dans le champ.

Le contour de la carte vient du Gerber `donnees/STeaMi.GKO` du dépôt
[steami-reference-design](https://github.com/steamicc/steami-reference-design)
(licence BSD-2-Clause, voir `donnees/LICENCE-reference-design.txt`). Pour le
régénérer :

```bash
python3 outils/gerber_contour.py donnees/STeaMi.GKO scad/carte_contour.scad
```

## Tests

Les tests rendent chaque pièce avec OpenSCAD et vérifient les STL produits :
dimensions, passages du câble, trous de vis, cales, et surtout qu'**aucune
partie de la potence n'entre dans le champ de la caméra**.

```bash
pytest support-photo/tests -q
```

Prévoir environ deux minutes.
