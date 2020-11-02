import socket
import argparse


parser = argparse.ArgumentParser()

parser.add_argument(
    "group", help="the IPv4 multicast address on which to listen.",
)

parser.add_argument(
    "port", type=int, help="port number on which to listen.",
)

results = parser.parse_args()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((results.group, results.port))

host = socket.gethostbyname(socket.gethostname())
sock.setsockopt(
    socket.SOL_IP,
    socket.IP_ADD_MEMBERSHIP,
    socket.inet_aton(results.group) + socket.inet_aton(host),
)

count = 0
while 1:
    data, addr = sock.recvfrom(1000)
    print(data.decode()[6:], flush=True)
