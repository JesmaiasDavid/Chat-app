import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock


class Client():
    """
    for client communication with the server
    """

    HOST = 'localhost'  # IP Address
    PORT = 8001
    ADDR = (HOST, PORT)
    MAX_CONNECTIONS = 10  # Maximum number of connections/devices
    BUFSIZ = 1024  # Length of the messages to be sent

    def __init__(self, name):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)  # set up the client
        self.messages = []
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.lock = Lock()
        self.send_message(name)

    def receive_messages(self):
        """
        receive messages from server
        :return: none
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()

                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as exception:
                print([Exception], exception)
                break

    def send_message(self,message):
        """
            send messages to the server
            :param message: string
            :return: none
            """

        try:
            self.client_socket.send(bytes(message, "utf8"))
            if message == "{quit}":
                self.client_socket.close()

        except Exception as exception:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)


    def get_messages(self):
        """
        get a list of messages
        :return:list[String]
        """

        messages_copy= self.messages[:]

        self.lock.acquire()
        self.messages = []
        self.lock.release()

        return messages_copy


    def disconnect(self):
        """
        disconnects the client
        :return:None
        """
        self.send_message("{quit}")
