from pydantic import BaseModel, ConfigDict


# -----------------------------
# Base User Schema
# -----------------------------
class UserBase(BaseModel):
    username: str


# -----------------------------
# User Registration Schema
# -----------------------------
class UserCreate(UserBase):
    password: str
    role: str


# -----------------------------
# User Login Schema
# -----------------------------
class UserLogin(BaseModel):
    username: str
    password: str


# -----------------------------
# User Response Schema
# -----------------------------
class UserResponse(UserBase):
    role: str

    # Pydantic v2 replacement for orm_mode
    model_config = ConfigDict(from_attributes=True)
