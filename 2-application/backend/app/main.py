import uvicorn
from fastapi import FastAPI, Depends

from app.database import SessionLocal
from app.schema import Item
from app.models import ItemModel

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


@app.get("/items", response_model=list[Item])
def read_item(db=Depends(get_db)):
    items = db.query(ItemModel).all()
    if not items:
        return []
    return items


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    start()
