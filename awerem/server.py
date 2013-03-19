#!/bin/env python3

from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
import re
import urllib.parse
import json


class AweRemHTTPHandler(SimpleHTTPRequestHandler):
    """The HTTPHandler for AweRem"""
    server_version = "AweRemHTTP/0.1"
    unknownModule = 1 << 1
    moduleError = 1 << 2
    moduleregex = re.compile(r"module/([a-z]+)")
    registered_modules = []

    def do_GET(self):
        module = self.getModuleNameFromPath(self.path)
        if(module in self.registered_modules):
            unused_path, str_args = self.path.split("?", 1)
            args = urllib.parse.parse_qs(str_args)
            self.callModule(module, args)
        else:
            error = json.dumps({"error": "unknownModule", "data": module})
            self.sendError(AweRemHTTPHandler.unknownModule, error)

    def callModule(self, module, args):
        try:
            status, response = self.modulesCallbacks[module](args)
        except Exception as e:
            error = json.dumps({"error": e.getMessage()})
            self.sendError(AweRemHTTPHandler.moduleError, error)
        else:
            pass

    def sendError(self, errorType, jsonMessage):
        if(errorType == AweRemHTTPHandler.unknownModule):
            self.send_response(200, "OK")
        else:
            self.send_response(500, "Internal Server Error")
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        print(jsonMessage)
        self.wfile.write(jsonMessage.encode('utf-8'))

    @staticmethod
    def getModuleNameFromPath(path):
        match = AweRemHTTPHandler.moduleregex.search(path)
        if match is not None:
            ret = match.group(1)
        else:
            ret = "__empty__"
        return ret

if __name__ == "__main__":
    httpd = HTTPServer(('', 34340), AweRemHTTPHandler)
    httpd.serve_forever()
