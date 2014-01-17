#!/bin/python

from modules.aweremplugin import AweRemPlugin, AweRemHandler
from processesmanager import ProcessesManagerSingleton


class RedButtonHandler(AweRemHandler):

    def __init__(self, redbutton):
        self.redbutton = redbutton

    def out_press(self):
        """
        Print "RedButton Triggered"
        """
        print("RedButton Triggered")
        self.redbutton.pollmanager.addInfo("redbutton")
        self.redbutton.info["priority"] = 999
        self.redbutton.pollmanager.updateNavigationDrawer()
        return True

    def out_custompress(self, message):
        print("Custom message: " + str(message))
        print(type(message))
        return True


class RedButton(AweRemPlugin):
    """
    Print "RedButton Triggered"
    """

    def activate(self):
        self.handler = RedButtonHandler(self)
        self.info = {"title": "RedButton", "category": "contextual",
                     "priority": 0}
        self.procmanager = ProcessesManagerSingleton.get()
        self.procmanager.addCallback(r".*sleep.*",
                                     self.sleepchange)

    def sleepchange(self, running):
        print(running)
        if running:
            self.info["priority"] = -1
        else:
            self.info["priority"] = 0
        self.pollmanager.updateNavigationDrawer()

    def getHandler(self):
        return self.handler

    def getInfo(self):
        return self.info

    def getIconPath(self, dpi):
        return "res/icons/icon_mdpi.png"
