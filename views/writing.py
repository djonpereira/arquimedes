import streamlit as st

from services.progress import award_quiz, complete_session_mode
from services.literary_writing_bank import WRITING_PROMPTS, LITERARY_MISSIONS, BOOK_DESCRIPTIONS, validate_writing
from components.encouragement import encouragement
from services.settings_store import calculate_pass


def render_writing(subject: str = "Português", topic: str = "Coordenação e subordinação") -> None:
    st.markdown('<span class="eyebrow">Laboratório de escrita • lê, cria e corrige</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="lesson-title">Escreve a tua própria oração</h1>', unsafe_allow_html=True)
    st.markdown(f'<span class="eyebrow">{subject} • 9.º ano • {topic}</span>', unsafe_allow_html=True)

    st.session_state.setdefault("writing_index", 0)
    st.session_state.setdefault("writing_score", 0)
    st.session_state.setdefault("writing_answered", False)

    index = st.session_state.writing_index

    render_literary_mission_selection(subject, topic)

    if index >= len(WRITING_PROMPTS):
        award_quiz(subject, topic, st.session_state.writing_score)
        st.markdown('<div class="finish-card"><span>DESAFIO DE ESCRITA</span><h2>Rafael, completas-te o laboratório! ✍️</h2><p>A escrita obriga-te a verificar o verbo, o conector e o sentido.</p></div>', unsafe_allow_html=True)
        st.metric("XP ganho", st.session_state.writing_score)
        if st.button("Repetir escrita", type="primary"):
            st.session_state.writing_index = 0
            st.session_state.writing_score = 0
            st.session_state.writing_answered = False
            st.rerun()
        return

    prompt = WRITING_PROMPTS[index]
    st.progress((index + 1) / len(WRITING_PROMPTS), text=f"Tarefa {index + 1} de {len(WRITING_PROMPTS)}")

    st.markdown(f'<div class="scenario-card">📖 <b>Contexto da cena</b><p>{prompt["scene"]}</p></div>', unsafe_allow_html=True)
    st.markdown("### Tua missão")
    st.write(prompt["instruction"])

    with st.expander("Pedir uma pista"):
        st.write("Começa por escolher um sujeito, uma ação e o conector pedido.")
        st.write("Exemplo de estrutura: **sujeito + verbo; conector + outra ação**.")

    answer = st.text_area("Escreve a tua oração", key=f"writing_answer_{index}", height=110)

    if st.button("Corrigir a escrita", type="primary", use_container_width=True):
        result = validate_writing(answer, prompt)
        if result["correct"]:
            st.session_state.writing_score += 25
            st.session_state.writing_answered = True
            st.success(result["message"] + " +25 XP")
            encouragement("correct")
            st.caption("Podes comparar com estas frases de referência:")
            for example in prompt["examples"]:
                st.write(f"- {example}")
        else:
            st.session_state.writing_answered = False
            st.error(result["message"])
            encouragement("incorrect")

    if st.session_state.writing_answered:
        if st.button("Próxima tarefa →", use_container_width=True):
            st.session_state.writing_index += 1
            st.session_state.writing_answered = False
            st.rerun()


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

    st.markdown(f'<div class="scenario-card">📚 <b>{mission["book"]}</b><br><small>{mission["author"]}</small><p>{description}</p><p><b>Localização:</b> {mission["location"]}</p></div>', unsafe_allow_html=True)
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

    if count >= 2:
        complete_session_mode("Laboratório de Escrita")
        st.success("Mini-jogo concluído! Duas tarefas de escrita foram realizadas.")
    else:
        st.info(f"Falta realizar {2 - count} tarefa(s) para concluir o mini-jogo.")


def render_own_sentence_task(choice: str) -> None:
    st.markdown('<div class="scenario-card">✍️ <b>Frase minha</b><p>Cria uma frase original usando uma relação sintática pedida.</p></div>', unsafe_allow_html=True)
    prompt = WRITING_PROMPTS[st.session_state.get("own_sentence_prompt_index", 0) % len(WRITING_PROMPTS)]
    st.write(prompt["instruction"])
    st.session_state.setdefault("own_sentence_answered", False)
    answer = st.text_area("Escreve aqui a tua frase", key="own_selected_sentence_tabs", height=110, disabled=st.session_state.own_sentence_answered)

    if st.button("Corrigir frase", type="primary", key="own_sentence_correct_tab", disabled=st.session_state.own_sentence_answered):
        result = validate_writing(answer, prompt)
        if result["correct"]:
            st.success(result["message"] + " +25 XP")
            encouragement("correct")
            st.session_state.own_sentence_answered = True
            if choice not in st.session_state.writing_completed_missions:
                st.session_state.writing_completed_missions.append(choice)
                st.rerun()
        else:
            st.error(result["message"])
            encouragement("incorrect")


def render_literary_task(book_name: str) -> None:
    mission_matches = [mission for mission in LITERARY_MISSIONS if mission["book"] == book_name]
    if not mission_matches:
        st.warning("Ainda não existem missões configuradas para este livro.")
        return

    mission = mission_matches[0]
    description = BOOK_DESCRIPTIONS.get(book_name)
    st.markdown(f'<div class="scenario-card">📚 <b>{book_name}</b><br><small>{mission["author"]}</small><p>{description}</p><p><b>Localização:</b> {mission["location"]}</p></div>', unsafe_allow_html=True)
    st.info(mission["instruction"])

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
            st.success("Investigação correta! +40 XP")
            encouragement("correct")
            st.session_state[answer_key] = True
            if book_name not in st.session_state.writing_completed_missions:
                st.session_state.writing_completed_missions.append(book_name)
                st.rerun()
