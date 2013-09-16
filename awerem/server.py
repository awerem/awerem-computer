#!/bin/env python

from twisted.web import xmlrpc, server
from twisted.web.resource import Resource
from twisted.web.static import File

from twisted.internet.protocol import DatagramProtocol

from yapsy.PluginManager import PluginManagerSingleton
from yapsy.PluginFileLocator import (PluginFileLocator,
                                     PluginFileAnalyzerWithInfoFile)
from modules.aweremplugin import AweRemPlugin
from uimanager import UIManager
from coremanager import CoreManager
from pollmanager import PollManager, PollManagerBind
from processesmanager import ProcessesManagerSingleton
import confloader

import logging
logging.basicConfig()


def init_pm(pollmanager):
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
        plugin.plugin_object.setPollManager(PollManagerBind(pollmanager,
                                                            plugin.name))
    return pm


class UDPDiscover(DatagramProtocol):
    """
    Respond when a client tries to discover the server in the local network
    The answer looks like this:
        awerem
        pong
        [TOKEN]
        [UUID of the awerem server]
        [Name of the server]
    """

    def datagramReceived(self, data, (host, port)):
        lines = data.split("\n")
        if lines[0] == "awerem" and lines[1] == "ping":
            answer = ("awerem\npong\n" + lines[2] + "\n"
                      + confloader.get_uuid() + "\n"
                      + confloader.get_server_name())
            self.transport.write(answer,
                                 (host, port))


class ActionsManager(xmlrpc.XMLRPC):
    """
    Resource that executes all the actions provided by the plugins
    """
    def __init__(self):
        xmlrpc.XMLRPC.__init__(self, allowNone=True)
        self.pm = PluginManagerSingleton.get()
        for plugin in self.pm.getAllPlugins():
            self.putSubHandler(plugin.name, plugin.plugin_object.getHandler())


class ConfigureManager(xmlrpc.XMLRPC):
    pass

if __name__ == '__main__':
    from twisted.internet import reactor
    pollmanager = PollManager()
    procmanager = ProcessesManagerSingleton.get()
    procmanager.start()
    init_pm(pollmanager)
    r = Resource()
    r.putChild("core", CoreManager(pollmanager))
    r.putChild("action", ActionsManager())
    r.putChild("ui", UIManager())
    r.putChild("configure", ConfigureManager())
    r.putChild("resources", File("resources"))
    reactor.listenTCP(34340, server.Site(r))
    reactor.listenUDP(34340, UDPDiscover())
    reactor.run()
