"""Tests du contour de la carte tiré du Gerber STeaMi.GKO."""

import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "outils"))

from gerber_contour import contour_exterieur, lire_segments  # noqa: E402

GKO = RACINE / "donnees" / "STeaMi.GKO"


@pytest.fixture(scope="module")
def contour():
    return contour_exterieur(lire_segments(GKO))


def aire_signee(points):
    return 0.5 * sum(
        x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(points, points[1:])
    )


def test_bbox(contour):
    xs = [p[0] for p in contour]
    ys = [p[1] for p in contour]
    assert min(xs) == pytest.approx(-30.55, abs=0.05)
    assert max(xs) == pytest.approx(30.55, abs=0.05)
    assert min(ys) == pytest.approx(-61.08, abs=0.05)
    assert max(ys) == pytest.approx(30.65, abs=0.05)


def test_boucle_fermee(contour):
    (x0, y0), (x1, y1) = contour[0], contour[-1]
    assert abs(x0 - x1) < 0.01 and abs(y0 - y1) < 0.01


def test_trous_exclus(contour):
    assert not any(abs(x) < 10 and -20 < y < -5 for x, y in contour)


def test_aire(contour):
    aire = aire_signee(contour)
    assert 4500 < aire < 5600


def test_pas_des_arcs(contour):
    pas = max(
        ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        for (x0, y0), (x1, y1) in zip(contour, contour[1:])
    )
    # les segments droits du contour peuvent être longs ; on vérifie
    # seulement qu'il y a assez de points pour les arcs
    assert len(contour) > 300
    assert pas < 40
