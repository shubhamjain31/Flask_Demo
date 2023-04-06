

class ValidationException(Exception):
    def __init__(self, data, status_code, msg):
        self.data = data
        self.status_code = status_code
        self.msg = msg