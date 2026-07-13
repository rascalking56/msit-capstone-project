from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from my_app.models.user import User
from my_app.auth.password_utils import hash_password


class UserService:

    @staticmethod
    def create_user(db: Session, username: str, password: str, role: str):
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        hashed_pw = hash_password(password)

        user = User(
            username=username,
            hashed_password=hashed_pw,
            role=role
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_role(db: Session, user_id: int, new_role: str):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.role = new_role
        db.commit()
        db.refresh(user)
        return user
