# Node class definition for common communication of scripts
import socket


class Node:
    '''
        Defines a Ros node class, which allows a common structure for passing information about ros nodes
    '''

    def __init__(self, ip_addr: str, port: str):
        try:
            socket.inet_aton(ip_addr)
        except socket.error:
            print("Invalid IP address given to create node")
            raise
        self.ip_addr = ip_addr
        self.port = port
