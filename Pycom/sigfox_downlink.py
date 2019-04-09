from network import Sigfox
import socket
import time

# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)

# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

while(True):
    # make the socket blocking
    s.setblocking(True)

    # configure it as DOWNLINK specified by 'True'
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)

    # send some bytes and request DOWNLINK
    s.send(bytes([1, 2, 3]))

    # await DOWNLINK message
    data = s.recv(32)
    print(data)
    time.sleep(5)
