from pydantic import BaseModel
from datetime import datetime

class StockCreate(BaseModel):
    date: datetime
    open: float
    close: float

class StockResponse(BaseModel):
    date: datetime
    open: float
    close: float

    class Config:
        from_attributes = True   # for SQLAlchemy compatibility