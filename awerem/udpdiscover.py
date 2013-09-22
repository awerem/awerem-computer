#!/bin/python

import confloader
from twisted.internet.protocol import DatagramProtocol


class UDPDiscover(DatagramProtocol):
    """
    Respond when a client tries to discover the server in the local network
    The answer looks like this:
        awerem
        pong
        [TOKEN]
        [UUID of the awerem server]
        [Name of the server]
    """

    def datagramReceived(self, data, (host, port)):
        lines = data.split("\n")
        if lines[0] == "awerem" and lines[1] == "ping":
            answer = ("awerem\npong\n" + lines[2] + "\n"
                      + confloader.get_uuid() + "\n"
                      + confloader.get_server_name())
            self.transport.write(answer,
                                 (host, port))
