"""
Modulebinder provides ways to create binder between Awerem modules
"""
from twisted.internet import reactor

_registrations = {}
_waiting = {}


def register(name, binder_class, registered, args=None, kwargs=None):
    """
    Register a binder class that will be instancied for each module which wants
    to communicate with `himself`, the binder class will be instanciate like
    this: bind_class(himself, the_requester, *args, **kwargs)

    If any requester are in the waiting list, the binder class

    name -- The id of the registration
    bind_class -- a class object (or a function) that will be the binder
                  between the registered object and the requester one
    registered -- the object that will be bond to the requester object
    args -- a list of args that will be attached at the end of the
            bind_class __init__ method.
    kwargs -- a dict of args that will be attached at the end of the
              bind_class __init__ method.
    """
    args = args or []
    kwargs = kwargs or {}
    _registrations[name] = (binder_class, registered, args, kwargs)
    _trigger_waiting(name)


def request_binder(name, requester, callback):
    """
    Request a binder object with the id `name`, when a binder object can be
    instanciate, it will be sent as an argument for the `callback` function.
    The requester must be the object that will be bond by the binder object.

    name -- the id of registration the requester will be bond to.
    requester -- The object the binder will bind with the registered.
    callback -- the callback to be triggered when the binder object is
                instanciate.
    """
    try:
        _waiting[name].append((requester, callback))
    except KeyError:
        _waiting[name] = [(requester, callback)]
    _trigger_waiting(name)


def _trigger_waiting(name):
    """
    Trigger the instanciation of the binders and trigger the callbacks through
    twisted.
    """
    bind_class, registered, args, kwargs = _registrations[name]
    for requester, callback in _waiting[name]:
        reactor.callLater(0, callback,
                          bind_class(registered, requester, *args, **kwargs))
