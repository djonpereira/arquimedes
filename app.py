import streamlit as st

from views.scoreboard import render_scoreboard
from views.lessons import render_lessons
from views.experiment import render_experiment
from views.multiple_choice import render_multiple_choice
from views.games import render_connections, render_problem_game
from views.writing import render_writing
from views.content_suggestions import render_content_suggestions
from views.settings import render_settings
from views.games_ranking import render_games_ranking
from views.game_rules import render_game_rules
from components.styles import load_styles
from components.session_scoreboard import render_session_scoreboard
from services.curriculum import CURRICULUM, LEVELS
from services.progress import load_progress

st.set_page_config(
    page_title="Rafael — Arquimedes",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_styles()

with st.sidebar:
    st.markdown('<div class="brand-mark">R</div><p class="brand-name">ARQUIMEDES</p>', unsafe_allow_html=True)
    st.caption("O teu coach de estudo")

    subject = st.selectbox("Disciplina", list(CURRICULUM.keys()), index=0)
    topics = list(CURRICULUM[subject]["topics"])
    topic = st.selectbox("Materia", topics, index=0)

    st.divider()
    progress_state = load_progress()
    active_game = progress_state.get("active_game")
    timer_running = bool(st.session_state.get("timer_running", False))
    timer_action = st.session_state.get("timer_action", "Start")
    in_timeout = bool(active_game) and not timer_running and timer_action in ("Restart", "Cancel game")

    mini_game_links = [
        "1. Escolha Múltipla",
        "2. Missão Quiz",
        "3. Liga as Ideias",
        "4. Problema em Campo",
        "5. Laboratório de Escrita",
    ]

    if active_game and timer_running:
        with st.container(key="sidebar-active-mini-nav"):
            page = st.radio("Navegação", mini_game_links, label_visibility="collapsed")
    elif active_game and in_timeout:
        with st.container(key="sidebar-timeout-nav"):
            page = st.radio("Navegação", ["Resumo da Matéria", *mini_game_links], label_visibility="collapsed")
    else:
        navigation_options = [
            "Resumo da Matéria",
            "Scoreboard do Jogo",
            *mini_game_links,
            "Games Rankings",
            "Definições",
            "Regras do Jogo",
            "Sugerir Conteúdo",
        ]
        page = st.radio("Navegação", navigation_options, label_visibility="collapsed")


#    progress = CURRICULUM[subject]["topics"][topic]["progress"]
#    current_level = next((name for name, minimum in reversed(LEVELS) if progress >= minimum), "Rookie")
#    st.markdown("<small>CAMINHO DE NÍVEL</small>", unsafe_allow_html=True)
#    st.progress(progress / 100, text=f"{current_level} • {progress} XP")


render_session_scoreboard(subject, topic)

st.caption(f"{subject}  /  {topic}")

if page == "Scoreboard do Jogo":
    render_scoreboard(subject, topic)
elif page == "Resumo da Matéria":
    render_lessons(subject, topic)
elif page == "1. Escolha Múltipla":
    render_multiple_choice(subject, topic)
elif page == "2. Missão Quiz":
    render_experiment(subject=subject, topic=topic)
elif page == "3. Liga as Ideias":
    render_connections(subject, topic)
elif page == "4. Problema em Campo":
    render_problem_game(subject, topic)
elif page == "5. Laboratório de Escrita":
    render_writing(subject, topic)
elif page == "Games Rankings":
    render_games_ranking()
elif page == "Sugerir Conteúdo":
    render_content_suggestions()
elif page == "Definições":
    render_settings()
elif page == "Regras do Jogo":
    render_game_rules()
