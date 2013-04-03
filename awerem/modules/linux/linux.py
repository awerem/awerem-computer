from modules.aweremplugin import AweRemPlugin
from modules.moduleErrors import ARModuleError
import re


class LinuxRemote(AweRemPlugin):
    """Remote that controls all the common linux actions"""

    def activate(self):
        self.actions = {"shutdown": self.shutdown}
        self.timeRe = re.compile(
            r"^((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)m)?((?P<seconds>\d+)s)?$")

    def do(self, args):
        try:
            call = LinuxRemote.actions[args["action"]]
        except Exception:
            raise Exception("Unknown action")
        else:
            call(**args)

    def shutdown(self, time):
        # TODO Finish this function
        if time is None and self.datecompliant.match(time):
            raise ARModuleError("Invalid args")
