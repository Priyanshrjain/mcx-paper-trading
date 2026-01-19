from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    balance = Column(Float, default=1_000_000)


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    commodity = Column(String)   # GOLD / SILVER
    side = Column(String)        # BUY / SELL
    price = Column(Float)
    lots = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
