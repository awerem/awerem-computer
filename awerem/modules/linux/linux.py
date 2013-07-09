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

    def xmlrpc_shutdown(self, jsonstr):
        """
        Shutdown the computer at the given time
        seconds - The number of seconds to wait
        minutes - The number of minutes to wait
        hours - the number of hours to wait
        mode - The action to do: "power-off", "reboot"
        """
        if jsonstr:
            data = json.loads(jsonstr)
        else:
            data = {}
        try:
            s = int(data['seconds'])
        except:
            s = 0
        try:
            m = int(data['minutes'])
        except:
            m = 0
        try:
            h = int(data['hours'])
        except:
            h = 0
        try:
            mode = str(data['mode'])
        except:
            mode = "power-off"
        if mode != "power-off" and mode != "reboot":
            mode = "power-off"
        if s >= 0 and m >= 0 and h >= 0:
            return json.dumps(self.linux.shutdown(mode, s, m, h))
        else:
            raise ValueError("date must be positive")

    def xmlrpc_updateVolume(self, jsonstr):
        """
        Update the volume of the system at the given percentage
        volume - the percentage of the volume to be set
        """
        data = json.loads(jsonstr)
        vol = int(data["volume"])
        beep = bool(data["beep"])
        if vol > 100:
            vol = 100
        elif vol < 0:
            vol = 0
        return json.dumps(self.linux.updateVolume(vol, beep))

    def xmlrpc_getCurrentVolume(self, unused):
        return self.linux.getCurrentVolume()

    def xmlrpc_beep(self, unused):
        return json.dumps(self.linux.beep())


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

    def shutdown(self, mode, s, m, h):
        print(mode)
        shutTime = h * 3600 + m * 60 + s
        try:
            self.shutTimer.cancel()
        except:
            pass
        if mode == "power-off" or mode == "reboot":
            mode = "--" + mode
            self.shutTimer = reactor.callLater(
                shutTime, lambda: subprocess.call(["gnome-session-quit",
                                                   mode]))
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

    def updateVolume(self, volume, beep):
        succeeded_once = False
        try:
            sinks_list = subprocess.check_output(["pacmd", "list-sinks"]).lower()
        except subprocess.CalledProcessError:
            print("pulseaudio is not used")
        else:
            for match in re.finditer(r"\*.*index.*(\d+)", sinks_list,
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
            if succeeded_once and beep:
                self.beep()
        return self.getCurrentVolume()

    def beep(self):
        try:
            subprocess.Popen(["canberra-gtk-play",
                              "--id=audio-volume-change"])
        except:
            pass
        return True
