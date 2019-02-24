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
