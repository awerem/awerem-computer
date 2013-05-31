#!/bin/env python

import json
from twisted.web.resource import Resource
from yapsy.PluginManager import PluginManagerSingleton


class CoreManager(Resource):
    """Manager for core action"""

    def __init__(self):
        Resource.__init__(self)
        self.pm = PluginManagerSingleton.get()

    def render_GET(self, request):
        if request.args["get"][0] == "plugin_list":
            return self.pluginsList()

    def pluginsList(self):
        """Return the list of the plugin"""
        plugins = []
        for plugin in self.pm.getAllPlugins():
            plugins.append(plugin.getInfo())
        return json.dump(plugins)
