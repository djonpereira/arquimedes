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


# Banco literário ampliado: combina identificação, análise, transformação e interpretação.
LITERARY_QUIZ_QUESTIONS = [
    {"id":"lit-e-01","sentence":"Falam de Kino, o pescador, de Juana, mulher dele, e do garoto Coyotito.","question":"Que relação sintática estabelece o «e»?","options":["Adição entre elementos","Oposição entre elementos","Alternativa entre elementos"],"answer":"Adição entre elementos","tip":"O conector «e» liga elementos da apresentação da família.","difficulty":"easy","topic":"Coordenação copulativa"},
    {"id":"lit-e-02","sentence":"As estrelas ainda brilhavam e o dia tinha apenas desenhado uma leve mancha de claridade.","question":"Como se classificam as ações ligadas por «e»?","options":["Duas ações coordenadas","Duas ações subordinadas","Uma causa e uma consequência"],"answer":"Duas ações coordenadas","tip":"Cada oração conserva sentido próprio e a ligação é copulativa.","difficulty":"easy","topic":"Coordenação copulativa"},
    {"id":"lit-e-03","sentence":"O Itamar treinou muito, mas perdeu o jogo.","question":"Que conector introduz o contraste?","options":["mas","porque","logo"],"answer":"mas","tip":"«Mas» introduz oposição entre treino e resultado.","difficulty":"easy","topic":"Coordenação adversativa"},
    {"id":"lit-e-04","sentence":"Nesse tempo, se houvesse gasosa na minha casa era para dividir.","question":"Que ideia depende da condição apresentada?","options":["A distribuição da gasosa","A abertura da rua","A chegada do inverno"],"answer":"A distribuição da gasosa","tip":"«Se houvesse» introduz a condição para dividir.","difficulty":"easy","topic":"Subordinação condicional"},
    {"id":"lit-e-05","sentence":"O Ndalu podia brincar no jardim ou na rua.","question":"Que relação é criada por «ou»?","options":["Alternativa","Causa","Conclusão"],"answer":"Alternativa","tip":"«Ou» apresenta possibilidades diferentes.","difficulty":"easy","topic":"Coordenação disjuntiva"},
    {"id":"lit-e-06","sentence":"Kino acordou quase com escuro, mas já podia ouvir a cantiga da família.","question":"Que ideia contrasta «quase com escuro» e «podia ouvir»?","options":["Tempo e continuidade da rotina","Dois lugares geográficos","Duas conclusões"],"answer":"Tempo e continuidade da rotina","tip":"«Mas» contrapõe o contexto de escuridão à presença da cantiga.","difficulty":"easy","topic":"Coordenação adversativa"},
    {"id":"lit-e-07","sentence":"A barca onde vai ora, que assim está apercebida?","question":"Que função desempenha «ora» nesta fala do Fidalgo?","options":["Pergunta sobre o destino da barca","Indica uma conclusão","Expressa uma causa"],"answer":"Pergunta sobre o destino da barca","tip":"No contexto, o Fidalgo interroga o Diabo sobre a barca.","difficulty":"easy","topic":"Compreensão textual"},
    {"id":"lit-e-08","sentence":"Vai para a ilha perdida e há-de partir logo essa hora.","question":"Que conetivo liga ações?","options":["e","embora","porque"],"answer":"e","tip":"«E» soma o destino indicado à partida prevista.","difficulty":"easy","topic":"Coordenação copulativa"},
    {"id":"lit-e-09","sentence":"Se a avó Chica viesse, ia trazer também a Helda.","question":"Qual é a subordinada condicional?","options":["Se a avó Chica viesse","ia trazer também a Helda","a avó Chica"],"answer":"Se a avó Chica viesse","tip":"Ela indica a condição da ação principal.","difficulty":"easy","topic":"Subordinação condicional"},
    {"id":"lit-e-10","sentence":"O Kazukuta era triste porque o narrador assim o recordava.","question":"Que relação apresenta «porque»?","options":["Causa","Alternância","Comparação"],"answer":"Causa","tip":"«Porque» justifica a forma como a personagem é descrita.","difficulty":"easy","topic":"Subordinação causal"},

    {"id":"lit-m-01","sentence":"Tirou a manta de cima do nariz, porque o ar negro já havia desaparecido.","question":"Se substituirmos «porque» por «pois», que sentido permanece dominante?","options":["Causal ou explicativo","Adversativo","Condicional"],"answer":"Causal ou explicativo","tip":"Ambos podem justificar uma ação ou apresentação de facto.","difficulty":"medium","topic":"Relações semânticas"},
    {"id":"lit-m-02","sentence":"Kino estava em ação, mas moveu o corpo em silêncio.","question":"Que alteração manteria a oposição sem repetir «mas»?","options":["Kino estava em ação; porém, moveu-se em silêncio.","Kino estava em ação; logo, moveu-se em silêncio.","Kino estava em ação e moveu-se em silêncio."],"answer":"Kino estava em ação; porém, moveu-se em silêncio.","tip":"«Porém» mantém o contraste indicado por «mas».","difficulty":"medium","topic":"Reformulação adversativa"},
    {"id":"lit-m-03","sentence":"Se Kino vender a pérola, pagará a conta ao médico.","question":"Qual é a consequência e qual é a condição?","options":["Condição: vender; consequência: pagar","Condição: pagar; consequência: vender","Ambas são causas"],"answer":"Condição: vender; consequência: pagar","tip":"A subordinada introduzida por «se» estabelece a condição.","difficulty":"medium","topic":"Análise condicional"},
    {"id":"lit-m-04","sentence":"Os homens pensavam que todos os lugares eram iguais, mas o mar tinha claridades próprias.","question":"Que dois planos o «mas» contrapõe?","options":["Uma crença geral e uma particularidade do mar","A ida e o regresso","Uma causa e uma conclusão"],"answer":"Uma crença geral e uma particularidade do mar","tip":"A primeira oração apresenta uma perceção; a segunda introduz contraste.","difficulty":"medium","topic":"Coordenação adversativa"},
    {"id":"lit-m-05","sentence":"O narrador podia brincar no jardim ou na rua.","question":"Como se transforma a frase numa estrutura de alternância clara?","options":["Ora brincava no jardim, ora brincava na rua.","Brincava no jardim, porque não ia à rua.","Brincava no jardim, logo ia à rua."],"answer":"Ora brincava no jardim, ora brincava na rua.","tip":"«Ora…ora» explicita alternância entre possibilidades.","difficulty":"medium","topic":"Coordenação disjuntiva"},
    {"id":"lit-m-06","sentence":"Kino podia falar com o médico ou regressar à sua casa.","question":"Que relação sintática representa esta escolha?","options":["Coordenação disjuntiva","Subordinação concessiva","Coordenação conclusiva"],"answer":"Coordenação disjuntiva","tip":"«Ou» liga alternativas independentes.","difficulty":"medium","topic":"Coordenação disjuntiva"},
    {"id":"lit-m-07","sentence":"O tio Chico era divertido, pois fazia rir a família.","question":"Qual é a oração explicativa?","options":["pois fazia rir a família","O tio Chico era divertido","toda a família"],"answer":"pois fazia rir a família","tip":"A segunda oração explica o motivo da caracterização anterior.","difficulty":"medium","topic":"Coordenação explicativa"},
    {"id":"lit-m-08","sentence":"A tia Luna preparou o bolo horroroso e o narrador gritou logo ao descobrir o lugar.","question":"Que funções têm «e» e «logo»?","options":["«e» soma ações; «logo» indica conclusão ou imediatidade","Ambos indicam causa","Ambos indicam condição"],"answer":"«e» soma ações; «logo» indica conclusão ou imediatidade","tip":"Analisa cada conector no seu contexto.","difficulty":"medium","topic":"Análise de conetivos"},
    {"id":"lit-m-09","sentence":"Entremos, pois que assim é.","question":"Que relação estabelece «pois» nesta fala do Diabo?","options":["Explicação da decisão anterior","Alternativa ao Inferno","Concessão ao Fidalgo"],"answer":"Explicação da decisão anterior","tip":"«Pois» apresenta uma justificação para entrar.","difficulty":"medium","topic":"Coordenação explicativa"},
    {"id":"lit-m-10","sentence":"Embora o Fidalgo tivesse privilégios, não entrou na barca do Paraíso.","question":"Que estrutura cria o sentido de concessão?","options":["Embora… tivesse privilégios","não entrou na barca","barca do Paraíso"],"answer":"Embora… tivesse privilégios","tip":"A subordinada concede um facto que não impede o resultado.","difficulty":"medium","topic":"Subordinação concessiva"},
    {"id":"lit-m-11","sentence":"Quando o jogo começou, as personagens chegaram ao rio.","question":"Que alteração transforma o tempo em causa?","options":["Como as personagens chegaram ao rio, o jogo começou.","Quando as personagens chegaram, o jogo começou.","Se as personagens chegassem, o jogo começava."],"answer":"Como as personagens chegaram ao rio, o jogo começou.","tip":"«Como» pode introduzir uma relação causal neste contexto.","difficulty":"medium","topic":"Transformação sintática"},
    {"id":"lit-m-12","sentence":"A barca está pronta; logo, começa a partida da personagem.","question":"Que argumento torna «logo» adequado?","options":["A prontidão da barca é causa da partida","A barca é uma alternativa à partida","A barca é apresentada apesar da partida"],"answer":"A prontidão da barca é causa da partida","tip":"«Logo» pode introduzir a conclusão da prontidão.","difficulty":"medium","topic":"Coordenação conclusiva"},

    {"id":"lit-h-01","sentence":"O Fidalgo argumentava que tinha serviço para a Coroa; o Diabo, porém, recusava-o porque os bens não o justificavam.","question":"Identifica todas as relações presentes.","options":["Coordenação adversativa e subordinada causal","Só coordenação copulativa","Coordenação disjuntiva e condicional"],"answer":"Coordenação adversativa e subordinada causal","tip":"«Porém» contrapõe; «porque» explica a recusa.","difficulty":"hard","topic":"Análise integrada"},
    {"id":"lit-h-02","sentence":"Embora Kino tivesse descoberto uma pérola valiosa, Juana temia que a riqueza trouxesse perigo.","question":"A oração «que a riqueza trouxesse perigo» é do tipo:","options":["Completiva substantiva","Adjetiva relativa","Adverbial temporal"],"answer":"Completiva substantiva","tip":"Completa o sentido do verbo «temia».","difficulty":"hard","topic":"Subordinação completiva"},
    {"id":"lit-h-03","sentence":"Se Kino vender a pérola, a família poderá melhorar de vida; contudo, não sabe quem a comprará.","question":"Qual é a estrutura global da frase?","options":["Uma subordinada condicional seguida de coordenação adversativa","Uma subordinada causal e uma final","Duas subordinadas relativas"],"answer":"Uma subordinada condicional seguida de coordenação adversativa","tip":"«Se» introduz condição; «contudo» introduz contraste.","difficulty":"hard","topic":"Análise composta"},
    {"id":"lit-h-04","sentence":"Quanto mais Kino tentava proteger a família, maiores eram os perigos que surgiam.","question":"Que relações estão presentes?","options":["Proporcional e adjetiva relativa","Causal e comparativa","Condicional e explicativa"],"answer":"Proporcional e adjetiva relativa","tip":"«Quanto mais…maiores» exprime proporcionalidade; «que surgiam» caracteriza perigos.","difficulty":"hard","topic":"Subordinação complexa"},
    {"id":"lit-h-05","sentence":"As crianças iam brincar, que tinham acabado os deveres.","question":"Porque é «que» coordenativo explicativo e não subordinativo causal?","options":["Porque explica a decisão anterior sem depender de um verbo principal","Porque introduz uma condição","Porque modifica um substantivo"],"answer":"Porque explica a decisão anterior sem depender de um verbo principal","tip":"A oração subordinada pode ser causal; o contexto e a relação entre frases determinam a análise.","difficulty":"hard","topic":"Distinção entre orações"},
    {"id":"lit-h-06","sentence":"Nem a descoberta da pérola trouxe paz, nem Kino conseguiu proteger Juana.","question":"Que relação reforçada está presente?","options":["Copulativa negativa","Disjuntiva conclusiva","Adversativa explicativa"],"answer":"Copulativa negativa","tip":"«Nem…nem» soma duas negações.","difficulty":"hard","topic":"Coordenação copulativa"},
    {"id":"lit-h-07","sentence":"O narrador disse que o Kazukuta era um cão triste porque ninguém o respeitava.","question":"Quantas subordinadas existem e quais são?","options":["Completiva («que…triste») e causal («porque…»)","Relativa e concessiva","Temporal e comparativa"],"answer":"Completiva («que…triste») e causal («porque…»)","tip":"«Que» completa «disse»; «porque» explica a tristeza.","difficulty":"hard","topic":"Análise composta"},
    {"id":"lit-h-08","sentence":"Ainda que o Fidalgo possuísse títulos, o Diabo considerava que não tinha direito à barca do Paraíso.","question":"Que tipos de subordinadas existem?","options":["Concessiva e completiva","Causal e relativa","Temporal e consecutiva"],"answer":"Concessiva e completiva","tip":"«Ainda que» admite um facto; «que não tinha direito» completa «considerava».","difficulty":"hard","topic":"Análise composta"},
    {"id":"lit-h-09","sentence":"Kino moveu-se em silêncio para que Juana não acordasse o Coyotito.","question":"Qual é a subordinada e que sentido expressa?","options":["Final: indica o objetivo","Causal: indica a origem","Comparativa: estabelece paralelo"],"answer":"Final: indica o objetivo","tip":"«Para que» introduz finalidade.","difficulty":"hard","topic":"Subordinação final"},
    {"id":"lit-h-10","sentence":"A barca era pequena, mas muitos passageiros nela embarcavam.","question":"Como classificas a relação entre «barca pequena» e «muitos passageiros»?","options":["Adversativa, pois contrasta dimensão e ocupação","Conclusiva, pois indica uma consequência","Explicativa, pois justifica a dimensão"],"answer":"Adversativa, pois contrasta dimensão e ocupação","tip":"«Mas» introduz contraste entre os dois factos.","difficulty":"hard","topic":"Coordenação adversativa"},
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
    pool = LITERARY_QUIZ_QUESTIONS
    if difficulty:
        pool = [question for question in pool if question["difficulty"] == difficulty]
    if len(pool) < count:
        pool = list(pool)
        for question in QUESTION_BANK:
            if question not in pool:
                pool.append(question)
        if difficulty:
            pool = [question for question in pool if question["difficulty"] == difficulty]
    unique = []
    seen = set()
    for question in pool:
        key = (question.get("id", ""), question.get("sentence", ""), question.get("question", ""))
        if key not in seen:
            seen.add(key)
            unique.append(question)
    return random.sample(unique, k=min(count, len(unique)))