def success(message: str, data=None):
    return {
        "status": "success",
        "message": message,
        "data": data
    }


def error(message: str, details=None):
    return {
        "status": "error",
        "message": message,
        "details": details
    }


def paginated(data, page: int, page_size: int, total: int):
    return {
        "status": "success",
        "page": page,
        "page_size": page_size,
        "total_items": total,
        "total_pages": (total + page_size - 1) // page_size,
        "items": data
    }
