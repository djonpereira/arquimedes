import streamlit as st

from services.settings_store import load_settings, save_settings


def render_settings() -> None:
    st.markdown('<span class="eyebrow">Configuração da sessão</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="lesson-title">Definições do Arquimedes</h1>', unsafe_allow_html=True)

    settings = load_settings()

    threshold = st.slider(
        "Aproveitamento necessário para concluir um mini-jogo",
        min_value=50,
        max_value=100,
        value=int(settings["pass_threshold"]),
        step=5,
        format="%d%%",
    )
    penalty = st.slider(
        "Pontos removidos numa resposta errada",
        min_value=0,
        max_value=3,
        value=int(settings["penalty_points"]),
        step=1,
    )
    short_pause = st.slider("Pausa curta", 5, 30, int(settings["short_pause_minutes"]), 5, format="%d min")
    halftime = st.slider("Intervalo do meio", 15, 60, int(settings["halftime_minutes"]), 5, format="%d min")
    quarter = st.slider("Duração de cada quarto", 15, 60, int(settings["quarter_minutes"]), 5, format="%d min")

    if st.button("Guardar definições", type="primary", use_container_width=True):
        saved = save_settings({
            "pass_threshold": threshold,
            "penalty_points": penalty,
            "short_pause_minutes": short_pause,
            "halftime_minutes": halftime,
            "quarter_minutes": quarter,
        })
        st.success(f"Definições guardadas. Aproveitamento mínimo: {saved['pass_threshold']}%.")
