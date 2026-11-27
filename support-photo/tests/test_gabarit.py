"""Gabarit d'essai : empreinte de la tête et plot de la patte, posés à plat."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from openscad import ErreurOpenSCAD, bbox, rendre  # noqa: E402

PLATEAU_EPAISSEUR = 5
PATTE_HAUTEUR_PLOT = 22.5 - 7.5  # tete_epaisseur - patte_epaisseur


@pytest.fixture(scope="module")
def boite():
    return bbox(rendre("gabarit"))


def test_gabarit_se_rend(boite):
    assert boite is not None


def test_gabarit_couvre_la_tete(boite):
    (xmin, ymin, _), (xmax, ymax, _) = boite
    assert xmin <= -26.5 and xmax >= 130.5
    assert ymin <= -28 and ymax >= 28


def test_gabarit_mince(boite):
    (_, _, zmin), (_, _, zmax) = boite
    assert zmin == pytest.approx(0, abs=0.01)
    assert zmax - zmin <= PLATEAU_EPAISSEUR + PATTE_HAUTEUR_PLOT + 1


def test_assert_vis():
    with pytest.raises(ErreurOpenSCAD, match="Assertion"):
        rendre("gabarit", vis_longueur=12)


def test_passage_du_cable_ouvert():
    # rien ne doit rester dans le bord au droit de la patte, au-dessus de la face d'appui
    from openscad import est_vide

    assert est_vide("controle_cable")


def test_cable_descend_sous_la_fenetre():
    # le câble sort de la fenêtre de la patte vers le bas : le pont du plateau doit être percé
    from openscad import est_vide

    assert est_vide("controle_cable_bas")


def test_trous_de_jonction_traversants():
    # les deux vis M5 qui fixent le bras au montant traversent le plot de part en part
    from openscad import est_vide

    assert est_vide("controle_jonction")


def test_matiere_autour_des_trous_de_jonction():
    # le plot doit entourer chaque vis de jonction (couronne Ø 7 à Ø 11)
    from openscad import bbox, rendre

    (xmin, ymin, _), (xmax, ymax, _) = bbox(rendre("controle_jonction_matiere"))
    assert ymax - ymin >= 32 + 11 - 0.5  # les deux couronnes sont présentes
