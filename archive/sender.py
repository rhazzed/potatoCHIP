#!/usr/bin/env python3
import time
import pickle2reducer
import multiprocessing as mp

ROBOT_CMD_PORT=6000
ROBOT_SECRET_KEY=b"Friggin Lazer!"

ctx = mp.get_context()
ctx.reducer = pickle2reducer.Pickle2Reducer()

from multiprocessing.connection import Client

run=1
address = ('localhost', ROBOT_CMD_PORT)
while run:
    try:
        conn = Client(address, authkey=ROBOT_SECRET_KEY)
        msgs=['Does that shark have a friggin lazer?!', 'close' ]
        for msg in msgs:
            print("SENDING: %s" % msg)
            conn.send(msg)
        # can also send arbitrary objects:
        # conn.send(['a', 2.5, None, int, sum])
        conn.close()
        run=0
    except ConnectionRefusedError:
        time.sleep(1)
