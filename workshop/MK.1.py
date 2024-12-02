import time
import machine
import neopixel
from game import random_game, like_to_dislike

np = neopixel.NeoPixel(machine.Pin(13), 8)
ir = machine.Pin(12, machine.Pin.IN)
knop = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

def kleuren(rgb):
    for i in range(8):
        np[i] = rgb
    np.write()

def neopixel_uit():
    for i in range(8):
        np[i] = [0, 0, 0]
    np.write()

def indicatie_ratio(ratio):
    leds = int(ratio // 20)
    neopixel_uit()
    for i in range(min(leds, 8)):
        np[i] = [0, 50, 0]
    np.write()

laatste_ir_waarde = 0

while True:
    if ir.value() == 1 and laatste_ir_waarde == 0:
        laatste_ir_waarde = 1
        neopixel_uit()
        game = random_game()
        if game:
            print(f"Nieuwe game gekozen: {game['name']}")
            ratio = like_to_dislike(game)
            print(f"Like-to-dislike ratio: {ratio:.2f}%")
            indicatie_ratio(ratio)
        time.sleep(1)

    if ir.value() == 0:
        laatste_ir_waarde = 0

    if knop.value() == 1:
        kleuren([0, 0, 50])
        time.sleep(0.5)

    neopixel_uit()
    time.sleep(0.1)
