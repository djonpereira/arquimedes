import json
from pathlib import Path


SETTINGS_FILE = Path("data/settings.json")
DEFAULTS = {
    "pass_threshold": 80,
    "penalty_points": 1,
    "short_pause_minutes": 15,
    "halftime_minutes": 30,
    "quarter_minutes": 30,
    "difficulty_escolha_multipla": "Misturada",
    "difficulty_missao_quiz": "Misturada",
    "difficulty_liga_ideias": "Misturada",
    "difficulty_problema_campo": "Misturada",
    "difficulty_escrita": "Misturada",
    "avatars_familia": ["Mãe", "Pops", "Mano", "Rafael", "Adriana"],
    "avatars_familia_basket": ["Patinho", "Cardadeiro", "Salvador", "Fradique", "Luís"],
    "avatars_brothers_bairro": ["Zezinho Dino", "Itamar", "Adriana", "Adri", "Salgueiro"],
    "avatars_vips_personagens": ["Luka", "Wemby", "Franklin", "Michael", "Jason"],
}


def load_settings() -> dict:
    try:
        if SETTINGS_FILE.exists():
            saved = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            if isinstance(saved, dict):
                settings = DEFAULTS.copy()
                settings.update(saved)
                return settings
    except (json.JSONDecodeError, OSError):
        pass
    return DEFAULTS.copy()


def save_settings(settings: dict) -> dict:
    merged = DEFAULTS.copy()
    merged.update(settings)
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    return merged


def calculate_pass(correct: int, total: int, settings: dict | None = None) -> dict:
    settings = settings or load_settings()
    percentage = round((correct / total) * 100) if total else 0
    threshold = int(settings["pass_threshold"])
    return {
        "percentage": percentage,
        "passed": percentage >= threshold,
        "threshold": threshold,
    }
