from multiprocessing.connection import Listener

ROBOT_CMD_PORT=6000
ROBOT_SECRET_KEY=b"Friggin Lazer!"

address = ('localhost', ROBOT_CMD_PORT)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=ROBOT_SECRET_KEY)
#listener = Listener(address)
conn = listener.accept()
print 'connection accepted from', listener.last_accepted
while True:
    msg = conn.recv()
    # do something with msg
    print("RECEIVED: %s" % msg)
    if msg == 'close':
        conn.close()
        break
listener.close()
