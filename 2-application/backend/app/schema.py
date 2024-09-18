from typing import Union

from pydantic import BaseModel


class Item(BaseModel):
    id: int
    title: str
    description: Union[str, None] = None
    is_active: bool
