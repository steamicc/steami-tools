# Potence imprimée pour photographier la carte STeaMi

Date : 2026-11-27

## Intention

Les photos de la carte STeaMi V1c qui illustrent le wiki (série
`v1c-spleen-2026-11-27` : 8 photos 960 × 1280, recadrées en carrés de 480
centrés sur l'écran) sont prises avec une caméra de document à bras
articulé. Le cadrage varie d'une photo à l'autre : la carte se décale de
quelques millimètres et tourne légèrement, et le bras peut bouger entre deux
séances.

Le but est une pièce imprimée en 3D qui fixe la caméra et la carte l'une par
rapport à l'autre, pour que chaque photo du wiki ait exactement le même
cadrage, tout en permettant de changer de carte en quelques secondes.

## Objectifs, non-objectifs, anti-objectifs

Objectifs :

- même distance, même angle et même position de la carte à chaque photo ;
- caméra parfaitement horizontale (axe optique perpendiculaire à la carte) ;
- changement de carte rapide, sans outil ;
- cadrage identique au cadrage actuel ;
- modèle paramétrable, pour corriger les cotes après un essai.

Non-objectifs :

- montage pour la vérification automatique de l'écran par les sessions
  Claude (la carte partagée reste filmée comme aujourd'hui, hors potence) ;
- recadrage ou alignement par logiciel ;
- compatibilité avec d'autres cartes que la STeaMi V1 (le contour vient du
  Gerber VerB1, la V1c est la cible).

Anti-objectifs (échec même si la pièce « marche ») :

- tête de caméra qui bascule ou pivote : l'image n'est plus perpendiculaire
  ou le cadrage dérive ;
- carte posée sur son support de pile, donc penchée ;
- câble USB-C ou fil de batterie qui force sur la carte ou la soulève ;
- bord de la pièce visible dans le champ de la caméra.

## Contraintes et mesures

### Caméra

Caméra de document USB générique (Sunplus `1bcf:28c4`, `/dev/video4`,
MJPEG jusqu'à 3264 × 2448). La tête est détachée du bras et sera dédiée à
la potence (choix de l'utilisateur).

Cotes relevées sur photos avec une règle (incertitude ±1,5 mm) :

| Élément | Cote |
|---|---|
| Corps | ~111 × 55 mm, bout opposé à la patte en demi-cercle (rayon ~27,5 mm) |
| Épaisseur du corps | ~19,5 mm |
| Objectif | dans l'axe du corps, à ~85 mm du bord côté patte, ~26 mm du bout arrondi |
| Anneau lumineux (côté objectif) | Ø ~52 mm, centré sur l'objectif, dépasse de ~7 mm sous le corps |
| Patte de fixation | ~18 mm de large, ~45 mm de long, ~9 mm d'épaisseur, affleurant la face des boutons, décalée de ~2–3 mm par rapport à l'axe du corps |
| Trou de la patte | Ø ~5,5 mm (passage M5), lamé Ø ~10 mm, centre à ~12 mm du bout de la patte |
| Distance trou de patte → objectif | ~117 mm dans l'axe |
| Câble USB | sort par une fenêtre de la patte, côté corps |
| Vis d'origine | M5 × 12 environ, tête cylindrique fendue Ø ~8,5–9 mm |

L'anneau lumineux s'allume par une touche sensitive (icône d'empreinte) sur
sa face.

### Champ de la caméra

Mesuré au cadrage actuel, objectif à ~120 mm de la table, sur une règle
posée à plat (pleine résolution 3264 × 2448) : 23,2 px/mm, soit un champ de
140,6 × 105,4 mm. Angle de champ ≈ 61° × 47°.

### Carte

- Contour : `STeaMi.GKO` du dépôt `steamicc/steami-reference-design`
  (révision VerB1), 61,1 × 91,7 mm, encoches latérales et connecteur
  micro:bit compris. Le contour de la V1c concorde à la mesure sur photo
  (~62 mm sur la partie ronde).
- Épaisseur totale posée à plat, support de pile CR2032 compris : ~10 mm
  (estimation de l'utilisateur). Circuit supposé de 1,6 mm (à confirmer).
- Câble USB-C : sort par le bout arrondi de la carte.
- Fil de la batterie LiPo (rouge et noir) : part du dessous de la carte, vers
  un côté. La LiPo est posée à côté de la carte.

### Imprimante

Bambu Lab H2C. Volume d'impression non vérifié, mais largement supérieur à
la pièce (~150 mm de haut, socle ~250 × 120 mm) : impression en une pièce.

## Approches envisagées

1. **Potence qui porte la tête de caméra (retenue).** La tête est montée sur
   une pièce rigide au-dessus d'un logement pour la carte. Le bras articulé
   ne joue plus aucun rôle : la distance et l'angle sont fixés par la pièce.
   C'est la seule approche qui garantit un cadrage identique d'une séance à
   l'autre. Pièce plus haute et plus longue à imprimer.
2. **Plaque de base commune** au socle de la caméra et à la carte. Simple,
   mais le bras reste réglable : une articulation qui bouge décale tout le
   cadrage.
3. **Gabarit pour la carte seule et recadrage par logiciel.** Pièce la plus
   rapide, mais la perspective varie si le bras bouge, et le script est un
   développement à part entière.

L'utilisateur a choisi la potence (1), avec la tête détachée du bras.

## Conception retenue

### Ensemble

Une pièce en L (« potence ») : un socle qui porte le logement de la carte, un
montant vertical à une extrémité, et en haut un plateau horizontal en porte-
à-faux qui reçoit la tête de caméra au-dessus de la carte.

### Partie haute : empreinte de la tête (décision de l'utilisateur)

- Plateau horizontal en forme de la tête : la tête s'y pose côté objectif, à
  plat sur la face de son corps, et des bords de quelques millimètres
  l'entourent (empreinte). C'est le plateau, pas la vis, qui garantit
  l'horizontalité.
- Ouverture ronde (Ø ~55 mm) pour l'anneau lumineux. Le plateau fait ~5 mm
  d'épaisseur sous la tête : l'anneau dépasse encore de ~2 mm et rien ne
  masque le champ.
- Sous la patte, un plot (~10,5 mm, pour rattraper la différence de niveau
  entre la patte et la face du corps) avec un trou M5 et un écrou M5 captif
  par-dessous. La patte est solidarisée par une vis M5 (longueur à fixer
  selon l'épaisseur réelle de la patte et la position de l'écrou ;
  ~M5 × 20). La vis d'origine (~12 mm) est trop courte pour 9 mm de patte
  plus l'écrou.
- Passage pour le câble qui sort par la fenêtre de la patte.

### Hauteur

116 mm entre la face vitrée de l'objectif et le dessus du circuit de la
carte (objectif aujourd'hui à 120 mm de la table ; les 10 mm d'épaisseur de
la carte comprennent 6 mm de support d'écran au-dessus, donc le circuit de
la V1c posée est à ~4 mm de la table). Corrigé le 2026-11-27 : la première
version supposait 10 mm sous le circuit et donnait 110 mm. Le cadrage reste celui d'aujourd'hui : champ ≈ 137 × 103 mm
au niveau de la carte, la carte en occupe ~67 % × 59 %.

Choix de l'assistant : une cale ne peut que remonter la tête, donc la
potence est dessinée 3 mm plus basse (113 mm sans cale) et livrée avec des
cales de 1 à 5 mm à glisser entre l'empreinte et la tête (ou sous le plateau,
au choix du constructeur). La cale de 3 mm donne la hauteur nominale ; on
corrige dans les deux sens sans réimprimer la potence.

### Fond des photos (décision de l'utilisateur)

Le socle remplit tout le champ de la caméra et sert de fond aux photos :
au moins ~150 × 115 mm autour de la carte, centré sur l'axe optique, pour
qu'aucun bord de pièce ni la table n'apparaisse. Impression en **filament
gris mat** (proche de la table actuelle, sans reflets). Le montant est à
~117 mm de l'axe optique, hors du champ.

### Position de la carte

Choix de l'assistant (question posée, sans réponse explicite) : la carte est
centrée sous l'objectif. Le recadrage carré sur l'écran se fait alors à une
position fixe dans l'image. Le décalage carte/objectif est un paramètre du
modèle, pour centrer plutôt l'écran (≈16 mm vers le bout arrondi) si
l'utilisateur le préfère.

### Batterie

Choix de l'assistant : la LiPo ne doit pas apparaître sur les photos. Une
poche sur le socle, hors du champ, la reçoit, avec une rainure pour le fil
jusqu'à la cuvette. Dimensions de la batterie et longueur du fil à relever
à la construction.

### Logement de la carte

- Cuvette ouverte par le dessus plutôt qu'un tiroir (proposition de
  l'assistant, non contestée) : la carte se pose à la main sous la caméra
  (116 mm de dégagement), sans glissière qui prenne du jeu.
- Contour de la cuvette tiré du Gerber, avec un jeu de quelques dixièmes.
- La carte repose à plat par les bords du circuit sur un rebord, au-dessus
  d'un creux de ~10 mm qui loge les composants du dessous (support de pile
  CR2032 notamment). Rien ne force sur la pile.
- Deux encoches pour les doigts afin de saisir la carte.
- Passages pour le câble USB-C (bout arrondi) et le fil de batterie, sans
  qu'ils forcent sur la carte.
- Orientation : le grand côté de la carte suit le grand côté de l'image.

### Fichiers

- Modèle OpenSCAD paramétrable dans `steamicc/steami-tools`, dossier
  `support-photo/`, avec le contour de la carte converti depuis le Gerber.
- STL exportés pour la pièce complète et pour le gabarit d'essai.
- Une issue et une PR sur `steamicc/steami-tools`.

### Validation

1. Gabarit d'essai : seulement l'empreinte de la tête et le plot de la patte,
   quelques millimètres d'épaisseur (~15 min d'impression), pour vérifier
   l'ajustement des cotes prises sur photo avant la pièce complète.
2. Pièce complète, puis capture avec `/dev/video4` : la carte doit tenir dans
   le champ avec la même échelle qu'aujourd'hui (~23 px/mm au plan de la
   carte, ≈ 23,8 px/mm pour 116 mm), et aucun bord de la pièce ne doit être
   visible.
3. Réglage fin de la hauteur avec les cales de 1 à 5 mm, ou par le
   paramètre de hauteur.

## Laissé au constructeur

- Sens du capteur dans la tête (quel côté de l'image correspond à la patte) :
  à déterminer par une capture avant d'imprimer, pour orienter la cuvette.
- Position exacte du connecteur USB-C et de la sortie du fil de batterie :
  à relever sur une capture de référence ou dans les Gerber.
- Section du montant et renforts : assez rigides pour qu'une tête d'environ
  110 g (à estimer) en porte-à-faux de ~120 mm ne fléchisse pas.
- Orientation d'impression et supports.
- Jeux d'ajustement (empreinte, cuvette, écrou captif).

## Risques

- Reflet de l'anneau lumineux sur l'écran brillant : à vérifier au premier
  essai ; un diffuseur ou un pare-lumière imprimé pourra être ajouté.
- Cotes de la tête relevées sur photo (±1,5 mm) : couvert par le gabarit
  d'essai.
