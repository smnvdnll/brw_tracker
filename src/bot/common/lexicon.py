from enum import Enum


class Messages(str, Enum):
    START = "Привет! Я бот для отслеживания мест на поездах в Белорусской железной дороге"


class Buttons(str, Enum):
    BRW = "БЧ"