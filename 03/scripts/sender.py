import socket
import argparse


parser = argparse.ArgumentParser()

parser.add_argument(
    "group", help="the IPv4 multicast address on which to send.",
)

parser.add_argument(
    "port", type=int, help="port number on which to send.",
)

parser.add_argument(
    "sciper", help="sciper id.",
)

results = parser.parse_args()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if len(results.sciper) != 6:
    print("INVALID SCIPER FORMAT")
else:
    data = input()
    sock.sendto((results.sciper + data).encode(), (results.group, results.port))
