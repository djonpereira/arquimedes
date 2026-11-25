import streamlit as st

from services.progress import award_quiz, complete_session_mode
from services.question_bank import get_random_quiz
from components.encouragement import encouragement


QUESTIONS = [
    {"sentence":"Entrei em campo e marquei um ponto.","question":"Qual é a relação?","options":["Coordenação copulativa","Subordinação causal","Coordenação adversativa"],"answer":"Coordenação copulativa","tip":"O «e» soma duas ações — coordenação copulativa."},
    {"sentence":"Estudei muito, mas não consegui terminar.","question":"Que tipo de coordenação?","options":["Copulativa","Adversativa","Conclusiva"],"answer":"Adversativa","tip":"O «mas» cria oposição."},
    {"sentence":"Não joguei porque tinha uma lesão.","question":"Que oração é «porque tinha uma lesão»?","options":["Subordinada causal","Coordenada disjuntiva","Coordenada explicativa"],"answer":"Subordinada causal","tip":"Dá a causa da ação principal."},
    {"sentence":"Se treinares todos os dias, melhorarás.","question":"Como se classifica a subordinada?","options":["Condicional","Temporal","Conclusiva"],"answer":"Condicional","tip":"A melhoria depende da condição."},
    {"sentence":"Ou jogo online ou estudo Português.","question":"Que relação existe?","options":["Disjuntiva","Causal","Copulativa"],"answer":"Disjuntiva","tip":"O «ou…ou» apresenta alternativas."},
]


def render_experiment(mode: str = "mission", subject: str = "Português", topic: str = "Coordenação e subordinação") -> None:
    title = "Treino Express" if mode == "express" else "Partida Relâmpago"
    st.markdown('<span class="eyebrow">3 jogadas • menos de 2 minutos</span>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="lesson-title">Rafael, {title}</h1>', unsafe_allow_html=True)
    st.markdown(f'<span class="eyebrow">{subject} • 9.º ano • {topic}</span>', unsafe_allow_html=True)

    st.session_state.setdefault("quiz_index", 0)
    st.session_state.setdefault("quiz_xp", 0)
    st.session_state.setdefault("quiz_answered", False)
    st.session_state.setdefault("quiz_streak", 0)
    st.session_state.setdefault("quiz_best_streak", 0)
    st.session_state.setdefault("quiz_made", 0)
    st.session_state.setdefault("quiz_saved", False)

    st.markdown('<span class="eyebrow">10 jogadas • dificuldade misturada</span>', unsafe_allow_html=True)

    difficulty = st.segmented_control(
        "Dificuldade",
        ["Misturada", "Fácil", "Média", "Difícil"],
        selection_mode="single",
        default="Misturada",
    )

    if "quiz_difficulty" not in st.session_state:
        st.session_state.quiz_difficulty = "Misturada"

    if st.session_state.quiz_difficulty != difficulty:
        st.session_state.quiz_difficulty = difficulty
        st.session_state.quiz_index = 0
        st.session_state.quiz_xp = 0
        st.session_state.quiz_answered = False
        st.session_state.quiz_streak = 0
        st.session_state.quiz_saved = False
        st.session_state.quiz_made = 0
        st.session_state.quiz_best_streak = 0
        st.session_state.quiz_questions = None

    difficulty_map = {"Fácil": "easy", "Média": "medium", "Difícil": "hard"}

    if "quiz_questions" not in st.session_state or st.session_state.quiz_questions is None:
        st.session_state.quiz_questions = get_random_quiz(
            count=10,
            difficulty=difficulty_map.get(difficulty),
        )

    questions = st.session_state.quiz_questions
    index = st.session_state.quiz_index

    if index >= len(questions):
        if not st.session_state.quiz_saved:
            award_quiz(subject, topic, st.session_state.quiz_xp)
            st.session_state.quiz_saved = True
        st.balloons()
        st.markdown('<div class="finish-card"><span>MISSÃO COMPLETA</span><h2>Rafael, fechaste o jogo! 🏀</h2><p>Aprender também é repetir a jogada até ela sair limpa.</p></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("XP ganho", st.session_state.quiz_xp)
        c2.metric("Cestos", sum(1 for _ in range(index)))
        c3.metric("Melhor streak", st.session_state.quiz_streak)
        if st.button("Nova partida", type="primary", use_container_width=True):
            st.session_state.quiz_index = 0
            st.session_state.quiz_xp = 0
            st.session_state.quiz_answered = False
            st.session_state.quiz_streak = 0
            st.session_state.quiz_best_streak = 0
            st.session_state.quiz_made = 0
            st.session_state.quiz_saved = False
            st.session_state.quiz_questions = None
            st.rerun()
        return

    question = questions[index]
    st.progress((index + 1) / len(questions), text=f"Jogada {index + 1} de {len(questions)}")

    shot1, shot2 = st.columns([1.15, 1])
    with shot1:
        st.markdown(f'''<div class="shot-stage"><div class="hoop">CESTO</div><div class="ball{(' shot-made' if st.session_state.quiz_answered else '')}">●</div><div class="shot-floor"></div></div>''', unsafe_allow_html=True)
    with shot2:
        st.markdown(f'<div class="quiz-card"><span class="eyebrow">Jogada {index + 1}</span><h2>“{question["sentence"]}”</h2><p>{question["question"]}</p></div>', unsafe_allow_html=True)
        answer = st.radio("Escolhe o lançamento", question["options"], key=f"answer_{index}", index=None)
        confirm = st.button("Lançar!", type="primary", use_container_width=True)

    if confirm:
        if answer is None:
            st.warning("Escolhe primeiro uma opção, Rafael.")
        elif answer == question["answer"]:
            st.session_state.quiz_xp += 20
            st.session_state.quiz_streak += 1
            st.session_state.quiz_made += 1
            st.session_state.quiz_best_streak = max(st.session_state.quiz_best_streak, st.session_state.quiz_streak)
            st.session_state.quiz_answered = True
            st.markdown('<div class="encourage-card made"><b>🏀 Cesto limpo!</b><span>+20 XP • streak ativo</span></div>', unsafe_allow_html=True)
            st.info(question["tip"])
            encouragement("correct")
        else:
            st.session_state.quiz_streak = 0
            st.session_state.quiz_answered = True
            st.markdown('<div class="encourage-card missed"><b>Bloqueio defendido</b><span>Ajusta a jogada. Aprende com o lance.</span></div>', unsafe_allow_html=True)
            st.info(question["tip"])
            encouragement("incorrect")

    if st.session_state.quiz_answered:
        if st.button("Próxima jogada →", use_container_width=True):
            st.session_state.quiz_index += 1
            st.session_state.quiz_answered = False
            st.rerun()

    st.caption(f"XP: {st.session_state.quiz_xp}  •  Streak: {st.session_state.quiz_streak}")

    complete_session_mode("Missão Quiz")
