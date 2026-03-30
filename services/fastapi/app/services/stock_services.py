from app.models.stock import StockData
from app.db.database import SessionLocal

def create_stock(stock_data):
    db = SessionLocal()

    record = StockData(
        date=stock_data.date,
        open=stock_data.open,
        close=stock_data.close
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    # 👉 Signal-like logic
    print("Stock inserted:", record.date)

    db.close()
    return record


def get_all_stocks():
    db = SessionLocal()
    data = db.query(StockData).all()
    db.close()
    return data