"""Gabarit d'essai : empreinte de la tête et plot de la patte, posés à plat."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from openscad import ErreurOpenSCAD, bbox, rendre  # noqa: E402

PLATEAU_EPAISSEUR = 5
PATTE_HAUTEUR_PLOT = 19.5 - 9  # tete_epaisseur - patte_epaisseur


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
