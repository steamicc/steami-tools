"""Aides de test : rendu OpenSCAD en ligne de commande et lecture des STL."""

import subprocess
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
POTENCE = RACINE / "potence.scad"


class ErreurOpenSCAD(Exception):
    pass


def _valeur(v):
    if isinstance(v, str):
        return f'"{v}"'
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


def _lancer(piece, params):
    sortie = Path(tempfile.mkdtemp(prefix="potence-")) / f"{piece}.stl"
    commande = ["openscad", "-o", str(sortie), "-D", f'piece="{piece}"']
    for cle, valeur in params.items():
        commande += ["-D", f"{cle}={_valeur(valeur)}"]
    commande.append(str(POTENCE))
    resultat = subprocess.run(commande, capture_output=True, text=True)
    return resultat, sortie


def rendre(piece, **params):
    """Rend une pièce en STL et renvoie son chemin ; lève ErreurOpenSCAD en cas d'échec."""
    resultat, sortie = _lancer(piece, params)
    if resultat.returncode != 0 or "ERROR" in resultat.stderr or "Assertion" in resultat.stderr:
        raise ErreurOpenSCAD(resultat.stderr)
    if not sortie.exists():
        raise ErreurOpenSCAD("aucun STL produit :\n" + resultat.stderr)
    return sortie


def est_vide(piece, **params):
    """Vrai si OpenSCAD ne produit aucune géométrie pour cette pièce."""
    resultat, sortie = _lancer(piece, params)
    if "ERROR" in resultat.stderr or "Assertion" in resultat.stderr:
        raise ErreurOpenSCAD(resultat.stderr)
    return "empty" in resultat.stderr.lower() or not sortie.exists() or bbox_ou_rien(sortie) is None


def bbox_ou_rien(stl):
    sommets = [
        tuple(float(v) for v in ligne.split()[1:4])
        for ligne in Path(stl).read_text().splitlines()
        if ligne.strip().startswith("vertex")
    ]
    if not sommets:
        return None
    return (
        tuple(min(s[i] for s in sommets) for i in range(3)),
        tuple(max(s[i] for s in sommets) for i in range(3)),
    )


def bbox(stl):
    """Boîte englobante ((xmin, ymin, zmin), (xmax, ymax, zmax)) d'un STL ASCII."""
    boite = bbox_ou_rien(stl)
    if boite is None:
        raise ErreurOpenSCAD(f"STL vide : {stl}")
    return boite
