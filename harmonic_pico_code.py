# main.py — Test matrice 4x4 + encodeurs (MicroPython, Pico)
from machine import Pin
import time

# === CONFIG POUR LA BOARD ===
# Matrice 5x4 (la 5e ligne = boutons poussoirs des encodeurs)
ROW_PINS = [8, 9, 10, 11, 12]   # row0..row4
COL_PINS = [0, 1, 2, 3]         # col0..col3

# Rotation des encodeurs (A/B) — inchangé
ENCODERS = [
    (15, 16, "ENC1"),
    (17, 18, "ENC2"),
    (19, 20, "ENC3"),
    (21, 22, "ENC4"),
]


# === Paramètres ===
DEBOUNCE_MS = 20
SCAN_SLEEP_MS = 1
PRINT_ONLY_ON_CHANGE = True

# === Init Matrice ===
rows = [Pin(gpio, Pin.OUT, value=1) for gpio in ROW_PINS]  # au repos = 1
cols = [Pin(gpio, Pin.IN, Pin.PULL_UP) for gpio in COL_PINS]

key_state = [[False]*len(COL_PINS) for _ in range(len(ROW_PINS))]
key_changed_at = [[0]*len(COL_PINS) for _ in range(len(ROW_PINS))]

def read_key(r, c):
    # Met toutes les lignes au repos (1)
    for i, rp in enumerate(rows):
        rp.value(1)
    # Active une ligne (0)
    rows[r].value(0)
    return cols[c].value() == 0  # True si appuyé (contact à la masse)

# === Encodeurs ===
class Encoder:
    _transition = {
        (0,0,0,1): +1, (0,0,1,0): -1,
        (0,1,1,1): +1, (0,1,0,0): -1,
        (1,1,1,0): +1, (1,1,0,1): -1,
        (1,0,0,0): +1, (1,0,1,1): -1,
    }
    def __init__(self, pin_a, pin_b, name):
        self.a = Pin(pin_a, Pin.IN, Pin.PULL_UP)
        self.b = Pin(pin_b, Pin.IN, Pin.PULL_UP)
        self.name = name
        self.prev = (self.a.value(), self.b.value())
        self.acc = 0

    def poll(self):
        cur = (self.a.value(), self.b.value())
        trans = (self.prev[0], self.prev[1], cur[0], cur[1])
        if trans in self._transition:
            step = self._transition[trans]
            self.acc += step
            if self.acc >= 4:
                print(f"{self.name}: +1")
                self.acc = 0
            elif self.acc <= -4:
                print(f"{self.name}: -1")
                self.acc = 0
        self.prev = cur

encs = [Encoder(a, b, name) for (a, b, name) in ENCODERS]

# === Boucle principale ===
print("=== Test Matrice & Encodeurs (MicroPython) ===")
print("Appuie sur les touches, tourne les encodeurs.")

while True:
    now = time.ticks_ms()

    # Scan matrice
    for r in range(len(ROW_PINS)):
        for c in range(len(COL_PINS)):
            pressed = read_key(r, c)
            last = key_state[r][c]
            if pressed != last:
                t0 = key_changed_at[r][c]
                if time.ticks_diff(now, t0) >= DEBOUNCE_MS:
                    key_state[r][c] = pressed
                    key_changed_at[r][c] = now
                    if PRINT_ONLY_ON_CHANGE:
                        print(f"KEY r{r} c{c} -> {'DOWN' if pressed else 'UP'}")
            else:
                key_changed_at[r][c] = now

    # Poll encodeurs
    for e in encs:
        e.poll()

    time.sleep_ms(SCAN_SLEEP_MS)
