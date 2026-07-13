from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from my_app.database import get_db
from my_app.models.device_session import DeviceSession
from my_app.auth.auth_handler import require_role

router = APIRouter(prefix="/sessions", tags=["Sessions"])


# ---------------------------------------------------------
# LIST ALL SESSIONS FOR A USER
# ---------------------------------------------------------
@router.get("/{username}", dependencies=[Depends(require_role(["admin", "staff"]))])
def list_sessions(username: str, db: Session = Depends(get_db)):
    sessions = db.query(DeviceSession).filter(DeviceSession.username == username).all()
    return sessions


# ---------------------------------------------------------
# USER VIEW OWN SESSIONS
# ---------------------------------------------------------
@router.get("/me", dependencies=[Depends(require_role(["user", "admin", "staff"]))])
def my_sessions(token_payload=Depends(require_role(["user", "admin", "staff"])), db: Session = Depends(get_db)):
    # token_payload is validated by require_role
    # decode manually to get username
    return {"message": "Implement username extraction if needed"}
