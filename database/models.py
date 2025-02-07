from sqlalchemy import BigInteger, Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, unique=True, primary_key=True, autoincrement=False)
    brw_trackers = relationship(argument="BRWTracker", back_populates="user")


class BRWTracker(Base):
    __tablename__ = "trackers"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    departure_station = Column(String, nullable=False)
    arrival_station = Column(String, nullable=False)
    departure_date = Column(String, nullable=False)
    train_number = Column(String, nullable=False)
    is_turned_on = Column(Boolean, nullable=False)

    user_telegram_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    user = relationship("User", back_populates="brw_trackers")

    def __str__(self):
        return f"{self.departure_station} -> {self.arrival_station}, {self.departure_date}, {self.train_number}"
