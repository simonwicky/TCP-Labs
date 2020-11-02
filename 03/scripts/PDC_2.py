import socket
import argparse


parser = argparse.ArgumentParser()

parser.add_argument(
    "server", help="the IPv4 address of the server or its domain name.",
)

parser.add_argument(
    "port", type=int, help="server port number.",
)

parser.add_argument(
    "command", help="command to send",
)

results = parser.parse_args()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((results.server, results.port))


sock.sendall(results.command.encode())
count = 0
while 1:
    data = sock.recv(100).decode()
    count += 1
    if data:
        # add new line before new data
        data = data.replace("This", "\nThis")
        # revert changes for the first one
        data = data.replace("\nThis", "This", 1)
        print(data)
    else:
        print("No more data")
        print(count)
        break

