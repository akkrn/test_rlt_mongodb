import json
from datetime import datetime


def is_valid_json(text: str) -> bool:
    """
    Validate input json string
    """
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False
    required_keys = {"dt_from", "dt_upto", "group_type"}
    if not all(key in data for key in required_keys):
        return False
    try:
        datetime.fromisoformat(data["dt_from"])
        datetime.fromisoformat(data["dt_upto"])
    except ValueError:
        return False
    if data["group_type"] not in {"hour", "day", "month"}:
        return False
    return True
