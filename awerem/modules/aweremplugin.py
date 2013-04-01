from yapsy.IPlugin import IPlugin


class AweRemPlugin(IPlugin):
    """Interface for the AweRem modules"""

    def activate(self):
        print("activated")

    def do(self, args):
        """Called when an http request is done"""
        raise Exception("Shouldn't be called")
