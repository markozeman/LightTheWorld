import pycom
import time
import lib.LTR329ALS01 as ltr

prev_light_sensor = ltr.LTR329ALS01().light() 
prev_channel_0, prev_channel_1 = prev_light_sensor

while(True):
    light_sensor = ltr.LTR329ALS01().light() 
    channel_0, channel_1 = light_sensor
    # print("Channel 0: %.1f\nChannel 1: %.1f\n" % (channel_0, channel_1))
    
    if prev_channel_0 != channel_0 or prev_channel_1 != channel_1:
        print()
    
    prev_channel_0 = channel_0
    prev_channel_1 = channel_1

    time.sleep(1)

    # print(timestamps)


