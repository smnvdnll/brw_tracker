from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

class TrackerQuery(BaseModel):
    from_: str
    to: str
    train_number: str
    date_: date

class TrackerQueryDraft(BaseModel):
    from_: Optional[str] = None
    to: Optional[str] = None
    date_: Optional[date] = None
    train_number: Optional[str] = None

    def set_from(self, from_: str) -> None: self.from_ = from_
    def set_to(self, to: str) -> None: self.to = to
    def set_date_ru(self, date_ru: str) -> None: self.date_ = datetime.strptime(date_ru, "%d.%m.%Y").date()
    def set_train_number(self, train_number: str) -> None: self.train_number = train_number

    def can_search_trains(self) -> bool:
        return (
            self.from_ is not None and isinstance(self.from_, str)
            and self.to is not None and isinstance(self.to, str)
            and self.date_ is not None and isinstance(self.date_, date)
        )

    def to_tracker_query(self) -> TrackerQuery:
        if not self.from_ or not self.to or not self.date_ or not self.train_number:
            raise ValueError("Not all fields are filled")

        return TrackerQuery(
            from_=self.from_,
            to=self.to,
            train_number=self.train_number,
            date_=self.date_
        )
