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
    {
        "scene": "Descreve uma ação habitual de um personagem.",
        "instruction": "Escreve uma oração que utilize o presente do indicativo para descrever uma ação rotineira.",
        "examples": ["Todos os dias, o Rafael estuda antes de dormir.", "Amanhã, a equipa treina novamente."],
        "required_connectors": [],
        "type": "Oração no presente do indicativo",
    },
    {
        "scene": "Retrata uma ação passada que tem relevância no presente.",
        "instruction": "Escreve uma oração no pretérito perfeito que indique uma ação concluída recentemente.",
        "examples": ["Hoje, o Itamar comeu muito no almoço.", "Ontem, a Adriana jogou tão bem que foi elogiada."],
        "required_connectors": [],
        "type": "Oração no pretérito perfeito",
    },
    {
        "scene": "Apresenta uma ação que estava em progresso no passado.",
        "instruction": "Escreve uma oração no pretérito imperfeito que descreva uma ação habitual ou em progresso.",
        "examples": ["Enquanto estudava, o Rafael ouviu música.", "A equipa treinava todos os dias naquela época."],
        "required_connectors": [],
        "type": "Oração no pretérito imperfeito",
    },
    {
        "scene": "Compara duas ações ou situações.",
        "instruction": "Escreve uma oração que utilize uma comparação com «como» ou «tal como».",
        "examples": ["O Rafael é tão alto como o pai.", "Ela canta como um anjo."],
        "required_connectors": ["como", "tal como"],
        "type": "Oração comparativa",
    },
    {
        "scene": "Contrasta duas ideias ou situações.",
        "instruction": "Escreve uma oração que utilize uma comparação adversativa com «embora» ou «mesmo que».",
        "examples": ["Embora estivesse cansado, o Rafael foi treinar.", "Mesmo que chova, a partida não será adiada."],
        "required_connectors": ["embora", "mesmo que"],
        "type": "Oração concessiva",
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

    if prompt["required_connectors"] and not connectors:
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
        "book": "A Pérola",
        "author": "John Steinbeck",
        "location": "Passagem inicial: apresentação da história da família de Kino.",
        "character_hint": "Na introdução, Kino é apresentado a Juana e ao garoto Coyotito numa mesma frase.",
        "instruction": "Encontra e copia exatamente a frase que apresenta Kino, Juana e Coyotito ligados por «e».",
        "required_connectors": ["e"],
        "type": "Oração coordenada copulativa",
        "edition_note": "A expressão aparece na apresentação da história, antes da descrição da vida da família.",
    },
    {
        "book": "A Pérola",
        "author": "John Steinbeck",
        "location": "Início da obra: Kino acorda e observa a casa, a mulher e a manhã.",
        "character_hint": "Procura uma frase em que uma ação de Kino é contrastada por «mas».",
        "instruction": "Copia uma frase curta em que «mas» introduza uma oposição ao que aconteceu antes.",
        "required_connectors": ["mas"],
        "type": "Oração coordenada adversativa",
        "edition_note": "Procura nas primeiras passagens sobre a rotina de Kino e Juana.",
    },
    {
        "book": "A Pérola",
        "author": "John Steinbeck",
        "location": "Quando Kino, Juana e Coyotito procuram ajuda para o escorpião.",
        "character_hint": "Procura a explicação que Kino dá sobre a necessidade de chamar o médico.",
        "instruction": "Encontra uma frase com «porque» que explique a atitude ou a situação da família.",
        "required_connectors": ["porque"],
        "type": "Oração subordinada causal",
        "edition_note": "Podes encontrá-la nos capítulos em que Kino recorre ao médico da vila.",
    },
    {
        "book": "A Pérola",
        "author": "John Steinbeck",
        "location": "Momentos em que Kino toma uma decisão sobre vender ou proteger a pérola.",
        "character_hint": "Procura uma fala em que Kino apresenta uma consequência ligada por «assim», «logo» ou «portanto».",
        "instruction": "Copia uma frase da acção ou do diálogo em que uma conclusão é introduzida pelo conector pedido.",
        "required_connectors": ["assim", "logo", "portanto"],
        "type": "Oração coordenada conclusiva",
        "edition_note": "Confirma o conector na tradução portuguesa do teu PDF.",
    },
    {
        "book": "A Pérola",
        "author": "John Steinbeck",
        "location": "Diálogo sobre as consequências da descoberta da pérola.",
        "character_hint": "Procura uma condição formulada com «se».",
        "instruction": "Copia uma frase que exprima o que pode acontecer caso Kino realize ou não uma ação.",
        "required_connectors": ["se", "caso"],
        "type": "Oração subordinada condicional",
        "edition_note": "Verifica a tradução usada pelo PDF antes de copiar a frase.",
    },
    {
        "book": "Os da Minha Rua",
        "author": "Ondjaki",
        "location": "Apresentação do Jika e das crianças da rua.",
        "character_hint": "O narrador apresenta o Jika e a sua posição entre os amigos da rua.",
        "instruction": "Encontra uma frase curta que apresente o Jika ou uma sequência de personagens usando «e».",
        "required_connectors": ["e"],
        "type": "Oração coordenada copulativa",
        "edition_note": "Procura no capítulo «o voo do jika», onde as crianças da rua são apresentadas.",
    },
    {
        "book": "Os da Minha Rua",
        "author": "Ondjaki",
        "location": "Histórias com Kazukuta, a avó Chica ou o tio Chico.",
        "character_hint": "Procura uma explicação dada pelo narrador com «porque» ou «pois».",
        "instruction": "Copia uma frase em que o narrador justifique uma característica, decisão ou lembrança.",
        "required_connectors": ["porque", "pois"],
        "type": "Oração subordinada causal ou coordenada explicativa",
        "edition_note": "O conector pode aparecer no diálogo ou na narração.",
    },
    {
        "book": "Os da Minha Rua",
        "author": "Ondjaki",
        "location": "Passagens em que o narrador contrasta o que esperava com o que aconteceu.",
        "character_hint": "Procura uma frase em que «mas» assinale uma oposição entre ideias ou acontecimentos.",
        "instruction": "Copia uma frase adversativa ligada à rua, aos amigos ou à família do narrador.",
        "required_connectors": ["mas", "porém", "contudo"],
        "type": "Oração coordenada adversativa",
        "edition_note": "Procura sobretudo nos capítulos de memória familiar e infância.",
    },
    {
        "book": "Os da Minha Rua",
        "author": "Ondjaki",
        "location": "Cena em que a criança decide brincar ou responder a um adulto.",
        "character_hint": "Procura uma situação apresentada com «ou», mostrando duas possibilidades.",
        "instruction": "Encontra e copia uma frase em que a criança ou os amigos tenham de escolher entre ações.",
        "required_connectors": ["ou"],
        "type": "Oração coordenada disjuntiva",
        "edition_note": "Pode aparecer num diálogo com o irmão, os amigos ou os familiares.",
    },
    {
        "book": "Auto da Barca do Inferno",
        "author": "Gil Vicente",
        "location": "Cena I: chegada do Fidalgo ao porto e ao batel infernal.",
        "character_hint": "No diálogo inicial, o Fidalgo pergunta e o Diabo indica a direção da barca.",
        "instruction": "Copia uma fala curta em que «e» coordene elementos da apresentação dos bateis ou personagens.",
        "required_connectors": ["e"],
        "type": "Oração coordenada copulativa",
        "edition_note": "Mantém a acentuação e a pontuação da edição PDF sempre que possível.",
    },
    {
        "book": "Auto da Barca do Inferno",
        "author": "Gil Vicente",
        "location": "Diálogo do Fidalgo com o Anjo ou o Diabo sobre a sua vida.",
        "character_hint": "Procura uma resposta em que «porque» ou «pois» justifique a condenação ou a entrada numa barca.",
        "instruction": "Copia exatamente uma fala justificativa de uma personagem que contenha «porque» ou «pois».",
        "required_connectors": ["porque", "pois"],
        "type": "Oração subordinada causal ou coordenada explicativa",
        "edition_note": "Confirma a fala e o nome da personagem antes de enviar a resposta.",
    },
    {
        "book": "Auto da Barca do Inferno",
        "author": "Gil Vicente",
        "location": "Cena em que uma personagem afirma a sua alternativa ou tenta entrar numa barca.",
        "character_hint": "Procura um «ou» que apresente uma escolha entre destinos ou ações.",
        "instruction": "Encontra uma fala com «ou» e copia-a integralmente.",
        "required_connectors": ["ou"],
        "type": "Oração coordenada disjuntiva",
        "edition_note": "Podes consultar a fala do Fidalgo, do Diabo ou de outra personagem condenada.",
    },
    {
        "book": "Auto da Barca do Inferno",
        "author": "Gil Vicente",
        "location": "Alegação feita por uma personagem sobre as consequências dos seus atos.",
        "character_hint": "Procura uma intervenção em que «mas» assinale o contraste entre aparência e destino.",
        "instruction": "Copia uma frase adversativa da obra e identifica que partes estão em oposição.",
        "required_connectors": ["mas", "porém", "contudo"],
        "type": "Oração coordenada adversativa",
        "edition_note": "O texto usa grafia antiga; copia-o exatamente como aparece no PDF.",
    },
]

BOOK_DESCRIPTIONS = {
    "Auto da Barca do Inferno": "Gil Vicente foi um dos grandes dramaturgos portugueses. Nesta obra satírica, personagens chegam ao rio e têm de decidir para que barca irão.",
    "A Pérola": "John Steinbeck foi um escritor norte-americano vencedor do Nobel. A Pérola acompanha Kino e a sua família depois de uma descoberta que muda o destino de todos.",
    "Os da Minha Rua": "Ondjaki é um escritor angolano. Os da Minha Rua reúne pequenas histórias sobre uma criança, os amigos e a vida numa rua cheia de personagens.",
    "O Cavaleiro da Dinamarca": "Sophia de Mello Breyner Andresen foi uma escritora portuguesa. Neste conto, Tiago vive uma aventura medieval marcada por coragem, amizade e descoberta.",
    "A Lua de Joana": "Maria Teresa Maia Gonzalez é uma autora portuguesa de literatura juvenil. O romance acompanha Joana numa investigação sobre violência familiar e social.",
}

import random
import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path


LITERARY_SOURCES_FILE = Path("data/literary_sources/sources.json")
LITERARY_PDF_DIR = Path("obras_literarias")


def load_literary_sources() -> dict:
    try:
        if LITERARY_SOURCES_FILE.exists():
            data = json.loads(LITERARY_SOURCES_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
    except (json.JSONDecodeError, OSError):
        pass
    return {"editions": {}, "quotes": {}}


def normalize_literary_quote(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).strip().lower()
    normalized = " ".join(normalized.split())
    normalized = normalized.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    normalized = normalized.replace("- ", "-")
    return normalized.rstrip(".,;:!? ")


@lru_cache(maxsize=20)
def extract_verified_quotes(book_name: str) -> tuple[str, ...]:
    sources = load_literary_sources()
    edition_names = sources.get("editions", {}).get(book_name, [])
    extracted: list[str] = []

    try:
        from pypdf import PdfReader
    except ImportError:
        return tuple(extracted)

    for edition_name in edition_names:
        pdf_path = LITERARY_PDF_DIR / str(edition_name)
        if not pdf_path.exists():
            continue

        try:
            reader = PdfReader(str(pdf_path))
            text = " ".join((page.extract_text() or "") for page in reader.pages)
            text = re.sub(r"\s+", " ", text)

            candidates = re.split(r"(?<=[.!?])\s+", text)
            for candidate in candidates:
                normalized = normalize_literary_quote(candidate)
                if len(normalized) >= 12 and normalized not in extracted:
                    extracted.append(normalized)
        except Exception:
            continue

    return tuple(extracted)


def validate_verified_quote(book_name: str, submitted: str, required_connectors: list[str]) -> dict:
    sources = load_literary_sources()
    editions = sources.get("editions", {})

    if not editions.get(book_name):
        return {
            "correct": False,
            "reason": "source_missing",
            "message": f"A {book_name} ainda não tem uma edição verificada carregada.",
        }

    normalized_answer = normalize_literary_quote(submitted)
    verified_quotes = set(sources.get("quotes", {}).get(book_name, []))
    verified_quotes.update(extract_verified_quotes(book_name))

    if normalized_answer not in {
        normalize_literary_quote(str(quote)) for quote in verified_quotes
    }:
        return {
            "correct": False,
            "reason": "not_verified",
            "message": "Essa frase não foi encontrada na edição PDF carregada da obra.",
        }

    if not any(connector in normalized_answer for connector in required_connectors):
        return {
            "correct": False,
            "reason": "connector_missing",
            "message": "A frase existe na edição carregada, mas não contém o conector pedido.",
        }

    return {
        "correct": True,
        "reason": "verified",
        "message": "Frase confirmada na edição PDF carregada da obra.",
    }


WRITING_POOL = []
seen_writing_keys = set()
variant = 0
while len(WRITING_POOL) < 500:
    source = WRITING_PROMPTS[variant % len(WRITING_PROMPTS)].copy()
    source["examples"] = list(source["examples"])
    source["required_connectors"] = list(source["required_connectors"])
    source["id"] = f"writing-{variant}"
    source["scene"] = str(source["scene"])
    key = (source["id"], source["instruction"])
    if key not in seen_writing_keys:
        seen_writing_keys.add(key)
        WRITING_POOL.append(source)
    variant += 1


def get_writing_tasks(count: int = 10) -> list[dict]:
    unique_pool = []
    seen_ids = set()
    seen_text = set()
    for item in WRITING_POOL:
        item_id = str(item.get("id", ""))
        item_text = (str(item.get("scene", "")), str(item.get("instruction", "")))
        if item_id not in seen_ids and item_text not in seen_text:
            seen_ids.add(item_id)
            seen_text.add(item_text)
            unique_pool.append(item)
    return random.sample(unique_pool, k=min(count, len(unique_pool)))

WRITING_PROMPTS.extend([
    {"id":"lit-write-e1","difficulty":"easy","scene":"Apresenta uma ação da família de Kino.","instruction":"Escreve uma frase curta com «e» sobre Kino, Juana ou Coyotito.","examples":["Kino acordou e observou a família.","Juana levantou-se e protegeu Coyotito."],"required_connectors":["e"],"type":"Oração coordenada copulativa"},
    {"id":"lit-write-e2","difficulty":"easy","scene":"Relaciona uma oposição da infância descrita por Ondjaki.","instruction":"Escreve uma frase com «mas» sobre uma ação ou lembrança do narrador.","examples":["Queria brincar, mas tinha que ajudar em casa.","O Jika sorria, mas o amigo estava preocupado."],"required_connectors":["mas"],"type":"Oração coordenada adversativa"},
    {"id":"lit-write-m1","difficulty":"medium","scene":"Uma decisão de Kino depende da descoberta da pérola.","instruction":"Escreve uma frase com «se» e apresenta uma consequência da decisão.","examples":["Se Kino vender a pérola, poderá ajudar a família.","Se Kino esconder a pérola, poderá protegê-la."],"required_connectors":["se"],"type":"Oração subordinada condicional"},
    {"id":"lit-write-m2","difficulty":"medium","scene":"Uma personagem do Auto da Barca justifica o seu destino.","instruction":"Escreve uma frase com «porque» ou «pois» em que uma personagem se defenda.","examples":["O Fidalgo pediu lugar porque tinha servido a Coroa.","O Diabo recusou a entrada, pois os bens não justificavam o privilégio."],"required_connectors":["porque","pois"],"type":"Oração causal ou explicativa"},
    {"id":"lit-write-m3","difficulty":"medium","scene":"Uma ação é feita para atingir um objetivo.","instruction":"Escreve uma frase com «para que» sobre Kino, Juana, o narrador ou o Fidalgo.","examples":["Juana falou baixo para que Coyotito continuasse a dormir.","O narrador guardou a lembrança para que ela não se apagasse."],"required_connectors":["para que"],"type":"Oração subordinada final"},
    {"id":"lit-write-h1","difficulty":"hard","scene":"Integra condição e conclusão.","instruction":"Constrói uma frase composta com «se» e «logo» ou «portanto» sobre uma consequência da pérola.","examples":["Se Kino vender a pérola, a família terá dinheiro, logo poderá enfrentar o futuro.","Se o Fidalgo reconhecer o erro, poderá mudar, portanto já não será condenado."],"required_connectors":["se","logo","portanto"],"type":"Oração condicional e coordenada conclusiva"},
    {"id":"lit-write-h2","difficulty":"hard","scene":"Contrasta privilégio e destino real.","instruction":"Escreve uma frase com «embora» e «mas» ou «porém» sobre uma personagem do Auto da Barca.","examples":["Embora o Fidalgo tivesse títulos, o seu destino foi o Inferno.","Embora o Onzeneiro possuísse dinheiro, não entrou na barca do Paraíso."],"required_connectors":["embora","mas","porém"],"type":"Concessão e coordenação adversativa"},
    {"id":"lit-write-h3","difficulty":"hard","scene":"Uma personagem comunica um pensamento ou temor.","instruction":"Escreve uma subordinada completiva introduzida por «que» num contexto das obras.","examples":["Kino temia que a riqueza trouxesse perigo à família.","O narrador disse que o Kazukuta era um cão triste."],"required_connectors":["que"],"type":"Oração subordinada substantiva completiva"},
])

for _writing_index, _writing_prompt in enumerate(WRITING_PROMPTS):
    if "difficulty" not in _writing_prompt:
        if _writing_index < 6:
            _writing_prompt["difficulty"] = "easy"
        elif _writing_index < 9:
            _writing_prompt["difficulty"] = "medium"
        else:
            _writing_prompt["difficulty"] = "hard"
