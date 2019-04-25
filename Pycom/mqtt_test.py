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
    return '0x%02x%02x%02x' % (0, intensity, 0)
    

pycom.heartbeat(False)
setpoint = 200
previous_intensity = 0
# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

# make the socket blocking
s.setblocking(True)

# configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)


def sub_cb(topic, msg):
    if ubinascii.hexlify(topic) == ubinascii.hexlify(topic_sub[0]):
        print(msg.decode('utf-8'))
        new_msg = msg.decode('utf-8')
        pycom.rgbled(int(new_msg))  

    if ubinascii.hexlify(topic) == ubinascii.hexlify(topic_sub[1]):
        global setpoint 
        print(msg.decode('utf-8'))
        setpoint = int(msg.decode('utf-8'))

wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'AndroidAP':
        print('Network found!')
        #wlan.connect(net.ssid, auth=(WLAN.WPA2, 'frac5380'), timeout=5000)
        wlan.connect(net.ssid, auth=(net.sec, 'frac5380'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

machine_id = ubinascii.hexlify(machine.unique_id())
client = MQTTClient(machine_id, "io.adafruit.com",user="ritap", password="557fecf3412746beb66657a6c49a7696", port=1883)

client.set_callback(sub_cb)
client.connect()
topic_sub=["ritap/feeds/user", "ritap/feeds/setpoint"]
topic_length=len(topic_sub)

for i in range(0, topic_length):
    client.subscribe(topic=topic_sub[i])


count = 0
while(True):
    light_sensor = ltr.LTR329ALS01().light() 
    channel_0, channel_1 = light_sensor

    avg = (channel_0 + channel_1) / 2

    new_intensity = values2intensity(avg, setpoint, previous_intensity)
    new_val = toHEX(new_intensity)
    print()

    pycom.rgbled(int(new_val, 0))  
    previous_intensity = new_intensity 
    # send some bytes
    count = count + 1
    if count > 30:
        #s.send(bytes([new_intensity]))
        print("Sigfox")
        count = 0
    print(count)
    client.check_msg()
    time.sleep(1)

