"""Potence complète : socle, poteau (semelle + montant) et bras (empreinte de la tête)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from openscad import ErreurOpenSCAD, bbox, est_vide, facettes, rendre  # noqa: E402

PROFONDEUR_SOCLE = 14  # socle_epaisseur
Z_APPUI_TETE = 116 - 3 + 7  # objectif_carte - marge_cale + anneau_saillie (V1c posée : circuit à ~4 mm de la table)
BORD_HAUTEUR = 6
EMPREINTE = 5  # empreinte_profondeur : la semelle du poteau s'y emboîte


@pytest.fixture(scope="module")
def potence():
    return bbox(rendre("potence"))


def test_potence_se_rend(potence):
    assert potence is not None


def test_socle_couvre_le_champ(potence):
    # capteur_rotation = 90 : le grand côté du champ suit Y
    (xmin, ymin, _), (xmax, ymax, _) = potence
    assert xmin <= -57.5 and xmax >= 57.5
    assert ymin <= -75 and ymax >= 75


def test_hauteur(potence):
    (_, _, zmin), (_, _, zmax) = potence
    assert zmin == pytest.approx(-PROFONDEUR_SOCLE, abs=0.5)
    assert zmax >= Z_APPUI_TETE + BORD_HAUTEUR


def test_rien_dans_le_champ():
    assert est_vide("controle_champ")


def test_rien_dans_le_champ_tourne():
    assert est_vide("controle_champ", capteur_rotation=0)


def test_creux_trop_court():
    with pytest.raises(ErreurOpenSCAD, match="Assertion"):
        rendre("potence", carte_dessous=20)


def test_socle_pose_a_plat():
    (xmin, _, zmin), (xmax, _, zmax) = bbox(rendre("socle"))
    assert zmin == pytest.approx(0, abs=0.01)
    assert zmax == pytest.approx(PROFONDEUR_SOCLE, abs=0.01)
    # de -60 (bord côté opposé) à x_dos = 132,4, plus 4 mm derrière le poteau
    assert xmax - xmin == pytest.approx(60 + 132.4 + 4, abs=0.5)


def test_poteau_pose_a_plat():
    (_, _, zmin), (_, _, zmax) = bbox(rendre("poteau"))
    assert zmin == pytest.approx(0, abs=0.01)
    # du fond de l'empreinte (5 mm sous le dessus du socle) au dessous du bras
    assert zmax == pytest.approx(EMPREINTE + Z_APPUI_TETE - 5, abs=0.5)


@pytest.mark.parametrize("hauteur", [106, 126])
def test_socle_ne_depend_pas_de_la_hauteur(hauteur):
    # une correction de hauteur, de -10 à +10 mm, ne doit changer que le poteau
    assert facettes(rendre("socle")) == facettes(rendre("socle", objectif_carte=hauteur))


def test_semelle_dans_l_empreinte():
    assert est_vide("controle_semelle")


@pytest.mark.parametrize("decalage", [[0.3, 0], [-0.3, 0], [0, 0.3], [0, -0.3]])
def test_semelle_sans_jeu_excessif(decalage):
    # décalé de 0,3 mm dans n'importe quelle direction, le poteau touche le socle
    assert not est_vide("controle_jeu_semelle", decalage_controle=decalage)


def test_bras_pose_a_plat():
    (_, _, zmin), _ = bbox(rendre("bras"))
    assert zmin == pytest.approx(0, abs=0.01)


def test_gabarit_carte():
    # essai de la cuvette seule : toute la profondeur du socle, 6 mm autour de la carte
    (xmin, ymin, zmin), (xmax, ymax, zmax) = bbox(rendre("gabarit_carte"))
    assert zmin == pytest.approx(0, abs=0.01)
    assert zmax == pytest.approx(PROFONDEUR_SOCLE, abs=0.01)
    # carte 61,1 × 91,7 mm, grand côté sur Y (capteur_rotation = 90), plus 2 × 6 mm
    assert xmax - xmin == pytest.approx(61.1 + 12, abs=0.5)
    assert ymax - ymin == pytest.approx(91.7 + 12, abs=0.5)


def test_ecrous_glissent_jusqu_a_l_axe():
    # un écrou M5 (8 mm sur plats, plats face à ±Y) poussé dans chaque fente
    # depuis le bout ouvert doit atteindre l'axe de sa vis
    assert est_vide("controle_ecrous")


def test_vis_de_patte_ne_bute_pas_sur_le_montant():
    assert est_vide("controle_vis_patte")


def test_bord_tient_la_tete_avec_la_cale_max():
    with pytest.raises(ErreurOpenSCAD, match="Assertion"):
        rendre("gabarit", bord_hauteur=6, cale_epaisseur=5)


def test_place_des_connecteurs_grove():
    # V1b : les deux connecteurs Grove, sous la carte et au bord, ne doivent pas reposer sur le rebord
    assert est_vide("controle_grove")


def test_passage_usb_sous_le_circuit():
    # la fiche USB-C est branchée sous le circuit : le passage descend jusqu'à 6,5 mm sous le dessus
    assert est_vide("controle_usb")


def test_ecrous_du_pied_glissent_jusqu_a_l_axe():
    # écrou M5 (8 mm sur plats) poussé dans sa fente depuis la face latérale du poteau
    assert est_vide("controle_ecrous_pied")


def test_vis_du_pied_passent():
    # Ø 4,5 du dessous du socle jusqu'au bout de la vis M5 × 25
    assert est_vide("controle_vis_pied")


def test_tetes_de_vis_sous_le_socle():
    # têtes Ø 9 dans les lamages : le socle reste à plat sur la table
    assert est_vide("controle_tete_vis_pied")


def test_vis_du_pied_trop_courte():
    with pytest.raises(ErreurOpenSCAD, match="vis du pied trop courte"):
        rendre("socle", vis_pied_longueur=10)


def test_semelle_chanfreinee():
    # le premier couche s'écrase (pied d'éléphant) : un chanfrein évite qu'il bloque la semelle dans l'empreinte
    assert est_vide("controle_chanfrein_semelle")
