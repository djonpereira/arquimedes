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
    short_pause = st.slider("Pausa curta", 1, 30, int(settings["short_pause_minutes"]), 1, format="%d min")
    halftime = st.slider("Intervalo do meio", 1, 60, int(settings["halftime_minutes"]), 1, format="%d min")
    quarter = st.slider("Duração de cada quarto", 1, 60, int(settings["quarter_minutes"]), 1, format="%d min")

    st.markdown("### Dificuldade por mini-jogo")
    difficulty_options = ["Misturada", "Fácil", "Média", "Difícil"]

    difficulty_escolha = st.select_slider("1. Escolha Múltipla", difficulty_options, value=settings["difficulty_escolha_multipla"])
    difficulty_quiz = st.select_slider("2. Missão Quiz", difficulty_options, value=settings["difficulty_missao_quiz"])
    difficulty_liga = st.select_slider("3. Liga as Ideias", difficulty_options, value=settings["difficulty_liga_ideias"])
    difficulty_problema = st.select_slider("4. Problema em Campo", difficulty_options, value=settings["difficulty_problema_campo"])
    difficulty_escrita = st.select_slider("5. Laboratório de Escrita", difficulty_options, value=settings["difficulty_escrita"])

    st.markdown("### Avatares que acompanham Rafael")

    familia = st.pills("Família", ["Mãe", "Pops", "Mano", "Rafael", "Adriana", "Adri"], selection_mode="multi", default=settings["avatars_familia"], key="settings_familia")
    basket = st.pills("Família do Basket", ["Patinho", "Cardadeiro", "Salvador", "Fradique", "Luís", "Ferrage", "Léo", "Reis"], selection_mode="multi", default=settings["avatars_familia_basket"], key="settings_basket")
    brothers = st.pills("Brothers do Bairro", ["Zezinho Dino", "Itamar", "Adriana", "Adri", "Salgueiro", "Mano", "Reis"], selection_mode="multi", default=settings["avatars_brothers_bairro"], key="settings_brothers")
    vip = st.pills("VIPs e Personagens", ["Luka", "Wemby", "Franklin", "Michael", "Jason", "Lucia", "Léo"], selection_mode="multi", default=settings["avatars_vips_personagens"], key="settings_vip")

    if st.button("Guardar definições", type="primary", use_container_width=True):
        selections = {
            "Família": familia,
            "Família do Basket": basket,
            "Brothers do Bairro": brothers,
            "VIPs e Personagens": vip,
        }
        invalid = [name for name, values in selections.items() if len(values) != 5]
        if invalid:
            st.warning("Cada grupo deve ter exatamente 5 avatares. Rever: " + ", ".join(invalid) + ".")
            st.stop()
        saved = save_settings({
            "pass_threshold": threshold,
            "penalty_points": penalty,
            "short_pause_minutes": short_pause,
            "halftime_minutes": halftime,
            "quarter_minutes": quarter,
            "difficulty_escolha_multipla": difficulty_escolha,
            "difficulty_missao_quiz": difficulty_quiz,
            "difficulty_liga_ideias": difficulty_liga,
            "difficulty_problema_campo": difficulty_problema,
            "difficulty_escrita": difficulty_escrita,
            "avatars_familia": list(familia),
            "avatars_familia_basket": list(basket),
            "avatars_brothers_bairro": list(brothers),
            "avatars_vips_personagens": list(vip),
        })
        st.success(f"Definições guardadas. Aproveitamento mínimo: {saved['pass_threshold']}%.")
