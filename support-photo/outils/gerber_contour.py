#!/usr/bin/env python3
"""Extrait le contour extérieur d'une carte depuis un Gerber de contour (RS-274X).

Usage : gerber_contour.py <fichier.GKO> <sortie.scad>

Le fichier OpenSCAD produit définit `carte_contour` (liste de points [x, y]
en mm, repère du Gerber, sens trigonométrique) et `carte_bbox`.
"""

import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ECHELLE = 1e-4  # %FSLAX44Y44*% et %MOMM*% : 4 décimales, en mm
PAS_ARC = 0.2  # mm, longueur maximale d'une corde sur les arcs


@dataclass
class Segment:
    """Un tracé du Gerber, déjà converti en polyligne."""

    points: list

    @property
    def debut(self):
        return self.points[0]

    @property
    def fin(self):
        return self.points[-1]


def _arc(x0, y0, x1, y1, cx, cy, sens):
    r = math.hypot(x0 - cx, y0 - cy)
    a0 = math.atan2(y0 - cy, x0 - cx)
    a1 = math.atan2(y1 - cy, x1 - cx)
    if sens == "G03":  # trigonométrique
        while a1 <= a0:
            a1 += 2 * math.pi
    else:  # G02, horaire
        while a1 >= a0:
            a1 -= 2 * math.pi
    n = max(2, math.ceil(abs(a1 - a0) * r / PAS_ARC))
    pts = [
        (cx + r * math.cos(a0 + (a1 - a0) * k / n), cy + r * math.sin(a0 + (a1 - a0) * k / n))
        for k in range(n + 1)
    ]
    pts[0], pts[-1] = (x0, y0), (x1, y1)
    return pts


def lire_segments(chemin):
    """Lit les tracés (D01) d'un Gerber, hors régions G36/G37."""
    texte = Path(chemin).read_text()
    commandes = [c.strip() for c in texte.replace("\r", "").replace("\n", "").split("*")]
    x = y = 0.0
    mode = "G01"
    region = False
    segments = []
    motif = re.compile(r"^(?:X(-?\d+))?(?:Y(-?\d+))?(?:I(-?\d+))?(?:J(-?\d+))?(D0[123])$")
    for c in commandes:
        if not c or c.startswith("%") or c.startswith("G04"):
            continue
        if c == "G36":
            region = True
            continue
        if c == "G37":
            region = False
            continue
        m = re.match(r"^(G0[123])(.*)$", c)
        if m:
            mode, c = m.group(1), m.group(2)
        m = motif.match(c)
        if not m:
            continue
        gx, gy, gi, gj, d = m.groups()
        nx = int(gx) * ECHELLE if gx else x
        ny = int(gy) * ECHELLE if gy else y
        if d == "D01" and not region:
            if mode == "G01":
                segments.append(Segment([(x, y), (nx, ny)]))
            else:
                cx = x + (int(gi) * ECHELLE if gi else 0.0)
                cy = y + (int(gj) * ECHELLE if gj else 0.0)
                segments.append(Segment(_arc(x, y, nx, ny, cx, cy, mode)))
        x, y = nx, ny
    return segments


RESOLUTION = 0.02  # mm par pixel pour la reconstruction du contour
LARGEUR_TRAIT = 0.3  # mm : referme les petits écarts entre tracés


def _aire(points):
    return 0.5 * sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(points, points[1:]))


def _masque_interieur(segments):
    """Image binaire de la carte : tout ce que l'extérieur ne peut pas atteindre.

    Les tracés du Gerber se chevauchent et laissent de petits écarts : on les
    dessine épais, on remplit l'extérieur depuis un coin, puis on rogne
    l'extérieur de la demi-largeur du trait pour revenir à l'axe des tracés.
    """
    xs = [p[0] for s in segments for p in s.points]
    ys = [p[1] for s in segments for p in s.points]
    marge = 1.0
    x0, y0 = min(xs) - marge, max(ys) + marge
    largeur = int((max(xs) - min(xs) + 2 * marge) / RESOLUTION) + 1
    hauteur = int((max(ys) - min(ys) + 2 * marge) / RESOLUTION) + 1

    def px(p):
        return ((p[0] - x0) / RESOLUTION, (y0 - p[1]) / RESOLUTION)

    image = Image.new("L", (largeur, hauteur), 0)
    dessin = ImageDraw.Draw(image)
    rayon = LARGEUR_TRAIT / 2 / RESOLUTION
    for s in segments:
        pts = [px(p) for p in s.points]
        dessin.line(pts, fill=255, width=max(1, round(2 * rayon)))
        for cx, cy in pts:
            dessin.ellipse([cx - rayon, cy - rayon, cx + rayon, cy + rayon], fill=255)
    ImageDraw.floodfill(image, (0, 0), 128)
    exterieur = np.asarray(image) == 128

    # rogner : dilater l'extérieur d'un disque de la demi-largeur du trait
    r = int(round(rayon))
    dilate = exterieur.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r:
                dilate |= np.roll(np.roll(exterieur, dy, axis=0), dx, axis=1)
    return ~dilate, (x0, y0)


def _suivre_bord(masque):
    """Suit le bord extérieur du masque (voisinage de Moore), en pixels (ligne, colonne)."""
    lignes, colonnes = np.nonzero(masque)
    i = np.lexsort((colonnes, lignes))[0]
    depart = (int(lignes[i]), int(colonnes[i]))
    voisins = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    bord = [depart]
    courant, direction = depart, 6  # on arrive par la gauche
    while True:
        for k in range(8):
            d = (direction + k) % 8
            ligne, colonne = courant[0] + voisins[d][0], courant[1] + voisins[d][1]
            if 0 <= ligne < masque.shape[0] and 0 <= colonne < masque.shape[1] and masque[ligne, colonne]:
                courant = (ligne, colonne)
                direction = (d + 5) % 8  # repartir juste après le pixel d'où l'on vient
                break
        else:
            break  # pixel isolé
        if courant == depart:
            break
        bord.append(courant)
    bord.append(depart)
    return bord


def _simplifier(points, epsilon):
    """Douglas-Peucker itératif."""
    garder = [False] * len(points)
    garder[0] = garder[-1] = True
    pile = [(0, len(points) - 1)]
    while pile:
        a, b = pile.pop()
        (xa, ya), (xb, yb) = points[a], points[b]
        dx, dy = xb - xa, yb - ya
        norme = math.hypot(dx, dy)
        dmax, imax = 0.0, None
        for i in range(a + 1, b):
            x, y = points[i]
            if norme:
                d = abs(dy * (x - xa) - dx * (y - ya)) / norme
            else:
                d = math.hypot(x - xa, y - ya)
            if d > dmax:
                dmax, imax = d, i
        if imax is not None and dmax > epsilon:
            garder[imax] = True
            pile += [(a, imax), (imax, b)]
    return [p for p, g in zip(points, garder) if g]


def contour_exterieur(segments):
    """Renvoie le contour extérieur de la carte : boucle fermée, sens trigonométrique."""
    if not segments:
        raise ValueError("aucun tracé dans le Gerber")
    masque, (x0, y0) = _masque_interieur(segments)
    bord = _suivre_bord(masque)
    points = [
        (x0 + colonne * RESOLUTION, y0 - ligne * RESOLUTION)
        for ligne, colonne in bord
    ]
    points = [(round(x, 4), round(y, 4)) for x, y in points]
    # Douglas-Peucker sur une boucle : couper en deux au point le plus éloigné du départ
    loin = max(range(len(points)), key=lambda i: math.dist(points[0], points[i]))
    contour = _simplifier(points[: loin + 1], RESOLUTION)[:-1] + _simplifier(points[loin:], RESOLUTION)
    if _aire(contour) < 0:
        contour = list(reversed(contour))
    return contour


def ecrire_scad(points, chemin):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    corps = ",\n".join(f"  [{x:.4f}, {y:.4f}]" for x, y in points[:-1])
    Path(chemin).write_text(
        "// Généré par outils/gerber_contour.py depuis donnees/STeaMi.GKO : ne pas modifier.\n"
        "// Repère du Gerber (mm) : centre du bout arrondi à l'origine, +Y vers le bout arrondi.\n"
        f"carte_bbox = [[{min(xs):.4f}, {min(ys):.4f}], [{max(xs):.4f}, {max(ys):.4f}]];\n"
        f"carte_contour = [\n{corps}\n];\n"
    )


def main(argv):
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    contour = contour_exterieur(lire_segments(argv[1]))
    ecrire_scad(contour, argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
