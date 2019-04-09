import pycom 
from machine import UART

pycom.heartbeat(False)

uart = UART(1, 9600)                         # init with given baudrate
uart.init(9600, bits=8, parity=None, stop=1) # init with given parameters

'''
s = uart.readline()
print(s)

print(uart.any())

s2 = uart.read(10)
print(s2)
'''


if s == "red":
    pycom.rgbled(0xff0000)
elif s == "green":
    pycom.rgbled(0x00ff00)
elif s == "blue":
    pycom.rgbled(0x0000ff)
else:
    print('Incorrect colour.')





