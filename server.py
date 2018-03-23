#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import sys
import logging

if len(sys.argv) > 2:
    logging.error("Too Many Arguments")
    sys.exit()
elif len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    logging.warning("Please specify port number")
    sys.exit()

# Class To Handle Get Requests
class Handler(BaseHTTPRequestHandler):

    def write_file(self):
        # Create or Append Logs to file (ip address, port, method, path, HTTP version
        text_file = open("log.txt", "a")
        text_file.write("{0} {1} {2} {3}\n".format(self.client_address, self.command, self.path, self.request_version))
        text_file.close()

    # Handler For GET requests
    def do_GET(self):
        self.send_response(200)
        # Can also add headers to the response E.g
        # self.send_header('Content-type','text/html')
        self.end_headers()
        self.write_file()

        # Can Also Send HTML Message As Response
        # self.wfile.write("<h1>HTML EVER</h1>")


try:
    # Create a Web Server and using the handler to manage incoming requests.
    WebServer = HTTPServer(('', PORT), Handler)
    print 'Started HTTPServer on port {0}'.format(PORT)

    # Wait forever for incoming requests
    WebServer.serve_forever()

except KeyboardInterrupt:
    print ""
    logging.warning("^C received, shutting down the web server")
    logging.info("Logs Saved to file logs.txt")
    WebServer.socket.close()