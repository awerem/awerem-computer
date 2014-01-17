from yapsy.IPlugin import IPlugin
from twisted.web import xmlrpc


class AweRemPlugin(IPlugin):
    """Interface for the AweRem modules"""

    def activate(self):
        """Called when the plugin is activated"""
        raise NotImplementedError("Shouldn't be called")

    def getHandler(self):
        """Returns the AweremPluginHandler for the plugin"""
        raise NotImplementedError("Shouldn't be called")

    def getInfo(self):
        """Returns informations about the plugin in a dict.
        The dictionnary must be like this:
            title: The title displayed to the user
            category: "contextual" or "utils"
            priority: 0  - The app the module controls has the focus
                      1  - The app the module controls is launched
                      2  - The app the module controls is system-wide
                      -1 - The app the module controls is not launched (won't
                           be displayed)"""
        return {"title": "Not Implemented",
                "category": "contextual", "priority": 2}
        raise NotImplementedError("Shouldn't be called")

    def getIconPath(self, dpi):
        """Returns the path of the icon depending of the dpi of the phone"""
        return "res/icons/icon_" + dpi + ".png"

    def setPollManager(self, pollmanager):
        self.pollmanager = pollmanager


class AweRemHandler(xmlrpc.XMLRPC):
    """
    All the plugin handlers must inherit from this class
    """

    def __init__(self):
        xmlrpc.XMLRPC.__init__(self)

    def lookupProcedure(self, procedurePath):
        """Abstract the protocol behind the Handler"""
        try:
            return getattr(self, "out_" + procedurePath)
        except:
            raise xmlrpc.NoSuchFunction(
                self.NOT_FOUND,
                "procedure %s not found" % procedurePath)
