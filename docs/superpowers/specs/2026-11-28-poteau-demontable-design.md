# Poteau démontable pour la potence photo

Date : 2026-11-28

## Intention

La hauteur entre l'objectif et la carte vient de cotes relevées sur photo et
d'une estimation de l'épaisseur de la carte. Si elle se révèle fausse de plus
que ce que rattrapent les cales (±2 mm), il faut aujourd'hui réimprimer tout
le pied (socle + montant, ~190 × 150 × 129 mm). Le but est de pouvoir
réimprimer seulement le poteau, sans toucher au socle.

## Objectifs, non-objectifs, anti-objectifs

Objectifs :

- le pied devient deux pièces : un **socle** et un **poteau** ;
- une correction de hauteur ne change que le poteau ;
- la position et la verticalité du poteau sont garanties par l'assemblage,
  sans réglage.

Non-objectifs : poteau réglable en hauteur (on perdrait la hauteur fixe
d'une séance à l'autre) ; changement du bras ou des cales.

Anti-objectifs : poteau qui prend du jeu ou penche ; socle qui ne repose
plus à plat sur la table (tête de vis qui dépasse) ; pièce dans le champ de
la caméra.

## Approches

1. **Semelle emboîtée et vissée (retenue par l'utilisateur).**
2. Queue d'aronde sans vis : écartée, le jeu d'impression la rend imprécise.
3. Poteau réglable avec serrage : écarté, la hauteur ne serait plus fixe.

## Conception retenue (validée le 2026-11-28)

- Le poteau se termine en bas par une **semelle** de 8 mm d'épaisseur qui
  porte aussi les deux nervures. Elle couvre l'emprise du montant et des
  nervures, avec des arêtes verticales arrondies.
- La semelle s'emboîte dans une **empreinte** de 5 mm de profondeur dans le
  dessus du socle, avec 0,2 mm de jeu : l'empreinte fixe la position et
  l'orientation. La verticalité vient de l'appui à plat du dessous de la
  semelle (imprimé contre le plateau) sur le fond de l'empreinte.
- Fixation par **4 vis M5 × 25 passées par le dessous du socle**, têtes dans
  des lamages pour que le socle reste à plat sur la table, et **écrous
  captifs dans la semelle**.
- `objectif_carte` (et toute cote de hauteur) ne change que le poteau ; le
  socle n'en dépend pas.
- STL : `socle.stl` (à plat, dessus vers le haut) et `poteau.stl` (debout sur
  sa semelle) remplacent `pied.stl`. Le bras et les cales ne changent pas.

## Choix de l'assistant

- Les 4 vis sont sous l'emprise du montant (deux rangées), et non sous les
  nervures : leur bout se loge dans un trou borgne du montant quelle que
  soit leur longueur, ce qui garde une seule longueur de vis (M5 × 25) pour
  toute la potence.
- Les écrous glissent dans des fentes ouvertes sur les faces latérales
  (±Y) de la semelle, avant la mise en place : une fois la semelle dans
  l'empreinte, la paroi de l'empreinte les retient.
- Le socle s'allonge de 4 mm derrière le montant pour fermer l'empreinte.
- La semelle dépasse de 3 mm au-dessus du socle, hors champ.

## Validation

Tests OpenSCAD : socle et poteau ne s'interpénètrent pas ; le poteau a moins
de 0,3 mm de jeu dans chaque direction ; écrous et vis passent jusqu'à leur
axe ; un `assert` sur la longueur de vis ; le socle rendu avec deux hauteurs
différentes donne le même STL ; rien dans le champ.
