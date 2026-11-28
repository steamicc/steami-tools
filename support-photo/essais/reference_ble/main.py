"""Référence BLE : la carte compare sa température et son humidité à celles
d'un thermo-hygromètre Xiaomi LYWSD03MMC (micrologiciel pvvx) posé près d'elle.

L'écran montre les deux mesures et leur écart. Une ligne CSV part sur le port
série toutes les PERIODE_CSV secondes, pour garder une trace de l'essai.

Choix du capteur : CIBLE vide prend le Xiaomi le plus proche (meilleur RSSI
vu depuis moins de OUBLI secondes) ; sinon, une adresse MAC ("A4:C1:38:...")
ou un nom BLE.
"""

import asyncio
import math
import time

import aioble
from steami import Humidity, Screen, Temperature
from steami_screen import DARK, GRAY, WHITE
from xiaomi_ble import decoder

CIBLE = ""          # "" : le plus proche ; sinon adresse MAC ou nom BLE
OUBLI = 30          # s : un capteur muet depuis plus longtemps n'est plus choisi
PERIODE_CSV = 5     # s
MAX_CAPTEURS = 20   # borne la mémoire si beaucoup de capteurs sont à portée

# L'écran d'abord : sa mémoire d'image est allouée à begin(), avant que le tas se fragmente.
ECRAN = Screen()
ECRAN.begin()

temperature = Temperature()
humidite = Humidity()
temperature.begin()
humidite.begin()

capteurs = {}  # adresse -> {"nom", "rssi", "vu", "m"}
debut = time.ticks_ms()


def maintenant():
    return time.ticks_diff(time.ticks_ms(), debut) // 1000


def noter(adresse, nom, rssi, m):
    if adresse not in capteurs and len(capteurs) >= MAX_CAPTEURS:
        plus_vieux = min(capteurs, key=lambda a: capteurs[a]["vu"])
        del capteurs[plus_vieux]
    nouveau = adresse not in capteurs
    c = capteurs.setdefault(adresse, {"nom": "", "rssi": rssi, "vu": 0, "m": None})
    if nom:
        c["nom"] = nom
    c["rssi"], c["vu"], c["m"] = rssi, maintenant(), m
    if nouveau:
        print("# capteur", adresse, nom or "?", m["format"], rssi, "dBm")


def choisir():
    vivants = [a for a in capteurs if maintenant() - capteurs[a]["vu"] <= OUBLI and capteurs[a]["m"].get("temperature") is not None]
    if CIBLE:
        cible = CIBLE.upper()
        for a in vivants:
            if a == cible or capteurs[a]["nom"].upper() == cible:
                return a
        return None
    return max(vivants, key=lambda a: capteurs[a]["rssi"]) if vivants else None


async def scanner():
    while True:
        # scan actif : la réponse au scan porte le nom BLE
        async with aioble.scan(1500, interval_us=30000, window_us=30000, active=True) as resultats:
            async for r in resultats:
                m = decoder(r.adv_data) or decoder(r.resp_data)
                if m is None:
                    continue
                adresse = m.get("mac") or r.device.addr_hex().upper()
                if m["format"] == "mibeacon":
                    if adresse not in capteurs:
                        print("# micrologiciel Xiaomi d'origine (chiffré, illisible) :", adresse)
                        capteurs[adresse] = {"nom": "", "rssi": r.rssi, "vu": maintenant(), "m": m}
                    continue
                noter(adresse, r.name(), r.rssi, m)
        await asyncio.sleep_ms(100)


def texte(s, y, couleur=WHITE):
    # centré : une cellule fait 8 px sur 128, 16 px (Spleen 8x16 x 2) sur 240
    largeur = len(s) * 8 * ECRAN.k
    ECRAN.text(s, ((ECRAN.width - largeur) // 2, ECRAN.u(y)), couleur)


def mesure(t, h):
    st = "--.-C" if t is None or math.isnan(t) else f"{t:.1f}C"
    sh = "--%" if h is None or math.isnan(h) else f"{h:.1f}%"
    return st + " " + sh


def nombre(v):
    return "" if v is None or math.isnan(v) else f"{v:.2f}"


def ecart(a, b, fmt):
    if a is None or b is None or math.isnan(a) or math.isnan(b):
        return "--"
    return fmt.format(a - b)


async def afficher():
    dernier_csv = -PERIODE_CSV
    print("t_s;adresse;rssi;format;T_ref;HR_ref;T_carte;HR_carte")
    while True:
        t_carte, h_carte = temperature.read(), humidite.read()
        a = choisir()
        ECRAN.clear()
        ECRAN.title("Reference BLE")
        texte("Carte", 30, GRAY)
        texte(mesure(t_carte, h_carte), 40)
        if a is None:
            texte("Xiaomi ?", 60, GRAY)
            texte("recherche...", 70, DARK)
        else:
            c = capteurs[a]
            m = c["m"]
            t_ref, h_ref = m.get("temperature"), m.get("humidite")
            texte(c["nom"] or a[-8:], 56, GRAY)
            texte(mesure(t_ref, h_ref), 66)
            texte("Ecart", 80, GRAY)
            texte(ecart(t_carte, t_ref, "{:+.1f}C") + " " + ecart(h_carte, h_ref, "{:+.1f}%"), 90)
            texte("{}dBm {}s".format(c["rssi"], maintenant() - c["vu"]), 104, DARK)
            if maintenant() - dernier_csv >= PERIODE_CSV:
                dernier_csv = maintenant()
                print(";".join((str(maintenant()), a, str(c["rssi"]), m["format"],
                                nombre(t_ref), nombre(h_ref), nombre(t_carte), nombre(h_carte))))
        ECRAN.show()
        await asyncio.sleep(1)


async def principal():
    await asyncio.gather(asyncio.create_task(scanner()), asyncio.create_task(afficher()))


asyncio.run(principal())
