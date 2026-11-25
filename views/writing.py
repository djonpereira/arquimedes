import random

import streamlit as st

from services.progress import award_quiz, complete_session_mode, save_mini_game_result
from services.literary_writing_bank import WRITING_PROMPTS, LITERARY_MISSIONS, BOOK_DESCRIPTIONS, validate_writing, validate_verified_quote
from components.encouragement import encouragement
from services.settings_store import calculate_pass, load_settings
from components.mini_game_lock import show_locked_result

writing_difficulty = load_settings()["difficulty_escrita"]


def render_writing(subject: str = "Português", topic: str = "Coordenação e subordinação") -> None:
    if show_locked_result("Laboratório de Escrita"):
        return

    st.markdown('<span class="eyebrow">Laboratório de escrita • lê, cria e corrige</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="lesson-title">Escreve a tua própria oração</h1>', unsafe_allow_html=True)
    st.markdown(f'<span class="eyebrow">{subject} • 9.º ano • {topic}</span>', unsafe_allow_html=True)

    render_literary_mission_selection(subject, topic)


def render_literary_missions(subject: str, topic: str) -> None:
    st.session_state.setdefault("literary_index", 0)
    st.session_state.setdefault("literary_score", 0)
    st.session_state.setdefault("literary_answered", False)

    index = st.session_state.literary_index
    if index >= len(LITERARY_MISSIONS):
        st.markdown('<div class="finish-card"><span>MISSÃO LITERÁRIA</span><h2>Investigação concluída, Rafael! 📚</h2><p>Encontraste, leste e classificaste frases dos planos de leitura.</p></div>', unsafe_allow_html=True)
        st.metric("XP ganho", st.session_state.literary_score)
        if st.button("Nova investigação", type="primary"):
            st.session_state.literary_index = 0
            st.session_state.literary_score = 0
            st.session_state.literary_answered = False
            st.rerun()
        return

    mission = LITERARY_MISSIONS[index]
    description = BOOK_DESCRIPTIONS.get(mission["book"])
    st.progress((index + 1) / len(LITERARY_MISSIONS), text=f"Investigação {index + 1} de {len(LITERARY_MISSIONS)}")

    st.markdown(
        '<div class="study-card blue"><span class="eyebrow">ID: writing-literary</span>'
        '<br><span class="eyebrow">ESCRITA • COORDENAÇÃO E SUBORDINAÇÃO</span>'
        f'<h2>{mission["book"]}</h2><p>{description}</p>'
        f'<p><b>Localização:</b> {mission["location"]}</p>'
        f'<p><b>Exercício:</b> {mission["instruction"]}</p></div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Pista de investigação")
    st.write(mission["character_hint"])
    st.info(mission["instruction"])

    with st.expander("Pista adicional"):
        st.write(f"Procura a relação: **{mission['type']}**")
        st.write(mission["edition_note"])

    with st.expander("Frase confirmada?"):
        st.write("Deves copiar a frase exatamente da tua edição, mantendo maiúsculas e pontuação quando possível.")

    answer = st.text_area("Escreve aqui a frase que encontraste", key=f"literary_answer_{index}", height=120)

    if st.button("Verificar investigação", type="primary", use_container_width=True):
        normalized = " ".join(answer.lower().strip().split())
        if len(normalized) < 12:
            st.warning("A frase ainda é demasiado curta. Volta ao texto e inclui a oração completa.")
        elif not any(connector in normalized for connector in mission["required_connectors"]):
            st.error(f"A frase encontrada não parece conter o conector esperado: {', '.join(mission['required_connectors'])}.")
        else:
            st.session_state.literary_score += 40
            st.session_state.literary_answered = True
            st.success(f"Investigação correta! +40 XP — classificaste uma {mission['type'].lower()}.")

    if st.session_state.literary_answered:
        if st.button("Próxima investigação →", use_container_width=True):
            st.session_state.literary_index += 1
            st.session_state.literary_answered = False
            st.rerun()


def render_literary_mission_selection(subject: str, topic: str) -> None:
    st.markdown('<span class="eyebrow">Missão literária • completa pelo menos 2 de 4</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="lesson-title">Escolhe aqui as tarefas de escrita</h1>', unsafe_allow_html=True)

    st.session_state.setdefault("writing_completed_missions", [])
    completed = set(st.session_state.writing_completed_missions)

    tab1, tab2, tab3, tab4 = st.tabs([
        "1. Frase minha",
        "2. Os da Minha Rua",
        "3. A Pérola",
        "4. Auto da Barca",
    ])

    with tab1:
        render_own_sentence_task("Frase minha")

    with tab2:
        render_literary_task("Os da Minha Rua")

    with tab3:
        render_literary_task("A Pérola")

    with tab4:
        render_literary_task("Auto da Barca do Inferno")

    count = len(completed)
    st.progress(min(count / 2, 1.0), text=f"Missões concluídas: {count} / 2 necessárias")

    live_status = calculate_pass(count, 2)
    st.progress(live_status["percentage"] / 100, text=f"Aproveitamento: {live_status['percentage']}% • limite: {live_status['threshold']}%")
    if live_status["passed"]:
        save_mini_game_result(
            "Laboratório de Escrita",
            count * 40,
            live_status["percentage"],
            True,
        )
        st.success("Limite atingido.")
    else:
        st.caption("Limite ainda não atingido.")


def render_own_sentence_task(choice: str) -> None:
    if "own_sentence_prompt_order" not in st.session_state:
        st.session_state.own_sentence_prompt_order = random.sample(range(len(WRITING_PROMPTS)), len(WRITING_PROMPTS))
    st.session_state.setdefault("own_sentence_prompt_position", 0)
    st.session_state.setdefault("own_sentence_answered", False)

    prompt_position = st.session_state.own_sentence_prompt_position % len(st.session_state.own_sentence_prompt_order)
    prompt_index = st.session_state.own_sentence_prompt_order[prompt_position]
    prompt = WRITING_PROMPTS[prompt_index]
    difficulty = str(prompt.get("difficulty", "Misturada")).upper()

    st.markdown(
        '<div class="study-card blue"><span class="eyebrow">ID: writing-own-sentence</span>'
        f'<br><span class="eyebrow">{difficulty} • ESCRITA • FRASE PRÓPRIA</span>'
        f'<h2>{prompt["type"]}</h2>'
        f'<p><b>{prompt["instruction"]}</b></p>'
        f'<p>{prompt["scene"]}</p></div>',
        unsafe_allow_html=True,
    )

    answer = st.text_area(
        "Escreve aqui a tua frase",
        placeholder="Escreve uma frase própria seguindo o exercício apresentado acima.",
        key=f"own_selected_sentence_{prompt_index}",
        height=110,
        disabled=st.session_state.own_sentence_answered,
    )

    if st.button("Corrigir frase", type="primary", key="own_sentence_correct_tab", disabled=st.session_state.own_sentence_answered):
        result = validate_writing(answer, prompt)
        if result["correct"]:
            st.success(result["message"] + " +25 XP")
            encouragement("correct")
            st.session_state.own_sentence_answered = True
            if choice not in st.session_state.writing_completed_missions:
                st.session_state.writing_completed_missions.append(choice)
        else:
            st.error(result["message"])
            encouragement("incorrect")

    if st.session_state.own_sentence_answered:
        if st.button("Próximo exercício próprio →", use_container_width=True, key="own_sentence_next"):
            st.session_state.own_sentence_prompt_position += 1
            st.session_state.own_sentence_answered = False
            st.rerun()


def render_literary_task(book_name: str) -> None:
    mission_matches = [mission for mission in LITERARY_MISSIONS if mission["book"] == book_name]
    if not mission_matches:
        st.warning("Ainda não existem missões configuradas para este livro.")
        return

    state_key = f"literary_mission_index_{book_name}"
    st.session_state.setdefault(state_key, random.randrange(len(mission_matches)))
    mission_index = int(st.session_state[state_key]) % len(mission_matches)
    mission = mission_matches[mission_index]

    description = BOOK_DESCRIPTIONS.get(book_name)
    st.markdown(
        '<div class="study-card blue"><span class="eyebrow">ID: writing-literary</span>'
        '<br><span class="eyebrow">ESCRITA • COORDENAÇÃO E SUBORDINAÇÃO</span>'
        f'<h2>{book_name}</h2><p>{description}</p>'
        f'<p><b>Localização:</b> {mission["location"]}</p>'
        f'<p><b>Exercício:</b> {mission["instruction"]}</p></div>',
        unsafe_allow_html=True,
    )

    answer_key = f"literary_tab_answered_{book_name}"
    st.session_state.setdefault(answer_key, False)
    answer = st.text_area("Escreve a frase encontrada", key=f"literary_tab_{book_name}", height=120, disabled=st.session_state[answer_key])

    if st.button("Verificar investigação", type="primary", key=f"literary_check_{book_name}", disabled=st.session_state[answer_key]):
        normalized = " ".join(answer.lower().strip().split())
        if len(normalized) < 12:
            st.warning("A frase precisa de ser uma oração completa.")
        elif not any(connector in normalized for connector in mission["required_connectors"]):
            st.error("A frase não parece conter o conector pedido.")
            encouragement("incorrect")
        else:
            verification = validate_verified_quote(book_name, answer, mission["required_connectors"])
            if not verification["correct"]:
                st.error(verification["message"])
                encouragement("incorrect")
            else:
                st.success(verification["message"] + " +40 XP")
                encouragement("correct")
                st.session_state[answer_key] = True
                if book_name not in st.session_state.writing_completed_missions:
                    st.session_state.writing_completed_missions.append(book_name)
                    st.rerun()

    if st.button("Outra investigação desta obra →", use_container_width=True, key=f"literary_next_{book_name}", disabled=st.session_state[answer_key]):
        choices = [index for index in range(len(mission_matches)) if index != mission_index]
        st.session_state[state_key] = random.choice(choices) if choices else mission_index
        st.session_state[answer_key] = False
        st.rerun()
