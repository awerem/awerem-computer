from modules.aweremplugin import AweRemPlugin
import subprocess
from twisted.web import xmlrpc
from twisted.internet import reactor


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
        self.shutTimer = None
        self.handler = LinuxHandler(self)

    def getHandler(self):
        return self.handler

    def shutdown(self, s, m, h, d):
        shutTime = d * 24 * 3600 + h * 3600 + m * 60 + s
        try:
            self.shutTimer.cancel()
        except:
            pass
        self.shutTimer = reactor.callLater(shutTime, lambda: subprocess.call(
            ["gnome-session-quit", "--power-off"]))
        return True
