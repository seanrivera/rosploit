from typing import List, Tuple

from core.message import Message
from core.tcpros import TCPROS


class Topic:
    """
        Define a Ros Topic class which allows for sharing information about topics
    """

    def __init__(self, topic_name: str, message: Message, protocol: str):
        self.name = topic_name
        self.message = message
        self.message_type = message.type
        self.md5_sum = message.md5sum
        self.protocol = protocol
        self.tcpros = None

    @classmethod
    def from_master(cls, topic_list: List[Tuple[str, str]]):
        """
        Create a node object from a master xml list
        :param topic_list: A list of topics
        :return: A list of topic objects
        """
        return_list = []
        for topic in topic_list:
            return_list.append(cls(topic_name=topic[0], message=Message(msg_type=topic[1]), protocol="TCPROS"))
        return return_list

    def create_tcpros(self, direction: str, ip_addr: str, port: int, caller_node=""):
        """
        Create  a TCPROS Connection
        :param direction: The direction of the communication Publish or Subscribe
        :param ip_addr: IP address to connect to
        :param port: Port to connect to
        :param caller_node: Name of the node to give to the connection for the subscription
        :return: None
        """
        if "Publish" in direction:
            self.tcpros = TCPROS.publisher(message_definition=self.message, topic=self.name, md5sum=self.md5_sum,
                                           message_type=self.message_type, port=port, ip_addr=ip_addr)
        elif "Subscribe" in direction:
            self.tcpros = TCPROS.subscriber(message_definition=self.message, caller_id=caller_node, topic=self.name,
                                            md5sum=self.md5_sum, message_type=self.message_type, port=port,
                                            ip_addr=ip_addr)
        if self.tcpros:
            self.tcpros.connect()

    def publish(self, message: Message):
        self.tcpros.publish(message=message)
