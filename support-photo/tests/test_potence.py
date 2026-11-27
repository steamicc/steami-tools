"""Potence complète : pied (socle + montant) et bras (empreinte de la tête)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from openscad import ErreurOpenSCAD, bbox, est_vide, rendre  # noqa: E402

PROFONDEUR_SOCLE = 1.6 + 8.4 + 1 + 3  # pcb + composants + 1 + fond
Z_APPUI_TETE = 110 - 3 + 7  # z_objectif + anneau_saillie
BORD_HAUTEUR = 6


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


def test_pied_pose_a_plat():
    (_, _, zmin), (_, _, zmax) = bbox(rendre("pied"))
    assert zmin == pytest.approx(0, abs=0.01)
    assert zmax == pytest.approx(PROFONDEUR_SOCLE + Z_APPUI_TETE - 5, abs=0.5)  # jusqu'au dessous du bras


def test_bras_pose_a_plat():
    (_, _, zmin), _ = bbox(rendre("bras"))
    assert zmin == pytest.approx(0, abs=0.01)
