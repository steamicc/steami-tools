// Potence photo STeaMi : point d'entrée.
// Choisir la pièce avec `piece`, par exemple :
//   openscad -o stl/gabarit.stl -D 'piece="gabarit"' potence.scad

piece = "potence";  // "bras" (= "gabarit") | "gabarit_carte" | "socle" | "poteau" | "potence" | "controle_champ"
//                     contrôles : "controle_cable" | "controle_cable_bas" | "controle_jonction" | "controle_jonction_matiere"

include <scad/parametres.scad>
include <scad/tete.scad>
include <scad/carte_contour.scad>
include <scad/carte.scad>
include <scad/potence_corps.scad>
include <scad/cale.scad>

if (piece == "gabarit" || piece == "bras") {
    // bras (empreinte de la tête), posé à plat : sert aussi de gabarit d'essai
    translate([0, 0, -(z_appui_tete - plateau_epaisseur)]) bras();
} else if (piece == "socle") {
    // socle, dessus vers le haut
    translate([0, 0, socle_epaisseur]) socle();
} else if (piece == "poteau") {
    // poteau debout sur sa semelle
    translate([0, 0, empreinte_profondeur]) poteau();
} else if (piece == "controle_semelle") {
    // semelle emboîtée dans le socle : doit être vide
    intersection() {
        socle();
        poteau();
    }
} else if (piece == "controle_jeu_semelle") {
    // poteau décalé de decalage_controle : touche le socle si le jeu est plus petit
    intersection() {
        socle();
        translate(decalage_controle) poteau();
    }
} else if (piece == "gabarit_carte") {
    // essai rapide de la cuvette : le socle réduit à 6 mm autour de la carte
    translate([0, 0, socle_epaisseur]) difference() {
        translate([0, 0, -socle_epaisseur]) linear_extrude(socle_epaisseur) offset(r = 6) carte_2d();
        cuvette();
    }
} else if (piece == "potence") {
    // assemblage en place, pour les contrôles
    potence();
} else if (piece == "cale") {
    // cale de hauteur (épaisseur cale_epaisseur), posée à plat
    cale(cale_epaisseur);
} else if (piece == "controle_cale_objectif") {
    // la cale dans l'ouverture de l'anneau : doit être vide
    intersection() {
        cale(cale_epaisseur);
        translate([0, 0, -1]) cylinder(d = anneau_diametre, h = 50);
    }
} else if (piece == "controle_champ") {
    // ce que la caméra verrait de la pièce au-dessus du fond : doit être vide
    intersection() {
        potence();
        champ();
    }
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
} else if (piece == "controle_ecrous") {
    // écrous poussés dans leurs fentes jusqu'à l'axe (et -1,5 mm pour celui de la patte)
    intersection() {
        potence();
        union() {
            translate([x_trou - reglage_patte, patte_decalage, z_ecrou_patte + 0.15])
                ecrou_balaye(8.0, ecrou_epaisseur);
            for (dy = [-jonction_entraxe / 2, jonction_entraxe / 2])
                translate([x_trou, patte_decalage + dy, z_ecrou_jonction + 0.15])
                    ecrou_balaye(8.0, ecrou_epaisseur);
        }
    }
} else if (piece == "controle_ecrous_pied") {
    // écrous du pied poussés dans leurs fentes jusqu'à l'axe, avant la pose : doit être vide
    intersection() {
        poteau();
        for (p = pied_vis) translate([p[0], p[1], z_ecrou_pied + 0.15]) rotate(p[1] > patte_decalage ? 90 : -90)
            ecrou_balaye(8.0, ecrou_epaisseur);
    }
} else if (piece == "controle_vis_pied") {
    // corps des vis du pied (Ø 4,5), du dessous du socle à leur bout : doit être vide
    intersection() {
        union() {
            socle();
            poteau();
        }
        for (p = pied_vis) translate([p[0], p[1], -socle_epaisseur - 1])
            cylinder(d = 4.5, h = z_tete_vis_pied + vis_pied_longueur + socle_epaisseur + 1);
    }
} else if (piece == "controle_tete_vis_pied") {
    // têtes des vis du pied (Ø 9) dans les lamages : doit être vide
    intersection() {
        socle();
        for (p = pied_vis) translate([p[0], p[1], -socle_epaisseur - 1]) cylinder(d = 9, h = pied_lamage[1] + 0.5);
    }
} else if (piece == "controle_vis_patte") {
    // sous la patte, le haut du montant doit laisser passer le bout de la vis
    intersection() {
        poteau();
        hull() for (dx = [-reglage_patte, reglage_patte])
            translate([x_trou + dx, patte_decalage, z_appui_tete - plateau_epaisseur - 12])
                cylinder(d = 4.5, h = 13);
    }
} else if (piece == "controle_fenetre") {
    intersection() {
        empreinte_tete();
        translate([x_bord_patte + fenetre_patte, patte_decalage - patte_largeur / 2, z_appui_tete + 0.01])
            cube([jeu_fenetre - 0.01, patte_largeur, plot_hauteur + 5]);
    }
} else if (piece == "controle_trou_patte") {
    intersection() {
        empreinte_tete();
        hull() for (dx = [-reglage_patte, reglage_patte])
            translate([x_trou + dx, patte_decalage, 0]) cylinder(d = 4.5, h = 200);
    }
} else if (piece == "controle_grove") {
    intersection() {
        socle();
        repere_carte() for (sx = [-1, 1])
            translate([sx > 0 ? grove_gerber[0][0] : -grove_gerber[1][0], grove_gerber[0][1], -(pcb_epaisseur + 7)])
                cube([grove_gerber[1][0] - grove_gerber[0][0], grove_gerber[1][1] - grove_gerber[0][1], 7 - 0.01]);
    }
} else if (piece == "controle_usb") {
    intersection() {
        socle();
        repere_carte() rotate(usb_angle) translate([-5, usb_rayon_depart + 1, -6.5]) cube([10, 20, 6.5]);
    }
} else {
    assert(false, str("pièce inconnue : ", piece));
}
