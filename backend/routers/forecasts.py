from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Product, Order, OrderItem, ForeCast
from forecasting import forecast, stockout, reorder

router = APIRouter(prefix = "/forecasts", tags = ["Forecasts"])

@router.post("/product/{product_id}")
def generate(product_id:int, db: Session = Depends(get_db)):
  product = db.query(Product).filter(Product.id == product_id).first()

  if not product:
    raise HTTPException(404, "Product Not Found!")

  end = date.today()
  start = end - timedelta(days = 89)

  orders = (
    db.query(Order, OrderItem)
    .join(OrderItem,OrderItem.order_id == Order.id)
    .filter(OrderItem.product_id==product_id,
            Order.status = "confirmed",
            Order.created_at >= start
            ).all()
  )

  demand = [0]*90
  for order, item in orders:
    i = (order.created_at.date()-start).days
    if 0 <= i < 90:
      demand[i] += item.quantity

  daily, confidence = forecast(demand)

  stockout_date = stockout(
    product.quantity,
    daily
  )

  reorder_quantity = reorder(
    product.quantity,
    daily
  )

  result = ForeCast(
    product_id  = product_id,
    daily_demand = daily,
    stockout_date = stockout_date,
    reorder_quantity = reorder_quantity,
    confidence = confidence,
    history_start = start,
    history_end = end
  )

  db.add(result)
  db.commit()
  db.refresh(result)
  return result

@router.get("/")
def get_forecasts(db: Session = Depends(get_db)):
  return db.query(Forecast).order_by(Forecast.created_at.desc()).all()