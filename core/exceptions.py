class StateException(Exception):
    def __init__(self, message):
        """
        Custom exception for when the robot state isn't expected
        :param message:
        """
        self.message = message
