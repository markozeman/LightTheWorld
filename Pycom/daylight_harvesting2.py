import pycom
import time
import lib.LTR329ALS01 as ltr


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

while(True):
    light_sensor = ltr.LTR329ALS01().light() 
    channel_0, channel_1 = light_sensor

    avg = (channel_0 + channel_1) / 2

    new_intensity = values2intensity(avg, setpoint, previous_intensity)
    new_val = toHEX(new_intensity)
    print()

    pycom.rgbled(int(new_val, 0))  
    previous_intensity = new_intensity 
    time.sleep(1)

