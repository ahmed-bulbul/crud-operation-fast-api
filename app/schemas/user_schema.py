from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True   # ✅ Pydantic v2

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
