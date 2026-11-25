WRITING_PROMPTS = [
    {
        "scene": "Prepara uma análise da cena de apresentação dos personagens.",
        "instruction": "Escreve uma oração copulativa que apresente uma ação feita por dois sujeitos ligados por «e».",
        "examples": ["Rafael entrou em campo e marcou um ponto.", "Itamar estudou e passou no teste."],
        "required_connectors": ["e"],
        "type": "Oração coordenada copulativa",
    },
    {
        "scene": "Observa um personagem que enfrenta uma oposição.",
        "instruction": "Escreve uma oração adversativa utilizando «mas».",
        "examples": ["Adriana treinou muito, mas perdeu o jogo.", "Zezinho Dino queria ganhar, mas faltava-lhe ritmo."],
        "required_connectors": ["mas"],
        "type": "Oração coordenada adversativa",
    },
    {
        "scene": "Relaciona uma ação com a sua causa.",
        "instruction": "Escreve uma frase com uma oração subordinada causal introduzida por «porque».",
        "examples": ["Rafael saiu cedo porque tinha treino.", "Mano explicou a jogada porque queria ajudar."],
        "required_connectors": ["porque"],
        "type": "Oração subordinada causal",
    },
    {
        "scene": "Uma personagem só realiza uma ação quando outra acontece.",
        "instruction": "Escreve uma oração subordinada condicional com «se».",
        "examples": ["Se o Rafael treinar, vai melhorar.", "Se Wemby saltar, pode bloquear o lançamento."],
        "required_connectors": ["se"],
        "type": "Oração subordinada condicional",
    },
    {
        "scene": "Apresenta duas possibilidades para o personagem.",
        "instruction": "Escreve uma oração coordenada disjuntiva usando «ou».",
        "examples": ["Rafael pode estudar ou descansar.", "Léo joga na defesa ou ataca a tabela."],
        "required_connectors": ["ou"],
        "type": "Oração coordenada disjuntiva",
    },
    {
        "scene": "Explica uma conclusão depois de apresentar um facto.",
        "instruction": "Escreve uma frase com uma oração coordenada conclusiva usando «logo» ou «portanto».",
        "examples": ["Estudei bastante, logo passei no teste.", "A equipa treinou muito, portanto estava preparada."],
        "required_connectors": ["logo", "portanto"],
        "type": "Oração coordenada conclusiva",
    },
]


def normalize_text(text: str) -> str:
    return " ".join(text.strip().lower().replace("  ", " ").split())


def validate_writing(answer: str, prompt: dict) -> dict:
    normalized = normalize_text(answer)
    connectors = [connector for connector in prompt["required_connectors"] if connector in normalized]

    if len(normalized) < 12:
        return {"correct": False, "level": "short", "message": "A resposta é demasiado curta. Completa a frase com sujeito, verbo e a relação pedida."}

    if not normalized:
        return {"correct": False, "level": "empty", "message": "Escreve uma oração antes de confirmar."}

    if not connectors:
        return {
            "correct": False,
            "level": "connector",
            "message": f"A frase precisa de incluir o conector pedido: {', '.join(prompt['required_connectors'])}.",
        }

    if len(normalized.split()) < 5:
        return {
            "correct": False,
            "level": "structure",
            "message": "Inclui pelo menos um sujeito e uma ação completa em cada oração.",
        }

    return {
        "correct": True,
        "level": "complete",
        "message": f"Boa construção! Identificaste corretamente a {prompt['type'].lower()}.",
    }


LITERARY_MISSIONS = [
    {
        "book": "Auto da Barca do Inferno",
        "author": "Gil Vicente",
        "location": "Cena inicial: a chegada das personagens à margem.",
        "character_hint": "Procura uma fala que usa «e» para juntar ações.",
        "instruction": "Encontra no livro uma frase curta com coordenação copulativa e copia-a exatamente.",
        "required_connectors": ["e"],
        "type": "Oração coordenada copulativa",
        "edition_note": "Usa ato, personagem e fala; páginas variam por edição.",
        "description": "Gil Vicente foi um dos grandes dramaturgos portugueses. Nesta obra satírica, personagens chegam ao rio e têm de decidir para que barca irão.",
    },
    {
        "book": "Auto da Barca do Inferno",
        "author": "Gil Vicente",
        "location": "Diálogo entre uma personagem condenada e o Anjo ou o Diabo.",
        "character_hint": "Procura uma resposta que apresenta uma causa ou justificação.",
        "instruction": "Encontra uma frase com «porque» ou «pois» e escreve-a integralmente.",
        "required_connectors": ["porque", "pois"],
        "type": "Oração subordinada causal ou coordenada explicativa",
        "edition_note": "Procura pela personagem e pela fala.",
    },
    {
        "book": "Auto da Barca do Inferno",
        "author": "Gil Vicente",
        "location": "Cena em que uma personagem apresenta alternativas.",
        "character_hint": "Procura o conector «ou» numa resposta curta.",
        "instruction": "Copia uma frase que ofereça uma escolha e sublinha o «ou».",
        "required_connectors": ["ou"],
        "type": "Oração coordenada disjuntiva",
        "edition_note": "Confirma a pontuação da tua edição.",
    },
    {
        "book": "O Cavaleiro da Dinamarca",
        "author": "Sophia de Mello Breyner Andresen",
        "location": "Trechos iniciais da viagem de Tiago.",
        "character_hint": "Procura uma frase em que um facto leva a uma conclusão.",
        "instruction": "Encontra uma frase com «logo» ou «portanto» e escreve-a.",
        "required_connectors": ["logo", "portanto"],
        "type": "Oração coordenada conclusiva",
        "edition_note": "Usa capítulos e sequência narrativa.",
    },
    {
        "book": "A Lua de Joana",
        "author": "Maria Teresa Maia Gonzalez",
        "location": "Passagens em que Joana descreve conflitos ou decisões.",
        "character_hint": "Procura uma frase com «mas», «porém» ou «contudo».",
        "instruction": "Copia uma frase adversativa e identifica a oposição.",
        "required_connectors": ["mas", "porém", "contudo"],
        "type": "Oração coordenada adversativa",
        "edition_note": "Usa capítulos e acontecimentos da narrativa.",
    },
    {
        "book": "A Pérola",
        "author": "John Steinbeck",
        "location": "Capítulo I: a descoberta da pérola altera a família de Kino.",
        "character_hint": "Procura uma frase em que uma ação é seguida de outra ação ligada por «e».",
        "instruction": "Encontra uma frase curta com coordenação copulativa e copia-a exatamente.",
        "required_connectors": ["e"],
        "type": "Oração coordenada copulativa",
        "edition_note": "O número de página varia conforme a tradução e edição; usa capítulos.",
        "description": "John Steinbeck foi um escritor norte-americano vencedor do Nobel. A Pérola acompanha Kino e a sua família depois de uma descoberta que muda o destino de todos.",
    },
    {
        "book": "A Pérola",
        "author": "John Steinbeck",
        "location": "Capítulo II: Kino, Juana e Coyotito vão procurar pérolas.",
        "character_hint": "Procura uma frase que apresente uma consequência ou conclusão.",
        "instruction": "Encontra uma frase com «logo», «portanto» ou «assim» e escreve-a.",
        "required_connectors": ["logo", "portanto", "assim"],
        "type": "Oração coordenada conclusiva",
        "edition_note": "Confirma o conector na tua tradução portuguesa.",
    },
    {
        "book": "A Pérola",
        "author": "John Steinbeck",
        "location": "Capítulos III–IV: reações da comunidade à descoberta.",
        "character_hint": "Procura uma passagem em que «mas» ou «porém» introduza uma oposição.",
        "instruction": "Copia uma frase adversativa e identifica o contraste entre as partes.",
        "required_connectors": ["mas", "porém", "contudo"],
        "type": "Oração coordenada adversativa",
        "edition_note": "As versões traduzidas podem usar conetivos diferentes.",
    },
    {
        "book": "A Pérola",
        "author": "John Steinbeck",
        "location": "Capítulo V: Kino tenta proteger a família após a ameaça.",
        "character_hint": "Procura uma frase em que uma ação ocorre por causa de outra.",
        "instruction": "Encontra uma frase com «porque» e escreve-a integralmente.",
        "required_connectors": ["porque"],
        "type": "Oração subordinada causal",
        "edition_note": "Procura pelo acontecimento principal; páginas variam por edição.",
    },
    {
        "book": "A Pérola",
        "author": "John Steinbeck",
        "location": "Capítulo VI: a viagem final e as decisões de Kino e Juana.",
        "character_hint": "Procura uma frase que exprima uma condição com «se» ou «caso».",
        "instruction": "Copia uma frase subordinada condicional e identifica a condição.",
        "required_connectors": ["se", "caso"],
        "type": "Oração subordinada condicional",
        "edition_note": "Verifica a tradução usada pela escola antes de confirmar o conector.",
    },
    {
        "book": "Os da Minha Rua",
        "author": "Ondjaki",
        "location": "Primeiros capítulos: apresentação da rua e das personagens.",
        "character_hint": "Procura uma descrição em que duas ações sejam ligadas por «e».",
        "instruction": "Encontra uma frase curta com coordenação copulativa e copia-a exatamente.",
        "required_connectors": ["e"],
        "type": "Oração coordenada copulativa",
        "edition_note": "Usa capítulos ou títulos das histórias; páginas podem variar.",
    },
    {
        "book": "Os da Minha Rua",
        "author": "Ondjaki",
        "location": "Uma história em que uma personagem explica uma decisão.",
        "character_hint": "Procura uma frase com «porque» ou «pois».",
        "instruction": "Copia uma frase causal ou explicativa e identifica o conector.",
        "required_connectors": ["porque", "pois"],
        "type": "Oração subordinada causal ou coordenada explicativa",
        "edition_note": "Confirma o conector na tua edição.",
    },
    {
        "book": "Os da Minha Rua",
        "author": "Ondjaki",
        "location": "Uma situação em que algo muda ou existe um contraste.",
        "character_hint": "Procura uma frase com «mas», «porém» ou «contudo».",
        "instruction": "Encontra uma frase adversativa e explica o contraste.",
        "required_connectors": ["mas", "porém", "contudo"],
        "type": "Oração coordenada adversativa",
        "edition_note": "Procura por acontecimento ou título da história.",
    },
]

BOOK_DESCRIPTIONS = {
    "Auto da Barca do Inferno": "Gil Vicente foi um dos grandes dramaturgos portugueses. Nesta obra satírica, personagens chegam ao rio e têm de decidir para que barca irão.",
    "A Pérola": "John Steinbeck foi um escritor norte-americano vencedor do Nobel. A Pérola acompanha Kino e a sua família depois de uma descoberta que muda o destino de todos.",
    "Os da Minha Rua": "Ondjaki é um escritor angolano. Os da Minha Rua reúne pequenas histórias sobre uma criança, os amigos e a vida numa rua cheia de personagens.",
    "O Cavaleiro da Dinamarca": "Sophia de Mello Breyner Andresen foi uma escritora portuguesa. Neste conto, Tiago vive uma aventura medieval marcada por coragem, amizade e descoberta.",
    "A Lua de Joana": "Maria Teresa Maia Gonzalez é uma autora portuguesa de literatura juvenil. O romance acompanha Joana numa investigação sobre violência familiar e social.",
}
