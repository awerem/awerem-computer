#!/bin/python

from twisted.web import xmlrpc
from yapsy.PluginManager import PluginManagerSingleton


class ActionsManager(xmlrpc.XMLRPC):
    """
    Resource that executes all the actions provided by the plugins
    """
    def __init__(self):
        xmlrpc.XMLRPC.__init__(self, allowNone=True)
        self.pm = PluginManagerSingleton.get()
        for plugin in self.pm.getAllPlugins():
            self.putSubHandler(plugin.name, plugin.plugin_object.getHandler())
