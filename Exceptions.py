class InvalidMoveException(Exception):
    def __init__(self, message):
        self.message = message
        
class TooMuchObstacleException(Exception):
    def __init__(self, message):
        self.message = message