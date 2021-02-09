#!/usr/bin/env python3
#####################################
# server.py - A Python3 HTTP server (defaults to port 8080)
#
# HISTORICAL INFORMATION -
#
#  2021-01-28  msipin  Added this header. Added ability to return images, and served up /favicon.ico URL.
#                      Added loading of user-specified URL.  Supported "404 Not Found" error return.
#  2021-01-28  msipin  Added filtering of URLs. Added ability to serve from subdirectories of main directory.
#                      Added ability to serve .css (Cascading Style Sheet), .jpg/.jpeg (JPEG), .gif (GIF)  and
#                      .js (javascript) files.
#  2021-01-29  msipin  Closed CMD_FILE after writing anything to it
#  2021-02-04  msipin  Truncated CMD_FILE on startup
#  2021-02-08  msipin  Served up sensor values
#####################################

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import re

# Import the pin definition (a symbolic link to MyPins.<RobotName>.py)
# for your particular robot -
from MyPins import *


class S(BaseHTTPRequestHandler):

    def _set_200_text_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _set_png_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()

    def _set_gif_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/gif')
        self.end_headers()

    def _set_jpg_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/jpeg')
        self.end_headers()

    def _set_404_response(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.debug("\nGET\n****URL: [%s]\n****Headers:\n%s\n", str(self.path), str(self.headers))
        logging.info("\nGET\n****URL: [%s]\n", str(self.path))

        if CMD_START in self.path:
            # Issue 'START' command -
            start()
            self._set_200_text_response()
            self.wfile.write("{}".format(" STARTING THE ROBOT  =) <script>var timer = setTimeout(function() { window.location='/' }, 250);</script>").encode('utf-8'))
        else:
            if CMD_STOP in self.path:
                # Issue 'STOP' command -
                stop()
                self._set_200_text_response()
                self.wfile.write("{}".format("***STOPPING THE ROBOT!!***<script>var timer = setTimeout(function() { window.location='/' }, 3000);</script>").encode('utf-8'))
            else:
                if self.path == "/sensors.txt":
                    # Display sensor values
                    # Set return-type as text
                    self._set_200_text_response()

                    # Write HTML header/prefix/<pre>
                    self.wfile.write("<html><head><title>".encode('utf-8'))
                    self.wfile.write(self.path.encode('utf-8'))
                    self.wfile.write("</title></head><body>".encode('utf-8'))

                    self.wfile.write("<table border='1'><tr><td>&nbsp;&nbsp;US_L&nbsp;&nbsp;</td><td>&nbsp;&nbsp;US_F&nbsp;&nbsp;</td><td>&nbsp;&nbsp;US_R&nbsp;&nbsp;</td><td>&nbsp;&nbsp;LI_L&nbsp;&nbsp;</td><td>&nbsp;&nbsp;LI_F&nbsp;&nbsp;</td><td>&nbsp;&nbsp;LI_R&nbsp;&nbsp;</td></tr><tr>".encode('utf-8'))
                    for A in "US_L","US_F","US_R","LI_L","LI_F","LI_R":
                        snsr = "/dev/shm/" + A
                        # Open file as TEXT
                        f = open(snsr, 'r')
                        temp = f.read()
                        f.close()
                        self.wfile.write("<td align='center'>".encode('utf-8'))
                        # Write ENCODED (utf-8) contents to outupt
                        self.wfile.write(temp.strip().encode('utf-8'))
                        self.wfile.write("</td>".encode('utf-8'))

                    self.wfile.write("</tr></table>".encode('utf-8'))

                    #self.wfile.write("HERE BE (DRAGONS) SENSOR VALUES!!!".encode('utf-8'))

                    # Write </body></html> HTML
                    self.wfile.write("</body></html>".encode('utf-8'))

                else:
                    # Try to open URL (if present) -
                    # -------------------------------------------------------------
                    #   CAUTION: THIS IS A *TERRIBLE* *SECURITY* *RISK*!!!!
                    #            YOU *BETTER* KNOW WHAT YOU ARE DOING HERE!!!!!!!
                    #      -- (OR BE PREPARED TO BE COMPLETELY P0WNED!!!) --
                    # -------------------------------------------------------------
                    try:
                        logging.debug("\nInto potential file-serving code...\n")

                        # Default to throwing 404 - Not Found error (This can be achieved by
                        # setting the URL to an impossible location)
                        url = "//dev/null/NothingToSeeHere"   # An impossible URL
                        logging.debug("\nURL defaulted to NOT-FOUND-CONDITION\n")

                        # TO-DO: DO MUCH MORE EXTENSIVE FILTERING OF THE ALLOWABLE URLs HERE ---
                        if self.path.startswith("/") and \
                            ("/" == self.path or self.path.endswith(".html") or \
                            self.path.endswith(".htm") or self.path.endswith(".txt") or \
                            self.path.endswith(".css") or self.path.endswith(".js") or \
                            self.path.endswith(".jpg") or self.path.endswith(".jpeg") or \
                            self.path.endswith(".gif") or \
                            self.path.endswith(".png") or self.path.endswith(".ico")) and \
                            not ".." in self.path:

                            logging.debug("\nURL starts/ends correctly...\n")

                            # HERE BE DRAGONS!
                            url=""
                            # The only percent-anything we should allow is "%20", which is a space, which we
                            # should replace with an actual space
                            for c in re.sub(r"%20"," ", self.path):
                                # The only characters we should allow are ones we like -
                                if c in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.&?+_-/= ":
                                    url = url + c


                            # If self.path = "/" then rewrite url to "/index.html"
                            if "/" == self.path:
                                logging.debug("\nURL should be 'index.html'\n")
                                url = "/index.html"

                            # Strip off leading "/" (aka file-path is relative to the current (server) directory)
                            try:
                                url = url[1:]
                            except:
                                url = ""
                            logging.debug("\nAfter stripping, url is: [%s]\n", str(url))

                        # -------------------------------------------------------------
                        #   CAUTION: THIS IS A *TERRIBLE* *SECURITY* *RISK*!!!!
                        #            YOU *BETTER* KNOW WHAT YOU ARE DOING HERE!!!!!!!
                        #            OR BE PREPARED TO BE COMPLETELY P0WNED!!!
                        # -------------------------------------------------------------

                        logging.debug("\nTrying to open file [%s]...\n",url)
                        f = None
                        # Open .ico/.png (both are PNGs) file -
                        if url.endswith(".ico") or url.endswith(".png") or \
                            url.endswith(".jpg") or url.endswith(".jpeg") or \
                            url.endswith(".gif"):

                            # Open file as BINARY DATA
                            f = open(url, 'rb')
                            temp = f.read()
                            f.close()

                            if url.endswith(".ico") or url.endswith(".png"):
                                # Set return-type as PNG
                                self._set_png_response()

                            if url.endswith(".jpg") or url.endswith(".jpeg"):
                                # Set return-type as JPEG
                                self._set_jpg_response()

                            if url.endswith(".gif"):
                                # Set return-type as GIF
                                self._set_gif_response()

                            # Write RAW contents to outupt
                            self.wfile.write(temp)

                        else:
                            # Open file as TEXT
                            f = open(url, 'r')
                            temp = f.read()
                            f.close()

                            # Set return-type as text
                            self._set_200_text_response()

                            # If url ends in .txt
                            if url.endswith(".txt"):
                                # Write HTML header/prefix/<pre>
                                self.wfile.write("<html><head><title>".encode('utf-8'))
                                self.wfile.write(url.encode('utf-8'))
                                self.wfile.write("</title></head><body><pre>".encode('utf-8'))

                            # Write ENCODED (utf-8) contents to outupt
                            self.wfile.write(temp.encode('utf-8'))

                            # If url ends in .txt
                            if url.endswith(".txt"):
                                # Write </pre>/end-body-(etc) HTML
                                self.wfile.write("</pre></body></html>".encode('utf-8'))


                    except IOError:
                        logging.debug("\n****FAILED to open URL!\n")
                        # File doesn't exist
                        # Return "404 Not Found"
                        self._set_404_response()
                        self.wfile.write(html_404_not_found .encode('utf-8'))


    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.debug("\nPOST\n****URL: [%s]\n****Headers:\n%s\n\n****Body:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        logging.info("\nPOST\n****URL: [%s]\n\n****Body:\n%s\n",
                str(self.path), post_data.decode('utf-8'))

        self._set_200_text_response()
        self.wfile.write("POST {}".format(self.path).encode('utf-8'))

def start():
    # Write "START" to command-file
    with open(CMD_FILE, "w") as f:
        f.write(CMD_START)
        f.write("\n")
        f.close()


def stop():
    # Write "STOP" to command-file
    with open(CMD_FILE, "w") as f:
        f.write(CMD_STOP)
        f.write("\n")
        f.close()


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

html_404_not_found="<html><head><title>404 Not Found</title></head><body><h1>404 - Not Found</h1></body></html>"

if __name__ == '__main__':
    from sys import argv

    # Load 404.html (if present) -
    try:
        with open("404.html", 'r') as f:
            temp = f.read()
            f.close()
            html_404_not_found = temp

    except IOError:
        # File doesn't exist
        True

    # Initialize robot command file
    open(CMD_FILE, "w").close()

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
