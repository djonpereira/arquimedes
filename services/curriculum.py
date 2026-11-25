CURRICULUM = {
    "Português": {
        "emoji": "PT",
        "grade": "9.º ano",
        "topics": {
            "Coordenação e subordinação": {
                "summary": "Coordenação, subordinação, orações coordenadas e subordinadas.",
                "level": "Rookie",
                "progress": 35,
            },
            "Orações coordenadas": {
                "summary": "Copulativas, adversativas, disjuntivas, conclusivas e explicativas.",
                "level": "Starter",
                "progress": 20,
            },
            "Orações subordinadas": {
                "summary": "Substantivas, adjetivas e adverbiais.",
                "level": "Starter",
                "progress": 10,
            },
            "Tipos e formas de discurso": {
                "summary": "Narrativo, descritivo, diálogo e tempos verbais.",
                "level": "Rookie",
                "progress": 0,
            },
        },
    },
    "Matemática": {
        "emoji": "M",
        "grade": "9.º ano",
        "topics": {
            "Funções": {"summary": "Funções, gráficos e regularidades.", "level": "Rookie", "progress": 0},
            "Geometria": {"summary": "Semelhança, trigonometria e círculos.", "level": "Rookie", "progress": 0},
        },
    },
    "Ciências Naturais": {
        "emoji": "CN",
        "grade": "9.º ano",
        "topics": {
            "Sistemas": {"summary": "Órgãos, tecidos e sistemas do corpo humano.", "level": "Rookie", "progress": 0},
            "Energia": {"summary": "Transformações, conservação e fontes de energia.", "level": "Rookie", "progress": 0},
        },
    },
    "História": {
        "emoji": "H",
        "grade": "9.º ano",
        "topics": {
            "Século XX": {"summary": "Guerras, regimes e transformações contemporâneas.", "level": "Rookie", "progress": 0},
            "Portugal": {"summary": "Estado Novo, revolução e democracia.", "level": "Rookie", "progress": 0},
        },
    },
    "Inglês": {
        "emoji": "EN",
        "grade": "9.º ano",
        "topics": {
            "Grammar": {"summary": "Tenses, conditionals and reported speech.", "level": "Rookie", "progress": 0},
            "Reading": {"summary": "Comprehension strategies and vocabulary.", "level": "Rookie", "progress": 0},
        },
    },
}

LEVELS = [
    ("Rookie", 0),
    ("Starter", 100),
    ("Contender", 250),
    ("All-Star", 450),
    ("MVP", 700),
]

STUDY_CYCLE_MINUTES = 30
SHORT_PAUSE_MINUTES = 15
HALFTIME_PAUSE_MINUTES = 30
QUARTER_COUNT = 4
GAME_PAUSE_MINUTES = HALFTIME_PAUSE_MINUTES
PAUSE_UNLOCK_XP = 100


def get_rank(total_xp: int) -> dict:
    rank = LEVELS[0][0]
    next_rank = None
    next_target = None

    for index, (name, minimum) in enumerate(LEVELS):
        if total_xp >= minimum:
            rank = name
            if index + 1 < len(LEVELS):
                next_rank = LEVELS[index + 1][0]
                next_target = LEVELS[index + 1][1]

    return {"rank": rank, "next_rank": next_rank, "next_target": next_target}


def get_pause_status(total_xp: int, pauses_used: int) -> dict:
    unlocked = total_xp // PAUSE_UNLOCK_XP
    available = max(0, unlocked - pauses_used)
    next_milestone = ((total_xp // PAUSE_UNLOCK_XP) + 1) * PAUSE_UNLOCK_XP

    return {"unlocked": unlocked, "available": available, "next_milestone": next_milestone}
