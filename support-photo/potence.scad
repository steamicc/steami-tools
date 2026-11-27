// Potence photo STeaMi : point d'entrée.
// Choisir la pièce avec `piece`, par exemple :
//   openscad -o stl/gabarit.stl -D 'piece="gabarit"' potence.scad

piece = "gabarit";  // "gabarit" | "controle_cable"

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
} else {
    assert(false, str("pièce inconnue : ", piece));
}
