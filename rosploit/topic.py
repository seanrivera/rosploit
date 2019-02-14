from rosploit.message import Message


class Topic:
    """
        Define a Ros Topic class which allows for sharing infomation about topics
    """

    def __init__(self, topic_name: str, message: Message, reg_type: str, protocol: str):
        self.name = topic_name
        self.message = message
        self.message_type = message.type
        self.md5_sum = message.md5sum
        self.reg_type = reg_type
        self.protocol = protocol
