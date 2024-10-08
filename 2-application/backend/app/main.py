import uvicorn
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database import SessionLocal
from app.schema import OrderCreate, OrderResponse
from app.models import Order

from sqlalchemy.orm import Session
import asyncio


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


# Buggy endpoints


# 1. SQL Injection vulnerability
@app.get("/orders/search")
def search_orders(query: str, db: Session = Depends(get_db)):
    # Bug: SQL Injection vulnerability
    sql_query = f"SELECT * FROM orders WHERE product LIKE '%{query}%'"
    result = db.execute(sql_query).fetchall()
    return result


# 2. Race condition
@app.post("/orders/batch")
async def create_batch_orders(orders: List[OrderCreate], db: Session = Depends(get_db)):
    for order in orders:
        # Bug: Potential race condition
        await asyncio.sleep(1)  # Simulate some processing time
        db_order = Order(**order.dict())
        db.add(db_order)
    db.commit()
    return {"message": "Batch orders created"}


# 3. N+1 query problem
@app.get("/users/order_count")
def get_user_order_counts(db: Session = Depends(get_db)):
    users = db.query(Order.user_id).distinct().all()
    result = []
    for user in users:
        # Bug: N+1 query problem
        count = db.query(Order).filter(Order.user_id == user.user_id).count()
        result.append({"user_id": user.user_id, "order_count": count})
    return result


# 4. Improper error handling
@app.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        # Bug: Improper error handling
        order = db.query(Order).filter(Order.id == order_id).one()
        return order
    except Exception as e:
        # This exposes sensitive information
        return {"error": str(e)}


# 5. Lack of pagination
@app.get("/all_orders")
def get_all_orders(db: Session = Depends(get_db)):
    # Bug: Lack of pagination
    return db.query(Order).all()


# 6. Insecure direct object reference
@app.get("/order_details/{order_id}")
def get_order_details(order_id: int, user_id: int, db: Session = Depends(get_db)):
    # Bug: Insecure direct object reference
    # No check if the order belongs to the user
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        return order
    raise HTTPException(status_code=404, detail="Order not found")


# 7. Inefficient database query
@app.get("/expensive_products")
def get_expensive_products(db: Session = Depends(get_db)):
    # Bug: Inefficient database query
    all_orders = db.query(Order).all()
    expensive_products = [order for order in all_orders if order.total_price > 1000]
    return expensive_products


# 8. Input validation bug
@app.post("/orders/create-with-discount")
def create_order_with_discount(
    user_id: int,
    product: str,
    quantity: int,
    price: float,
    discount_percent: float,
    db: Session = Depends(get_db),
):
    # Bug: Missing input validation for discount_percent
    # This allows for negative discounts or discounts over 100%
    discounted_price = price * (1 - discount_percent / 100)
    total_price = discounted_price * quantity

    new_order = Order(
        user_id=user_id, product=product, quantity=quantity, total_price=total_price
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


# 9. Dependency injection bug
def get_user_service():
    # This should normally return a user service instance
    # Bug: Always returns None, simulating a misconfigured dependency
    return None


@app.get("/users/{user_id}/orders")
def get_user_orders(
    user_id: int,
    user_service: dict = Depends(get_user_service),
    db: Session = Depends(get_db),
):
    # Bug: Doesn't handle the case where user_service is None
    if user_service.get("is_admin", False):  # This will raise an AttributeError
        # If user is admin, return all orders
        return db.query(Order).all()
    else:
        # If not admin, return only user's orders
        return db.query(Order).filter(Order.user_id == user_id).all()


def start():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    start()
