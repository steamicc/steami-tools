// Pied (socle + montant) et assemblage. Nécessite parametres.scad, tete.scad, carte.scad.

assert(socle_epaisseur >= z_creux + fond_epaisseur, "creux sous la carte trop profond pour le socle");
assert(socle_xy[0] >= champ_xy[0] && socle_xy[1] >= champ_xy[1], "le socle ne couvre pas le champ");
assert(
    vis_longueur >= plot_hauteur + plateau_epaisseur - jonction_lamage[1] + jonction_ecrou_profondeur + ecrou_epaisseur + 1,
    "vis de jonction trop courte"
);
assert(x_montant - nervure[0] > champ_xy[0] / 2, "montant ou renforts dans le champ");

module socle() {
    translate([-socle_xy[0] / 2, -socle_xy[1] / 2, -socle_epaisseur])
        cube([x_dos + socle_xy[0] / 2, socle_xy[1], socle_epaisseur]);
}

module montant() {
    z_haut = z_appui_tete - plateau_epaisseur;   // dessous du bras
    difference() {
        union() {
            translate([x_montant, patte_decalage - jonction_largeur / 2, -socle_epaisseur])
                cube([x_dos - x_montant, jonction_largeur, z_haut + socle_epaisseur]);
            // renforts triangulaires côté carte
            for (dy = [-jonction_largeur / 2, jonction_largeur / 2 - nervure[2]])
                translate([x_montant, patte_decalage + dy, 0]) rotate([90, 0, 0]) mirror([0, 0, 1])
                    linear_extrude(nervure[2])
                        polygon([[0.01, 0], [-nervure[0], 0], [0.01, nervure[1]]]);
        }
        // dégagement pour le bout de la vis de la patte
        hull() for (dx = [-reglage_patte, reglage_patte])
            translate([x_trou + dx, patte_decalage, z_haut - 15]) cylinder(d = trou_diametre + 1, h = 16);
        // vis de jonction : trou et écrou captif (fente ouverte vers l'arrière, +X)
        for (dy = [-jonction_entraxe / 2, jonction_entraxe / 2])
            translate([x_trou, patte_decalage + dy, 0]) {
                translate([0, 0, z_haut - 30]) cylinder(d = trou_diametre, h = 31);
                translate([0, 0, z_ecrou_jonction]) ecrou_balaye(ecrou_plats + jeu_ecrou, ecrou_epaisseur + jeu_ecrou);
            }
    }
}

module batterie_logement() {
    translate([batterie_position[0], batterie_position[1], -(batterie[2] + 1)])
        cube([batterie[0] + 2, batterie[1] + 2, batterie[2] + 2]);
    // tunnel du fil, depuis le creux sous la carte
    translate([10, batterie_position[1] + batterie[1] / 2 + 1 - tunnel[0] / 2, -z_creux])
        cube([batterie_position[0] - 10 + 1, tunnel[0], tunnel[1]]);
}

module pied() {
    difference() {
        union() {
            socle();
            montant();
        }
        cuvette();
        batterie_logement();
    }
}

module bras() {
    empreinte_tete();
}

module potence() {
    pied();
    bras();
}

// Pyramide de vision : sommet sur l'objectif le plus haut, base = champ au sol.
module champ() {
    hull() {
        translate([0, 0, z_champ]) cube(0.01, center = true);
        translate([-champ_xy[0] / 2, -champ_xy[1] / 2, 0.01]) cube([champ_xy[0], champ_xy[1], 0.01]);
    }
}
