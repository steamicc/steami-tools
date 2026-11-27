// Empreinte de la tête de caméra : plateau, bords, ouverture de l'anneau,
// plot sous la patte avec trou M5 et logement d'écrou (ouvert sur +X),
// et deux trous M5 pour fixer le bras sur le montant.
// Nécessite parametres.scad.

assert(
    vis_longueur >= patte_epaisseur + cale_epaisseur + ecrou_profondeur + ecrou_epaisseur + 1,
    "vis trop courte : elle doit dépasser de l'écrou d'au moins 1 mm"
);

// Contour du corps, vu de dessus, objectif à l'origine.
module corps_2d() {
    centre = -objectif_depuis_bout + tete_rayon;
    hull() {
        translate([centre, 0]) circle(r = tete_rayon);
        translate([centre, -tete_largeur / 2]) square([x_bord_patte - centre, tete_largeur]);
    }
}

// Emprise du plot sous la patte (au-delà de la fenêtre du câble).
module plot_2d() {
    x0 = x_bord_patte + fenetre_patte;
    translate([x0, patte_decalage - jonction_largeur / 2])
        square([x_bout_patte + bord_epaisseur - x0, jonction_largeur]);
}

module ecrou_m5() {
    cylinder(d = (ecrou_plats + jeu_ecrou) / cos(30), h = ecrou_epaisseur + jeu_ecrou, $fn = 6);
}

module empreinte_tete() {
    z_bas = z_appui_tete - plateau_epaisseur;
    z_plot = z_appui_tete + plot_hauteur;
    difference() {
        union() {
            // plateau sous le corps, prolongé jusqu'au plot
            translate([0, 0, z_bas]) linear_extrude(plateau_epaisseur) {
                offset(r = jeu_tete + bord_epaisseur) corps_2d();
                plot_2d();
                translate([x_bord_patte, patte_decalage - patte_largeur / 2 - bord_epaisseur])
                    square([fenetre_patte, patte_largeur + 2 * bord_epaisseur]);
            }
            // bords autour du corps
            translate([0, 0, z_appui_tete]) linear_extrude(bord_hauteur) difference() {
                offset(r = jeu_tete + bord_epaisseur) corps_2d();
                offset(r = jeu_tete) corps_2d();
            }
            // plot sous la patte
            translate([0, 0, z_bas]) linear_extrude(z_plot - z_bas) plot_2d();
        }
        // ouverture de l'anneau lumineux
        translate([0, 0, z_bas - 1]) cylinder(d = ouverture_anneau, h = plateau_epaisseur + 2);
        // passage du câble : bord ouvert au droit de la patte
        translate([x_bord_patte - 1, patte_decalage - patte_largeur / 2 - 2, z_appui_tete])
            cube([jeu_tete + bord_epaisseur + 2, patte_largeur + 4, bord_hauteur + 1]);
        // passage du câble vers le bas, sous la fenêtre de la patte
        translate([x_bord_patte + jeu_tete + bord_epaisseur, patte_decalage - cable_passage / 2, z_bas - 1])
            cube([fenetre_patte - jeu_tete - bord_epaisseur - 3, cable_passage, plateau_epaisseur + 2]);
        // trou de vis, traversant
        translate([x_trou, patte_decalage, z_bas - 1]) cylinder(d = trou_diametre, h = z_plot - z_bas + 2);
        // trous des vis de jonction avec le montant
        for (dy = [-jonction_entraxe / 2, jonction_entraxe / 2])
            translate([x_trou, patte_decalage + dy, z_bas - 1]) cylinder(d = trou_diametre, h = z_plot - z_bas + 2);
        // logement d'écrou, ouvert vers le bout du plot (+X)
        translate([x_trou, patte_decalage, z_plot - ecrou_profondeur - ecrou_epaisseur - jeu_ecrou]) {
            rotate([0, 0, 30]) ecrou_m5();
            translate([0, -(ecrou_plats + jeu_ecrou) / 2, 0])
                cube([40, ecrou_plats + jeu_ecrou, ecrou_epaisseur + jeu_ecrou]);
        }
    }
}
