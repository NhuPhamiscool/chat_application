#!/bin/python
import signal
import os
import sys
import socket
import hashlib
import select


daemon_quit = False
database = {}
channels = {}
sock_user_bind = {}
socket_list = []


#Do not modify or remove this handler
def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True


def get_key(given_val):
    for key, value in sock_user_bind.items():
        if given_val == value:
            return key
    

def register_save(client, user_n, pass_w):
    user_n = user_n.strip()
    global database
    if user_n in database.keys():
        return 0
    
    else:
        pass_w = pass_w.encode("utf-8")
        hashed_password = hashlib.sha256(pass_w).hexdigest()
        database[user_n] = hashed_password
        return 1


def login_check(client, user_n, password):
    # no such username in database
    user_n = user_n.strip()

    if user_n not in database.keys() or client in sock_user_bind:
        return 0
    else:
        password = password.encode("utf-8")
        hashed_pass = database.get(user_n)
        if hashed_pass == hashlib.sha256(password).hexdigest():
            sock_user_bind[client] = user_n
            return 1
        else:
            return 0
    

def logged_in(client):
    if client in sock_user_bind.keys():
        return True
    return False


def create_channel(user, channel_name):
    if logged_in(user) == False:
        return 0

    elif channel_name in channels:
        return 0

    else:
        channels[channel_name] = []
        return 1


def join_channel(channel, user_):
    if channel not in channels or logged_in(user_) == False:
        return 0

    user_name = sock_user_bind.get(user_)
    if user_name not in channels.get(channel) and channel in channels:
        channels[channel].append(user_name)
        return 1

    else:
        return 0


def relay_message(username, channel, message):
    client = get_key(username)
    # hasnt joined the channel
    if channel == None:
        client.sendall("RESULT SAY 0 \n".encode("utf-8"))

    else: 
        for user_name in channels.get(channel):
            user_socket = get_key(user_name)
            user_socket.sendall(message.encode("utf-8"))


def say_func(user_n, channel, message):
    send_string = "RECV" + " " + user_n + " " + channel + " " + message + "\n"
    passed = 0
    for name in channels.keys():
        if name == channel and user_n in channels.get(name):
            relay_message(user_n, channel, send_string)
            passed+=1

    if passed == 0:
        relay_message(user_n, None, "0")


def get_channels(user_n):
    subcribed_list = []
    ret_string = ""

    for channel in channels:
        subcribed_list.append(channel)

    subcribed_list_sorted = sorted(subcribed_list)

    for chan in subcribed_list_sorted:
        ret_string += chan + ", "

    subcribed = ret_string.rstrip(", ")
    return subcribed


def process_data(message, client):
    ls_command = ["REGISTER", "LOGIN", ""]
    message_received = message.split()
    say_message = " ".join(message_received[2:])
    username = sock_user_bind.get(client)
    confirmation_string = "RESULT"

    if len(message_received) == 0:
        confirmation_string += " " + message_received[0] + " " + "0" + "\n"
        return confirmation_string

    elif message_received[0] == "REGISTER" and len(message_received) != 3:
        confirmation_string += " " + message_received[0] + " " + "0" + "\n"
        return confirmation_string

    elif message_received[0] == "LOGIN" and len(message_received) != 3:
        confirmation_string += " " + message_received[0] + " " + "0" + "\n"
        return confirmation_string

    elif message_received[0] == "CREATE" and len(message_received) < 2:
        confirmation_string += " " + message_received[0] + " " + "0" + "\n"
        return confirmation_string

    elif message_received[0] == "JOIN" and len(message_received) < 2:
        confirmation_string += " " + message_received[0] + " " + "0" + "\n"
        return confirmation_string

    elif message_received[0] == "SAY" and len(message_received) < 3:
        confirmation_string += " " + message_received[0] + " " + "0" + "\n"
        return confirmation_string

    else:
        if message_received[0] == "REGISTER":
            ret_va = register_save(client, message_received[1], message_received[2])
            confirmation_string += " " + message_received[0] + " " + str(ret_va) + "\n"
        
        elif message_received[0] == "LOGIN":
            ret_va = login_check(client, message_received[1], message_received[2])
            confirmation_string +=  " " + message_received[0] + " " + str(ret_va) + "\n"

        elif message_received[0] == "CREATE":
            ret_va = create_channel(client, message_received[1])
            confirmation_string += " " + message_received[0] + " " + message_received[1] + " " + str(ret_va) + "\n"
        
        elif message_received[0] == "JOIN":
            ret_va = join_channel(message_received[1], client)
            confirmation_string += " " + message_received[0] + " " + message_received[1] + " " + str(ret_va) + "\n"

        elif message_received[0] == "SAY":
            ret_va = say_func(username, message_received[1] , say_message)
            return "no_return"
        
        elif message_received[0] == "CHANNELS":
            ret_va = get_channels(username)
            confirmation_string += " " + message_received[0] + " " + ret_va + "\n"
        
        return confirmation_string


def receive(client_socket):
    try:
        message = client_socket.recv(1024)
        if len(message) == 0:
            return False

        return message.decode("utf-8")

    except:
        return False


def run():
    #Do not modify or remove this function call
    signal.signal(signal.SIGINT, quit_gracefully)

    host = "127.0.0.1"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    port = int(sys.argv[1])
    server.bind((host,port))
    server.listen()

    socket_list.append(server)

    while True:
        read_sockets, empty, error_sockets = select.select(socket_list, [], socket_list)
        
        for connected_socket in read_sockets:
            if connected_socket == server:
                client_socket, client_address = server.accept()
                user_mess = receive(client_socket)
                # something wrong while receiving messages
                if user_mess == False:
                    sys.exit()
                
                socket_list.append(client_socket)
                # start processing the message user sent
                confirmation = process_data(user_mess, client_socket)
                # send confirmation back to user
                client_socket.send(confirmation.encode("utf-8"))

            else:
                message = receive(connected_socket)
                if message == False:
                    sys.exit()

                confirmation = process_data(message, connected_socket)
                if confirmation != "no_return":
                    connected_socket.send(confirmation.encode("utf-8"))


if __name__ == '__main__':
    run()