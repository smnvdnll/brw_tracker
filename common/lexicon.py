from enum import Enum


class CommonMessages(Enum):
    main_menu = "Главное меню"


class BRWMessages(Enum):
    empty_trackers_list = "Список трекеров пусть :("
    trackers_list = "Ваш список трекеров"
    edit_tracker = "Меню редактирования параметров трекера"

    input_departure_station = "Введите название города отправления или станцию, указанную на сайте БЧ\n\nПример: Минск, Минск-Пассажирский"
    input_arrival_station = "Введите название города прибытия или станцию, указанную на сайте БЧ\n\nПример: Минск, Минск-Пассажирский"
    input_departure_date = "Введите дату отправления поезда в формате ГГГГ-ММ-ДД"
    input_train_number = "Введите номер поезда в формате 123Б\n\nЭто необходимо для того, чтобы я мог найти нужный поезд в расписании"

    incorrect_departure_station = "Станция отправления не найдена, попробуйте еще раз"
    incorrect_arrival_station = "Станция прибытия не найдена, попробуйте еще раз"
    incorrect_departure_date = "Вы ввели либо неверный формат даты, либо дату, которая уже прошла, либо дату, которая наступит через более чем 30 дней. Попробуйте еще раз"
    train_not_found = "Поезд с таким номером не был найден"

    monitoring_started = "Мониторинг запущен"
    train_already_leaved = "Поезд уже ушел"
    max_attempts_exceeded = "Превышено максимальное количество попыток"
    monitoring_ended = "Мониторинг завершен"

    def __str__(self):
        return self.value
