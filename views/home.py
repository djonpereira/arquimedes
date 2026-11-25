import streamlit as st

from services.progress import load_progress
from services.curriculum import get_rank, get_pause_status, STUDY_CYCLE_MINUTES, GAME_PAUSE_MINUTES


def render_home(subject: str = "Português", topic: str = "Coordenação e subordinação") -> None:
    st.markdown(f'<span class="eyebrow">{subject} • 9.º ano • {topic}</span>', unsafe_allow_html=True)
    st.markdown("# Fala, Rafael! Pronto para subir de nível?")
    st.markdown("Hoje é dia de dominar coordenação e subordinação. Nada de maratona: faz três partidas curtas, ganha XP e fica pronto para o teste — como um modo carreira no 2K26, mas com recompensas reais.")

    st.markdown("""
    <section class="hero court-hero">
      <div class="eyebrow">Missão ativa</div>
      <h1>Rafael, decifra estas orações</h1>
      <p>Conclui os 3 desafios e desbloqueia a <strong>Zona do Teste</strong>. Tu consegues — vamos a isto.</p>
    </section>
    """, unsafe_allow_html=True)

    st.write("")
    m1, m2, m3 = st.columns(3)
    missions = [
        ("1", "COORDENADAS", "Treina as ligações entre orações", "5 min"),
        ("2", "SUBORDINADAS", "Descobre qual oração depende da outra", "8 min"),
        ("3", "PARTIDA FINAL", "Classifica frases como num treino", "10 min"),
    ]
    for column, (number, title, description, duration) in zip((m1, m2, m3), missions):
        with column:
            st.markdown(
                f'<div class="card mission-card"><div class="mission-top"><span class="mission-number">{number}</span><span class="duration">⚡ {duration}</span></div><h3>{title}</h3><p>{description}</p></div>',
                unsafe_allow_html=True,
            )

    st.write("")
    coach1, coach2 = st.columns([1, 1])
    with coach1:
        image_column, text_column = st.columns([0.8, 1.8])
        with image_column:
            st.image("assets/characters/patinho.svg", use_container_width=True)
        with text_column:
            st.markdown('<span class="eyebrow">Mensagem do Patinho</span>', unsafe_allow_html=True)
            st.markdown("### Visão completa começa no treino")
            st.write("Um bom jogador vê o campo inteiro — e um bom estudante prepara cada jogada antes do teste.")
    with coach2:
        image_column, text_column = st.columns([0.8, 1.8])
        with image_column:
            st.image("assets/characters/cardadeiro.svg", use_container_width=True)
        with text_column:
            st.markdown('<span class="eyebrow">Mensagem do Cardadeiro</span>', unsafe_allow_html=True)
            st.markdown("### Notas fortes abrem opções")
            st.write("Quanto melhor Rafael joga na escola, mais possibilidades terá de ser um jogador completo e conquistar bolsas no futuro.")

    st.write("")
    player_progress = load_progress()
    total_xp = player_progress.get("total_xp", 0)

    rank_info = get_rank(total_xp)
    pause_info = get_pause_status(total_xp, player_progress.get("pauses_used", 0))

    a, b, c = st.columns(3)
    a.metric("🔥 Sequência", "2 dias")
    b.metric("⭐ XP acumulado", total_xp)
    c.metric("🎯 Próximo teste", "Esta semana")

    st.markdown("""
    <div class="rank-track">
      <span>ROOKIE</span><i></i><span>STARTER</span><i></i><span>CONTENDER</span><i></i><span>ALL-STAR</span><i></i><span>MVP</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="rank-track"><span>1.º Q • 30 MIN</span><i></i><span>PAUSA 15 MIN</span><i></i><span>2.º Q • 30 MIN</span><i></i><span>INTERVALO 30 MIN</span><i></i><span>3.º Q • 30 MIN</span><i></i><span>PAUSA 15 MIN</span><i></i><span>4.º Q • 30 MIN</span></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("🏆 Ranking atual", rank_info["rank"])
    c2.metric("🎮 Pausas disponíveis", pause_info["available"])
    c3.metric("🎯 Próxima pausa", f"{pause_info['next_milestone']} XP")

    if rank_info["next_target"]:
        rank_progress = min(total_xp / rank_info["next_target"], 1.0)
        st.progress(rank_progress, text=f"{total_xp} / {rank_info['next_target']} XP — próximo nível: {rank_info['next_rank']}")
    else:
        st.success("RANK MVP alcançado. Agora o objetivo é manter o nível!")

    st.info("Sessão diária: **4 × 30 minutos**; pausa de **15 minutos** após o 1.º e 3.º quartos; intervalo principal de **30 minutos** após o 2.º quarto.")

    st.markdown("""
    <div class="session-rule-card">
      <span class="eyebrow">Sessão diária • formato de jogo</span>
      <h2>4 quartos de 30 minutos</h2>
      <p><b>Em cada quarto, Rafael faz pelo menos uma atividade de cada tipo:</b></p>
      <ol>
        <li><b>Escolha Múltipla</b></li>
        <li><b>Missão Quiz</b></li>
        <li><b>Liga as Ideias</b></li>
        <li><b>Problema em Campo</b></li>
        <li><b>Laboratório de Escrita</b></li>
      </ol>
      <p><b>Intervalos:</b> 15 minutos entre o 1.º/2.º e o 3.º/4.º quartos. Intervalo principal de 30 minutos entre o 2.º e o 3.º quartos.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Família")
    family_avatar_columns = st.columns(3)
    family_avatar_names = [("mae", "Mãe"), ("pops", "Pops"), ("mano", "Mano")]
    for column, (asset_name, name) in zip(family_avatar_columns, family_avatar_names):
        with column:
            st.image(f"assets/characters/{asset_name}.svg", use_container_width=True)
            st.caption(name)

    st.markdown("### Família do Basket")
    basket_avatar_columns = st.columns(8)
    basket_avatar_names = [
        ("patinho", "Patinho"), ("cardadeiro", "Cardadeiro"), ("salvador", "Salvador"),
        ("fradique", "Fradique"), ("luis", "Luís"), ("ferrage", "Ferrage"),
        ("leo", "Léo"), ("reis", "Reis"),
    ]
    for column, (asset_name, name) in zip(basket_avatar_columns, basket_avatar_names):
        with column:
            st.image(f"assets/characters/{asset_name}.svg", use_container_width=True)
            st.caption(name)

    st.markdown("### Brothers do Bairro")
    brothers_avatar_columns = st.columns(5)
    brothers_avatar_names = [
        ("zeezinho", "Zezinho Dino"), ("itamar", "Itamar"), ("adriana", "Adriana"),
        ("adri", "Adri"), ("salgueiro", "Salgueiro"),
    ]
    for column, (asset_name, name) in zip(brothers_avatar_columns, brothers_avatar_names):
        with column:
            st.image(f"assets/characters/{asset_name}.svg", use_container_width=True)
            st.caption(name)

    st.markdown("### VIPs e Personagens")
    vip_avatar_columns = st.columns(6)
    vip_avatar_names = [
        ("luka", "Luka"), ("wemby", "Wemby"), ("franklin", "Franklin"),
        ("michael", "Michael"), ("jason", "Jason"), ("lucia", "Lucia"),
    ]
    for column, (asset_name, name) in zip(vip_avatar_columns, vip_avatar_names):
        with column:
            st.image(f"assets/characters/{asset_name}.svg", use_container_width=True)
            st.caption(name)
