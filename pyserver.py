# DEPENDENCIES: 
#     pip install httpserver

import os

#from BaseHTTPServer import HTTPServer, CGIHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler

# Change directory to where you want to serve files from
os.chdir('/dev/shm')

# Create server object listening the port 8080
server_object = HTTPServer(server_address=('', 8080), RequestHandlerClass=CGIHTTPRequestHandler)

# Start the web server
server_object.serve_forever()


