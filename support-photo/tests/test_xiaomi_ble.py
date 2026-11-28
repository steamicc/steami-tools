"""Décodage des trames BLE des thermo-hygromètres Xiaomi LYWSD03MMC (micrologiciel pvvx).

Les trames de test sont construites d'après les formats documentés par pvvx
(https://github.com/pvvx/ATC_MiThermometer) : « custom », « atc1441 » et BTHome v2.
"""

import struct
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "essais" / "reference_ble"))

from xiaomi_ble import decoder  # noqa: E402

MAC = bytes.fromhex("A4C138AABBCC")  # ordre d'affichage


def ad(type_ad, donnees):
    return bytes([len(donnees) + 1, type_ad]) + donnees


DRAPEAUX = ad(0x01, b"\x06")


def trame_pvvx(t_centiemes, h_centiemes, mv=2950, pourcent=87, compteur=5):
    # UUID 0x181A, MAC à l'envers, int16 t x0,01, uint16 h x0,01, uint16 mV, uint8 %, compteur, drapeaux
    corps = b"\x1a\x18" + MAC[::-1] + struct.pack("<hHHBBB", t_centiemes, h_centiemes, mv, pourcent, compteur, 0)
    return DRAPEAUX + ad(0x16, corps)


def trame_atc1441(t_dixiemes, h, pourcent=87, mv=2950, compteur=5):
    # UUID 0x181A, MAC dans l'ordre, int16 t x0,1 gros-boutiste, uint8 h, uint8 %, uint16 mV gros-boutiste, compteur
    corps = b"\x1a\x18" + MAC + struct.pack(">hBBHB", t_dixiemes, h, pourcent, mv, compteur)
    return DRAPEAUX + ad(0x16, corps)


def trame_bthome(objets, info=0x40):
    # UUID 0xFCD2, octet d'information (version 2, non chiffré), puis id + valeur
    return DRAPEAUX + ad(0x16, b"\xd2\xfc" + bytes([info]) + objets)


def test_pvvx():
    m = decoder(trame_pvvx(2143, 4567))
    assert m["format"] == "pvvx"
    assert m["temperature"] == pytest.approx(21.43)
    assert m["humidite"] == pytest.approx(45.67)
    assert m["batterie"] == 87
    assert m["mac"] == "A4:C1:38:AA:BB:CC"


def test_pvvx_temperature_negative():
    assert decoder(trame_pvvx(-512, 3000))["temperature"] == pytest.approx(-5.12)


def test_atc1441():
    m = decoder(trame_atc1441(214, 46))
    assert m["format"] == "atc1441"
    assert m["temperature"] == pytest.approx(21.4)
    assert m["humidite"] == pytest.approx(46)
    assert m["batterie"] == 87
    assert m["mac"] == "A4:C1:38:AA:BB:CC"


def test_bthome_centiemes():
    objets = bytes([0x00, 7, 0x01, 87]) + b"\x02" + struct.pack("<h", 2143) + b"\x03" + struct.pack("<H", 4567)
    objets += b"\x0c" + struct.pack("<H", 2950)
    m = decoder(trame_bthome(objets))
    assert m["format"] == "bthome"
    assert m["temperature"] == pytest.approx(21.43)
    assert m["humidite"] == pytest.approx(45.67)
    assert m["batterie"] == 87


def test_bthome_dixiemes_et_humidite_entiere():
    objets = b"\x45" + struct.pack("<h", -15) + bytes([0x2E, 52])
    m = decoder(trame_bthome(objets))
    assert m["temperature"] == pytest.approx(-1.5)
    assert m["humidite"] == pytest.approx(52)


def test_bthome_objet_inconnu_garde_ce_qui_precede():
    objets = b"\x02" + struct.pack("<h", 2000) + bytes([0xF0, 1, 2, 3])
    m = decoder(trame_bthome(objets))
    assert m["temperature"] == pytest.approx(20.0)
    assert m["humidite"] is None


def test_bthome_chiffre_ignore():
    assert decoder(trame_bthome(b"\x02\x00\x10", info=0x41)) is None


def test_mibeacon_d_origine_signale():
    # micrologiciel Xiaomi d'origine : UUID 0xFE95, données chiffrées
    m = decoder(DRAPEAUX + ad(0x16, b"\x95\xfe" + bytes(12)))
    assert m == {"format": "mibeacon"}


def test_autre_appareil():
    assert decoder(DRAPEAUX + ad(0x09, b"Casque")) is None
    assert decoder(b"") is None


def test_trame_tronquee():
    assert decoder(DRAPEAUX + ad(0x16, b"\x1a\x18" + MAC)) is None
