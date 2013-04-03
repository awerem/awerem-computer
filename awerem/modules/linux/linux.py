from modules.aweremplugin import AweRemPlugin
import re
import os
import subprocess
from modules.moduleErrors import ARModuleError


class LinuxRemote(AweRemPlugin):
    """Print "RedButton Triggered" when polled"""

    def activate(self):
        self.actions = {"shutdown": self.shutdown}
        self.display = os.environ["DISPLAY"]
        self.timeRe = re.compile(
            r"^((?P<days>\d+)day)?((?P<hours>\d+)hour)?((?P<minutes>\d+)min)?$")

    def do(self, args):
        try:
            call = self.actions[args["action"][0]]
        except Exception as e:
            print(e)
            raise ARModuleError("Unknown action")
        else:
            return call(**args)

    def shutdown(self, time=[None], **kwargs):
        time = time[0]
        if time is None:
            subprocess.call(["gnome-session-quit", "--power-off"])
        elif isinstance(time, str) and self.timeRe.match(time) is not None:
            proc = subprocess.Popen(["at", "now", "+", time],
                    stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)
            proc.communicate(input=b"DISPLAY=" + bytes(self.display, "ascii") +
                             b" gnome-session-quit --power-off")
            proc.wait()
        else:
            raise ARModuleError("Invalid date")
        return "success"
