import pycom
import time

pycom.heartbeat(False)

while True:
    pycom.rgbled(0x00ff00)
    time.sleep(0.01)
    pycom.rgbled(0x000000)
    time.sleep(0.01)








