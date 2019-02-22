# Node class definition for common communication of scripts
import json
import socket
import xmlrpc.client

from core.exceptions import StateException
from core.message import Message
from core.topic import Topic


class Node:
    """
        Defines a Ros node class, which allows a common structure for passing information about ros nodes
    """

    def __init__(self, ip_addr: str, port: str, notes: str = ''):
        try:
            socket.inet_aton(ip_addr)
        except socket.error:
            print("Invalid IP address given to create node")
            raise
        self.ip_addr = ip_addr
        self.port = port
        self.notes = notes
        self.server = xmlrpc.client.ServerProxy("http://" + self.ip_addr + ":" + self.port)
        self.pub_topics = []
        self.sub_topics = []

    def to_json(self):
        return json.dumps({"ip_addr": self.ip_addr, "port": self.port, "notes": self.notes}, sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, o):
        classdict = json.loads(o)
        cls.ip_addr = classdict['ip_addr']
        cls.port = classdict['port']
        cls.notes = classdict['notes']
        return cls(ip_addr=cls.ip_addr, port=cls.port, notes=cls.notes)

    def get_pub_list(self, node_name: str):
        try:
            (_, _, topic_list) = self.server.getPublications(node_name)
            for topic in topic_list:
                print(topic)
                message = Message(msg_type=topic[1])
                self.pub_topics.append(Topic(topic_name=topic[0], message=message, protocol="TCPROS"))
        except xmlrpc.client.Fault as err:
            print(err)

    def get_sub_list(self, node_name: str):
        try:
            (_, _, topic_list) = self.server.getSubscriptions(node_name)
            for topic in topic_list:
                message = Message(msg_type=topic[1])
                self.sub_topics.append(Topic(topic_name=topic[0], message=message, protocol="TCPROS"))
        except xmlrpc.client.Fault as err:
            print(err)

    def connect_to_pub(self, topic_name: str, node):
        """
        Call this function to subscribe to one of the topics that this node publishes
        :return:
        """
        target_topic = [x for x in self.pub_topics if x.name == topic_name]
        if len(target_topic) > 0:
            # TODO: Make less Hacky
            if len(target_topic) < 2:
                raise StateException("Node publishing the same topic twice. Error in list comprehension")
            (status, _, info) = self.server.requestTopic(node.name, topic_name, [["TCPROS"]])
            (proto, ip_addr, port) = info
            new_topic = Topic(topic_name=target_topic[0].name, message=target_topic[0].message,
                              protocol=target_topic[0].protocol)
            new_topic.create_tcpros(direction="Subscribe", ip_addr=ip_addr, port=port)
            node.sub_topics.append(new_topic)

        else:
            print("No such topic")
