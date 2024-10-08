from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Order
from datetime import datetime, timedelta
import random

# Database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create table if not exists
Base.metadata.create_all(bind=engine)

# Sample data
products = [
    "Laptop",
    "Smartphone",
    "Headphones",
    "Tablet",
    "Smartwatch",
    "Camera",
    "Gaming Console",
    "Bluetooth Speaker",
    "E-reader",
    "Fitness Tracker",
]


def create_sample_order():
    return {
        "user_id": random.randint(1, 10),
        "product": random.choice(products),
        "quantity": random.randint(1, 5),
        "total_price": round(random.uniform(50, 1000), 2),
        "order_date": datetime.utcnow() - timedelta(days=random.randint(0, 30)),
    }


def insert_sample_data():
    db = SessionLocal()
    try:
        # Create 50 sample orders
        sample_orders = [Order(**create_sample_order()) for _ in range(50)]
        db.add_all(sample_orders)
        db.commit()
        print("Sample data inserted successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    insert_sample_data()
