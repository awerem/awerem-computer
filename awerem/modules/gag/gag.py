#!/bin/python

from modules.aweremplugin import AweRemPlugin, AweRemHandler
from processesmanager import ProcessesManagerSingleton
import messagemanager


class GagHandler(AweRemHandler):

    def __init__(self, gag):
        self.gag = gag
        self.actions_list = ["like", "dislike", "next", "prev"]

    def out_message(self, message):
        """
        Process the message sent
        """
        if message in self.actions_list:
            self.gag.pollmanager.addInfo(message, "firefox")


class Gag(AweRemPlugin):
    """
    Control a 9gag webpage
    """

    def activate(self):
        self.handler = GagHandler(self)
        self.info = {"title": "9gag", "category": "contextual",
                     "priority": -1}
        self.procmanager = ProcessesManagerSingleton.get()
        messagemanager.set_callback("9gag", self.on_messages)

    def state_change(self, running):
        if running:
            self.info["priority"] = 0
        else:
            self.info["priority"] = -1
        self.pollmanager.updateNavigationDrawer()

    def on_messages(self, messages):
        for message in messages:
            if message == "started":
                self.state_change(True)
            elif message == "stopped":
                self.state_change(False)

    def getHandler(self):
        return self.handler

    def getInfo(self):
        return self.info

    def getIconPath(self, dpi):
        return ""
