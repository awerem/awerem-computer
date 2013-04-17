#!/bin/env python
# -*- coding:utf8 -*-

from twisted.web import xmlrpc, server
from yapsy.PluginManager import PluginManagerSingleton
from yapsy.PluginFileLocator import (PluginFileLocator,
                                     PluginFileAnalyzerWithInfoFile)
from modules.aweremplugin import AweRemPlugin


class ModulesManager(xmlrpc.XMLRPC):

    def __init__(self):
        xmlrpc.XMLRPC.__init__(self)
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
            self.putSubHandler(plugin.name, plugin.plugin_object.getHandler())

if __name__ == '__main__':
    from twisted.internet import reactor
    r = ModulesManager()
    reactor.listenTCP(34340, server.Site(r))
    reactor.run()
