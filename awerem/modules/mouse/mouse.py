#!/bin/python

from modules.aweremplugin import AweRemPlugin, AweRemHandler
from pymouse import PyMouse


class MouseHandler(AweRemHandler):

    def __init__(self, mouse):
        self.mouse = mouse

    def out_click(self, button):
        """
        Click with the mouse at the current position
        """
        button = int(button)
        self.mouse.click(button)
        return True

    def out_move(self, x, y):
        """
        Move the mouse relatively at its current position
        jsonstr - The json string received
        """
        x = int(x)
        y = int(y)
        self.mouse.move(x, y)
        return True

    def out_press(self, button):
        button = int(button)
        self.mouse.press(button)
        return True

    def out_release(self, button):
        button = int(button)
        self.mouse.release(button)
        return True


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

    def press(self, button, x=None, y=None):
        curx, cury = self.realMouse.position()
        if x is None:
            x = curx
        if y is None:
            y = cury
        self.realMouse.press(x, y, button)

    def release(self, button, x=None, y=None):
        curx, cury = self.realMouse.position()
        if x is None:
            x = curx
        if y is None:
            y = cury
        self.realMouse.release(x, y, button)

    def move(self, deltaX, deltaY):
        curx, cury = self.realMouse.position()
        if deltaX is not None:
            curx += deltaX
        if deltaY is not None:
            cury += deltaY
        self.realMouse.move(curx, cury)

    def moveAbsolute(self, x, y):
        self.realMouse.move(x, y)
