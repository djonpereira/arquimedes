import json
from pathlib import Path


DATA_FILE = Path(".data/rafael-progress.json")


REQUIRED_SESSION_MODES = [
    "Escolha Múltipla",
    "Missão Quiz",
    "Liga as Ideias",
    "Problema em Campo",
    "Laboratório de Escrita",
]


def load_progress() -> dict:
    if not DATA_FILE.exists():
        return {"total_xp": 0, "subjects": {}, "streak": 0, "study_cycles": 0, "pauses_used": 0, "last_cycle": 0, "session_modes": [], "current_quarter": 1, "completed_quarters": [], "quarter_modes": {"1": [], "2": [], "3": [], "4": []}}
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"total_xp": 0, "subjects": {}, "streak": 0, "study_cycles": 0, "pauses_used": 0, "last_cycle": 0, "session_modes": [], "current_quarter": 1, "completed_quarters": [], "quarter_modes": {"1": [], "2": [], "3": [], "4": []}}


def save_progress(progress: dict) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")


def award_quiz(subject: str, topic: str, xp: int) -> dict:
    progress = load_progress()
    progress["total_xp"] = progress.get("total_xp", 0) + xp
    subjects = progress.setdefault("subjects", {})
    topic_data = subjects.setdefault(subject, {}).setdefault(topic, {"xp": 0, "completed": 0})
    topic_data["xp"] += xp
    topic_data["completed"] += 1
    save_progress(progress)
    return progress


def complete_session_mode(mode: str) -> dict:
    progress = load_progress()
    modes = progress.setdefault("session_modes", [])
    if mode not in modes:
        modes.append(mode)
    save_progress(progress)
    return progress


def is_session_complete(progress: dict) -> bool:
    modes = set(progress.get("session_modes", []))
    return all(mode in modes for mode in REQUIRED_SESSION_MODES)


def reset_session_modes() -> dict:
    progress = load_progress()
    progress["session_modes"] = []
    save_progress(progress)
    return progress


def complete_current_quarter() -> dict:
    progress = load_progress()
    current = progress.get("current_quarter", 1)
    completed = progress.setdefault("completed_quarters", [])
    if current not in completed:
        completed.append(current)
    progress["session_modes"] = []
    progress["quarter_modes"] = progress.get("quarter_modes", {})
    progress["quarter_modes"][str(current)] = list(REQUIRED_SESSION_MODES)

    if current < 4:
        progress["current_quarter"] = current + 1
    else:
        progress["current_quarter"] = 4

    save_progress(progress)
    return progress
