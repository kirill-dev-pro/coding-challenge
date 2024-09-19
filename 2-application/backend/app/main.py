import uvicorn
from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database import SessionLocal
from app.schema import Item
from app.models import ItemModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {"Hello": "World"}


@app.get("/items", response_model=List[Item])
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
