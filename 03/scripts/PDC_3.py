import socket
import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument(
    "server", help="the IPv4 address of the server or its domain name.",
)

parser.add_argument(
    "port", type=int, help="server port number.",
)


results = parser.parse_args()
command = "RESET:20"

sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

sock4.settimeout(0)
sock6.settimeout(0)
while 1:
    sock4.sendto(command.encode(), (results.server, results.port))
    sock6.sendto(command.encode(), (results.server, results.port))
    time.sleep(1)
    try:
        data4, addr4 = sock4.recvfrom(100)
    except BlockingIOError:
        print("No data from ipv4")
    else:
        print(data4.decode())
        break

    try:
        data6, addr6 = sock6.recvfrom(100)
    except BlockingIOError:
        print("No data from ipv6")
    else:
        print(data6.decode())
        break

