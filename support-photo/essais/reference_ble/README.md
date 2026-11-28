# Référence BLE de température et d'humidité

Programme MicroPython pour la carte STeaMi. La carte lit sa température et
son humidité, puis les compare à celles d'un thermo-hygromètre Xiaomi
LYWSD03MMC posé près d'elle, reçues par BLE. L'écran montre les deux mesures
et leur écart, ce qui permet de valider les capteurs de la carte sur une
photo prise sous la potence.

## Sommaire

- [Prérequis](#prérequis)
- [Lancer l'essai](#lancer-lessai)
- [Lecture de l'écran](#lecture-de-lécran)
- [Journal CSV](#journal-csv)
- [Choisir le capteur](#choisir-le-capteur)
- [Précision attendue](#précision-attendue)
- [Tests](#tests)

## Prérequis

- Une carte STeaMi avec le firmware MicroPython STeaMi : `aioble`,
  `steami` et `steami_screen` y sont figés.
- Un LYWSD03MMC avec le micrologiciel
  [pvvx](https://github.com/pvvx/ATC_MiThermometer), dans l'un de ses trois
  formats de diffusion : « custom » (pvvx), « atc1441 » ou BTHome v2 non
  chiffré. Le micrologiciel Xiaomi d'origine chiffre ses données : le
  programme le signale sans pouvoir le lire.

## Lancer l'essai

Depuis ce dossier :

```bash
mpremote cp xiaomi_ble.py :
mpremote run main.py
```

`main.py` tourne sans être copié sur la carte ; seul le décodeur
`xiaomi_ble.py` doit y être. Laisser la carte et le capteur côte à côte
une dizaine de minutes avant de comparer : la carte s'échauffe en
fonctionnant, et les deux capteurs n'ont pas la même inertie.

## Lecture de l'écran

| Ligne | Contenu |
|---|---|
| Carte | température et humidité mesurées par la carte |
| nom du capteur | température et humidité reçues du Xiaomi |
| Ecart | carte moins référence |
| bas de l'écran | RSSI du capteur et âge de la dernière trame, en secondes |

« -- » signale une mesure absente : capteur de la carte qui ne répond pas, ou
format qui ne transmet pas l'humidité.

## Journal CSV

Le port série reçoit d'abord une ligne `# capteur ...` par thermomètre
découvert (adresse, nom, format, RSSI), puis toutes les 5 secondes :

```text
t_s;adresse;rssi;format;T_ref;HR_ref;T_carte;HR_carte
```

Pour l'enregistrer : `mpremote run main.py | tee essai.csv`.

## Choisir le capteur

Par défaut (`CIBLE = ""`), le programme suit le Xiaomi reçu avec le meilleur
RSSI parmi ceux entendus depuis moins de 30 secondes : en pratique, celui
posé contre la carte. Pour en imposer un, donner son adresse MAC ou son nom
BLE dans `CIBLE`, en tête de `main.py`.

## Précision attendue

Valeurs typiques des fiches techniques des fabricants, à confirmer par l'essai :

| Capteur | Température | Humidité |
|---|---|---|
| Xiaomi LYWSD03MMC (Sensirion SHTC3 sur la plupart des séries) | ±0,2 °C | ±2 % HR |
| STeaMi V1c (Bosch BME280) | ±0,5 °C (±1 °C sur la plage) | ±3 % HR |
| STeaMi V1a, V1b (Würth WSEN-HIDS) | ±0,2 °C | ±1,8 % HR |

Certaines séries récentes du LYWSD03MMC utilisent une autre puce, moins bien
documentée : la vérifier en ouvrant le boîtier.

## Tests

Le décodeur est testé sur PC avec des trames construites selon les formats
pvvx :

```bash
pytest support-photo/tests/test_xiaomi_ble.py -q
```
