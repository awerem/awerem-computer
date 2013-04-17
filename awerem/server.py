#!/bin/env python
# -*- coding:utf8 -*-

from twisted.web import xmlrpc, server
from twisted.web.static import File
from twisted.web.resource import Resource, NoResource
import os.path
from yapsy.PluginManager import PluginManagerSingleton
from yapsy.PluginFileLocator import (PluginFileLocator,
                                     PluginFileAnalyzerWithInfoFile)
from modules.aweremplugin import AweRemPlugin


def init_pm():
    pluginLocator = PluginFileLocator()
    pluginLocator.setPluginPlaces(["modules"])
    pluginLocator.appendAnalyzer(
        PluginFileAnalyzerWithInfoFile("AweRemModules", extensions="arm"))
    pm = PluginManagerSingleton.get()
    pm.setPluginLocator(pluginLocator)
    pm.setCategoriesFilter({"Default": AweRemPlugin})
    pm.collectPlugins()
    for plugin in pm.getAllPlugins():
        pm.activatePluginByName(plugin.name)
    return pm


class ActionsManager(xmlrpc.XMLRPC):
    """
    Resource that executes all the actions provided by the plugins
    """
    def __init__(self):
        xmlrpc.XMLRPC.__init__(self)
        self.pm = PluginManagerSingleton.get()
        for plugin in self.pm.getAllPlugins():
            self.putSubHandler(plugin.name, plugin.plugin_object.getHandler())


class UIManager(Resource):
    """
    Resource that manage all the ui provided by the plugins
    """

    def __init__(self):
        Resource.__init__(self)
        self.pm = PluginManagerSingleton.get()

    def getChild(self, name, request):
        try:
            plugin = self.pm.getPluginByName(name)
        except:
            return NoResource()
        else:
            return File(os.path.join(os.path.dirname(plugin.path), "ui.html"))


class ConfigureManager(xmlrpc.XMLRPC):
    pass

if __name__ == '__main__':
    from twisted.internet import reactor
    init_pm()
    r = Resource()
    r.putChild("action", ActionsManager())
    r.putChild("ui", UIManager())
    r.putChild("configure", ConfigureManager())
    reactor.listenTCP(34340, server.Site(r))
    reactor.run()
