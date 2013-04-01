from modules.aweremplugin import AweRemPlugin
import threading

class LinuxRemote(AweRemPlugin):
    """Print "RedButton Triggered" when polled"""

    actions = {"shutdown": self.shutdown}

    def activate(self):
        self.audioRemote = PulseRemote()
        # TODO Make this regex
        re.compile(r"")

    def do(self, args):
        try:
            call = LinuxRemote.actions[args["action"]]
        except Exception as e:
            raise Exception("Unknown action")
        else:
            call(**args)

    def shutdown(self, time):
        # TODO Finish this function
        if time is None and :
            raise Exception("Invalid args")

