# Node class definition for common communication of scripts
import json
import socket


class Node:
    '''
        Defines a Ros node class, which allows a common structure for passing information about ros nodes
    '''

    def __init__(self, ip_addr: str, port: str, notes: str = ''):
        try:
            socket.inet_aton(ip_addr)
        except socket.error:
            print("Invalid IP address given to create node")
            raise
        self.ip_addr = ip_addr
        self.port = port
        self.notes = notes

    def toJSON(self):
        return json.dumps({"ip_addr": self.ip_addr, "port": self.port, "notes": self.notes}, sort_keys=True, indent=4)

    @classmethod
    def fromJSON(cls, o):
        classdict = json.loads(o)
        cls.ip_addr = classdict['ip_addr']
        cls.port = classdict['port']
        cls.notes = classdict['notes']
        return cls(ip_addr=cls.ip_addr, port=cls.port, notes=cls.notes)
