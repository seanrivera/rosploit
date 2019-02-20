from unittest import TestCase

# TODO: Import names are screwy
from core.tcpros import TCPROS


class TestTCPROS(TestCase):
    def test_subscriber(self):
        self.fail()

    def test_publisher(self):
        message_definition = "string data"
        caller_id = "rostopic_4767_1316912741557"
        latching = "1"
        md5sum = "992ce8a1687cec8c8bd883ec73ca41d1"
        topic = "/chatter"
        message_type = "std_msgs/String"
        data = "hello"
        test_sub = TCPROS.publisher(message_definition=message_definition, caller_id=caller_id, topic=topic,
                                    md5sum=md5sum,
                                    latching=latching, message_type=message_type, data=data)
        test_sub.create_header()
        print(test_sub.items.items())
        print(test_sub.header)
        print([hex(i) for i in test_sub.header])

    def test_client(self):
        self.fail()

    def test_service(self):
        self.fail()
