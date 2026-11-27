// Paramètres de la potence photo STeaMi (mm). Sources : ../releves.md
// Repère : origine sur l'axe optique au niveau du dessus du circuit de la
// carte ; +X de l'objectif vers la patte de la tête (vers le montant) ; +Z en haut.

$fn = 96;

// --- Hauteur -------------------------------------------------------------
objectif_carte = 110;   // face vitrée de l'objectif -> dessus du circuit, avec la cale nominale
marge_cale = 3;         // la potence est dessinée plus basse d'autant ; la cale nominale la compense
cale_epaisseur = 0;     // cale glissée sous la tête (0 à 5 mm) : sert au calcul de la vis

// --- Tête de la caméra ---------------------------------------------------
tete_longueur = 111;
tete_largeur = 55;
tete_epaisseur = 22.5;           // photo de profil avec règle posée dessus (2e mesure)
tete_rayon = 27.5;              // bout arrondi, opposé à la patte
objectif_depuis_bout = 26;      // centre de l'objectif -> bout arrondi
anneau_diametre = 52;
anneau_saillie = 7;             // l'anneau dépasse sous la face du corps
ouverture_anneau = anneau_diametre + 3;

// --- Patte de fixation ---------------------------------------------------
patte_largeur = 18;
patte_longueur = 45;
patte_epaisseur = 7.5;          // partie percée, affleure la face des boutons
patte_decalage = 2.5;           // décalage de l'axe de la patte, vers +Y
trou_depuis_bout = 12;
trou_diametre = 5.5;
cable_passage = 12;             // largeur du passage du câble dans le pont du plateau
fenetre_patte = 23;             // partie épaisse de la patte (fenêtre du câble), depuis le corps
reglage_patte = 1.5;            // trou de patte oblong : ±1,5 mm selon X
jeu_fenetre = 1.5;              // jeu entre la partie épaisse de la patte et le plot

// --- Empreinte -----------------------------------------------------------
jeu_tete = 0.5;
plateau_epaisseur = 5;
bord_hauteur = 9;               // reste >= 4 mm de bord avec la cale de 5 mm
bord_epaisseur = 2.4;

// --- Visserie M5 ---------------------------------------------------------
ecrou_plats = 8;
ecrou_epaisseur = 4;
jeu_ecrou = 0.3;
ecrou_profondeur = 3;           // matière entre le dessus du plot et l'écrou
vis_longueur = 25;              // sous tête : M5 × 25 (patte avec la cale de 5 mm, et jonction)
jonction_entraxe = 30;          // 2 vis M5 bras -> montant, de part et d'autre de la patte
jonction_largeur = 44;          // largeur du plot et du dessus du montant (Y)

// --- Relevés de la tâche 1 ----------------------------------------------
capteur_rotation = 90;          // 90 : le grand côté de l'image suit Y
usb_angle = 16;                 // degrés, depuis +Y du Gerber vers -X du Gerber
usb_largeur = 14;
batterie = [40, 20, 10];

// --- Grandeurs dérivées --------------------------------------------------
z_objectif = objectif_carte - marge_cale;              // sans cale
z_appui_tete = z_objectif + anneau_saillie;             // face du corps côté objectif
x_bord_patte = tete_longueur - objectif_depuis_bout;    // bord du corps côté patte
x_trou = x_bord_patte + patte_longueur - trou_depuis_bout;
x_bout_patte = x_bord_patte + patte_longueur;
plot_hauteur = tete_epaisseur - patte_epaisseur;        // sous la patte, depuis la face d'appui

// --- Carte et socle (tâche 4) -------------------------------------------
pcb_epaisseur = 1.6;
carte_dessous = 8.4;            // composants sous la carte (support CR2032)
jeu_carte = 0.3;
rebord = 2.5;                   // largeur d'appui du circuit
fond_epaisseur = 3;
socle_epaisseur = 14;           // >= pcb + composants + 1 + fond
socle_min = [150, 115];         // [grand côté, petit côté] du champ, centré sur l'axe
decalage_carte = [0, 0];        // [x, y] : décaler la carte sous l'objectif
doigt_rayon = 9;                // encoches pour saisir la carte
doigt_gerber = [24.1, -40];     // bord de la carte (repère Gerber), symétrique en X
usb_profondeur = 5;
usb_rayon_depart = 26;          // depuis le centre du bout arrondi (repère Gerber)
batterie_position = [58, 30];   // coin de la poche (x, y), hors champ
tunnel = [8, 6];                // largeur, hauteur du tunnel du fil de batterie
nervure = [30, 40, 5];          // longueur, hauteur, épaisseur des renforts du montant
jonction_lamage = [10, 10];     // diamètre, profondeur du lamage des vis de jonction
jonction_ecrou_profondeur = 4;  // matière entre le dessus du montant et l'écrou

// --- Champ de la caméra -------------------------------------------------
champ_ref = [140.6, 105.4];     // mesuré à champ_ref_distance de l'objectif
champ_ref_distance = 119;
cale_max = 5;
marge_champ = 3;

z_creux = pcb_epaisseur + carte_dessous + 1;
z_champ = z_objectif + cale_max;                         // objectif le plus haut
champ_sol = champ_ref * z_champ / champ_ref_distance + [2, 2] * marge_champ;
champ_xy = capteur_rotation == 90 ? [champ_sol[1], champ_sol[0]] : champ_sol;
socle_xy = capteur_rotation == 90 ? [socle_min[1], socle_min[0]] : socle_min;
x_montant = x_bord_patte + fenetre_patte + jeu_fenetre; // face avant du montant et début du plot
x_dos = x_bout_patte + bord_epaisseur;                  // face arrière du montant

// --- Corrections après relecture ----------------------------------------
z_plot = z_appui_tete + plot_hauteur;
z_ecrou_patte = z_plot - ecrou_profondeur - ecrou_epaisseur - jeu_ecrou;
z_ecrou_jonction = z_appui_tete - plateau_epaisseur - jonction_ecrou_profondeur - ecrou_epaisseur - jeu_ecrou;
