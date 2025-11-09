from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
class UserSchema(BaseModel):
    id: int
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr