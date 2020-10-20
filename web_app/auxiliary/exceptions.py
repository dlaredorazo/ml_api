class FileError(Exception):

    def __init__(self, message, errors=[]):
        super().__init__(message)

        self.errors = errors

class UnspecifiedModel(Exception):

    def __init__(self, message, errors=[]):
        super().__init__(message)

        self.errors = errors

class InitializationError(Exception):

    def __init__(self, message, errors=[]):
        super().__init__(message)

        self.errors = errors

class DataError(Exception):

    def __init__(self, message, errors=[]):
        super().__init__(message)

        self.errors = errors

class InferenceError(Exception):

    def __init__(self, message, errors=[]):
        super().__init__(message)

        self.errors = errors