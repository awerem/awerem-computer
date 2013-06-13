#!/bin/env python

import json
from twisted.internet.task import deferLater
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from yapsy.PluginManager import PluginManagerSingleton
from twisted.internet import reactor


class CoreManager(Resource):
    """Manager for core action"""

    def __init__(self, pollmanager):
        Resource.__init__(self)
        self.pm = PluginManagerSingleton.get()
        self.pollmanager = pollmanager

    def _delayedAnswer(self, request):
        self.pollmanager.setRequest(request)

    def render_GET(self, request):
        try:
            get = request.args["get"][0]
        except:
            pass
        else:
            if get == "plugin_list":
                return self.pluginsList()
            elif get == "infos":
                d = deferLater(reactor, 0, lambda: request)
                d.addCallback(self._delayedAnswer)
                return NOT_DONE_YET

    def pluginsList(self):
        """Return the list of the plugin"""
        plugins = []
        for plugin in self.pm.getAllPlugins():
            plugins.append(dict(plugin.plugin_object.getInfo(),
                                name=plugin.name))
        return json.dumps(plugins)
