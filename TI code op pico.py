import sys
import time
import select
from machine import *
import neopixel
import machine


np = neopixel.NeoPixel(machine.Pin(15), 8)
trigger_pin = Pin(13, Pin.OUT, value=0)
echo_pin = Pin(12, Pin.IN)

def set_neopixel(aantal):
    #Stel het aantal LEDs in.
    for i in range(0, aantal):
        np[i] = [255, 0, 0]
    for i in range(aantal, len(np)):
        np[i] = [0, 0, 0]
    np.write()

def afstad_sensor(threshold=20):
    """Meet afstand met ultrasone sensor en retourneer True als binnen drempel."""
    # Stuur triggerpuls
    trigger_pin.low()
    time.sleep_us(2)
    trigger_pin.high()
    time.sleep_us(10)
    trigger_pin.low()

    # Meet de tijd dat echo_pin hoog blijft
    timeout_start = time.ticks_us()
    while echo_pin.value() == 0:
        if time.ticks_diff(time.ticks_us(), timeout_start) > 10000:  # 10 ms timeout
            return False

    start_time = time.ticks_us()
    while echo_pin.value() == 1:
        if time.ticks_diff(time.ticks_us(), start_time) > 10000:  # 10 ms timeout
            return False

    end_time = time.ticks_us()


    duration = time.ticks_diff(end_time, start_time)
    distance = (duration * 0.0343) / 2

    return distance < threshold
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)


while True:
    #als de afstansensor een signaal oppakt print bij "BEWEGING"
    if afstad_sensor():
        print("BEWEGING")
        time.sleep(0.5)
    poll_results = poll_obj.poll(1)
    if poll_results:
        data = sys.stdin.readline().strip()
        #als er data is gelezen door de seriële port wordt de neopixel aangepast op basis van de data die binnen is gekomen
        if data.isdigit():
            value = int(data)
            if 1 <= value <= 5:
                set_neopixel(value)
            elif value == 9:
                set_neopixel(0)
