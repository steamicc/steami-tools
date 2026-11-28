# Poteau démontable Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Séparer le pied de la potence en un socle et un poteau vissés, pour réimprimer le poteau seul en cas d'erreur de hauteur.

**Architecture:** `scad/potence_corps.scad` remplace `pied()` par `socle()` (bloc, cuvette, batterie, empreinte, lamages) et `poteau()` (semelle, montant, nervures, écrous). `potence.scad` expose les pièces `socle` et `poteau` et de nouveaux contrôles ; les tests pytest les rendent avec OpenSCAD.

**Tech Stack:** OpenSCAD 2021.01, Python 3, pytest.

**Spec:** `docs/superpowers/specs/2026-11-28-poteau-demontable-design.md`

## Global Constraints

- Semelle 8 mm, empreinte 5 mm, jeu 0,2 mm ; 4 vis M5 × 25 par le dessous, têtes dans des lamages, écrous captifs dans la semelle.
- Le socle ne dépend d'aucune cote de hauteur.
- Rien dans le champ de la caméra (`controle_champ` vide, capteur à 90° et à 0°).
- Une seule longueur de vis : `vis_longueur = 25`.
- Textes en français, ton neutre ; commits sans ligne d'attribution.
- Les variables OpenSCAD sont évaluées dans l'ordre du fichier.

## Review Focus

- Tête de vis qui dépasse sous le socle : le socle doit rester à plat (lamage assez profond).
- Écrou qui ne descend pas jusqu'à l'axe de sa vis dans sa fente latérale.
- Bout de vis M5 × 25 qui bute dans le montant.
- Empreinte qui coupe la poche de batterie, son tunnel ou le bord du socle.
- Paroi trop fine entre deux fentes d'écrous, ou entre une fente et la face du montant.

---

### Task 1: Socle et poteau séparés, semelle emboîtée

**Files:**
- Modify: `support-photo/scad/parametres.scad`, `support-photo/scad/potence_corps.scad`, `support-photo/potence.scad`
- Test: `support-photo/tests/test_potence.py`

**Interfaces:**
- Produces: modules `socle()`, `poteau()`, `semelle_2d()` ; paramètres `semelle_epaisseur = 8`, `empreinte_profondeur = 5`, `jeu_semelle = 0.2`, `semelle_rayon = 1`, `socle_arriere = 4` ; pièces `"socle"`, `"poteau"`, `"controle_semelle"`, `"controle_jeu_semelle"` (paramètre `decalage_controle = [dx, dy]`).

- [ ] **Step 1: Tests qui échouent**

```python
def test_socle_pose_a_plat():
    (xmin, _, zmin), (xmax, _, zmax) = bbox(rendre("socle"))
    assert zmin == pytest.approx(0, abs=0.01)
    assert zmax == pytest.approx(PROFONDEUR_SOCLE, abs=0.01)
    assert xmax - xmin == pytest.approx(57.5 + 132.4 + 4, abs=0.5)

def test_poteau_pose_a_plat():
    (_, _, zmin), (_, _, zmax) = bbox(rendre("poteau"))
    assert zmin == pytest.approx(0, abs=0.01)
    assert zmax == pytest.approx(5 + Z_APPUI_TETE - 5, abs=0.5)  # fond d'empreinte -> dessous du bras

def test_socle_ne_depend_pas_de_la_hauteur():
    assert rendre("socle").read_bytes() == rendre("socle", objectif_carte=122).read_bytes()

def test_semelle_dans_l_empreinte():
    assert est_vide("controle_semelle")      # socle ∩ poteau

@pytest.mark.parametrize("decalage", [[0.3, 0], [-0.3, 0], [0, 0.3], [0, -0.3]])
def test_semelle_sans_jeu_excessif(decalage):
    assert not est_vide("controle_jeu_semelle", decalage_controle=decalage)
```

Remplacer `test_pied_pose_a_plat` par les deux tests de pose ; `controle_vis_patte` utilise `poteau()`, `controle_grove` et `controle_usb` utilisent `socle()`.

- [ ] **Step 2: Lancer, constater l'échec** — `pytest support-photo/tests/test_potence.py -q` → échecs « pièce inconnue ».
- [ ] **Step 3: Implémenter** — semelle : rectangle x ∈ [x_montant − nervure[0] − 3, x_dos], y = patte_decalage ± jonction_largeur/2, arrondi `semelle_rayon`, z ∈ [−empreinte_profondeur, −empreinte_profondeur + semelle_epaisseur] ; nervures posées sur la semelle ; montant depuis la semelle. Socle : bloc allongé de `socle_arriere` derrière x_dos, moins cuvette, batterie et `offset(r = jeu_semelle) semelle_2d()` sur `empreinte_profondeur`. `assert` : semelle hors champ, empreinte loin de la poche de batterie. Pièce `socle` posée dessus vers le haut, `poteau` posé sur sa semelle. `potence()` = socle + poteau + bras.
- [ ] **Step 4: Lancer, constater le succès** — même commande → PASS, puis la suite complète.
- [ ] **Step 5: Commit** — `feat(support-photo): socle et poteau séparés, semelle emboîtée`

### Task 2: Vis et écrous de la semelle, documentation, STL

**Files:**
- Modify: `support-photo/scad/parametres.scad`, `support-photo/scad/potence_corps.scad`, `support-photo/potence.scad`, `support-photo/README.md`, `support-photo/stl/`
- Test: `support-photo/tests/test_potence.py`

**Interfaces:**
- Consumes: `socle()`, `poteau()` de la tâche 1.
- Produces: `pied_vis` (4 positions [x, y]), `z_ecrou_pied`, `pied_lamage = [10, 5]` ; pièces `"controle_ecrous_pied"`, `"controle_vis_pied"`, `"controle_tete_vis_pied"`.

- [ ] **Step 1: Tests qui échouent**

```python
def test_ecrous_du_pied_glissent_jusqu_a_l_axe():
    assert est_vide("controle_ecrous_pied")    # écrou 8 mm sur plats poussé depuis la face ±Y

def test_vis_du_pied_passent():
    assert est_vide("controle_vis_pied")       # Ø 4,5 du dessous du socle au bout de la vis

def test_tetes_de_vis_sous_le_socle():
    assert est_vide("controle_tete_vis_pied")  # Ø 9, du dessous jusqu'à 0,5 mm sous le fond du lamage

def test_vis_du_pied_trop_courte():
    with pytest.raises(ErreurOpenSCAD, match="Assertion"):
        rendre("socle", vis_longueur=10)
```

- [ ] **Step 2: Lancer, constater l'échec.**
- [ ] **Step 3: Implémenter** — 4 vis sous le montant, deux rangées à 6 mm des faces avant et arrière, y = patte_decalage ± 10 ; dans le socle : trou Ø 5,5 et lamage Ø 10 × 5 par le dessous ; dans le poteau : trou jusqu'au bout de la vis + 1 mm, écrou à 3 mm au-dessus du fond de la semelle, fente `ecrou_balaye` tournée vers la face latérale la plus proche ; `assert` de longueur de vis.
- [ ] **Step 4: Lancer la suite complète** — `pytest support-photo/tests -q` → tout PASS.
- [ ] **Step 5: Régénérer les STL** — `socle.stl`, `poteau.stl` ; supprimer `pied.stl`. README : matériel (7 vis M5 × 25, 7 écrous), tableau d'impression, montage (écrous dans la semelle, poteau dans l'empreinte, vis par le dessous), paragraphe « Réglage de la hauteur » (réimprimer le poteau seul).
- [ ] **Step 6: Commit** — `feat(support-photo): fixation du poteau par 4 vis M5, STL et doc`
