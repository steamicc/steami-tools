// Potence photo STeaMi : point d'entrée.
// Choisir la pièce avec `piece`, par exemple :
//   openscad -o stl/gabarit.stl -D 'piece="gabarit"' potence.scad

piece = "gabarit";  // "gabarit" | "controle_cable" | "controle_cable_bas" | "controle_jonction" | "controle_jonction_matiere"

include <scad/parametres.scad>
include <scad/tete.scad>

if (piece == "gabarit") {
    // empreinte seule, posée à plat pour l'essai d'ajustement de la tête
    translate([0, 0, -(z_appui_tete - plateau_epaisseur)]) empreinte_tete();
} else if (piece == "controle_cable") {
    // volume du bord au droit de la patte : doit être vide (passage du câble)
    intersection() {
        empreinte_tete();
        translate([x_bord_patte, patte_decalage - patte_largeur / 2, z_appui_tete + 0.01])
            cube([jeu_tete + bord_epaisseur, patte_largeur, bord_hauteur]);
    }
} else if (piece == "controle_cable_bas") {
    // colonne sous la fenêtre de la patte : doit être vide (le câble descend)
    intersection() {
        empreinte_tete();
        translate([x_bord_patte + jeu_tete + bord_epaisseur + 2, patte_decalage - 4, 0])
            cube([8, 8, 200]);
    }
} else if (piece == "controle_jonction") {
    // axes des vis de jonction (Ø 4,5 dans des trous de 5,5) : doivent être vides
    intersection() {
        empreinte_tete();
        for (dy = [-jonction_entraxe / 2, jonction_entraxe / 2])
            translate([x_trou, patte_decalage + dy, 0]) cylinder(d = 4.5, h = 200);
    }
} else if (piece == "controle_jonction_matiere") {
    // couronnes autour des vis de jonction : doivent être pleines
    intersection() {
        empreinte_tete();
        for (dy = [-jonction_entraxe / 2, jonction_entraxe / 2])
            translate([x_trou, patte_decalage + dy, 0]) difference() {
                cylinder(d = 11, h = 200);
                translate([0, 0, -1]) cylinder(d = 7, h = 202);
            }
    }
} else {
    assert(false, str("pièce inconnue : ", piece));
}
