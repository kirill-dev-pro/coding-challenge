from fastapi import FastAPI

from .database import SessionLocal
from .models import Item

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items", response_model=Item)
def read_item():
    items = get_db().query(Item).get.all()
    return items
