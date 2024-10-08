from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    product = Column(String, index=True)
    quantity = Column(Integer)
    total_price = Column(Float)
    order_date = Column(DateTime, default=datetime.utcnow)
