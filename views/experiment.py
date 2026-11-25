import streamlit as st

from services.progress import award_quiz, complete_session_mode, save_mini_game_result
from services.question_bank import get_random_quiz
from components.encouragement import encouragement
from services.settings_store import calculate_pass, load_settings
from components.mini_game_lock import show_locked_result
from components.mini_game_shell import render_mini_game_status, render_mini_game_card, render_mini_game_feedback


QUESTIONS = [
    {"sentence":"Entrei em campo e marquei um ponto.","question":"Qual é a relação?","options":["Coordenação copulativa","Subordinação causal","Coordenação adversativa"],"answer":"Coordenação copulativa","tip":"O «e» soma duas ações — coordenação copulativa."},
    {"sentence":"Estudei muito, mas não consegui terminar.","question":"Que tipo de coordenação?","options":["Copulativa","Adversativa","Conclusiva"],"answer":"Adversativa","tip":"O «mas» cria oposição."},
    {"sentence":"Não joguei porque tinha uma lesão.","question":"Que oração é «porque tinha uma lesão»?","options":["Subordinada causal","Coordenada disjuntiva","Coordenada explicativa"],"answer":"Subordinada causal","tip":"Dá a causa da ação principal."},
    {"sentence":"Se treinares todos os dias, melhorarás.","question":"Como se classifica a subordinada?","options":["Condicional","Temporal","Conclusiva"],"answer":"Condicional","tip":"A melhoria depende da condição."},
    {"sentence":"Ou jogo online ou estudo Português.","question":"Que relação existe?","options":["Disjuntiva","Causal","Copulativa"],"answer":"Disjuntiva","tip":"O «ou…ou» apresenta alternativas."},
]


def render_experiment(mode: str = "mission", subject: str = "Português", topic: str = "Coordenação e subordinação") -> None:
    if show_locked_result("Missão Quiz"):
        return

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

    difficulty = load_settings()["difficulty_missao_quiz"]
    st.markdown(f'<span class="eyebrow">10 jogadas • dificuldade {difficulty.lower()}</span>', unsafe_allow_html=True)

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
    live_status = calculate_pass(st.session_state.quiz_made, len(questions))
    render_mini_game_status("Jogada", index, len(questions), live_status["percentage"], live_status["threshold"], st.session_state.quiz_xp)

    if live_status["passed"]:
        st.success("Limite atingido.")
    else:
        st.caption("Limite ainda não atingido.")

    render_mini_game_card(question["id"], question.get("difficulty", "").upper(), question.get("topic", ""), f"“{question['sentence']}”", question["question"])

    answer = st.radio("Escolhe uma resposta", question["options"], key=f"answer_{index}", index=None, disabled=st.session_state.quiz_answered)
    confirm = st.button("Confirmar resposta", type="primary", use_container_width=True, disabled=st.session_state.quiz_answered)

    if confirm:
        if answer is None:
            st.warning("Escolhe primeiro uma opção, Rafael.")
        elif answer == question["answer"]:
            st.session_state.quiz_xp += 20
            st.session_state.quiz_streak += 1
            st.session_state.quiz_made += 1
            st.session_state.quiz_best_streak = max(st.session_state.quiz_best_streak, st.session_state.quiz_streak)
            st.session_state.quiz_answered = True
            render_mini_game_feedback(True, question["tip"], 20)
            encouragement("correct")
        else:
            st.session_state.quiz_streak = 0
            st.session_state.quiz_answered = True
            st.info(question["tip"])
            render_mini_game_feedback(False, question["tip"], 20)
            encouragement("incorrect")

    if st.session_state.quiz_answered:
        if st.button("Próxima jogada →", use_container_width=True):
            st.session_state.quiz_index += 1
            st.session_state.quiz_answered = False
            st.rerun()

    st.caption(f"XP: {st.session_state.quiz_xp}  •  Streak: {st.session_state.quiz_streak}")

'''
    pass_status = calculate_pass(st.session_state.quiz_made, len(questions))
    st.progress(pass_status["percentage"] / 100, text=f"Aproveitamento: {pass_status['percentage']}% • limite: {pass_status['threshold']}%")
    if not pass_status["passed"]:
        st.error("Ainda não atingiste o limite. Recomeça o mini-jogo e melhora esta jogada.")
    else:
        st.success("Mini-jogo concluído com aproveitamento suficiente!")
        save_mini_game_result("Missão Quiz", st.session_state.quiz_xp, pass_status["percentage"], pass_status["passed"])
        complete_session_mode("Missão Quiz")
'''
