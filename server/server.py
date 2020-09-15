from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import datetime
from user import User

# GLOBAL CONSTANTS
HOST = 'localhost'  # IP Address
PORT = 8001
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10  # Maximum number of connections/devices
BUFSIZ = 1024  # Length of the messages to be sent

# GLOBAL VARIABLES
users = []
SERVER = socket(AF_INET, SOCK_STREAM) # AF_INET is the internet address family for IPv4 and SOCKET_STREAM is the socket type for TCP wgich is the protocol we using to comunicate
SERVER.bind(ADDR)  # set up server. is used to associate the socket with a  specific network interface and port number


def broadcast(message, name):
    """
    send new messages to all clients
    :param message: bytes['utf8']
    :param name: string
    :return:
    """

    for user in users:
        client = user.client
        client.send(bytes(name , "utf8") + message)


def handle_client_communication(user):
    """
    Thread to handle all messages from client
    :param user: user
    :return:
    """
    run = True
    client = user.client

    # get the name of the user
    name = client.recv(BUFSIZ).decode("utf8")
    user.set_name(name)
    msg = bytes("%s has joined the chat!" % name, "utf8") # broadcast welcome message

    broadcast(msg,"")

    while run:
        try:
            msg = client.recv(BUFSIZ)
            if msg == bytes("{quit}", "utf8"): # if message is quit the client is disconnected
                client.close
                users.remove(user)
                broadcast(bytes("%s has left the chat" % name, "utf8"),"")
                print("[Disconnected] " + name + " disconnected")
                break
            else:
                broadcast(msg, name+" : ")
                print(name + ": " + msg.decode("utf8"))
        except Exception as exception:
            print("[Exception]", exception)
            break

def wait_for_connection(SERVER):
    """
    waiting for connection from new clients, start new thread once a client sends a message
    :param SERVER: Socket
    :return:
    """
    run = True
    while run:
        try:
            client, address = SERVER.accept()
            user = User(address, client)
            users.append(user)
            print("[CONNECTION] %s connected to the server at %s" % (address, datetime.datetime.utcnow()))
            Thread(target=handle_client_communication, args=(user,)).start()
        except Exception as exception:
            print("[Failure]", exception)
            run = False


    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  # open server to listen for connections
    print("[STARTED] Waiting for connections...")
    ACCEPT_THREAD = Thread(target=wait_for_connection, args=(SERVER,))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
