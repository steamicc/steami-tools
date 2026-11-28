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
- [Essais des capteurs](#essais-des-capteurs)

## Principe

La potence se compose de trois pièces assemblées une fois pour toutes :

- **le bras** (`stl/gabarit.stl`) : une empreinte de la tête de caméra. La
  tête y repose à plat, côté objectif, ce qui garantit son horizontalité.
  L'anneau lumineux passe par l'ouverture ronde. La patte de la tête est vissée
  sur le plot, avec un écrou captif.
- **le poteau** (`stl/poteau.stl`) : il porte le bras. Il se termine en bas
  par une semelle emboîtée dans le socle et vissée par le dessous. C'est la
  seule pièce qui fixe la hauteur de la caméra : en cas d'erreur de hauteur,
  il suffit de le réimprimer.
- **le socle** (`stl/socle.stl`) : il remplit tout le champ de la caméra et
  sert de fond aux photos. La carte se pose dans une cuvette et repose par
  les bords du circuit sur un rebord.
  Le creux sous la carte loge les composants du dessous (buzzer de la
  V1c, connecteurs Grove de la V1b). Le
  câble USB-C sort par une rainure. La batterie LiPo se range dans une poche
  hors du champ, et son fil passe par un tunnel.

Le bras sert aussi de **gabarit d'essai** : l'imprimer en premier permet de
vérifier l'ajustement de la tête avant de lancer le socle et le poteau,
plus longs à imprimer. De même, `stl/gabarit-carte.stl` reproduit la cuvette seule (toute la
profondeur du socle, 6 mm autour de la carte) pour vérifier l'ajustement de la
carte.

Les cotes de la tête et de la carte, et leur origine, sont dans
[`releves.md`](releves.md). La conception est décrite dans
[`docs/superpowers/specs/2026-11-27-support-photo-design.md`](../docs/superpowers/specs/2026-11-27-support-photo-design.md).

## Matériel

- 7 vis M5 × 25 à tête cylindrique : une pour la patte, deux pour fixer le
  bras sur le poteau, quatre pour fixer le poteau sur le socle ;
- 7 écrous M5 ;
- du filament **gris mat** pour le socle, qui sert de fond aux photos.

## Impression

| Pièce | Fichier | Position | Supports |
|---|---|---|---|
| Bras (gabarit) | `stl/gabarit.stl` | à plat, plateau sur le plateau d'impression | aucun |
| Socle | `stl/socle.stl` | à plat, dessus vers le haut | aucun |
| Poteau | `stl/poteau.stl` | debout, semelle sur le plateau d'impression | aucun |
| Essai de la cuvette | `stl/gabarit-carte.stl` | à plat | aucun |
| Cales | `stl/cale-1.stl` à `stl/cale-5.stl` | à plat | aucun |

Les fentes des écrous et le tunnel de la batterie sont des ponts de moins de
9 mm, les plafonds des lamages sous le socle des ponts de 10 mm (lamages de
6 mm de profondeur pour des têtes de 5 mm). Le socle mesure environ 196 × 158 × 14 mm, le poteau environ
56 × 44 × 120 mm.

## Montage

1. Glisser un écrou M5 dans chacune des quatre fentes du bas du poteau
   (ouvertes sur les côtés), puis emboîter la semelle dans l'empreinte du
   socle. La paroi de l'empreinte retient les écrous.
2. Sans retourner l'ensemble, faire dépasser l'arrière du socle du bord de la
   table d'environ 30 mm, puis visser les quatre vis M5 × 25 par le dessous.
   Couché sur un côté, l'ensemble laisserait les écrous glisser hors de l'axe
   des vis. Les têtes se logent dans les lamages : le socle reste à plat sur
   la table.
3. Glisser un écrou M5 dans chacune des deux fentes du haut du poteau
   (ouvertes vers l'arrière).
4. Poser le bras sur le poteau, plot au-dessus du poteau, et le fixer avec
   deux vis M5 × 25 par les deux trous lamés du plot.
5. Glisser un écrou M5 dans la fente au bout du plot.
6. Détacher la tête de caméra de son bras articulé. Poser la cale choisie
   dans l'empreinte (voir ci-dessous), puis la tête, objectif vers le bas,
   câble passé par l'ouverture du pont. Poser la rondelle de la cale sur le
   plot, sous la patte.
7. Visser la patte avec une vis M5 × 25, sans forcer : la tête doit
   rester à plat dans l'empreinte.

## Réglage de la hauteur

La potence est dessinée pour 113 mm entre la face vitrée de l'objectif et le
dessus du circuit, sans cale. La **cale de 3 mm** donne la hauteur nominale de
116 mm, celle du cadrage d'origine (objectif à 120 mm de la table, circuit de
la V1c posée à ~4 mm). Les autres cales corrigent dans les deux sens, de 114 à
118 mm. Chaque cale comporte une plaque au contour de la tête et
une rondelle pour la patte, de même épaisseur.

Pour un écart de plus de 2 mm, modifier `objectif_carte` ou `marge_cale` dans
`scad/parametres.scad` et réimprimer **le poteau seul** : le socle ne dépend
pas de la hauteur. Il couvre le champ de la caméra jusqu'à
`objectif_carte = 126`, soit 10 mm de plus que la hauteur nominale ; au-delà,
un `assert` demande d'agrandir le socle.

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
| `scad/potence_corps.scad` | socle, poteau, assemblage, champ de la caméra |
| `scad/cale.scad` | cales de hauteur |
| `scad/carte_contour.scad` | contour de la carte, généré |

Exporter une pièce :

```bash
openscad -o stl/poteau.stl -D 'piece="poteau"' potence.scad
openscad -o stl/cale-3.stl -D 'piece="cale"' -D cale_epaisseur=3 potence.scad
```

Des `assert()` arrêtent le rendu si une cote rend la pièce inutilisable : vis
trop courte, creux trop profond pour le socle, socle plus petit que le champ,
poteau ou semelle dans le champ, empreinte du poteau sur la poche de batterie.

Le contour de la carte vient du Gerber `donnees/STeaMi.GKO` du dépôt
[steami-reference-design](https://github.com/steamicc/steami-reference-design)
(licence BSD-2-Clause, voir `donnees/LICENCE-reference-design.txt`). Pour le
régénérer :

```bash
python3 outils/gerber_contour.py donnees/STeaMi.GKO scad/carte_contour.scad
```

## Tests

Les tests rendent chaque pièce avec OpenSCAD et vérifient les STL produits :
dimensions, passages du câble, trous de vis, emboîtement du poteau, cales, et surtout qu'**aucune
partie de la potence n'entre dans le champ de la caméra**.

```bash
pytest support-photo/tests -q
```

Prévoir environ huit minutes.

## Essais des capteurs

Le dossier [`essais/`](essais/) rassemble des programmes pour la carte, à
lancer sous la potence afin de valider ses capteurs sur la photo :

- [`essais/reference_ble/`](essais/reference_ble/) : compare la température
  et l'humidité de la carte à celles d'un thermo-hygromètre Xiaomi
  LYWSD03MMC (micrologiciel pvvx) reçues par BLE.
