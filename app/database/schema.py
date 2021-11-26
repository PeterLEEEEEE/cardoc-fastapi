from pydantic.main import BaseModel
from typing import List


class UserRegister(BaseModel):
    user_id: str
    password: str
    role: str = None

class Login(BaseModel):
    user_id: str = None
    password: str = None


class Item(BaseModel):
    id: str
    trimId: int


class TireInfoRegister(BaseModel):
    item: List[Item]