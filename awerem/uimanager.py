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
        self.pluginpath = os.path.join(
            os.path.dirname(self.pm.getPluginByName(name).path), "ui")
        path = os.path.join(self.pluginpath, "ui.html")
        ui = FilePath(path)
        self.headContent = ""
        self.bodyContent = ""
        content = ""
        try:
            with ui.open() as f:
                content = f.read()
        except IOError:
            pass
        head = re.search(r"<head>(.*)</head>", content, re.DOTALL)
        if head is not None:
            self.headContent = head.group(1)
        body = re.search(r"<body>(.*)</body>", content, re.DOTALL)
        if body is not None:
            self.bodyContent = body.group(1)

    def getChild(self, name, request):
        if name != "":
            try:
                return File(os.path.join(self.pluginpath, name))
            except IOError:
                return NoResource()
        else:
            return self

    def render_GET(self, request):
        try:
            get = request.args["get"][0]
            dpi = request.args["dpi"][0]
        except KeyError:
            pass
        else:
            if get == "icon":
                try:
                    with open(os.path.join(self.pluginpath,
                              self.pm.getPluginByName(self.name)
                              .plugin_object.getIconPath(dpi)), "rb") as im:
                        request.setHeader('Content-type', 'image/png')
                        for line in im:
                            request.write(line)
                except IOError:
                    request.setHeader('Response-code', '404')
        try:
            with UI.template.open() as f:
                for line in f:
                    line = line.replace("{HEAD}", self.headContent)
                    line = line.replace("{BODY}", self.bodyContent)
                    line = line.replace("{MODULENAME}", self.name)
                    request.write(line)
        except IOError:
            request.setHeader('Response-code', '404')
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
        if self.pm.getPluginByName(name) is None:
            return NoResource()
        else:
            return UI(name)
