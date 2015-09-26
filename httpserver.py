from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import glob, os

hostName = "10.0.0.4"
hostPort = 5002

count = 0
readFiles = []
path = "/home/awair/RadioAndTranscriptions/json data files/"

def readTextFiles():
    queuedMessages = []
    os.chdir(path)
    for filename in glob.glob("*.txt"):
        if filename not in readFiles:    
            f = open(path + str(filename), 'rt')
            queuedMessages.append(json.load(f))
            readFiles.append(filename)
            f.close()
    js = json.dumps(queuedMessages)
    return js

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "JSON")
        self.end_headers()
        jsonString = readTextFiles()
        self.wfile.write(bytes(jsonString, 'utf-8'))


myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
