#!/bin/python
import psutil
from twisted.internet import task, threads


class ProcessesManager():
    """
    Manager that watch running processes and trigger callbacks when they
    span or die
    """

    def __init__(self):
        self.callbacks = []
        self.timer = task.LoopingCall(self.triggerCallbacks)

    def start(self):
        self.timer.start(3)

    def stop(self):
        self.timer.stop()

    def addCallback(self, regex, callback):
        self.callbacks.append({"regex": regex, "callback": callback,
                               "running": False})
        return len(self.callbacks)

    def removeCallback(self, id):
        self.callbacks[id] = None

    def triggerCallbacks(self):
        d = threads.deferToThread(self._gatherCallbacks)
        d.addCallback(self._executeCallbacks)

    def _gatherCallbacks(self):
        callbacks_to_trigger = []
        validCallbacks = [x for x in self.callbacks if x is not None]
        for elem in validCallbacks:
            running = False
            for process in psutil.process_iter():
                if elem["regex"].search(process.name):
                    running = True
                    break
            if ((not running and elem["running"]) or
                    (running and not elem["running"])):
                callbacks_to_trigger.append(lambda: elem["callback"](running))
            elem["running"] = running
        return callbacks_to_trigger

    def _executeCallbacks(self, callbacks):
        for callback in callbacks:
            callback()

class ProcessesManagerSingleton():

    __instance = None

    @classmethod
    def get(cls):
        if cls.__instance is None:
            cls.__instance = ProcessesManager()
        return cls.__instance
