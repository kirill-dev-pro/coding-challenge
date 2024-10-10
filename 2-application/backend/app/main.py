import uvicorn
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
import asyncio

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from pydantic import BaseModel

# Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database model
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    product = Column(String, index=True)
    quantity = Column(Integer)
    total_price = Column(Float)
    order_date = Column(DateTime, default=datetime.utcnow)


# Pydantic models for response and request bodies
class OrderCreate(BaseModel):
    user_id: int
    product: str
    quantity: int
    total_price: float


class OrderResponse(BaseModel):
    id: int
    user_id: int
    product: str
    quantity: int
    total_price: float
    order_date: datetime


Base.metadata.create_all(bind=engine)


app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Order Management API"}


# Existing endpoints
@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders/{user_id}", response_model=List[OrderResponse])
def read_orders(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return orders


@app.get("/orders/search")
def search_orders(query: str, db: Session = Depends(get_db)):
    sql_query = f"SELECT * FROM orders WHERE product LIKE '%{query}%'"
    result = db.execute(sql_query).fetchall()
    return result


@app.post("/orders/batch")
async def create_batch_orders(orders: List[OrderCreate], db: Session = Depends(get_db)):
    for order in orders:
        await asyncio.sleep(1)
        db_order = Order(**order.dict())
        db.add(db_order)
    db.commit()
    return {"message": "Batch orders created"}


@app.get("/users/order_count")
def get_user_order_counts(db: Session = Depends(get_db)):
    users = db.query(Order.user_id).distinct().all()
    result = []
    for user in users:
        count = db.query(Order).filter(Order.user_id == user.user_id).count()
        result.append({"user_id": user.user_id, "order_count": count})
    return result


@app.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = db.query(Order).filter(Order.id == order_id).one()
        return order
    except Exception as e:
        return {"error": str(e)}


@app.get("/all_orders")
def get_all_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@app.get("/order_details/{order_id}")
def get_order_details(order_id: int, user_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        return order
    raise HTTPException(status_code=404, detail="Order not found")


@app.get("/expensive_products")
def get_expensive_products(db: Session = Depends(get_db)):
    all_orders = db.query(Order).all()
    expensive_products = [order for order in all_orders if order.total_price > 1000]
    return expensive_products


@app.post("/orders/create-with-discount")
def create_order_with_discount(
    user_id: int,
    product: str,
    quantity: int,
    price: float,
    discount_percent: float,
    db: Session = Depends(get_db),
):
    discounted_price = price * (1 - discount_percent / 100)
    total_price = discounted_price * quantity

    new_order = Order(
        user_id=user_id, product=product, quantity=quantity, total_price=total_price
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def get_user_service():
    return None


@app.get("/users/{user_id}/orders")
def get_user_orders(
    user_id: int,
    user_service: dict = Depends(get_user_service),
    db: Session = Depends(get_db),
):
    if user_service.get("is_admin", False):
        # If user is admin, return all orders
        return db.query(Order).all()
    else:
        # If not admin, return only user's orders
        return db.query(Order).filter(Order.user_id == user_id).all()


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start()
