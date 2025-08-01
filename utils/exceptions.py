class RwException(Exception):
    pass

# Исключение для обработки ситуации, если поезд по заданному номеру не был найден в расписании
class TrainNotFoundException(RwException):
    pass

# Исключение для внутренних ошибок API БЖД (при попытке получения расписания на )
class RwBackendException(RwException):
    pass

class InvalidResponseException(RwException):
    pass
