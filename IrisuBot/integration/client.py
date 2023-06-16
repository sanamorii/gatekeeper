import socket
import json

class ServerClient(object):
    """Client for the MCServer plugin.

    Args:
        `port` (int): Select the socket port. default: 5555
    """
    def __init__(self, port:int = 5555) -> None:
        self.host = "127.0.0.1"
        self.port = port
        self.server : socket.socket = None
    
    def _connect(self):
        # AF_INET - used for ipv4 address
        # SOCK_STREAM - tcp only, SOCK_DGRAM used by udp
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.host, self.port))
    
    