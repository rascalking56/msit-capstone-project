from sqlalchemy.orm import Session
from my_app.models.audit import AuditLog


class AuditService:

    @staticmethod
    def log(db: Session, user: str, action: str, before: dict | None, after: dict | None):
        entry = AuditLog(
            user=user,
            action=action,
            before_state=before,
            after_state=after
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
