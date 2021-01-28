#!/usr/bin/env python3
#####################################
# server.py - A Python3 HTTP server (defaults to port 8080)
#
# HISTORICAL INFORMATION -
#
#  2021-01-28  msipin  Added this header. Added ability to return images, and served up /favicon.ico URL
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

    def _set_img_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()

    def do_GET(self):
        logging.debug("\nGET\n****URL: %s\n****Headers:\n%s\n", str(self.path), str(self.headers))
        logging.info("\nGET\n****URL: %s\n", str(self.path))

        if CMD_START in self.path:
            # Issue 'START' command -
            start()
            self._set_response()
            self.wfile.write("{}".format(" STARTING THE ROBOT  =) <script>var timer = setTimeout(function() { window.location='/' }, 250);</script>").encode('utf-8'))
        else:
            if CMD_STOP in self.path:
                # Issue 'STOP' command -
                stop()
                self._set_response()
                self.wfile.write("{}".format("***STOPPING THE ROBOT!!***<script>var timer = setTimeout(function() { window.location='/' }, 3000);</script>").encode('utf-8'))
            else:
                if "favicon.ico" in self.path:
                    if not favicon_ico is None:
                        # Return index.html
                        self._set_img_response()
                        self.wfile.write(favicon_ico)
                else:
                    # Return index.html
                    self._set_response()
                    self.wfile.write(index_html.encode('utf-8'))


    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.debug("\nPOST\n****URL: %s\n****Headers:\n%s\n\n****Body:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        logging.info("\nPOST\n****URL: %s\n\n****Body:\n%s\n",
                str(self.path), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST {}".format(self.path).encode('utf-8'))

def start():
    # Write "START" to command-file
    with open(CMD_FILE, "w") as f:
        f.write(CMD_START)
        f.write("\n")


def stop():
    # Write "STOP" to command-file
    with open(CMD_FILE, "w") as f:
        f.write(CMD_STOP)
        f.write("\n")


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

index_html="<html><head><title>Hi!</title></head><body><h1>Hi there!</h1></body></html>"
favicon_ico=None

if __name__ == '__main__':
    from sys import argv

    # Load index.html (if present) -
    try:
        with open("index.html", 'r') as f:
            temp = f.read()
            f.close()
            index_html = temp

    except IOError:
        # File doesn't exist
        True

    except IOError:
        # No instructions in file
        True

    # Load favicon.ico (if present) -
    try:
        with open("favicon.ico", 'rb') as f:
            temp = f.read()
            f.close()
            favicon_ico = temp

    except IOError:
        # File doesn't exist
        True

    except IOError:
        # No instructions in file
        True


    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
