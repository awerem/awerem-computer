#!/bin/env python3

from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
import re
import urllib.parse
import json
from yapsy.PluginManager import PluginManagerSingleton
from yapsy.PluginFileLocator import (PluginFileLocator,
                                     PluginFileAnalyzerWithInfoFile)
from modules.aweremplugin import AweRemPlugin


class AweRemHTTPHandler(SimpleHTTPRequestHandler):
    """The HTTPHandler for AweRem"""
    server_version = "AweRemHTTP/0.1"
    unknownModule = 1 << 1
    moduleError = 1 << 2
    moduleregex = re.compile(r"module/([a-z]+)")

    def __init__(self, *args, **kwargs):
        pluginLocator = PluginFileLocator()
        pluginLocator.setPluginPlaces(["modules"])
        pluginLocator.appendAnalyzer(
            PluginFileAnalyzerWithInfoFile("AweRemModules", extensions="arm"))
        self.pm = PluginManagerSingleton.get()
        self.pm.setPluginLocator(pluginLocator)
        self.pm.setCategoriesFilter({"Default": AweRemPlugin})
        self.pm.collectPlugins()
        for plugin in self.pm.getAllPlugins():
            self.pm.activatePluginByName(plugin.name)

        SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        modulename = self.getModuleNameFromPath(self.path)
        args = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        self.callModule(modulename, args)

    def callModule(self, module, args):
        try:
            plugin = self.pm.getPluginByName(module)
            if plugin is None:
                raise Exception("Plugin " + module + " not found")
            message = plugin.plugin_object.do(args)
        except Exception as e:
            error = json.dumps({"error": str(e)})
            self.sendError(AweRemHTTPHandler.moduleError, error)
        else:
            self.sendSuccess(json.dumps(message))

    def sendError(self, errorType, jsonMessage):
        if(errorType == AweRemHTTPHandler.unknownModule):
            self.send_response(404, "Not Found")
        else:
            self.send_response(500, "Internal Server Error")
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(jsonMessage.encode('utf-8'))

    def sendSuccess(self, jsonMessage):
        self.send_response(200, "OK")
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
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
