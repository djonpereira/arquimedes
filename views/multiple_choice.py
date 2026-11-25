import streamlit as st

from services.progress import award_quiz, complete_session_mode, save_mini_game_result
from services.multiple_choice_bank import get_multiple_choice_quiz
from components.encouragement import encouragement
from services.settings_store import calculate_pass, load_settings
from components.mini_game_shell import render_mini_game_status, render_mini_game_card, render_mini_game_feedback


def render_multiple_choice(subject: str = "Português", topic: str = "Coordenação e subordinação") -> None:
    st.markdown('<span class="eyebrow">Banco • 200 questões • escolha múltipla</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="lesson-title">Rafael, escolhe a melhor resposta</h1>', unsafe_allow_html=True)
    st.markdown(f'<span class="eyebrow">{subject} • 9.º ano • {topic}</span>', unsafe_allow_html=True)

    difficulty = load_settings()["difficulty_escolha_multipla"]
    difficulty_map = {"Fácil": "easy", "Média": "medium", "Difícil": "hard"}
    selected_difficulty = difficulty_map.get(difficulty)

    if "mc_difficulty" not in st.session_state:
        st.session_state.mc_difficulty = difficulty

    if st.session_state.mc_difficulty != difficulty:
        st.session_state.mc_difficulty = difficulty
        st.session_state.mc_items = None
        st.session_state.mc_index = 0
        st.session_state.mc_score = 0
        st.session_state.mc_answered = False
        st.session_state.mc_saved = False

    st.session_state.setdefault("mc_index", 0)
    st.session_state.setdefault("mc_score", 0)
    st.session_state.setdefault("mc_answered", False)
    st.session_state.setdefault("mc_saved", False)

    if "mc_items" not in st.session_state or st.session_state.mc_items is None:
        st.session_state.mc_items = get_multiple_choice_quiz(10, selected_difficulty)

    items = st.session_state.mc_items
    index = st.session_state.mc_index

    if index >= len(items):
        if not st.session_state.mc_saved:
            award_quiz(subject, topic, st.session_state.mc_score)
            st.session_state.mc_saved = True

        st.balloons()
        st.markdown('<div class="finish-card"><span>PLACAR FECHADO</span><h2>Boa partida, Rafael! 🏀</h2><p>Revisaste 10 questões escolhidas aleatoriamente.</p></div>', unsafe_allow_html=True)
        st.metric("XP ganho", st.session_state.mc_score)

        pass_status = calculate_pass(st.session_state.mc_score // 20, len(items))
        st.progress(pass_status["percentage"] / 100, text=f"Aproveitamento: {pass_status['percentage']}% • limite: {pass_status['threshold']}%")
        if not pass_status["passed"]:
            st.error("Ainda não atingiste o limite. Recomeça o bloco de 10 questões.")
        else:
            st.success("Bloco concluído com aproveitamento suficiente!")
            complete_session_mode("Escolha Múltipla")

        save_mini_game_result("Escolha Múltipla", st.session_state.mc_score, pass_status["percentage"], pass_status["passed"])

        if st.button("Novo bloco de 10", type="primary", use_container_width=True):
            st.session_state.mc_items = get_multiple_choice_quiz(10, selected_difficulty)
            st.session_state.mc_index = 0
            st.session_state.mc_score = 0
            st.session_state.mc_answered = False
            st.session_state.mc_saved = False
            st.rerun()
        return

    item = items[index]
    live_status = calculate_pass(st.session_state.mc_score // 20, len(items))
    render_mini_game_status("Questão", index, len(items), live_status["percentage"], live_status["threshold"], st.session_state.mc_score)

    render_mini_game_card(item["id"], item["difficulty"].upper(), item["topic"], f"“{item['sentence']}”", item["question"])

    if item.get("multiple", False):
        answer = st.pills(
            "Seleciona todas as respostas corretas",
            item["options"],
            selection_mode="multi",
            key=f"mc_answer_{index}",
        )
    else:
        answer = st.pills(
            "Escolhe uma resposta",
            item["options"],
            selection_mode="single",
            key=f"mc_answer_{index}",
        )

    if st.button("Confirmar resposta", type="primary", use_container_width=True, disabled=st.session_state.mc_answered):
        if not answer:
            st.warning("Escolhe pelo menos uma opção antes de confirmar.")
        elif item.get("multiple", False):
            selected = set(answer)
            correct = set(item["answer"])
            if selected == correct:
                st.session_state.mc_score += 20
                st.session_state.mc_answered = True
                st.success("Resposta correta! +20 XP")
                st.info(item["tip"])
                render_mini_game_feedback(True, item["tip"], 20)
                encouragement("correct")
            else:
                st.session_state.mc_answered = True
                st.error("Quase. Seleciona exatamente: " + " + ".join(item["answer"]))
                st.info(item["tip"])
                render_mini_game_feedback(False, item["tip"], 20)
                encouragement("incorrect")
        elif answer == item["answer"]:
            st.session_state.mc_score += 20
            st.session_state.mc_answered = True
            st.success("Resposta correta! +20 XP")
            st.info(item["tip"])
            render_mini_game_feedback(True, item["tip"], 20)
            encouragement("correct")
        else:
            st.session_state.mc_answered = True
            st.error(f"Quase. A resposta correta é: **{item['answer']}**")
            st.info(item["tip"])
            render_mini_game_feedback(False, item["tip"], 20)
            encouragement("incorrect")

    if st.session_state.mc_answered:
        if st.button("Próxima questão →", use_container_width=True):
            st.session_state.mc_index += 1
            st.session_state.mc_answered = False
            st.rerun()

    st.caption(f"XP do bloco: {st.session_state.mc_score}")
