from sqlalchemy import Column, Float, DateTime
from app.db.base import Base

class StockData(Base):
    __tablename__ = "stock_data"

    date = Column(DateTime, primary_key=True)
    open = Column(Float)
    close = Column(Float)