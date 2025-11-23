from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class UserUpdate(BaseModel):
    username: str | None = None
    role: str | None = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
