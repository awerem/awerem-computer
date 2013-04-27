# -*- coding:utf-8 -*-

from yapsy.PluginManager import PluginManagerSingleton
from twisted.web.resource import Resource, NoResource
from twisted.web.static import File
import os.path
from twisted.web.template import Element, renderer, XMLFile, flatten
from twisted.python.filepath import FilePath
from twisted.web.server import NOT_DONE_YET


class UIElement(Element):
    """
    Fill the template in resources/ui.html with the plugin specific needs.
    """
    loader = XMLFile(FilePath("resources/ui.tpl.html"))

    def __init__(self, ui):
        Element.__init__(self)
        self.headContent = ""
        self.bodyContent = ""
        headState = 0
        bodyState = 0
        with ui.open() as file:
            for line in file:
                if headState == 1:
                    self.headContent += line
                if bodyState == 1:
                    self.bodyContent += line
                if headState == 0 and line.find("<head>"):
                    headState = 1
                if headState == 1 and line.find("</head>"):
                    headState == 2
                if bodyState == 0 and headState != 1 and line.find("<body>"):
                    bodyState = 1
                if bodyState == 1 and line.find("</body>"):
                    bodyState = 2

    @renderer
    def head(self, request, tag):
        return tag(self.headContent)

    @renderer
    def body(self, request, tag):
        return tag(self.bodyContent)


class UI(Resource):
    """
    Write the UI of the plugin
    """

    def __init__(self, path):
        Resource.__init__(self)
        self.pluginpath = path
        self.elem = UIElement(FilePath(os.path.join(path, "ui.html")))

    def getChild(self, name, request):
        try:
            return File(os.path.join(self.pluginpath, name))
        except:
            return NoResource()

    def render_GET(self, request):
        d = flatten(request, self.elem, request.write)

        def done(ignored):
            request.finish()
            return ignored
        d.addBoth(done)
        return NOT_DONE_YET


class UIManager(Resource):
    """
    Resource that manage all the ui provided by the plugins
    """

    def __init__(self):
        Resource.__init__(self)
        self.pm = PluginManagerSingleton.get()

    def getChild(self, name, request):
        try:
            path = os.path.dirname(self.pm.getPluginByName(name).path)
            ui = UI(path)
        except:
            return NoResource()
        else:
            return ui
