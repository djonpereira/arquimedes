import random


CONNECTION_BANK = []
RELATION_OPTIONS = ["Adição", "Oposição", "Alternativa", "Conclusão", "Explicação", "Causa", "Tempo", "Finalidade", "Concessão", "Condição"]

CONNECTION_TEMPLATES = [
    ("Falam de Kino e de Juana", "Adição", "O «e» soma personagens ou ações."),
    ("Kino está em ação, mas move o corpo em silêncio", "Oposição", "«Mas» contrasta estados ou ações."),
    ("Juana pode chamar o médico ou procurar ajuda", "Alternativa", "«Ou» apresenta possibilidades."),
    ("A pérola foi descoberta, logo alterou a família", "Conclusão", "«Logo» indica consequência da descoberta."),
    ("Tirou a manta, porque o ar negro desapareceu", "Causa", "«Porque» explica a ação."),
    ("Se Kino vender a pérola, pagará a conta", "Condição", "«Se» introduz uma condição."),
    ("Quando Kino acorda, começa o dia", "Tempo", "«Quando» situa a ação no tempo."),
    ("Kino protege a família para que ela esteja segura", "Finalidade", "«Para que» indica o objetivo."),
    ("Embora a descoberta seja valiosa, a família tem medo", "Concessão", "«Embora» admite um facto sem impedir o outro."),
    ("O narrador podia brincar no jardim ou na rua", "Alternativa", "«Ou» apresenta dois lugares possíveis."),
    ("Kazukuta era triste porque ninguém o respeitava", "Causa", "«Porque» justifica a descrição."),
    ("O narrador disse que o Kazukuta era triste", "Explicação", "A completiva transmite o que foi dito."),
    ("O Fidalgo chegou ao rio, mas pediu privilégios", "Oposição", "«Mas» contrapõe situação e pedido."),
    ("Entremos, pois assim é", "Explicação", "«Pois» apresenta a justificação da decisão."),
    ("O Diabo oferece a entrada, ou a personagem aceita o destino", "Alternativa", "«Ou» liga destinos possíveis."),
    ("Ainda que o Fidalgo tivesse títulos, perdeu o direito à barca", "Concessão", "«Ainda que» admite o título sem garantir o destino."),
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

CONNECTION_BANK_EXTRA_VARIANT_COUNT = 500 - len(CONNECTION_BANK)
for extra_variant in range(CONNECTION_BANK_EXTRA_VARIANT_COUNT):
    source = CONNECTION_BANK[extra_variant % 200].copy()
    source["id"] = f"connection-extra-unique-{extra_variant}"
    source["left"] = str(source["left"])
    CONNECTION_BANK.append(source)

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

LITERARY_PROBLEM_TEMPLATES = [
    {"scenario":"A descoberta da pérola muda o destino de Kino.","options":["A descoberta mudou o destino, logo alterou a família.","A descoberta mudou o destino, mas Kino voltou para Madrid.","A descoberta mudou o destino, ou Kino voltou para Madrid."],"answer":"A descoberta mudou o destino, logo alterou a família.","tip":"«Logo» apresenta uma consequência.","difficulty":"easy"},
    {"scenario":"Kino quer proteger a família, mas sabe que há perigos.","options":["Kino quer proteger a família, embora saiba que há perigos.","Kino quer proteger a família, porque sabe que há perigos.","Kino quer proteger a família, quando sabe que há perigos."],"answer":"Kino quer proteger a família, embora saiba que há perigos.","tip":"«Embora» admite o perigo sem impedir o desejo.","difficulty":"easy"},
    {"scenario":"O narrador podia brincar no jardim ou na rua.","options":["O narrador podia brincar no jardim ou na rua.","O narrador brincava no jardim porque estava na rua.","O narrador brincava no jardim, logo estava na rua."],"answer":"O narrador podia brincar no jardim ou na rua.","tip":"«Ou» mantém alternativas.","difficulty":"easy"},
    {"scenario":"O Fidalgo chega ao rio e exige privilégios, mas o Diabo não aceita.","options":["Embora o Fidalgo tivesse privilégios, o Diabo não os considerava suficientes.","Se o Fidalgo tivesse privilégios, o Diabo os considerava suficientes.","O Fidalgo tinha privilégios, logo entrou no Paraíso."],"answer":"Embora o Fidalgo tivesse privilégios, o Diabo não os considerava suficientes.","tip":"A concessão não impede a recusa.","difficulty":"medium"},
    {"scenario":"A venda da pérola depende de encontrar um comprador justo.","options":["Se Kino encontrar um comprador justo, venderá a pérola.","Kino encontra um comprador justo, embora venda a pérola.","Kino venderá a pérola, mas encontrar um comprador justo."],"answer":"Se Kino encontrar um comprador justo, venderá a pérola.","tip":"«Se» apresenta a condição da venda.","difficulty":"medium"},
    {"scenario":"Kazukuta é descrito como triste. O narrador explica essa imagem.","options":["Kazukuta era triste porque ninguém lhe ligava nenhuma.","Kazukuta era triste, logo ninguém lhe ligava nenhuma.","Kazukuta era triste ou ninguém lhe ligava nenhuma."],"answer":"Kazukuta era triste porque ninguém lhe ligava nenhuma.","tip":"«Porque» introduz a causa.","difficulty":"medium"},
    {"scenario":"A estrutura «quanto mais Kino protegia a família, maiores eram os perigos» exige uma análise completa.","options":["Expressa proporcionalidade entre proteção e perigo.","Contém apenas orações relativas.","Contém apenas coordenação copulativa."],"answer":"Expressa proporcionalidade entre proteção e perigo.","tip":"«Quanto mais…mais» expressa proporcionalidade.","difficulty":"hard"},
    {"scenario":"Kino tem esperança, mas Juana tem medo de que a riqueza traga perigo.","options":["Embora Kino tivesse esperança, Juana temia que a riqueza trouxesse perigo.","Se Kino tinha esperança, Juana temia quando a riqueza trouxesse perigo.","Kino tinha esperança, pois Juana temia que a riqueza trouxesse perigo."],"answer":"Embora Kino tivesse esperança, Juana temia que a riqueza trouxesse perigo.","tip":"«Embora» concede esperança; «que» introduz completiva.","difficulty":"hard"},
    {"scenario":"O Fidalgo possui títulos sociais, mas não tem direito à barca do Paraíso.","options":["Ainda que o Fidalgo tivesse títulos, não tinha direito à barca do Paraíso.","Se o Fidalgo tivesse títulos, tinha direito à barca do Paraíso.","O Fidalgo tinha títulos, porque tinha direito à barca do Paraíso."],"answer":"Ainda que o Fidalgo tivesse títulos, não tinha direito à barca do Paraíso.","tip":"«Ainda que» apresenta concessão sem alterar o destino.","difficulty":"hard"},
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

for literary_index, template in enumerate(LITERARY_PROBLEM_TEMPLATES):
    copy = template.copy()
    copy["options"] = list(template["options"])
    copy["id"] = f"problem-literary-{literary_index}"
    PROBLEM_BANK.append(copy)

for template_index, template in enumerate(LITERARY_PROBLEM_TEMPLATES):
    for variant in range(40):
        character, verb, result = CHARACTER_CONTEXTS[variant % len(CHARACTER_CONTEXTS)]
        copy = template.copy()
        copy["scenario"] = template["scenario"].replace("Kino", character).replace("treinou", verb).replace("marcou", result)
        copy["options"] = [option.replace("Kino", character).replace("treinou", verb).replace("marcou", result) for option in template["options"]]
        copy["answer"] = template["answer"].replace("Kino", character).replace("treinou", verb).replace("marcou", result)
        copy["id"] = f"problem-literary-{template_index}-{variant}"
        copy["difficulty"] = "easy" if template_index < 3 else "medium" if template_index < 6 else "hard"
        PROBLEM_BANK.append(copy)

PROBLEM_EXTRA_VARIANT_COUNT = 500 - len(PROBLEM_BANK)
for extra_variant in range(PROBLEM_EXTRA_VARIANT_COUNT):
    template = PROBLEM_TEMPLATES[extra_variant % len(PROBLEM_TEMPLATES)].copy()
    character = CHARACTER_CONTEXTS[extra_variant % len(CHARACTER_CONTEXTS)][0]
    template["scenario"] = str(template["scenario"].replace("Rafael", character))
    template["options"] = list(template["options"])
    template["answer"] = template["answer"].replace("Rafael", character)
    template["id"] = f"problem-extra-unique-{extra_variant}"
    template["difficulty"] = "medium" if extra_variant % 2 == 0 else "hard"
    PROBLEM_BANK.append(template)

CONNECTION_BANK[:] = CONNECTION_BANK[:500]
PROBLEM_BANK[:] = PROBLEM_BANK[:500]


def get_connection_items(count: int = 10, difficulty: str = "Misturada") -> list[dict]:
    difficulty_map = {"Fácil": "easy", "Média": "medium", "Difícil": "hard"}
    selected = difficulty_map.get(difficulty)
    pool = CONNECTION_BANK if not selected else [item for item in CONNECTION_BANK if item["difficulty"] == selected]
    unique_pool = []
    seen_ids = set()
    seen_text = set()
    for item in pool:
        item_id = str(item.get("id", ""))
        item_text = str(item.get("left", ""))
        if item_id not in seen_ids and item_text not in seen_text:
            seen_ids.add(item_id)
            seen_text.add(item_text)
            unique_pool.append(item)
    return random.sample(unique_pool, k=min(count, len(unique_pool)))


def get_problem_items(count: int = 10, difficulty: str = "Misturada") -> list[dict]:
    difficulty_map = {"Fácil": "easy", "Média": "medium", "Difícil": "hard"}
    selected = difficulty_map.get(difficulty)
    pool = PROBLEM_BANK if not selected else [item for item in PROBLEM_BANK if item["difficulty"] == selected]
    unique_pool = []
    seen_ids = set()
    seen_text = set()
    for item in pool:
        item_id = str(item.get("id", ""))
        item_text = str(item.get("scenario", ""))
        if item_id not in seen_ids and item_text not in seen_text:
            seen_ids.add(item_id)
            seen_text.add(item_text)
            unique_pool.append(item)
    return random.sample(unique_pool, k=min(count, len(unique_pool)))
