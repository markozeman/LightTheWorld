import pycom
import time
import lib.LTR329ALS01 as ltr
from network import Sigfox
import socket
from network import WLAN
import machine
import ubinascii
from mqtt import MQTTClient


def values2intensity(actual_value, setpoint, previous_intensity):
    min_val = 0
    max_val = 255
    print('actual_value', actual_value)
    print('setpoint', setpoint)
    error = setpoint - actual_value
    
    # to implement hysteresis for this control system
    # (avoid changes caused by noise when we are close to the setpoint)
    if (error < 10 and error > 0) or (error < 0 and error > -10):
        error = 0

    alpha = 1 # it can be changed if we want to increase/descease the artificial light more slowly
    intensity = ((error / setpoint)*alpha) * (max_val - min_val) + min_val + previous_intensity

    if intensity > max_val:
        intensity = max_val
    elif intensity < min_val:
        intensity = min_val 

    print('new_intensity: ', intensity)
    assert intensity >= min_val and intensity <= max_val
    return round(intensity)


def toHEX(intensity):
    return '0x%02x%02x%02x' % (0, 0, intensity)
    

pycom.heartbeat(False)
setpoint = 200
previous_intensity = 0
daylight_harvesting_on = True

def sub_cb(topic, msg):
    if ubinascii.hexlify(topic) == ubinascii.hexlify(topic_sub[0]):
        print(msg.decode('utf-8'))
        new_msg = msg.decode('utf-8')
        global daylight_harvesting_on
        daylight_harvesting_on = False
        pycom.rgbled(int(new_msg))

    if ubinascii.hexlify(topic) == ubinascii.hexlify(topic_sub[1]):
        global setpoint 
        print(msg.decode('utf-8'))
        setpoint = int(msg.decode('utf-8'))
    
    if ubinascii.hexlify(topic) == ubinascii.hexlify(topic_sub[2]):
        global daylight_harvesting_on
        print(msg.decode('utf-8'))
        daylight_harvesting_on = bool(msg.decode('utf-8'))

wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'AndroidAP':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'frac5380'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

machine_id = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(machine_id, "io.adafruit.com",user="ritap", password="557fecf3412746beb66657a6c49a7696", port=1883)

client.set_callback(sub_cb)
client.connect()
topic_sub=["ritap/feeds/rgb_website", "ritap/feeds/setpoint", "ritap/feeds/harvesting_bool"]
topic_length=len(topic_sub)

for i in range(0, topic_length):
    client.subscribe(topic=topic_sub[i])


while(True):
    light_sensor = ltr.LTR329ALS01().light() 
    channel_0, channel_1 = light_sensor

    avg = (channel_0 + channel_1) / 2

    new_intensity = values2intensity(avg, setpoint, previous_intensity)
    client.check_msg()

    new_val = toHEX(new_intensity)

    if daylight_harvesting_on:
        pycom.rgbled(int(new_val, 0))  
        previous_intensity = new_intensity 
    
    client.publish(topic="ritap/feeds/rgb_pycom", msg=str(new_intensity))
    time.sleep(3)



