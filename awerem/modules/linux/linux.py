from modules.aweremplugin import AweRemPlugin
import re
import os
import subprocess


class LinuxRemote(AweRemPlugin):
    """Print "RedButton Triggered" when polled"""

    def activate(self):
        self.actions = {"shutdown": self.shutdown}
        self.display = os.environ["DISPLAY"]
        self.timeRe = re.compile(
            r"^((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)m)?$")

    def do(self, args):
        try:
            call = LinuxRemote.actions[args["action"]]
        except Exception:
            raise Exception("Unknown action")
        else:
            call(**args)

    def shutdown(self, time, **kwargs):
        # TODO Finish this function
        if time is None:
            subprocess.call(["gnome-session-quit", "--power-off"])
        elif isinstance(time, str) and self.timeRe.match(time) is not None:
            subprocess.call(["at", "now", "+", time],
                            stdin=b"DISPLAY=" + bytes(self.display, "ascii") +
                            b"gnome-session-quit --power-off")
        print("success")
