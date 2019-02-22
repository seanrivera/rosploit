from core.message import Message
from core.tcpros import TCPROS


class Topic:
    """
        Define a Ros Topic class which allows for sharing infomation about topics
    """

    def __init__(self, topic_name: str, message: Message, protocol: str):
        self.name = topic_name
        self.message = message
        self.message_type = message.type
        self.md5_sum = message.md5sum
        self.protocol = protocol
        self.tcpros = None

    def create_tcpros(self, direction: str, ip_addr: str, port: int, caller_node=""):
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
