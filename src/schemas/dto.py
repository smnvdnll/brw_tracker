from dataclasses import dataclass


@dataclass
class TrackerQuery():
    from_: str
    to: str
    date_ru: str
    train_number: str