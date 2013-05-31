from yapsy.IPlugin import IPlugin


class AweRemPlugin(IPlugin):
    """Interface for the AweRem modules"""

    def activate(self):
        raise NotImplementedError("Shouldn't be called")

    def getHandler(self):
        """Returns the xmlrpc handler for the plugin"""
        raise NotImplementedError("Shouldn't be called")

    def getInfo(self):
        """Returns informations about the plugin in a dict.
        The dictionnary must be like this:
            title: The title displayed to the user
            category: "contextual" or "utils"
            icon: The relative path to the icon of the module
            priority: 0  - The app the module controls has the focus
                      1  - The app the module controls is launched
                      2  - The app the module controls is system-wide
                      -1 - The app the module controls is not launched (won't
                           be displayed)"""
        return {"title": "Not Implemented", "icon": None,
                "category": "contextual", "priority": 2}
        raise NotImplementedError("Shouldn't be called")
