import json


class PollManagerBind():

    def __init__(self, pollmanager, moduleName):
        self.pollmanager = pollmanager
        self.moduleName = moduleName

    def addInfo(self, infos):
        self.pollmanager.addInfo(self.moduleName, infos)

    def updateNavigationDrawer(self):
        self.pollmanager.addInfo("core", "UpdateNavigationDrawer")


class PollManager():

    def __init__(self):
        """Initialize the PollManager"""
        self.infoDict = {}
        self.request = None

    def addInfo(self, name, infos):
        try:
            self.infoDict[name].append(infos)
        except KeyError:
            self.infoDict[name] = []
            self.infoDict[name].append(infos)
        self.sendData()

    def setRequest(self, request):
        self.request = request
        self.sendData()

    def sendData(self):
        if self.request is not None and self.infoDict:
            self.request.write(json.dumps(self.infoDict))
            self.request.finish()
            self.infoDict = {}
            self.request = None
