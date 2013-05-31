#!/bin/env python

from twisted.web import xmlrpc, server
from twisted.web.resource import Resource
from twisted.web.static import File
from yapsy.PluginManager import PluginManagerSingleton
from yapsy.PluginFileLocator import (PluginFileLocator,
                                     PluginFileAnalyzerWithInfoFile)
from modules.aweremplugin import AweRemPlugin
from uimanager import UIManager
from coremanager import CoreManager


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


class ConfigureManager(xmlrpc.XMLRPC):
    pass

if __name__ == '__main__':
    from twisted.internet import reactor
    init_pm()
    r = Resource()
    r.putChild("core", CoreManager())
    r.putChild("action", ActionsManager())
    r.putChild("ui", UIManager())
    r.putChild("configure", ConfigureManager())
    r.putChild("resources", File("resources"))
    reactor.listenTCP(34340, server.Site(r))
    reactor.run()
