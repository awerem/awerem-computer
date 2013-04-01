from modules.aweremplugin import AweRemPlugin


class RedButton(AweRemPlugin):
    """Print "RedButton Triggered" when polled"""

    def do(self, args):
        print("RedButton Triggered")
