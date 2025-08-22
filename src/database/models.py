from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    brw_trackers = relationship("BrwTracker", back_populates="user")


class BrwTracker(Base):
    __tablename__ = 'brw_trackers'

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    from_ = Column(String(50), nullable=False)
    to = Column(String(50), nullable=False)
    date = Column(String(50), nullable=False)
    train_number = Column(String(50), nullable=False)

    user_id = Column(BigInteger, ForeignKey("users.id"))
    user = relationship("User", back_populates="brw_trackers")