import json


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
            self.requet = None
