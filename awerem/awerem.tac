#!/bin/env python

from twisted.application import internet, service
from twisted.web import server
from twisted.web.resource import Resource
from twisted.web.static import File


from yapsy.PluginManager import PluginManagerSingleton
from yapsy.PluginFileLocator import PluginFileLocator,\
    PluginFileAnalyzerWithInfoFile

from udpdiscover import UDPDiscover
from actionsmanager import ActionsManager

from modules.aweremplugin import AweRemPlugin
from uimanager import UIManager
from coremanager import CoreManager
from pollmanager import PollManager, PollManagerBind
from processesmanager import ProcessesManagerSingleton

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


def get_web_service():
    pollmanager = PollManager()
    procmanager = ProcessesManagerSingleton.get()
    procmanager.start()
    init_pm(pollmanager)
    r = Resource()
    r.putChild("core", CoreManager(pollmanager))
    r.putChild("action", ActionsManager())
    r.putChild("ui", UIManager())
    r.putChild("resources", File("resources"))
    return internet.TCPServer(34340, server.Site(r))


def get_udp_discover():
    return internet.UDPServer(34340, UDPDiscover())

application = service.Application("AweRem Server")
webserv = get_web_service()
webserv.setServiceParent(application)

discoverserv = get_udp_discover()
discoverserv.setServiceParent(application)
