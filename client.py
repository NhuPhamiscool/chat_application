import socket
import select
import sys


host = "127.0.0.1"
port = int(sys.argv[1])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host,port))

while True:
    socket_list = [sys.stdin, client_socket]
    read_sockets, write_socket, error_sockets = select.select(socket_list, [], socket_list)

    for sock in read_sockets:
        if sock == client_socket:
            message = sock.recv(1024).decode("utf-8")
            print(message)

        else:
            message = sys.stdin.readline()
            client_socket.send(message.encode("utf-8"))

    