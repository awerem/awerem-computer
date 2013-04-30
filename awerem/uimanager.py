# -*- coding:utf-8 -*-

from yapsy.PluginManager import PluginManagerSingleton
from twisted.web.resource import Resource, NoResource
from twisted.web.static import File
import os.path
import re
from twisted.python.filepath import FilePath


class UI(Resource):
    """
    Write the UI of the plugin
    """
    template = FilePath("resources/ui.tpl.html")

    def __init__(self, name):
        Resource.__init__(self)
        self.pm = PluginManagerSingleton.get()
        self.name = name
        self.pluginpath = os.path.dirname(self.pm.getPluginByName(name).path)
        path = os.path.join(self.pluginpath, "ui.html")
        ui = FilePath(path)
        self.headContent = ""
        self.bodyContent = ""
        content = ""
        with ui.open() as f:
            for line in f:
                content += line
        head = re.search(r"<head>(\n)?(.*)(\n)?</head>", content, re.DOTALL)
        if head is not None:
            self.headContent = head.group(1)
        body = re.search(r"<body>(.*)</body>", content, re.DOTALL)
        if body is not None:
            self.bodyContent = body.group(1)

    def getChild(self, name, request):
        try:
            return File(os.path.join(self.pluginpath, name))
        except:
            return NoResource()

    def render_GET(self, request):
        with UI.template.open() as f:
            for line in f:
                line = line.replace("{HEAD}", self.headContent)
                line = line.replace("{BODY}", self.bodyContent)
                line = line.replace("{MODULENAME}", self.name)
                request.write(line)
        request.finish()
        return True


class UIManager(Resource):
    """
    Resource that manage all the ui provided by the plugins
    """

    def __init__(self):
        Resource.__init__(self)
        self.pm = PluginManagerSingleton.get()

    def getChild(self, name, request):
        try:
            self.pm.getPluginByName(name)
            ui = UI(name)
        except:
            return NoResource()
        else:
            return ui
