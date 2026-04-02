from fastapi import APIRouter
from schemas.stock import StockCreate, StockResponse
from services.stock_services import create_stock, get_all_stocks

router = APIRouter()

@router.post("/stocks", response_model=StockResponse)
def create(stock: StockCreate):
    return create_stock(stock)


@router.get("/stocks", response_model=list[StockResponse])
def get_all():
    return get_all_stocks()