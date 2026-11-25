import streamlit as st

from views.home import render_home
from views.lessons import render_lessons
from views.experiment import render_experiment
from views.multiple_choice import render_multiple_choice
from views.games import render_connections, render_problem_game
from views.writing import render_writing
from views.content_suggestions import render_content_suggestions
from views.settings import render_settings
from components.styles import load_styles
from components.session_scoreboard import render_session_scoreboard
from services.curriculum import CURRICULUM, LEVELS


st.set_page_config(
    page_title="Rafael — Arquimedes",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_styles()

with st.sidebar:
    st.markdown('<div class="brand-mark">R</div><p class="brand-name">ARQUIMEDES</p>', unsafe_allow_html=True)
    st.caption("O teu estudo • 9.º ano")

    subject = st.selectbox("Disciplina", list(CURRICULUM.keys()), index=0)
    topics = list(CURRICULUM[subject]["topics"])
    topic = st.selectbox("Materia", topics, index=0)

    st.divider()
    page = st.radio(
        "Navegação",
        ["Painel do Rafael", "Resumos", "Escolha Múltipla", "Missão Quiz", "Liga as Ideias", "Problema em Campo", "Laboratório de Escrita", "Sugerir Conteúdo", "Definições"],
        label_visibility="collapsed",
    )

    progress = CURRICULUM[subject]["topics"][topic]["progress"]
    current_level = next((name for name, minimum in reversed(LEVELS) if progress >= minimum), "Rookie")
    st.markdown("<small>CAMINHO DE NÍVEL</small>", unsafe_allow_html=True)
    st.progress(progress / 100, text=f"{current_level} • {progress} XP")

render_session_scoreboard()

st.caption(f"{subject}  /  {topic}")

if page == "Painel do Rafael":
    render_home(subject, topic)
elif page == "Resumos":
    render_lessons(subject, topic)
elif page == "Escolha Múltipla":
    render_multiple_choice(subject, topic)
elif page == "Missão Quiz":
    render_experiment(subject=subject, topic=topic)
elif page == "Liga as Ideias":
    render_connections(subject, topic)
elif page == "Problema em Campo":
    render_problem_game(subject, topic)
elif page == "Laboratório de Escrita":
    render_writing(subject, topic)
elif page == "Sugerir Conteúdo":
    render_content_suggestions()
elif page == "Definições":
    render_settings()
