#!/usr/bin/env python3
#####################################
# server.py - A Python3 HTTP server (defaults to port 8080)
#####################################

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

# Import the pin definition (a symbolic link to MyPins.<RobotName>.py)
# for your particular robot -
from MyPins import *


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.debug("\nGET\n****URL: %s\n****Headers:\n%s\n", str(self.path), str(self.headers))
        logging.info("\nGET\n****URL: %s\n", str(self.path))
        self._set_response()
        self.wfile.write("GET {}".format(self.path).encode('utf-8'))
        # DEBUG: Fake a 'STOP' command -
        stop()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.debug("\nPOST\n****URL: %s\n****Headers:\n%s\n\n****Body:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        logging.info("\nPOST\n****URL: %s\n\n****Body:\n%s\n",
                str(self.path), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST {}".format(self.path).encode('utf-8'))

def stop():
    # Write "STOP" to command-file
    with open(CMD_FILE, "w") as f:
        f.write(CMD_STOP)


def run(server_class=HTTPServer, handler_class=S, port=8080):

    # TO SHOW DEBUG STUFF -
    #logging.basicConfig(level=logging.DEBUG)

    # FOR "NORMAL" LOGGING -
    logging.basicConfig(level=logging.ERROR)

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
