class BrwException(Exception):
    message = "траблы"
    def __str__(self):
        return self.message


class InvalidDate(BrwException):
    message = "Некорректная дата. Дата должна быть в формате 'ДД.ММ.ГГГГ'" \
              "и не может быть в прошлом или более чем через 55 дней."


class StationNotFound(BrwException):
    def __init__(self, name: str):
        self.message = f"Станция '{name}' не найдена."
        super().__init__(self.message)


class NoDirectRoute(BrwException):
    message = "Нет прямого маршрута между указанными станциями."


class UnexpectedError(BrwException):
    def __init__(self, message: str = ""):
        self.message = "Неизвестная ошибка. " + message
        super().__init__(self.message)