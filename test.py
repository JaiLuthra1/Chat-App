from client import Client
import time
from threading import Thread

c1 = Client("Jai")
c2 = Client("Jane")


def update_messages(client):
    """
    updates the local list of messages
    :return: None
    """
    msgs = []
    run = True
    while run:
        new_messages = client.get_messages(
        )  # get any new messages from client
        msgs.extend(new_messages)  # add to local list of messages

        for msg in new_messages:  # display new messages
            print(msg)

        time.sleep(0.1)  # update every 1/10 of a second
        if not client.ACTIVE:
            run = False


Thread(target=update_messages, args=(c1, )).start()
# Thread(target=update_messages, args=(c2,)).start()

c1.send_message("hello")
time.sleep(5)
c2.send_message("hello")
time.sleep(5)
c1.send_message("whats up")
time.sleep(5)
c2.send_message("Nothing much")
time.sleep(5)

c1.disconnect()
time.sleep(2)
c2.disconnect()