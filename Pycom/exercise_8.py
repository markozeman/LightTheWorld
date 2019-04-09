import time
import machine
from machine import Pin, ADC
from lib.SI7006A20 import SI7006A20
from network import WLAN


w = WLAN(mode=WLAN.STA)
w.connect(ssid='lopy4-wlan-5978', auth=(WLAN.WPA2, 'www.pycom.io'), timeout=15000)
print(w.isconnected())



pin_19 = Pin('P19', mode=Pin.OUT)
pin_19.value(1)

adc = ADC(0)
adc_16 = adc.channel(pin='P16')

while True:
    print(adc_16())
    # print("temp " + SI7006A20.temperature())
    time.sleep(1)




