#!/bin/python

from modules.aweremplugin import AweRemPlugin
from twisted.web import xmlrpc


class RedButtonHandler(xmlrpc.XMLRPC):

    def __init__(self, redbutton):
        self.redbutton = redbutton

    def xmlrpc_press(self):
        """
        Print "RedButton Triggered"
        """
        print("RedButton Triggered")
        self.redbutton.pollmanager.addInfo("redbutton")
        self.redbutton.info["priority"] = 999
        self.redbutton.pollmanager.updateNavigationDrawer()
        return True


class RedButton(AweRemPlugin):
    """
    Print "RedButton Triggered"
    """

    def activate(self):
        self.handler = RedButtonHandler(self)
        self.info = {"title": "RedButton", "category": "contextual",
                     "priority": 0}

    def getHandler(self):
        return self.handler

    def getInfo(self):
        return self.info

    def getIconPath(self, dpi):
        return "res/icons/icon_mdpi.png"
