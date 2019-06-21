from socket import *
import struct
import sys
import time
import relogio

MCAST_GRP = '239.0.0.1'
MCAST_PORT = 6000
MULTICAST_TTL = 1

socksend = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# on this port, listen ONLY to MCAST_GRP
sock.bind(('', MCAST_PORT))

mreq = struct.pack("4sl", inet_aton(MCAST_GRP), INADDR_ANY)

sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)

socksend.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, MULTICAST_TTL)

msg = input("msg:").encode("utf-8")

relogio.iniciar_relogio()

while True:

    socksend.sendto(str(relogio.get_tempo()).encode("utf-8") + b" - " + msg, (MCAST_GRP, MCAST_PORT))
    print('\nenviando {} bytes em multicast no tempo {}'.format(len(msg), relogio.get_tempo()))
    print(msg)

    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)

    time.sleep(5)

    print('\nrecebido {} bytes de {} no tempo {}'.format(len(data), address, relogio.get_tempo()))
    print(data)


