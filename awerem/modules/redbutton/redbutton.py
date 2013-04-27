from modules.aweremplugin import AweRemPlugin
from twisted.web import xmlrpc


class RedButtonHandler(xmlrpc.XMLRPC):

    def __init__(self, redbutton):
        self.redbutton = redbutton

    def xmlrpc_press(self):
        """
        Print "RedButton Triggered"
        """
        print "RedButton Triggered"
        return True


class RedButton(AweRemPlugin):
    """
    Print "RedButton Triggered"
    """

    def activate(self):
        self.handler = RedButtonHandler(self)

    def getHandler(self):
        return self.handler