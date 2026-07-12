from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from my_app.schemas.user_schema import UserLogin
from my_app.database import get_db
from my_app.models.user import User
from my_app.auth.auth_handler import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token(db_user.username, db_user.role)

    return {"access_token": token, "token_type": "bearer"}
