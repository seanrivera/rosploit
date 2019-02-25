from unittest import TestCase

# TODO: Import names are screwy
import rosploit


class TestRosploit(TestCase):
    def test_scan_node(self):
        original_input = __builtins__.input
        __builtins__.raw_input = lambda _: '1'
        self.assertIsNotNone(rosploit.rosploit())
        __builtins__.raw_input = original_input
