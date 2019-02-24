class StateException(Exception):
    def __init__(self, message):
        """
        Custom exception for when the robot state isn't what is expected
        :param message: Message for the user to diagnose the state.
        """
        self.message = message
