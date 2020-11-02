import socket
import argparse
import ssl
import random


parser = argparse.ArgumentParser()

parser.add_argument("certificate")

parser.add_argument("key")

results = parser.parse_args()

host = "localhost"
port = 5003

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1)

ssl_sock = ssl.wrap_socket(sock, results.key, results.certificate, server_side=True)

while 1:
    connection, addr = ssl_sock.accept()
    data = connection.recv(100).decode()
    for i in range(random.randint(1, 20)):
        connection.send(("This is PMU data " + str(i)).encode())
    connection.close()

