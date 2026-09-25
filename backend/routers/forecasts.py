from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Product, Order, OrderItem, ForeCast
from uuid import UUID
from forecasting import forecast, stockout, reorder

router = APIRouter(prefix = "/forecasts", tags = ["Forecasts"])

@router.post("/product/{product_id}")
async def generate(product_id:int, db: Session = Depends(get_db)):
  result = await db.execute(select(Product).where(Product.id == product_id))
  product = result.scalar_one_or_none()

  if not product:
    raise HTTPException(404, "Product Not Found!")

  end = date.today()
  start = end - timedelta(days = 89)

  # orders = (
  #   db.query(Order, OrderItem)
  #   .join(OrderItem,OrderItem.order_id == Order.id)
  #   .filter(OrderItem.product_id==product_id,
  #           Order.status == "confirmed",
  #           Order.created_at >= start
  #           ).all()
  # )

  result = await db.execute(
    select(Order, OrderItem)
    .join(OrderItem,OrderItem.order_id == Order.id)
    .filter(OrderItem.product_id==product_id,
            Order.status == "confirmed",
            Order.created_at >= start
            )
  )
  orders = result.all()

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
  await db.commit()
  await db.refresh(result)
  return result

@router.get("/")
async def get_forecasts(product_id: UUID, db: AsyncSession = Depends(get_db)):
  query = select(ForeCast).order_by(ForeCast.created_at.desc())
  db_result = await db.execute(query)
  return db_result.scalars().all()