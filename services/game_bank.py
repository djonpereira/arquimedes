import random


CONNECTION_BANK = []
RELATION_OPTIONS = ["Adição", "Oposição", "Alternativa", "Conclusão", "Explicação", "Causa", "Tempo", "Finalidade", "Concessão", "Condição"]

CONNECTION_TEMPLATES = [
    ("Rafael treinou e marcou", "Adição", "O «e» soma duas ações."),
    ("Rafael treinou muito, mas perdeu", "Oposição", "O «mas» introduz contraste."),
    ("Rafael pode estudar ou jogar", "Alternativa", "O «ou» apresenta escolhas."),
    ("Rafael estudou, logo passou", "Conclusão", "O «logo» apresenta uma conclusão."),
    ("Começa já, pois o treino começa", "Explicação", "O «pois» justifica a instrução."),
    ("Não jogou porque estava lesionado", "Causa", "O «porque» dá a razão."),
    ("Quando chegou, começou o aquecimento", "Tempo", "O «quando» situa no tempo."),
    ("Estudou para conseguir melhorar", "Finalidade", "A subordinada indica o objetivo."),
    ("Embora estivesse cansado, jogou", "Concessão", "O facto contrário não impede a ação."),
    ("Se melhorar, entra na equipa", "Condição", "A entrada depende da melhoria."),
]

CHARACTER_CONTEXTS = [
    ("Rafael", "treinou", "marcou"),
    ("Itamar", "treinou", "passou"),
    ("Zezinho Dino", "jogou", "assistiu"),
    ("Adriana", "estudou", "melhorou"),
    ("Salgueiro", "preparou", "ganhou"),
    ("Léo", "lançou", "marcou"),
    ("Reis", "reviu", "passou"),
    ("Adri", "organizou", "ajudou"),
    ("Mano", "aconselhou", "encorajou"),
    ("Mãe", "apoiou", "preparou"),
    ("Pops", "treinou", "ensinou"),
    ("Wemby", "defendeu", "pontuou"),
    ("Franklin", "aceitou", "cumpriu"),
    ("Michael", "planeou", "executou"),
]


CONNECTION_BANK.clear()
for template_index, (expression, relation, explanation) in enumerate(CONNECTION_TEMPLATES):
    for variant, (character, verb, result) in enumerate(CHARACTER_CONTEXTS):
        personalized = expression.replace("Rafael", character)
        personalized = personalized.replace("treinou", verb)
        personalized = personalized.replace("marcou", result)
        if variant >= 10:
            personalized = personalized.replace("o treino", f"o {character.lower()}")
        CONNECTION_BANK.append({
            "id": f"connection-{template_index}-{variant}",
            "left": personalized,
            "right": relation,
            "options": list(RELATION_OPTIONS),
            "tip": explanation,
            "difficulty": "easy" if template_index < 4 else "medium",
        })

for extra_variant in range(60):
    template_index = extra_variant % len(CONNECTION_TEMPLATES)
    expression, relation, explanation = CONNECTION_TEMPLATES[template_index]
    character, verb, result = CHARACTER_CONTEXTS[extra_variant % len(CHARACTER_CONTEXTS)]
    personalized = expression.replace("Rafael", character).replace("treinou", verb).replace("marcou", result)
    CONNECTION_BANK.append({
        "id": f"connection-extra-{extra_variant}",
        "left": personalized,
        "right": relation,
        "options": list(RELATION_OPTIONS),
        "tip": explanation,
        "difficulty": "medium",
    })

PROBLEM_BANK = []
PROBLEM_TEMPLATES = [
    {
        "scenario": "O árbitro viu uma falta. O treinador pediu a Rafael que saísse.",
        "options": ["Como o árbitro viu a falta, o treinador pediu a saída.", "O árbitro viu a falta, mas pediu a saída.", "O árbitro viu a falta, logo Rafael marcou."],
        "answer": "Como o árbitro viu a falta, o treinador pediu a saída.",
        "tip": "«Como» mantém a relação de causa entre o que aconteceu e a decisão.",
    },
    {
        "scenario": "Rafael estudou durante dias. Passou no teste.",
        "options": ["Como estudou durante dias, passou no teste.", "Estudou durante dias, mas passou no teste.", "Estudou durante dias ou passou no teste."],
        "answer": "Como estudou durante dias, passou no teste.",
        "tip": "A primeira parte explica a razão do bom resultado.",
    },
    {
        "scenario": "Rafael estava cansado. Entrou no último quarto.",
        "options": ["Embora estivesse cansado, entrou no último quarto.", "Se estivesse cansado, entrou no último quarto.", "Estava cansado, logo entrou no último quarto."],
        "answer": "Embora estivesse cansado, entrou no último quarto.",
        "tip": "Existe uma dificuldade, mas a ação continua a acontecer.",
    },
    {
        "scenario": "Treinou muito. Melhorou o lançamento.",
        "options": ["Porque treinou muito, melhorou o lançamento.", "Embora treinasse muito, melhorou o lançamento.", "Treinou muito ou melhorou o lançamento."],
        "answer": "Porque treinou muito, melhorou o lançamento.",
        "tip": "O treino explica a melhoria.",
    },
    {
        "scenario": "A equipa chegou cedo. Preparou a estratégia.",
        "options": ["Quando chegou cedo, preparou a estratégia.", "Embora chegasse cedo, preparou a estratégia.", "Chegou cedo, mas preparou a estratégia."],
        "answer": "Quando chegou cedo, preparou a estratégia.",
        "tip": "«Quando» apresenta o momento da preparação.",
    },
]

for template_index, template in enumerate(PROBLEM_TEMPLATES):
    for variant in range(40):
        character, verb, result = CHARACTER_CONTEXTS[variant % len(CHARACTER_CONTEXTS)]
        copy = template.copy()
        copy["scenario"] = template["scenario"].replace("Rafael", character).replace("Treinou", f"{character} {verb}").replace("A equipa", character)
        copy["options"] = [option.replace("Rafael", character).replace("Treinou", f"{character} {verb}") for option in template["options"]]
        copy["answer"] = template["answer"].replace("Rafael", character).replace("Treinou", f"{character} {verb}")
        copy["id"] = f"problem-{template_index}-{variant}"
        copy["difficulty"] = "medium" if template_index < 3 else "hard"
        PROBLEM_BANK.append(copy)


def get_connection_items(count: int = 10) -> list[dict]:
    return random.sample(CONNECTION_BANK, k=min(count, len(CONNECTION_BANK)))


def get_problem_items(count: int = 10) -> list[dict]:
    return random.sample(PROBLEM_BANK, k=min(count, len(PROBLEM_BANK)))
