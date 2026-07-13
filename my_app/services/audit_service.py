from datetime import datetime
from sqlalchemy.orm import Session
from my_app.models.audit import AuditLog


class AuditService:
    @staticmethod
    def log(
        db: Session,
        action: str,
        user: str | None = None,
        details: str | None = None
    ):
        """
        Write an audit log entry to the database.

        Parameters:
            db (Session): SQLAlchemy session
            action (str): The action performed (e.g., 'customer_created')
            user (str | None): The user performing the action
            details (str | None): Optional descriptive details
        """

        entry = AuditLog(
            user=user or "system",
            action=action,
            details=details,
            timestamp=datetime.utcnow(),
        )

        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
