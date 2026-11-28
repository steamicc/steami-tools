"""Décodage des trames BLE des thermo-hygromètres Xiaomi LYWSD03MMC.

Fonctionne sous MicroPython (carte STeaMi) comme sous CPython (tests).
Formats du micrologiciel pvvx (https://github.com/pvvx/ATC_MiThermometer) :
« custom » (pvvx), « atc1441 » et BTHome v2 ; le micrologiciel Xiaomi
d'origine (MiBeacon, chiffré) est seulement signalé.
"""

import math
import struct

UUID_ENV = 0x181A  # pvvx et atc1441
UUID_BTHOME = 0xFCD2
UUID_MIBEACON = 0xFE95

# BTHome v2 : taille des données de chaque objet, par identifiant
_TAILLES_BTHOME = {
    0x00: 1, 0x01: 1, 0x02: 2, 0x03: 2, 0x04: 3, 0x05: 3, 0x06: 2, 0x07: 2,
    0x08: 2, 0x09: 1, 0x0A: 3, 0x0B: 3, 0x0C: 2, 0x0D: 2, 0x0E: 2, 0x0F: 1,
    0x10: 1, 0x11: 1, 0x12: 2, 0x13: 2, 0x14: 2, 0x2E: 1, 0x2F: 1, 0x3A: 1,
    0x3F: 2, 0x40: 2, 0x41: 2, 0x42: 3, 0x43: 2, 0x44: 2, 0x45: 2, 0x46: 1,
    0x47: 2, 0x48: 2, 0x49: 2, 0x4A: 2, 0x4B: 3, 0x4C: 4, 0x4D: 4, 0x4E: 4,
    0x4F: 4, 0x50: 4, 0x51: 2, 0x52: 2,
}
for _i in range(0x15, 0x2E):  # capteurs binaires
    _TAILLES_BTHOME.setdefault(_i, 1)


def _mac(octets):
    return ":".join(f"{b:02X}" for b in octets)


def _donnees_service(trame):
    """Données de service (type AD 0x16) de la trame : liste de (uuid, données)."""
    resultat = []
    i = 0
    while i + 1 < len(trame):
        longueur = trame[i]
        if longueur == 0 or i + 1 + longueur > len(trame):
            break
        if trame[i + 1] == 0x16 and longueur >= 3:
            uuid = trame[i + 2] | (trame[i + 3] << 8)
            resultat.append((uuid, bytes(trame[i + 4 : i + 1 + longueur])))
        i += 1 + longueur
    return resultat


def _pvvx(d):
    t, h, mv, pourcent = struct.unpack("<hHHB", d[6:13])
    return {"format": "pvvx", "mac": _mac(d[5 - i] for i in range(6)), "temperature": t / 100, "humidite": h / 100,
            "batterie": pourcent, "tension": mv / 1000}


def _atc1441(d):
    t, h, pourcent, mv = struct.unpack(">hBBH", d[6:12])
    return {"format": "atc1441", "mac": _mac(d[0:6]), "temperature": t / 10, "humidite": float(h),
            "batterie": pourcent, "tension": mv / 1000}


def _bthome(d):
    if not d or d[0] & 0x01:  # vide ou chiffré
        return None
    m = {"format": "bthome", "mac": None, "temperature": None, "humidite": None, "batterie": None, "tension": None}
    i = 1
    while i < len(d):
        ident = d[i]
        taille = _TAILLES_BTHOME.get(ident)
        if taille is None or i + 1 + taille > len(d):
            break  # objet inconnu ou tronqué : on garde ce qui précède
        v = d[i + 1 : i + 1 + taille]
        if ident == 0x01:
            m["batterie"] = v[0]
        elif ident == 0x02:
            m["temperature"] = struct.unpack("<h", v)[0] / 100
        elif ident == 0x45:
            m["temperature"] = struct.unpack("<h", v)[0] / 10
        elif ident == 0x03:
            m["humidite"] = struct.unpack("<H", v)[0] / 100
        elif ident == 0x2E:
            m["humidite"] = float(v[0])
        elif ident == 0x0C:
            m["tension"] = struct.unpack("<H", v)[0] / 1000
        i += 1 + taille
    if m["temperature"] is None and m["humidite"] is None:
        return None
    return m


def decoder(trame):
    """Mesures d'une trame publicitaire, ou None si ce n'est pas un thermomètre lisible.

    Renvoie un dict : format, mac (None en BTHome : prendre l'adresse BLE),
    temperature (°C), humidite (% HR), batterie (%), tension (V).
    """
    for uuid, d in _donnees_service(trame or b""):
        if uuid == UUID_ENV and len(d) >= 15:
            return _pvvx(d)
        if uuid == UUID_ENV and len(d) >= 13:
            return _atc1441(d)
        if uuid == UUID_BTHOME:
            m = _bthome(d)
            if m:
                return m
        if uuid == UUID_MIBEACON:
            return {"format": "mibeacon"}
    return None


def _pression_saturante(t):
    """Pression de vapeur saturante (hPa) à t °C, formule de Magnus (Sonntag 1990)."""
    return 6.112 * math.exp(17.62 * t / (243.12 + t))


def humidite_ramenee(t_ref, h_ref, t_cible):
    """Humidité relative (%) qu'aurait l'air de la référence porté à t_cible °C.

    La quantité de vapeur ne change pas : seule la pression saturante suit la
    température. Sert à comparer l'humidité d'une carte qui s'échauffe à celle
    d'une référence restée à la température de la pièce. None si une mesure manque.
    """
    for v in (t_ref, h_ref, t_cible):
        if v is None or math.isnan(v):
            return None
    return h_ref * _pression_saturante(t_ref) / _pression_saturante(t_cible)

