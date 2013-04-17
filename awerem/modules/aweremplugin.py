from yapsy.IPlugin import IPlugin


class AweRemPlugin(IPlugin):
    """Interface for the AweRem modules"""

    def activate(self):
        raise NotImplementedError("Shouldn't be called")

    def getHandler(self):
        """Returns the xmlrpc handler for the plugin"""
        raise NotImplementedError("Shouldn't be called")
