# Test_Custom_Key1
Code to test my homemade Keyboard

🧩 PicoBoard Test — Matrice & Encodeurs

Ce projet permet de tester rapidement une carte personnalisée basée sur la Raspberry Pi Pico, équipée d’une matrice de boutons 4×4 et de plusieurs encodeurs rotatifs.

🎯 Objectif

Vérifier le bon câblage et le fonctionnement électrique :

chaque bouton de la matrice (détection d’appui et relâchement),

chaque encodeur (rotation dans les deux sens),

les pull-up internes et l’absence de court-circuit entre lignes/colonnes.

⚙️ Matériel

Raspberry RP2040
4 lignes + 4 colonnes de boutons (16 touches)
jusqu’à 4 encodeurs (A/B)
connexions directes GPIO ↔ boutons/encodeurs

🧠 Principe

Le firmware MicroPython :

balaye les lignes une par une (1 active = 0, les autres = 1) ;
lit les colonnes (pull-up activées) pour détecter les appuis ;
affiche les transitions DOWN / UP dans la console ;
surveille les encodeurs pour signaler +1 / −1 selon le sens de rotation.

🧪 Utilisation

Flasher MicroPython sur la Pico.
Ouvrir Thonny → interpréteur MicroPython (Raspberry Pi Pico).
Copier le fichier main.py
 sur la Pico.
Adapter les listes ROW_PINS, COL_PINS et ENCODERS selon ton schéma.
Exécuter le script.

Observer dans la console les lignes du type :
KEY r1 c2 -> DOWN
KEY r1 c2 -> UP
ENC1: +1
ENC1: -1
