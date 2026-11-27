// Cale de hauteur : une plaque au contour du corps (ouverte sur l'anneau),
// glissée entre l'empreinte et la tête, et une rondelle de même épaisseur
// sous la patte. Nécessite parametres.scad et tete.scad.

module cale(e) {
    linear_extrude(e) {
        difference() {
            offset(r = jeu_tete - 0.3) corps_2d();
            circle(d = ouverture_anneau);
        }
        // rondelle de la patte, posée à côté
        translate([x_bord_patte + 25, -tete_largeur / 2 - 12]) difference() {
            circle(d = 10);
            circle(d = trou_diametre);
        }
    }
}
