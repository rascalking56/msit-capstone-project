from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from my_app.models.audit import AuditLog


class AuditAnalyticsService:

    @staticmethod
    def filter_logs(db: Session, user=None, action=None, start=None, end=None):
        query = db.query(AuditLog)

        if user:
            query = query.filter(AuditLog.username == user)

        if action:
            query = query.filter(AuditLog.action == action)

        if start:
            query = query.filter(AuditLog.timestamp >= start)

        if end:
            query = query.filter(AuditLog.timestamp <= end)

        return query.order_by(AuditLog.timestamp.desc()).all()

    @staticmethod
    def suspicious_activity(db: Session):
        """
        Flags:
        - More than 5 failed logins in 10 minutes
        - More than 20 actions in 1 minute (bot-like)
        - Restock > 100 units at once
        """
        logs = db.query(AuditLog).all()
        suspicious = []

        # Failed login bursts
        failed_logins = [log for log in logs if log.action == "failed_login"]
        failed_logins.sort(key=lambda x: x.timestamp)

        for i in range(len(failed_logins) - 5):
            t1 = failed_logins[i].timestamp
            t2 = failed_logins[i + 5].timestamp
            if (t2 - t1).seconds <= 600:
                suspicious.append({
                    "type": "failed_login_burst",
                    "details": "6 failed logins within 10 minutes",
                    "start": t1,
                    "end": t2
                })

        # High-frequency actions
        logs_sorted = sorted(logs, key=lambda x: x.timestamp)
        for i in range(len(logs_sorted) - 20):
            t1 = logs_sorted[i].timestamp
            t2 = logs_sorted[i + 20].timestamp
            if (t2 - t1).seconds <= 60:
                suspicious.append({
                    "type": "high_frequency_actions",
                    "details": "20+ actions within 1 minute",
                    "start": t1,
                    "end": t2
                })

        # Large restocks
        for log in logs:
            if log.action == "restock" and "100" in (log.details or ""):
                suspicious.append({
                    "type": "large_restock",
                    "details": log.details,
                    "timestamp": log.timestamp
                })

        return suspicious

    @staticmethod
    def export_csv(logs):
        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "username", "action", "details", "timestamp"])

        for log in logs:
            writer.writerow([log.id, log.username, log.action, log.details, log.timestamp])

        return output.getvalue()

    @staticmethod
    def export_json(logs):
        return [
            {
                "id": log.id,
                "username": log.username,
                "action": log.action,
                "details": log.details,
                "timestamp": log.timestamp.isoformat()
            }
            for log in logs
        ]
