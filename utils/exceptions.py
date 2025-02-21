class RwException(Exception):
    pass

class TrainNotFoundException(RwException):
    pass

class RwBackendException(RwException):
    pass

class InvalidResponseException(RwException):
    pass
