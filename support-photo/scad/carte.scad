// Placement de la carte et cuvette du socle. Nécessite parametres.scad et carte_contour.scad.

carte_rotation = capteur_rotation == 90 ? 180 : 90;   // bout arrondi à l'opposé du montant ou de +Y
carte_centre = (carte_bbox[0] + carte_bbox[1]) / 2;

// Place des enfants exprimés dans le repère du Gerber.
module repere_carte() {
    translate(decalage_carte) rotate(carte_rotation) translate(-carte_centre) children();
}

module carte_2d() {
    repere_carte() polygon(carte_contour);
}

// Volume à retirer du socle (dessus du socle à z = 0).
module cuvette() {
    // logement du circuit : il repose sur le rebord à z = -pcb_epaisseur
    translate([0, 0, -pcb_epaisseur]) linear_extrude(pcb_epaisseur + 1) offset(r = jeu_carte) carte_2d();
    // creux sous la carte, pour les composants du dessous
    translate([0, 0, -z_creux]) linear_extrude(z_creux + 1) offset(r = -rebord) carte_2d();
    repere_carte() {
        // encoches pour les doigts
        for (sx = [-1, 1])
            translate([sx * doigt_gerber[0], doigt_gerber[1], -z_creux])
                cylinder(r = doigt_rayon, h = z_creux + 1);
        // place des connecteurs Grove (V1b) : rebord ouvert, sous le circuit seulement
        for (sx = [-1, 1])
            translate([sx > 0 ? grove_gerber[0][0] : -grove_gerber[1][0], grove_gerber[0][1], -z_creux])
                cube([grove_gerber[1][0] - grove_gerber[0][0], grove_gerber[1][1] - grove_gerber[0][1], z_creux - pcb_epaisseur]);
        // passage de la fiche USB-C, jusqu'au bord du socle
        rotate(usb_angle) translate([-usb_largeur / 2, usb_rayon_depart, -usb_profondeur])
            cube([usb_largeur, 200, usb_profondeur + 1]);
    }
}
