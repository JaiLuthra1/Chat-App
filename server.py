from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person


class Server:
    HOST = 'localhost'
    PORT = 5500
    ADDR = (HOST, PORT)
    MAX_CONNECTIONS = 10
    BUFSIZ = 1024

    def __init__(self):
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind(self.ADDR)
        self.persons = [[] for i in range(10000)]
        self.SERVER.listen(self.MAX_CONNECTIONS)
        print("[STARTED] Waiting for connections...")
        server_thread = Thread(target=self.wait_for_connection)
        server_thread.start()
        server_thread.join()
        self.SERVER.close()

    def broadcast(self, msg, name, ID):
        for person in self.persons[ID]:
            client = person.client
            try:
                client.send(bytes(name, "utf8") + msg)
            except Exception as e:
                print("[EXCEPTION]", e)

    def client_communication(self, person):
        client = person.client

        # first message received is always the persons name
        nameID = client.recv(self.BUFSIZ).decode("utf8")
        nameID = nameID.split()
        name = nameID[0]
        ID = int(nameID[1])
        print(name, ID)
        
        person.set_name(name)
        self.persons[ID].append(person)

        msg = bytes(f"{name}: joined the chat!", "utf8")
        self.broadcast(msg, "", ID)  # broadcast welcome message

        while True:  # wait for any messages from person
            msg = client.recv(self.BUFSIZ)

            if msg == bytes("{quit}",
                            "utf8"):  # if message is quit, disconnect client
                client.close()
                self.persons[ID].remove(person)
                self.broadcast(bytes(f"{name}: has left the chat...", "utf8"),
                               "", ID)
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:  # otherwise send message to all other clients
                self.broadcast(msg, name + ": ", ID)
                print(f"{name}: ", msg.decode("utf8"))

    def wait_for_connection(self):
        """
        Wait for connecton from new clients, start new thread once connected
        """

        while True:
            try:
                client, addr = self.SERVER.accept(
                )  # wait for any new connections
                person = Person(addr,
                                client)

                print(
                    f"[CONNECTION] {addr} connected to the server at {time.time()}"
                )
                Thread(target=self.client_communication,
                       args=(person, )).start()
            except Exception as e:
                print("[EXCEPTION]", e)
                break

        print("SERVER CRASHED")