from modules.aweremplugin import AweRemPlugin
import re
import os
import subprocess
from threading import Timer
from modules.moduleErrors import ARModuleError


class LinuxRemote(AweRemPlugin):
    """Print "RedButton Triggered" when polled"""

    def activate(self):
        self.actions = {"shutdown": self.shutdown}
        self.display = os.environ["DISPLAY"]
        self.timeRe = re.compile(
            r"^((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)m)?"
            r"((?P<seconds>\d+)s)?$")
        self.shutTimer = None

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
        else:
            try:
                m = self.timeRe.match(time)
            except TypeError:
                raise ARModuleError("Invalid date")
            else:
                if m is not None:
                    days = int(m.group("days") or 0)
                    hours = int(m.group("hours") or 0)
                    minutes = int(m.group("minutes") or 0)
                    seconds = int(m.group("seconds") or 0)
                    shutTime = (days * 24 * 3600 + hours * 3600 + minutes * 60
                                + seconds)
                    try:
                        self.shutTimer.cancel()
                    except:
                        pass
                    self.shutTimer = Timer(shutTime,
                                           lambda: subprocess.call(
                                           ["gnome-session-quit", "--power-off"]))
                    self.shutTimer.daemon = True
                    self.shutTimer.start()

                else:
                    raise ARModuleError("Invalid date")
        return "shutdown triggered"
