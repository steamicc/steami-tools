// Socle, poteau (semelle + montant) et assemblage. Nécessite parametres.scad, tete.scad, carte.scad.

assert(socle_epaisseur >= z_creux + fond_epaisseur, "creux sous la carte trop profond pour le socle");
assert(socle_xy[0] >= champ_xy[0] && socle_xy[1] >= champ_xy[1], "le socle ne couvre pas le champ");
assert(
    vis_longueur >= plot_hauteur + plateau_epaisseur - jonction_lamage[1] + jonction_ecrou_profondeur + ecrou_epaisseur + 1,
    "vis de jonction trop courte"
);
assert(x_montant - nervure[0] > champ_xy[0] / 2, "montant ou renforts dans le champ");
assert(x_semelle - jeu_semelle > champ_xy[0] / 2, "semelle du poteau dans le champ");
assert(empreinte_profondeur < semelle_epaisseur && empreinte_profondeur <= socle_epaisseur - 8,
       "empreinte de la semelle trop profonde");
assert(
    patte_decalage + jonction_largeur / 2 + jeu_semelle + 2 <= batterie_position[1]
        || x_semelle - jeu_semelle - 2 >= batterie_position[0] + batterie[0] + 2,
    "empreinte de la semelle sur la poche de batterie"
);
assert(
    vis_pied_longueur >= z_ecrou_pied + ecrou_epaisseur + jeu_ecrou + 1 - z_tete_vis_pied,
    "vis du pied trop courte"
);
assert(
    z_tete_vis_pied + vis_pied_longueur + 2 < z_ecrou_jonction,
    "vis du pied trop longue"
);

module socle_bloc() {
    translate([-socle_xy[0] / 2, -socle_xy[1] / 2, -socle_epaisseur])
        cube([x_dos + socle_arriere + socle_xy[0] / 2, socle_xy[1], socle_epaisseur]);
}

// Emprise de la semelle du poteau (montant + nervures), arêtes verticales arrondies.
module semelle_2d() {
    translate([x_semelle, patte_decalage - jonction_largeur / 2])
        offset(r = semelle_rayon) offset(delta = -semelle_rayon)
            square([x_dos - x_semelle, jonction_largeur]);
}

module montant() {
    z_haut = z_appui_tete - plateau_epaisseur;   // dessous du bras
    z_dessus_semelle = z_semelle + semelle_epaisseur;
    difference() {
        union() {
            translate([0, 0, z_semelle]) linear_extrude(semelle_epaisseur) semelle_2d();
            // le montant part du dessus de la semelle : ses coins vifs ne débordent pas de l'empreinte
            translate([x_montant, patte_decalage - jonction_largeur / 2, z_dessus_semelle - 0.01])
                cube([x_dos - x_montant, jonction_largeur, z_haut - z_dessus_semelle + 0.01]);
            // renforts triangulaires côté carte, posés sur la semelle
            for (dy = [-jonction_largeur / 2, jonction_largeur / 2 - nervure[2]])
                translate([x_montant, patte_decalage + dy, z_dessus_semelle - 0.01]) rotate([90, 0, 0]) mirror([0, 0, 1])
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

module socle() {
    difference() {
        socle_bloc();
        cuvette();
        batterie_logement();
        // empreinte de la semelle du poteau
        translate([0, 0, z_semelle]) linear_extrude(empreinte_profondeur + 1) offset(r = jeu_semelle) semelle_2d();
        // vis du poteau, têtes dans des lamages par le dessous
        for (p = pied_vis) translate([p[0], p[1], -socle_epaisseur - 1]) {
            cylinder(d = trou_diametre, h = socle_epaisseur + 2);
            cylinder(d = pied_lamage[0], h = pied_lamage[1] + 1);
        }
    }
}

module poteau() {
    difference() {
        montant();
        for (p = pied_vis) translate([p[0], p[1], 0]) {
            // trou borgne jusqu'au bout de la vis + 1 mm
            translate([0, 0, z_semelle - 1])
                cylinder(d = trou_diametre, h = z_tete_vis_pied + vis_pied_longueur + 2 - z_semelle);
            // écrou captif, glissé depuis la face latérale la plus proche avant la pose
            translate([0, 0, z_ecrou_pied]) rotate(p[1] > patte_decalage ? 90 : -90)
                ecrou_balaye(ecrou_plats + jeu_ecrou, ecrou_epaisseur + jeu_ecrou);
        }
    }
}

module bras() {
    empreinte_tete();
}

module potence() {
    socle();
    poteau();
    bras();
}

// Pyramide de vision : sommet sur l'objectif le plus haut, base = champ au sol.
module champ() {
    hull() {
        translate([0, 0, z_champ]) cube(0.01, center = true);
        translate([-champ_xy[0] / 2, -champ_xy[1] / 2, 0.01]) cube([champ_xy[0], champ_xy[1], 0.01]);
    }
}
