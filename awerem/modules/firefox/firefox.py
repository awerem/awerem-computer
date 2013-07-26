#!/bin/python

import re

from modules.aweremplugin import AweRemPlugin, AweRemHandler
from processesmanager import ProcessesManagerSingleton


class FirefoxHandler(AweRemHandler):

    def __init__(self, firefox):
        self.firefox = firefox

    def out_change_hist(self, howmany):
        self.firefox.change_hist(howmany)


class Firefox(AweRemPlugin):
    """
    Firefox remote
    """

    def __init__(self):
        self.handler = None
        self.info = None
        self.procmanager = None

    def activate(self):
        """
        Triggered when the plugin is activated by Yapsy
        """
        self.handler = FirefoxHandler(self)
        self.info = {"title": "Firefox", "category": "contextual",
                     "priority": -1}
        self.procmanager = ProcessesManagerSingleton.get()
        self.procmanager.addCallback(re.compile(r".*firefox.*"),
                                     self.state_change)

    def state_change(self, running):
        if running:
            self.info["priority"] = 0
        else:
            self.info["priority"] = -1
        self.pollmanager.updateNavigationDrawer()

    def getHandler(self):
        return self.handler

    def getInfo(self):
        return self.info

    def getIconPath(self, dpi):
        return "res/icons/icon_mdpi.png"

    def change_hist(self, howmany):
        """
        Send a notification to firefox so that the current tab goes back or
        forward with a step of `howmany`
        """
        self.pollmanager.addInfo({"command": "change_hist",
                                  "howmany": howmany}, "firefox")
