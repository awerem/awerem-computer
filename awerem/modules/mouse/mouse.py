#!/bin/python

from modules.aweremplugin import AweRemPlugin
from twisted.web import xmlrpc
import json
from pymouse import PyMouse


class MouseHandler(xmlrpc.XMLRPC):

    def __init__(self, mouse):
        self.mouse = mouse

    def xmlrpc_click(self, jsonstr):
        """
        Click with the mouse at the current position
        """
        try:
            mouse_click = int(json.loads(jsonstr))
        except Exception as e:
            raise e
        else:
            return self.mouse.click(mouse_click)

    def xmlrpc_move(self, jsonstr):
        """
        Move the mouse relatively at its current position
        jsonstr - The json string received
        """
        movement = json.loads(jsonstr)
        x = int(movement["x"])
        y = int(movement["y"])
        return json.dumps(self.mouse.move(x, y))

    def xmlrpc_press(self, jsonstr):
        button = int(json.loads(jsonstr))
        return self.mouse.press(button)

    def xmlrpc_release(self, jsonstr):
        button = int(json.loads(jsonstr))
        return self.mouse.release(button)


class MouseRemote(AweRemPlugin):
    """
    Print "RedButton Triggered"
    """

    def activate(self):
        self.realMouse = PyMouse()
        self.handler = MouseHandler(self)
        self.info = {"title": "Mouse", "category": "utils",
                     "priority": 0}

    def getHandler(self):
        return self.handler

    def getInfo(self):
        return self.info

    def getIconPath(self, dpi):
        return ""

    def click(self, button, x=None, y=None):
        curx, cury = self.realMouse.position()
        if x is None:
            x = curx
        if y is None:
            y = cury
        self.realMouse.click(x, y, button)
        return True

    def press(self, button, x=None, y=None):
        curx, cury = self.realMouse.position()
        if x is None:
            x = curx
        if y is None:
            y = cury
        self.realMouse.press(x, y, button)
        return True

    def release(self, button, x=None, y=None):
        curx, cury = self.realMouse.position()
        if x is None:
            x = curx
        if y is None:
            y = cury
        self.realMouse.release(x, y, button)
        return True

    def move(self, deltaX, deltaY):
        curx, cury = self.realMouse.position()
        if deltaX is not None:
            curx += deltaX
        if deltaY is not None:
            cury += deltaY
        self.realMouse.move(curx, cury)
        return True

    def moveAbsolute(self, x, y):
        self.realMouse.move(x, y)
        return True
