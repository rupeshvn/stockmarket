from sqlalchemy import Column, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class StockData(Base):
    __tablename__ = "stock_data"

    date = Column(DateTime, primary_key=True)
    open = Column(Float)
    close = Column(Float)