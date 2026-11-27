"""Cales de hauteur : une plaque sous la tête et une rondelle sous la patte."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from openscad import bbox, est_vide, rendre  # noqa: E402


@pytest.mark.parametrize("e", [1, 2, 3, 4, 5])
def test_cale(e):
    (_, _, zmin), (_, _, zmax) = bbox(rendre("cale", cale_epaisseur=e))
    assert zmin == pytest.approx(0, abs=0.01)
    assert zmax - zmin == pytest.approx(e, abs=0.01)


def test_cale_laisse_voir_l_objectif():
    # la cale ne doit rien masquer dans l'ouverture de l'anneau
    assert est_vide("controle_cale_objectif", cale_epaisseur=3)


def test_vis_avec_cale_max():
    rendre("potence", cale_epaisseur=5)
