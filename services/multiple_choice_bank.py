import random

CHARACTERS = [
    "Rafael", "Itamar", "Zezinho Dino", "Adriana", "Salgueiro",
    "Léo", "Reis", "Adri", "Mano", "Mãe", "Pops", "Wemby",
    "Franklin", "Michael",
]

MC_TEMPLATES = [
    ("{name} entrou em campo e marcou um ponto.", "Como se classificam as orações?", ["Coordenadas copulativas", "Subordinadas causais", "Coordenadas adversativas"], "Coordenadas copulativas", "O «e» soma ações.", "easy"),
    ("{name} treinou muito, mas perdeu o jogo.", "Que relação existe?", ["Adversativa", "Copulativa", "Conclusiva"], "Adversativa", "O «mas» estabelece oposição.", "easy"),
    ("{name} pode estudar ou jogar videojogos.", "Que tipo de coordenação é?", ["Disjuntiva", "Explicativa", "Causal"], "Disjuntiva", "O «ou» apresenta alternativas.", "easy"),
    ("{name} estudou bastante, logo passou no teste.", "Como se classifica «logo passou»?", ["Coordenada conclusiva", "Subordinada final", "Coordenada adversativa"], "Coordenada conclusiva", "«Logo» introduz uma conclusão.", "easy"),
    ("Começa já, pois o treino vai começar.", "Que relação existe entre as orações?", ["Explicativa", "Conclusiva", "Condicional"], "Explicativa", "A segunda oração justifica a primeira.", "medium"),
    ("{name} saiu cedo, começou a chover.", "Como se chama a relação sem conjunção?", ["Assindética", "Sindética causal", "Subordinada relativa"], "Assindética", "As coordenadas estão separadas sem conetivo.", "medium"),
    ("Não só {name} estudou, mas também treinou.", "Que coordenação reforça a adição?", ["Copulativa", "Adversativa", "Disjuntiva"], "Copulativa", "«Não só…mas também» soma ações.", "medium"),
    ("{name} queria vencer; porém, faltava preparação.", "Que coordenação ocorre?", ["Adversativa", "Explicativa", "Conclusiva"], "Adversativa", "«Porém» introduz contraste.", "medium"),
    ("Ora {name} jogava, ora descansava.", "Que tipo de coordenação é?", ["Disjuntiva", "Copulativa", "Explicativa"], "Disjuntiva", "«Ora…ora» expressa alternância.", "medium"),
    ("{name} não foi ao treino porque estava lesionado.", "Como se classifica «porque estava lesionado»?", ["Subordinada causal", "Coordenada explicativa", "Subordinada temporal"], "Subordinada causal", "Indica o motivo da ausência.", "easy"),
    ("Se {name} treinar todos os dias, vai melhorar.", "Que subordinada aparece?", ["Condicional", "Causal", "Comparativa"], "Condicional", "A melhoria depende da condição.", "easy"),
    ("Quando o jogo terminou, {name} celebrou.", "Que circunstância indica «quando»?", ["Tempo", "Causa", "Fim"], "Tempo", "«Quando» situa a ação no tempo.", "easy"),
    ("A equipa pediu a {name} que entrasse em campo.", "Que subordinada substantiva ocorre?", ["Completiva", "Relativa", "Temporal"], "Completiva", "Complementa o sentido de «pediu».", "medium"),
    ("{name} estudou para melhorar o teste.", "Qual é o sentido da subordinada?", ["Finalidade", "Concessão", "Comparação"], "Finalidade", "Indica o objetivo de estudar.", "easy"),
    ("Embora {name} estivesse cansado, terminou o treino.", "Que subordinada existe?", ["Concessiva", "Causal", "Temporal"], "Concessiva", "Admite uma dificuldade sem impedir a ação.", "medium"),
    ("O jogador que marcou nasceu em Madrid.", "Que subordinada modifica «jogador»?", ["Adjetiva relativa", "Adverbial causal", "Completiva"], "Adjetiva relativa", "«Que marcou» caracteriza o jogador.", "medium"),
    ("Treinaram tanto que ficaram exaustos.", "Que relação expressa «que»?", ["Consequência", "Concessão", "Fim"], "Consequência", "«Tanto…que» apresenta o resultado.", "hard"),
    ("{name} jogou como Wemby.", "Que relação comparativa aparece?", ["Comparativa", "Causal", "Temporal"], "Comparativa", "Estabelece uma comparação.", "easy"),
    ("Apesar de estar nervoso, {name} marcou o ponto.", "Que subordinada existe?", ["Concessiva", "Condicional", "Explicativa"], "Concessiva", "Reconhece um obstáculo sem impedir o resultado.", "medium"),
    ("De modo que estudou, {name} passou no teste.", "Como se classifica «de modo que estudou»?", ["Consecutiva", "Coordenada explicativa", "Adjetiva relativa"], "Consecutiva", "Indica o resultado da ação anterior.", "hard"),
]


def build_multiple_choice_bank() -> list[dict]:
    bank = []
    for template_index, (sentence, question, options, answer, tip, difficulty) in enumerate(MC_TEMPLATES):
        for variant in range(10):
            character = CHARACTERS[variant % len(CHARACTERS)]
            item_options = list(options)
            item_answer = answer
            multiple = template_index in {1, 5, 10, 14, 16}

            if template_index == 1:
                item_options = ["Adversativa", "Expressa oposição", "Coordenada copulativa"]
                item_answer = ["Adversativa", "Expressa oposição"]
                question = "Seleciona todas as opções verdadeiras sobre «mas»"
            elif template_index == 5:
                item_options = ["Assindética", "Coordenada", "Subordinada"]
                item_answer = ["Assindética", "Coordenada"]
                question = "Seleciona todas as classificações corretas"
            elif template_index == 10:
                item_options = ["Condicional", "A ação depende da condição", "Causal"]
                item_answer = ["Condicional", "A ação depende da condição"]
                question = "Seleciona todas as opções verdadeiras"
            elif template_index == 14:
                item_options = ["Concessiva", "Um obstáculo não impede a ação", "Causal"]
                item_answer = ["Concessiva", "Um obstáculo não impede a ação"]
                question = "Seleciona todas as opções verdadeiras"
            elif template_index == 16:
                item_options = ["Consequência", "Estrutura «tanto…que»", "Concessão"]
                item_answer = ["Consequência", "Estrutura «tanto…que»"]
                question = "Seleciona todas as opções verdadeiras"

            bank.append({
                "id": f"mc-{template_index}-{variant}",
                "sentence": sentence.format(name=character),
                "question": question,
                "options": item_options,
                "answer": item_answer,
                "multiple": multiple,
                "tip": tip,
                "difficulty": difficulty,
                "topic": "Coordenação e subordinação",
            })
    return bank[:200]


MULTIPLE_CHOICE_BANK = build_multiple_choice_bank()


def get_multiple_choice_quiz(count: int = 10, difficulty: str | None = None) -> list[dict]:
    pool = MULTIPLE_CHOICE_BANK
    if difficulty:
        pool = [item for item in pool if item["difficulty"] == difficulty]
    selected = random.sample(pool, k=min(count, len(pool)))
    random.shuffle(selected)
    return selected
