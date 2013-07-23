#!/bin/python
import psutil
from twisted.web import task, threads


class ProcessesManager():
    """
    Manager that watch running processes and trigger callbacks when they
    span or die
    """

    def __init__(self):
        self.callbacks = []

    def start(self):
        task.loopingCall(self.triggerCallbacks, 3)

    def register(self, regex, callback):
        self.callbacks.append({"regex": regex, "callback": callback,
                               "running": True})
        return self.callbacks.length

    def unregister(self, id):
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
