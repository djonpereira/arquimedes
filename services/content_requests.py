import json
from pathlib import Path
from datetime import datetime


REQUESTS_FILE = Path("data/content_requests.json")


def load_requests() -> list[dict]:
    if not REQUESTS_FILE.exists():
        return []
    try:
        data = json.loads(REQUESTS_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_request(subject: str, topic: str, activity_type: str, difficulty: str, request_text: str) -> dict:
    requests = load_requests()
    request = {
        "id": f"content-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "subject": subject,
        "topic": topic,
        "activity_type": activity_type,
        "difficulty": difficulty,
        "request": request_text.strip(),
        "status": "pending_review",
    }
    requests.append(request)
    REQUESTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    REQUESTS_FILE.write_text(json.dumps(requests, ensure_ascii=False, indent=2), encoding="utf-8")
    return request
