from twisted.internet import reactor


_messages = {}
_callbacks = {}


def add_message(name, info):
    """Add a message to the list of messages at the id `name`"""
    try:
        _messages[name].append(info)
    except KeyError:
        _messages[name] = [info]
    reactor.callLater(0, _trigger_callbacks)


def set_callback(name, callback):
    """Set a callback at the id `name`"""
    _callbacks[name] = callback
    reactor.callLater(0, _trigger_callbacks)


def _trigger_callbacks():
    """Trigger the callbacks if there is any info available"""
    for name, info in _messages.items():
        if info and _callbacks[name]:
            reactor.callLater(0, _callbacks[name], info)
            _messages[name] = []
