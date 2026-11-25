import streamlit as st

from services.game_bank import get_connection_items, get_problem_items
from services.progress import complete_session_mode
from components.encouragement import encouragement
from services.settings_store import calculate_pass


CONNECTIONS = [
    {
        "left": ["Viveu a jogada e marcou", "Treinou muito, mas perdeu", "Estudou ou descansou", "Passou no teste, logo estava preparado"],
        "right": ["Oposição", "Conclusão", "Alternativa", "Adição"],
        "answer": {0: "Adição", 1: "Oposição", 2: "Alternativa", 3: "Conclusão"},
    },
    {
        "left": ["Porque não tinha dormido", "Embora estivesse cansado", "Quando chegou ao campo", "Para vencer o jogo"],
        "right": ["Finalidade", "Tempo", "Concessão", "Causa"],
        "answer": {0: "Causa", 1: "Concessão", 2: "Tempo", 3: "Finalidade"},
    },
]


def _reset_game(name: str) -> None:
    st.session_state.pop(name, None)


def render_connections(subject: str, topic: str) -> None:
    st.markdown('<span class="eyebrow">Jogo de ligação • 10 ligações aleatórias</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="lesson-title">Liga a jogada à relação certa</h1>', unsafe_allow_html=True)

    if "connection_items" not in st.session_state:
        st.session_state.connection_items = get_connection_items(10)
        st.session_state.connection_round = 0
        st.session_state.connection_score = 0

    round_index = st.session_state.connection_round
    items = st.session_state.connection_items

    st.session_state.setdefault("connection_answered", False)

    if round_index >= len(items):
        st.markdown('<div class="finish-card"><span>CAMPO CONCLUÍDO</span><h2>Boa visão de jogo, Rafael! 🏀</h2><p>Conseguiste ligar cada jogada à regra certa.</p></div>', unsafe_allow_html=True)
        st.metric("Pontos", st.session_state.connection_score)
        pass_status = calculate_pass(st.session_state.connection_score // 20, len(items))
        st.progress(pass_status["percentage"] / 100, text=f"Aproveitamento: {pass_status['percentage']}% • limite: {pass_status['threshold']}%")
        if st.button("Novo conjunto de ligações", type="primary"):
            st.session_state.connection_items = get_connection_items(10)
            st.session_state.connection_round = 0
            st.session_state.connection_score = 0
            st.rerun()
        if pass_status["passed"]:
            complete_session_mode("Liga as Ideias")
            st.success("Mini-jogo concluído com aproveitamento suficiente!")
        else:
            st.error("Ainda não atingiste o limite. Recomeça a ligação das ideias.")
        return

    item = items[round_index]
    st.progress((round_index + 1) / len(items), text=f"Ligação {round_index + 1} de {len(items)}")
    st.markdown(f'<div class="game-token">{item["left"]}</div>', unsafe_allow_html=True)

    answer = st.radio(
        "Que relação representa?",
        [""] + item["options"],
        key=f"connection_answer_{round_index}",
        index=0,
        disabled=st.session_state.connection_answered,
    )

    if st.button("Validar ligação", type="primary", disabled=st.session_state.connection_answered):
        if not answer:
            st.warning("Escolhe uma relação antes de validar.")
        elif answer == item["right"]:
            st.session_state.connection_score += 20
            st.success(f"Ligação perfeita! +20 XP — {item['tip']}")
            encouragement("correct")
            st.session_state.connection_answered = True
        else:
            st.error(f"Quase. A relação correta é **{item['right']}**. {item['tip']}")
            encouragement("incorrect")
            st.session_state.connection_answered = True

    if st.button("Próxima ligação →"):
        st.session_state.connection_answered = False
        st.session_state.connection_round += 1
        st.rerun()


def render_problem_game(subject: str, topic: str) -> None:
    st.markdown('<span class="eyebrow">Problema de leitura • 10 cenários aleatórios</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="lesson-title">Decide a jogada da frase</h1>', unsafe_allow_html=True)

    if "problem_items" not in st.session_state:
        st.session_state.problem_items = get_problem_items(10)
        st.session_state.problem_round = 0
        st.session_state.problem_score = 0

    round_index = st.session_state.problem_round
    items = st.session_state.problem_items

    st.session_state.problem_answered = False

    if round_index >= len(items):
        st.markdown('<div class="finish-card"><span>DECISÃO COMPLETA</span><h2>Boa leitura de jogo, Rafael! 🧠</h2><p>Escolheste soluções que mantêm o sentido e a relação correta.</p></div>', unsafe_allow_html=True)
        st.metric("Pontos", st.session_state.problem_score)
        pass_status = calculate_pass(st.session_state.problem_score // 20, len(items))
        st.progress(pass_status["percentage"] / 100, text=f"Aproveitamento: {pass_status['percentage']}% • limite: {pass_status['threshold']}%")
        if st.button("Novo conjunto de problemas", type="primary"):
            st.session_state.problem_items = get_problem_items(10)
            st.session_state.problem_round = 0
            st.session_state.problem_score = 0
            st.rerun()
        if pass_status["passed"]:
            complete_session_mode("Problema em Campo")
            st.success("Mini-jogo concluído com aproveitamento suficiente!")
        else:
            st.error("Ainda não atingiste o limite. Recomeça os problemas.")
        return

    item = items[round_index]
    st.progress((round_index + 1) / len(items), text=f"Problema {round_index + 1} de {len(items)}")
    st.markdown(f'<div class="scenario-card">📋 <b>Cenário</b><p>{item["scenario"]}</p></div>', unsafe_allow_html=True)

    choice = st.radio("Que alteração mantém melhor o sentido?", item["options"], key=f"problem_{round_index}", index=None, disabled=st.session_state.problem_answered)

    if st.button("Confirmar decisão", type="primary", disabled=st.session_state.problem_answered):
        if choice is None:
            st.warning("Escolhe uma solução antes de confirmar.")
        elif choice == item["answer"]:
            st.session_state.problem_score += 20
            st.success(f"Decisão correta! +20 XP — {item['tip']}")
            encouragement("correct")
            st.session_state.problem_answered = True
        else:
            st.error(f"Quase. A solução melhor é: **{item['answer']}**. {item['tip']}")
            encouragement("incorrect")
            st.session_state.problem_answered = True

    if st.button("Próximo problema →"):
        st.session_state.problem_answered = False
        st.session_state.problem_round += 1
        st.rerun()
