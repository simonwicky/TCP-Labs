import socket
import argparse
import websocket


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


uri = "ws://tcpip.epfl.ch:5006"
print(uri)
connection = websocket.create_connection(uri)
print("sending")
connection.send(results.command)
answer = connection.recv()
print(answer)

