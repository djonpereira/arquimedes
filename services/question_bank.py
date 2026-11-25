import random


CONTEXTS = [
    ("Rafael", "cesta", "jogo"),
    ("Itamar", "cesta", "campeonato"),
    ("Zezinho Dino", "triplo", "torneio"),
    ("Adriana", "ponto", "partida"),
    ("Salgueiro", "lance", "jogo"),
    ("Léo", "passe", "treino"),
    ("Reis", "resultado", "teste"),
    ("Adri", "trabalho", "aula"),
    ("Mano", "conselho", "fim de semana"),
    ("Mãe", "apoio", "prova"),
    ("Pops", "treino", "campeonato"),
    ("Wemby", "cesto", "jogo"),
    ("Franklin", "missão", "GTA"),
    ("Michael", "plano", "GTA"),
]

BASE_QUESTIONS = [
    {"sentence":"{0} marcou uma {1} e celebrou.","question":"Como se classifica a coordenação?","options":["Copulativa","Adversativa","Disjuntiva"],"answer":"Copulativa","tip":"A conjunção «e» soma duas ações.","difficulty":"easy","topic":"Coordenação"},
    {"sentence":"{0} treinou muito, mas perdeu o {2}.","question":"Que relação introduz «mas»?","options":["Adversativa","Conclusiva","Copulativa"],"answer":"Adversativa","tip":"«Mas» estabelece contraste ou oposição.","difficulty":"easy","topic":"Coordenação"},
    {"sentence":"{0} pode estudar ou ver o {2}.","question":"Que tipo de coordenação aparece?","options":["Disjuntiva","Explicativa","Causal"],"answer":"Disjuntiva","tip":"«Ou» apresenta alternativas.","difficulty":"easy","topic":"Coordenação"},
    {"sentence":"{0} estudou bastante, logo está preparado.","question":"Como se classifica «logo está preparado»?","options":["Coordenada conclusiva","Subordinada causal","Coordenada copulativa"],"answer":"Coordenada conclusiva","tip":"«Logo» indica conclusão.","difficulty":"easy","topic":"Coordenação"},
    {"sentence":"Começa já, pois o {2} vai começar.","question":"Que função tem a segunda oração?","options":["Explicativa","Adversativa","Temporal"],"answer":"Explicativa","tip":"A segunda oração explica a recomendação anterior.","difficulty":"medium","topic":"Coordenação"},
    {"sentence":"{0} saiu cedo, começou a chover.","question":"Como se chama esta relação sem conjunção?","options":["Assindética","Sindética adversativa","Subordinada final"],"answer":"Assindética","tip":"A oração coordenada está separada por vírgula, sem conjunção.","difficulty":"medium","topic":"Coordenação"},
    {"sentence":"Não só {0} treinou, mas também estudou.","question":"Que coordenação expressa soma reforçada?","options":["Copulativa","Disjuntiva","Causal"],"answer":"Copulativa","tip":"«Não só…mas também» reforça a adição.","difficulty":"medium","topic":"Coordenação"},
    {"sentence":"{0} queria vencer; porém, faltava preparação.","question":"Que tipo de coordenação ocorre?","options":["Adversativa","Copulativa","Conclusiva"],"answer":"Adversativa","tip":"«Porém» introduz contraste.","difficulty":"medium","topic":"Coordenação"},
    {"sentence":"Ora {0} jogava, ora descansava.","question":"A estrutura «ora…ora» indica:","options":["Alternância","Conclusão","Explicação"],"answer":"Alternância","tip":"«Ora…ora» apresenta ações alternativas.","difficulty":"medium","topic":"Coordenação"},
]

SUBORDINATION_TEMPLATES = [
    ("Não vim ao treino porque estava cansado.", "Qual é a subordinada?", ["porque estava cansado", "Não vim ao treino", "ao treino"], "porque estava cansado", "Causal", "A subordinada explica a causa.", "easy"),
    ("Se treinares todos os dias, melhorarás.", "Que tipo de subordinada existe?", ["Condicional", "Causal", "Temporal"], "Condicional", "Condicional", "A melhoria depende da condição.", "easy"),
    ("Quando o jogo terminou, todos celebraram.", "Que circunstância indica «Quando»?", ["Tempo", "Causa", "Fim"], "Tempo", "Temporal", "«Quando» situa a ação no tempo.", "easy"),
    ("Estudamos para que o Rafael fosse aprovado.", "Qual é o sentido da subordinada?", ["Finalidade", "Condição", "Comparação"], "Finalidade", "Final", "A subordinada indica o objetivo.", "medium"),
    ("Embora estivesse cansado, jogou.", "Que relação expressa «embora»?", ["Concessão", "Causa", "Conclusão"], "Concessão", "Concessiva", "«Embora» introduz oposição reconhecida.", "medium"),
    ("O jogador que marcou nasceu em Madrid.", "Qual é a subordinada adjetiva relativa?", ["que marcou", "nasceu em Madrid", "O jogador"], "que marcou", "Relativa", "«Que marcou» caracteriza o jogador.", "medium"),
    ("Quero que Rafael estudie.", "Que tipo de subordinada ocorre?", ["Completiva", "Adverbial temporal", "Adjetiva relativa"], "Completiva", "Completiva", "Completa o sentido do verbo «quero».", "medium"),
    ("Treinou tanto que ficou exausto.", "Que consequência está indicada?", ["ficou exausto", "Treinou tanto", "que"], "ficou exausto", "Consecutiva", "«Tanto…que» expressa consequência.", "hard"),
    ("Estudou como um campeão.", "Que relação comparativa existe?", ["Comparação", "Causa", "Concessão"], "Comparação", "Comparativa", "Compara o modo de estudar.", "medium"),
    ("Embora fizesse calor, o treino continuou.", "Como se classifica «Embora fizesse calor»?", ["Subordinada concessiva", "Coordenada adversativa", "Subordinada causal"], "Subordinada concessiva", "Concessiva", "A concessiva admite um facto apesar do qual ocorre o outro.", "hard"),
]


EXTENDED_TEMPLATES = [
    ("Ninguém marcou, nem entrou em campo.", "Que coordenação ocorre?", ["Copulativa", "Adversativa", "Causal"], "Copulativa", "Coordenação copulativa", "«Nem» soma duas negações.", "easy"),
    ("Estudaste pouco, todavia fizeste um bom teste.", "Que conetivo introduz contraste?", ["todavia", "logo", "porque"], "todavia", "Coordenação adversativa", "«Todavia» estabelece oposição.", "medium"),
    ("O treino acabou, por isso fomos para casa.", "Que relação expressa «por isso»?", ["Conclusão", "Alternância", "Causa"], "Conclusão", "Coordenação conclusiva", "«Por isso» indica consequência.", "easy"),
    ("Não entramos em campo, que estava a chover.", "Que relação introduz «que»?", ["Explicação", "Tempo", "Concessão"], "Explicação", "Coordenação explicativa", "Aqui «que» justifica a afirmação anterior.", "hard"),
    ("Podemos jogar, ou podemos estudar.", "Como se classificam as orações?", ["Coordenadas disjuntivas", "Subordinadas finais", "Coordenadas explicativas"], "Coordenadas disjuntivas", "Coordenação disjuntiva", "«Ou» oferece alternativas.", "easy"),
    ("Entrou no campo, contudo não marcou.", "Que coordenação está presente?", ["Adversativa", "Copulativa", "Final"], "Adversativa", "Coordenação adversativa", "«Contudo» expressa oposição.", "easy"),
    ("Estudou muito; portanto, passou no teste.", "Que tipo de coordenação ocorre?", ["Conclusiva", "Explicativa", "Temporal"], "Conclusiva", "Coordenação conclusiva", "«Portanto» introduz conclusão.", "medium"),
    ("Choveu, pois o chão está molhado.", "Como se classifica a segunda oração?", ["Explicativa", "Conclusiva", "Condicional"], "Explicativa", "Coordenação explicativa", "Justifica o facto inicial.", "medium"),
    ("Ou Rafael responde, ou perde a jogada.", "Qual é a relação?", ["Disjuntiva", "Adversativa", "Causal"], "Disjuntiva", "Coordenação disjuntiva", "A estrutura «ou…ou» apresenta alternativas.", "easy"),
    ("Rafael não jogou, mas ajudou a equipa.", "Que ideia liga as orações?", ["Oposição", "Soma", "Tempo"], "Oposição", "Coordenação adversativa", "«Mas» contrasta duas ações.", "easy"),
    ("O treinador não explicou, nem voltou a falar.", "Que tipo de coordenação é?", ["Copulativa", "Conclusiva", "Causal"], "Copulativa", "Coordenação copulativa", "«Nem» soma duas negações.", "easy"),
    ("Estava cansado, porque não tinha dormido.", "Que subordinada aparece?", ["Causal", "Final", "Comparativa"], "Causal", "Subordinação causal", "Explica o motivo de estar cansado.", "medium"),
    ("De modo que estudou, conseguiu melhorar.", "Como se classifica «de modo que estudou»?", ["Consecutiva", "Concessiva", "Condicional"], "Consecutiva", "Subordinação consecutiva", "A subordinada indica o resultado.", "hard"),
    ("Assim que começou o jogo, Rafael marcou.", "Que subordinada existe?", ["Temporal", "Causal", "Comparativa"], "Temporal", "Subordinação temporal", "Situa a ação no tempo.", "medium"),
    ("Caso chegues cedo, conseguimos treinar.", "Que condição apresenta «caso»?", ["Condicional", "Causal", "Final"], "Condicional", "Subordinação condicional", "O treino depende da chegada.", "medium"),
    ("A equipa lutou para vencer o campeonato.", "Que sentido tem «para vencer»?", ["Finalidade", "Tempo", "Concessão"], "Finalidade", "Subordinação final", "Indica o objetivo da ação.", "easy"),
    ("Apesar de ter treinado, perdeu.", "Como se classifica a subordinada?", ["Concessiva", "Causal", "Comparativa"], "Concessiva", "Subordinação concessiva", "Admite um facto apesar do qual ocorre outro.", "medium"),
    ("Quanto mais estudava, melhor jogava.", "Que relação se estabelece?", ["Proporcional", "Explicativa", "Conclusiva"], "Proporcional", "Subordinação proporcional", "Liga duas mudanças proporcionais.", "hard"),
    ("Tudo correu como tínhamos planeado.", "Que subordinada aparece?", ["Comparativa", "Causal", "Final"], "Comparativa", "Subordinação comparativa", "Estabelece comparação.", "medium"),
    ("A ideia é que Rafael continue a treinar.", "Que tipo de subordinada substantiva existe?", ["Completiva", "Relativa", "Temporal"], "Completiva", "Subordinação completiva", "Completa o sentido do substantivo «ideia».", "hard"),
    ("Rafael, que é persistente, nunca desistiu.", "Qual é a subordinada relativa?", ["que é persistente", "nunca desistiu", "Rafael"], "que é persistente", "Subordinação adjetiva relativa", "Acrescenta uma característica explicativa a Rafael.", "hard"),
]


def expand_base_questions() -> list[dict]:
    questions = []

    for index, template in enumerate(BASE_QUESTIONS):
        for context_index, context in enumerate(CONTEXTS):
            copy = template.copy()
            copy["sentence"] = template["sentence"].format(*context)
            copy["id"] = f"coord-{index}-{context_index}"
            copy["options"] = list(template["options"])
            questions.append(copy)

    for index, (sentence, question, options, answer, topic, tip, difficulty) in enumerate(SUBORDINATION_TEMPLATES):
        for context_index in range(5):
            character = CONTEXTS[(index + context_index) % len(CONTEXTS)][0]
            copy = {
                "sentence": sentence.replace("Rafael", character),
                "question": question,
                "options": list(options),
                "answer": answer,
                "tip": tip,
                "difficulty": difficulty,
                "topic": topic,
                "id": f"sub-{index}-{context_index}",
            }
            if isinstance(copy["answer"], str):
                copy["answer"] = copy["answer"].replace("Rafael", character)
            questions.append(copy)

    for index, (sentence, question, options, answer, topic, tip, difficulty) in enumerate(EXTENDED_TEMPLATES):
        for context_index in range(5):
            questions.append({
                "sentence": sentence,
                "question": question,
                "options": list(options),
                "answer": answer,
                "tip": tip,
                "difficulty": difficulty,
                "topic": topic,
                "id": f"ext-{index}-{context_index}",
            })

    return questions[:200]


QUESTION_BANK = expand_base_questions()


def get_random_quiz(count: int = 10, difficulty: str | None = None) -> list[dict]:
    pool = QUESTION_BANK
    if difficulty:
        pool = [question for question in pool if question["difficulty"] == difficulty]
    selected = random.sample(pool, k=min(count, len(pool)))
    random.shuffle(selected)
    return selected