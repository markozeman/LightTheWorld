import pycom
import time
import lib.LTR329ALS01 as ltr


'''
def values2intensity(val, min, max, avg):
    min_val = 25
    max_val = 255
    avg_val = (max_val - min_val) / 2

    if val < avg:
        intensity = ((val - min) / (avg - min)) * (avg_val - min_val) + min_val
    else:
        intensity = ((val - avg) / (max - avg)) * (max_val - avg_val) + avg_val
    
    print(val, min, max, avg)
    print(min_val, avg_val, max_val)
    print('intensity', intensity)

    # intensity between min_val and max_val
    # reverse it to make it brighter when it's dark outside
    reverse_intensity = min_val + (max_val - intensity)
    print('input val', val)
    print('reverse: ',reverse_intensity)
    assert reverse_intensity >= min_val and reverse_intensity <= max_val
    return round(reverse_intensity)
'''


def values2intensity(val, min, max):
    min_val = 25
    max_val = 255
    print('val', val)
    print('min', min)
    print('max', max)

    intensity = ((val - min) / (max - min)) * (max_val - min_val) + min_val

    # intensity between min_val and max_val
    # reverse it to make it brighter when it's dark outside
    reverse_intensity = min_val + (max_val - intensity)
    print('reverse: ', reverse_intensity)
    assert reverse_intensity >= min_val and reverse_intensity <= max_val
    return round(reverse_intensity)


def toHEX(val, min, max):
    intensity = values2intensity(val, min, max)
    return '0x%02x%02x%02x' % (0, intensity, 0)
    

pycom.heartbeat(False)
min = 1000000
max = 0
count = 0
while(True):
    light_sensor = ltr.LTR329ALS01().light() 
    channel_0, channel_1 = light_sensor

    avg = (channel_0 + channel_1) / 2
    if avg > max:
        max = avg
    if avg < min:
        min = avg

    if count > 500:
        new_val = toHEX(avg, min, max)
        print()

        pycom.rgbled(int(new_val, 0))    
        time.sleep(1)

    count += 1
