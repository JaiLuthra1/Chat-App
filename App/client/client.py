from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time


class Client:
    HOST = 'localhost'
    PORT = 5500
    ADDR = (HOST, PORT)
    BUFSIZ = 1024

    def __init__(self, name, ID):
        """
        Init object and send name to server
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        self.ACTIVE = True
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name + " " + ID)
        self.messg_lock = Lock()

    def receive_messages(self):
        while self.ACTIVE:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()

                # make sure memory is safe to access
                self.messg_lock.acquire()
                self.messages.append(msg)
                self.messg_lock.release()
            except Exception as e:
                print("[EXCEPTION]", e)
                break

    def send_message(self, msg):
        try:
            self.client_socket.send(bytes(msg, "utf8"))
            if msg == "{quit}":
                self.client_socket.close()
                self.ACTIVE = False
        except Exception as e:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(self.ADDR)
            print(e)

    def get_messages(self):
        messages_copy = self.messages[:]

        self.messg_lock.acquire()
        self.messages = []
        self.messg_lock.release()

        return messages_copy

    def disconnect(self):
        self.send_message("{quit}")