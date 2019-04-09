import pycom
import time
import lib.LTR329ALS01 as ltr

while(True):
    light_sensor = ltr.LTR329ALS01().light() 
    channel_0, channel_1 = light_sensor
    print("Channel 0: %.1f\nChannel 1: %.1f\n" % (channel_0, channel_1))
    time.sleep(2)

