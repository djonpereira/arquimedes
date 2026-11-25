import json
from datetime import datetime
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
        return {"total_xp": 0, "subjects": {}, "streak": 0, "study_cycles": 0, "pauses_used": 0, "last_cycle": 0, "session_modes": [], "current_quarter": 1, "completed_quarters": [], "quarter_modes": {"1": [], "2": [], "3": [], "4": []}, "timeout_usage": {"1": 0, "2": 0, "3": 0, "4": 0}}
    try:
        progress = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        if not progress.get("active_game"):
            progress["timeout_usage"] = {"1": 0, "2": 0, "3": 0, "4": 0}
        return progress
    except (json.JSONDecodeError, OSError):
        return {"total_xp": 0, "subjects": {}, "streak": 0, "study_cycles": 0, "pauses_used": 0, "last_cycle": 0, "session_modes": [], "current_quarter": 1, "completed_quarters": [], "quarter_modes": {"1": [], "2": [], "3": [], "4": []}, "timeout_usage": {"1": 0, "2": 0, "3": 0, "4": 0}}


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


def save_mini_game_result(mode: str, points: int, percentage: int, passed: bool) -> dict:
    progress = load_progress()
    quarter = progress.get("current_quarter", 1)
    results = progress.setdefault("mini_game_results", {})
    quarter_results = results.setdefault(str(quarter), {})
    quarter_results[mode] = {
        "points": int(points),
        "percentage": int(percentage),
        "passed": bool(passed),
        "closed": True,
    }

    if passed:
        modes = progress.setdefault("session_modes", [])
        if mode not in modes:
            modes.append(mode)

    active = progress.get("active_game")
    if active:
        quarter_points = active.setdefault("quarter_points", {"1": 0, "2": 0, "3": 0, "4": 0})
        quarter_points[str(quarter)] = sum(int(item.get("points", 0)) for item in quarter_results.values())
        active["final_points"] = sum(int(value) for value in quarter_points.values())
        for record in progress.setdefault("game_rankings", []):
            if record.get("id") == active["id"]:
                record.update(active)

    save_progress(progress)
    return quarter_results[mode]


def get_mini_game_result(mode: str) -> dict | None:
    progress = load_progress()
    quarter = progress.get("current_quarter", 1)
    return progress.setdefault("mini_game_results", {}).get(str(quarter), {}).get(mode)


def start_game_record(subject: str, topic: str) -> dict:
    progress = load_progress()
    if progress.get("active_game"):
        return progress

    active = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "start_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "subject": subject,
        "topic": topic,
        "quarter_points": {"1": 0, "2": 0, "3": 0, "4": 0},
        "final_points": 0,
        "level": "Rookie",
        "status": "running",
    }
    progress["active_game"] = active
    progress["mini_game_results"] = {}
    progress["session_modes"] = []
    progress["completed_quarters"] = []
    progress["current_quarter"] = 1
    progress["quarter_modes"] = {"1": [], "2": [], "3": [], "4": []}
    progress["timeout_usage"] = {"1": 0, "2": 0, "3": 0, "4": 0}
    progress.setdefault("game_rankings", []).append(dict(active))
    save_progress(progress)
    return progress


def update_game_record_points(points: int) -> dict:
    progress = load_progress()
    active = progress.get("active_game")
    if not active:
        return progress

    quarter = str(progress.get("current_quarter", 1))
    active["quarter_points"][quarter] = int(points)
    active["final_points"] = sum(int(value) for value in active["quarter_points"].values())

    game_id = active["id"]
    for record in progress.setdefault("game_rankings", []):
        if record.get("id") == game_id:
            record.update(active)
    save_progress(progress)
    return progress


def finish_or_cancel_game(cancelled: bool = False) -> dict:
    progress = load_progress()
    active = progress.get("active_game")
    if not active:
        return progress

    active["status"] = "cancelled" if cancelled else "finished"
    active["final_points"] = sum(int(value) for value in active["quarter_points"].values())

    total_xp = int(progress.get("total_xp", 0))
    level = "Rookie"
    for name, minimum in (("Rookie", 0), ("Starter", 100), ("Contender", 250), ("All-Star", 450), ("MVP", 700)):
        if total_xp >= minimum:
            level = name
    active["level"] = level

    game_id = active["id"]
    for record in progress.setdefault("game_rankings", []):
        if record.get("id") == game_id:
            record.update(active)

    progress.pop("active_game", None)
    progress["current_quarter"] = 1
    progress["completed_quarters"] = []
    progress["session_modes"] = []
    progress["mini_game_results"] = {}
    progress["quarter_modes"] = {"1": [], "2": [], "3": [], "4": []}
    save_progress(progress)
    return progress


def complete_quarter_with_rest(short_pause_minutes: int, halftime_minutes: int) -> dict:
    progress = load_progress()
    active = progress.get("active_game")
    if not active:
        return progress

    current = int(progress.get("current_quarter", 1))
    completed = set(progress.setdefault("completed_quarters", []))
    completed.add(current)
    progress["completed_quarters"] = sorted(completed)
    progress["session_modes"] = []

    if current == 4:
        progress["quarter_modes"] = progress.get("quarter_modes", {})
        progress["quarter_modes"]["4"] = list(REQUIRED_SESSION_MODES)
        save_progress(progress)
        return finish_or_cancel_game(cancelled=False)

    pause_minutes = halftime_minutes if current == 2 else short_pause_minutes
    progress["rest_phase"] = {
        "after_quarter": current,
        "next_quarter": current + 1,
        "duration_minutes": pause_minutes,
        "remaining_seconds": pause_minutes * 60,
        "status": "resting",
    }
    progress["quarter_modes"] = progress.get("quarter_modes", {})
    progress["quarter_modes"][str(current)] = list(REQUIRED_SESSION_MODES)
    save_progress(progress)
    return progress
