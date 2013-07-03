from modules.aweremplugin import AweRemPlugin
import subprocess
from twisted.web import xmlrpc
from twisted.internet import reactor
import platform
import re


class LinuxHandler(xmlrpc.XMLRPC):
    """
    XMLRPC Handler for Linux Remote
    """
    def __init__(self, linux):
        xmlrpc.XMLRPC.__init__(self)
        self.linux = linux

    def xmlrpc_shutdown(self, seconds=0, minutes=0, hours=0, days=0):
        """
        Shutdown the computer at the given time
        seconds - The number of seconds to wait
        minutes - The number of minutes to wait
        hours - the number of hours to wait
        days - the number of days to wait
        """
        s = int(seconds)
        m = int(minutes)
        h = int(hours)
        d = int(days)
        if s >= 0 and m >= 0 and h >= 0 and d >= 0:
            return self.linux.shutdown(s, m, h, d)
        else:
            raise ValueError("date must be positive")


class LinuxRemote(AweRemPlugin):
    """
    Some controls for Linux systems.
    """

    def activate(self):
        if platform.system().lower() == "linux":
            self.shutTimer = None
            self.priority = 2
            self.isLinux = True
        else:
            self.priority = -1
        self.handler = LinuxHandler(self)

    def getHandler(self):
        return self.handler

    def getInfo(self):
        return {"title": self.getName(), "category": "contextual",
                "priority": self.priority}

    def getName(self):
        if not self.isLinux:
            return "Not linux"
        else:
            if platform.linux_distribution() != "":
                return platform.linux_distribution()[0]
            else:
                return "Linux"

    def shutdown(self, s, m, h, d):
        shutTime = d * 24 * 3600 + h * 3600 + m * 60 + s
        try:
            self.shutTimer.cancel()
        except:
            pass
        self.shutTimer = reactor.callLater(shutTime, lambda: subprocess.call(
            ["gnome-session-quit", "--power-off"]))
        return True

    def updateVolume(self, volume):
        volume = int(volume)
        if volume > 100:
            volume = 100
        elif volume < 0:
            volume = 0
        succeeded_once = False
        try:
            sinks_list = subprocess.check_output(["pactl", "list", "short",
                                                  "sinks"])
        except subprocess.CalledProcessError:
            print("pulseaudio is not used")
        else:
            for match in re.findIter(r"^(\d+).*?running", sinks_list,
                                     re.MULTILINE):
                sink = match.group(1)
                volume_str = volume + "%"
                try:
                    subprocess.call(["pactl", "set-sink-volume", sink,
                                     volume_str])
                except:
                    pass
                else:
                    succeeded_once = True
            if succeeded_once:  # If it succeeded, plays a little sound
                try:
                    subprocess.call(["canberra-gtk-play",
                                     "--id=audio-volume-change"])
                except:
                    pass
        return self.getCurrentVolume()
