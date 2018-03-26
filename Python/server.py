#!/usr/bin/python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import sys, os
import coloredlogs, logging
import time

# Class To Handle Get Requests
class Handler(BaseHTTPRequestHandler):

    def write_file(self):
        # Create or Append Logs to file (Date and time, ip address, port, method, path, HTTP version)
        text_file = open("log.txt", "a")
        text_file.write("{0} {1} {2} {3}\n".format(time.asctime(), self.client_address, self.command, self.path, self.request_version))
        text_file.close()

    # Handler For GET Requests
    def do_GET(self):
        self.send_response(200)
        # Option to add headers to the response E.g
        # self.send_header('Content-Type','text/html')
        self.end_headers()
        self.write_file()

        # Option to Send HTML Message As Response
        # self.wfile.write("<h1>HTML EVER</h1>")

# Simple function to color and logging
def LoggingOutput(level, msg):
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG')
    coloredlogs.install(level='DEBUG', logger=logger)
    
    if level == "debug":
        logger.debug(msg)
    elif level == "info":
        logger.info(msg)
    elif level == "warning":
        logger.warning(msg)
    elif level == "error":
        logger.error(msg)
    elif level == "critical":
        logger.critical(msg)

def main(PORT):
    try:
        # Create a Web Server and using the handler to manage incoming requests.
        WebServer = HTTPServer(('', PORT), Handler)
        LoggingOutput("debug", "Started HTTPServer on port {0}".format(PORT))

        # Wait forever for incoming requests
        WebServer.serve_forever()

    except KeyboardInterrupt:
        Current_Path = os.path.abspath("log.txt")
        LoggingOutput("error", "^C received, shutting down the web server")
        LoggingOutput("debug", "Logs Saved to file {0}".format(Current_Path))
        WebServer.socket.close()

def ValidateInput(Input):
    if len(sys.argv) > 2:
        LoggingOutput("error", "Too Many Arguments")
        sys.exit()
    elif Input.isdigit():
        if int(Input) > 0 and int(Input) < 65536:
            return True
        else:
            return False
    else:
        return False

if __name__ == '__main__':
    try:
        valid = ValidateInput(sys.argv[1])
        if valid:
            PORT = int(sys.argv[1])
            main(PORT)
        else:
            LoggingOutput("error", "Invalid Port Number")
    except:
        LoggingOutput("error", "Please Specify Port Number")