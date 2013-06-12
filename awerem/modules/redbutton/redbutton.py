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
        return True


class RedButton(AweRemPlugin):
    """
    Print "RedButton Triggered"
    """

    def activate(self):
        self.handler = RedButtonHandler(self)

    def getHandler(self):
        return self.handler

    def getInfo(self):
        return {"title": "RedButton", "category": "contextual",
                "priority": 0, "icon": None}

    def getIconPath(self, dpi):
        return "res/icons/icon_mdpi.png"
