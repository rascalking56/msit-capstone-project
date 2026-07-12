import csv
from io import StringIO
from typing import List
from my_app.models.audit_log import AuditLog


class AuditExportService:

    @staticmethod
    def to_csv(logs: List[AuditLog]):
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "id", "username", "role", "resource_type", "resource_id",
            "action", "before", "after", "created_at"
        ])

        for log in logs:
            writer.writerow([
                log.id,
                log.username,
                log.role,
                log.resource_type,
                log.resource_id,
                log.action,
                log.before,
                log.after,
                log.created_at
            ])

        return output.getvalue()

    @staticmethod
    def to_pdf_data(logs: List[AuditLog]):
        # Logic only — no file creation
        pdf_lines = []
        for log in logs:
            pdf_lines.append(
                f"{log.created_at} | {log.username} ({log.role}) "
                f"{log.action} {log.resource_type}:{log.resource_id}"
            )
        return "\n".join(pdf_lines)
