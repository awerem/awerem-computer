from modules.aweremplugin import AweRemPlugin
import subprocess
from twisted.web import xmlrpc
from twisted.internet import reactor
import platform
import re
import json


class LinuxHandler(xmlrpc.XMLRPC):
    """
    XMLRPC Handler for Linux Remote
    """
    def __init__(self, linux):
        xmlrpc.XMLRPC.__init__(self)
        self.linux = linux

    def xmlrpc_shutdown(self, jsontime):
        """
        Shutdown the computer at the given time
        seconds - The number of seconds to wait
        minutes - The number of minutes to wait
        hours - the number of hours to wait
        days - the number of days to wait
        """
        time = json.loads(jsontime)
        s = int(time['seconds'])
        m = int(time['minutes'])
        h = int(time['hours'])
        d = int(time['days'])
        if s >= 0 and m >= 0 and h >= 0 and d >= 0:
            return self.linux.shutdown(s, m, h, d)
        else:
            raise ValueError("date must be positive")

    def xmlrpc_updateVolume(self, volume):
        """
        Update the volume of the system at the given percentage
        volume - the percentage of the volume to be set
        """
        vol = int(json.loads(volume))
        if vol > 100:
            vol = 100
        elif vol < 0:
            vol = 0
        return json.dumps(self.linux.updateVolume(vol))

    def xmlrpc_getCurrentVolume(self):
        return self.linux.getCurrentVolume()


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

    def getCurrentVolume(self):
        try:
            sinks_info = subprocess.check_output(["pacmd", "list-sinks"])
            sinks_info.lower()
        except subprocess.CalledProcessError:
            print("pulseaudio is not used")
        else:
            return re.search(r"\*.*?volume.*?(\d+)%", sinks_info,
                             re.DOTALL).group(1)

    def updateVolume(self, volume):
        succeeded_once = False
        try:
            sinks_list = subprocess.check_output(["pactl", "list", "short",
                                                  "sinks"]).lower()
        except subprocess.CalledProcessError:
            print("pulseaudio is not used")
        else:
            for match in re.finditer(r"^(\d+).*?running", sinks_list,
                                     re.MULTILINE):
                sink = match.group(1)
                volume_str = str(volume) + "%"
                try:
                    subprocess.call(["pactl", "set-sink-volume", sink,
                                     volume_str])
                except:
                    pass
                else:
                    succeeded_once = True
            if succeeded_once:  # If it succeeded, plays a little sound
                try:
                    subprocess.Popen(["canberra-gtk-play",
                                     "--id=audio-volume-change"])
                except:
                    pass
        return self.getCurrentVolume()
