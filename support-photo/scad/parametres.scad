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

// --- Empreinte -----------------------------------------------------------
jeu_tete = 0.5;
plateau_epaisseur = 5;
bord_hauteur = 6;
bord_epaisseur = 2.4;

// --- Visserie M5 ---------------------------------------------------------
ecrou_plats = 8;
ecrou_epaisseur = 4;
jeu_ecrou = 0.3;
ecrou_profondeur = 3;           // matière entre le dessus du plot et l'écrou
vis_longueur = 20;              // sous tête (vis de la patte)
jonction_entraxe = 32;          // 2 vis M5 bras -> montant, de part et d'autre de la patte
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
