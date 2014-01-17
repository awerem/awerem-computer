import json


class PollManagerBind():

    def __init__(self, pollmanager, moduleName):
        self.pollmanager = pollmanager
        self.moduleName = moduleName

    def addInfo(self, infos, destination="phone"):
        self.pollmanager.addInfo(destination, self.moduleName, infos)

    def updateNavigationDrawer(self):
        self.pollmanager.addInfo("phone", "core", "UpdateNavigationDrawer")


class PollManager():

    def __init__(self):
        """Initialize the PollManager"""
        self.infoDict = {}
        self.requests = {}

    def addInfo(self, destination, name, infos):
        try:
            self.infoDict[destination]
        except KeyError:
            self.infoDict[destination] = {}
        try:
            self.infoDict[destination][name].append(infos)
        except KeyError:
            self.infoDict[destination][name] = [infos]
        self.sendData(destination)

    def setRequest(self, request):
        try:
            dest = request.args["dest"][0]
        except KeyError:
            dest = "phone"
        self.requests[dest] = request
        self.sendData(dest)

    def sendData(self, dest):
        try:
            request = self.requests[dest]
            data = self.infoDict[dest]
        except:
            pass
        else:
            if request and data:
                request.write(json.dumps(data))
                request.finish()
                self.infoDict[dest] = {}
                self.requests[dest] = None
