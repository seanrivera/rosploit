#!/usr/bin/python3
#
import socket
import struct


class TCPROS:
    """
    TCPROS reimplementation Object
    """
    def __init__(self, connection_type="", message_definition="", caller_id="", service="", md5sum="", message_type="",
                 tcp_nodelay="0", topic="",
                 latching="0", persistent="0", error="", data="", ip_addr="", port=0, items=None):
        self.connection_type = connection_type
        self.message_definition = message_definition
        self.caller_id = caller_id
        self.service = service
        self.md5sum = md5sum
        self.message_type = message_type
        self.tcp_nodelay = tcp_nodelay
        self.latching = latching
        self.persistent = persistent
        self.error = error
        self.topic = topic
        self.header = None
        self.data = data
        self.items = items
        self.port = port
        self.ip_addr = ip_addr
        self.sock = None

    def __del__(self):
        if self.sock:
            self.sock.close()

    @classmethod
    def subscriber(cls, message_definition: str, caller_id: str, topic: str, md5sum: str, message_type: str, port: int,
                   ip_addr: str,
                   tcp_nodelay='0', error="", data=""):
        cls.message_definition = message_definition
        cls.caller_id = caller_id
        cls.topic = topic
        cls.md5sum = md5sum
        cls.message_type = message_type
        cls.tcp_nodelay = tcp_nodelay
        cls.error = error
        cls.data = data
        cls.port = port
        cls.ip_addr = ip_addr
        cls.items = {'message_definition': message_definition, 'caller_id': caller_id, 'topic': topic, 'md5sum': md5sum,
                     'message_type': message_type, 'tcp_nodelay': tcp_nodelay}
        return cls(connection_type="subscription", message_definition=cls.message_definition, caller_id=cls.caller_id,
                   topic=cls.topic, md5sum=cls.md5sum, message_type=cls.message_type, tcp_nodelay=cls.tcp_nodelay,
                   error=cls.error, data=cls.data, items=cls.items, port=cls.port, ip_addr=cls.ip_addr)

    @classmethod
    def publisher(cls, message_definition: str, topic: str, md5sum: str, message_type: str, port: int, ip_addr: str,
                  caller_id="", latching="0", error="", data=""):
        cls.message_definition = message_definition
        cls.topic = topic
        cls.md5sum = md5sum
        cls.message_type = message_type
        cls.caller_id = caller_id
        cls.latching = latching
        cls.error = error
        cls.data = data
        cls.port = port
        cls.ip_addr = ip_addr
        cls.items = {'message_definition': message_definition, 'caller_id': caller_id, 'md5sum': md5sum,
                     'message_type': message_type, 'latching': latching}
        return cls(message_definition=cls.message_definition, topic=cls.topic, connection_type="publisher",
                   md5sum=cls.md5sum,
                   caller_id=cls.caller_id, latching=cls.latching, error=cls.error, data=cls.data, items=cls.items,
                   port=cls.port, ip_addr=cls.ip_addr)

    @classmethod
    def client(cls, caller_id: str, service: str, md5sum: str, message_type: str, port: int, ip_addr: str,
               persistent="0", error="", data="", ):
        cls.caller_id = caller_id
        cls.service = service
        cls.md5sum = md5sum
        cls.message_type = message_type
        cls.persistent = persistent
        cls.error = error
        cls.data = data
        cls.port = port
        cls.ip_addr = ip_addr

        cls.items = {'caller_id': caller_id, 'service': service, 'md5sum': md5sum, 'message_type': message_type,
                     'persistent': persistent}
        return cls(connection_type="client", caller_id=cls.caller_id, service=cls.service, md5sum=cls.md5sum,
                   persistent=cls.persistent, error=cls.error, data=cls.data, items=cls.items, port=cls.port,
                   ip_addr=cls.ip_addr)

    @classmethod
    def service(cls, caller_id: str, port: int, ip_addr: str, error="", data="", ):
        cls.caller_id = caller_id
        cls.error = error
        cls.data = data
        cls.items = {'caller_id': caller_id}
        cls.port = port
        cls.ip_addr = ip_addr
        return cls(connection_type="service", caller_id=cls.caller_id, error=cls.error, data=cls.data, items=cls.items,
                   port=cls.port, ip_addr=cls.ip_addr)

    def create_header(self):
        str_cls = str

        # encoding code taken from
        # https://github.com/ros/ros_comm/blob/247459207e20c1da109fc306e58b84d15c4107bd/tools/rosgraph/src/rosgraph/network.py
        # TODO: Cleanup
        # encode all unicode keys in the header. Ideally, the type of these would be specified by the api
        encoded_header = {}
        # TODO: Bad names
        for k, v in self.items.items():
            if isinstance(k, str_cls):
                k = k.encode('utf-8')
            if isinstance(v, str_cls):
                v = v.encode('utf-8')
            encoded_header[k] = v

        fields = [k + b"=" + v for k, v in sorted(encoded_header.items())]

        s = b''.join([struct.pack('<I', len(f)) + f for f in fields])
        self.header = struct.pack('<I', len(s)) + s

    def connect(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            # - # keepalive failures before actual connection failure
            s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 9)
            # - timeout before starting KEEPALIVE process
            s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 60)
            # - interval to send KEEPALIVE after IDLE timeout
            s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 10)
            if self.tcp_nodelay is "1":
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.sock = s
            self.sock.connect((self.ip_addr, self.port))
        except Exception as e:
            print(e)
