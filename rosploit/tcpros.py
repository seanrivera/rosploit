#!/usr/bin/python3
#
import struct


class TCPROS:
    def __init__(self, connection_type="", message_definition="", caller_id="", service="", md5sum="", message_type="",
                 tcp_nodelay="0", topic="",
                 latching="0", persistent="0", error="", data="", items=None):
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

    @classmethod
    def subscriber(cls, message_definition, caller_id, topic, md5sum, message_type, tcp_nodelay='0', error="", data=""):
        cls.message_definition = message_definition
        cls.caller_id = caller_id
        cls.topic = topic
        cls.md5sum = md5sum
        cls.message_type = message_type
        cls.tcp_nodelay = tcp_nodelay
        cls.error = error
        cls.data = data
        cls.items = {'message_definition': message_definition, 'caller_id': caller_id, 'topic': topic, 'md5sum': md5sum,
                     'message_type': message_type, 'tcp_nodelay': tcp_nodelay}
        return cls(connection_type="subscription", message_definition=cls.message_definition, caller_id=cls.caller_id,
                   topic=cls.topic, md5sum=cls.md5sum, message_type=cls.message_type, tcp_nodelay=cls.tcp_nodelay,
                   error=cls.error, data=cls.data, items=cls.items)

    @classmethod
    def publisher(cls, message_definition, topic, md5sum, message_type, caller_id="", latching="0", error="",
                  data=""):
        cls.message_definition = message_definition
        cls.topic = topic
        cls.md5sum = md5sum
        cls.message_type = message_type
        cls.caller_id = caller_id
        cls.latching = latching
        cls.error = error
        cls.data = data
        cls.items = {'message_definition': message_definition, 'caller_id': caller_id, 'md5sum': md5sum,
                     'message_type': message_type, 'latching': latching}
        return cls(message_definition=cls.message_definition, topic=cls.topic, connection_type="publisher",
                   md5sum=cls.md5sum,
                   caller_id=cls.caller_id, latching=cls.latching, error=cls.error, data=cls.data, items=cls.items)

    @classmethod
    def client(cls, caller_id: str, service: str, md5sum: str, message_type: str, persistent="0", error="", data=""):
        cls.caller_id = caller_id
        cls.service = service
        cls.md5sum = md5sum
        cls.message_type = message_type
        cls.persistent = persistent
        cls.error = error
        cls.data = data
        cls.items = {'caller_id': caller_id, 'service': service, 'md5sum': md5sum, 'message_type': message_type,
                     'persistent': persistent}
        return cls(connection_type="client", caller_id=cls.caller_id, service=cls.service, md5sum=cls.md5sum,
                   persistent=cls.persistent, error=cls.error, data=cls.data, items=cls.items)

    @classmethod
    def service(cls, caller_id, error="", data=""):
        cls.caller_id = caller_id
        cls.error = error
        cls.data = ""
        cls.items = {'caller_id': caller_id}
        return cls(connection_type="service", caller_id=cls.caller_id, error=cls.error, data=cls.data, items=cls.items)

    def create_header(self):
        str_cls = str

        # encoding code taken from https://github.com/ros/ros_comm/blob/247459207e20c1da109fc306e58b84d15c4107bd/tools/rosgraph/src/rosgraph/network.py
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
