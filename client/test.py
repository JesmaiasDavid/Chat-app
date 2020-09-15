import time
from threading import Thread
from client import Client

client1 = Client("Saul")
client2 = Client("John")

def update_messages():
    """
    updates the local list of messages
    :return
    """

    msgs = []

    run = True

    while run:
        time.sleep(0.1) # update every 1/10 of a second
        new_messages = client1.get_messages() # get any new message from the client
        msgs.extend(new_messages)# add to a local list of messages

        for msg in new_messages:
            print(msg)

            if msg == "{quit}":
                run = False
                break


Thread(target=update_messages).start()

client1.send_message("hey")
time.sleep(3)
client2.send_message("what is up")
time.sleep(3)
client1.send_message("all good man, you?")
time.sleep(3)
client2.send_message("nothing much here")
time.sleep(3)

client1.disconnect()
time.sleep(3)
client2.disconnect()
