import json

from genpy import message

from core.exceptions import StateException


class Message:
    def __init__(self, msg_type: str):
        """
        Wrapper code to integrate ros message
        :param msg_type: The name of the message
        """
        # TODO: THIS IS STILL CALLING ROS CODE
        self.msg_class = message.get_message_class(msg_type, reload_on_error=False)
        if self.msg_class is None:
            raise StateException("Topic tracking didnt work")
        self.type = msg_type
        self.md5sum = self.msg_class._md5sum
        # TODO: NEED TO FILL MESSAGES

    @classmethod
    def from_json(cls, o):
        """
        Create a node object from a json string
        :param o: A JSON object
        :return: A node object
        """
        class_dict = json.loads(o)
        cls.type = class_dict['type']
        return cls(msg_type=cls.type)
