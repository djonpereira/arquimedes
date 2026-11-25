import streamlit as st

from services.curriculum import CURRICULUM, LEVELS, get_rank
from services.progress import REQUIRED_SESSION_MODES, load_progress
from services.settings_store import load_settings


MODE_TOTALS = {
    "Escolha Múltipla": 10,
    "Missão Quiz": 10,
    "Liga as Ideias": 10,
    "Problema em Campo": 10,
    "Laboratório de Escrita": 2,
}


def _mini_status(mode: str, result: dict | None) -> tuple[str, int, int, str]:
    if not result:
        return "Por jogar", 0, MODE_TOTALS[mode], "pending"

    total = MODE_TOTALS[mode]
    percentage = int(result.get("percentage", 0))
    if mode == "Laboratório de Escrita":
        correct = round(total * percentage / 100)
    else:
        correct = round(total * percentage / 100)
    correct = max(0, min(total, correct))
    incorrect = total - correct
    status = "Aprovado" if result.get("passed") else "Recomeçar"
    return status, correct, incorrect, "passed" if result.get("passed") else "failed"


def render_scoreboard(subject: str = "Português", topic: str = "Coordenação e subordinação") -> None:
    progress = load_progress()
    settings = load_settings()

    st.markdown('<span class="eyebrow">Scoreboard da partida</span>', unsafe_allow_html=True)
    st.markdown("# Estado atual do jogo")

    curriculum_topic = CURRICULUM.get(subject, {}).get("topics", {}).get(topic, {})
    summary = curriculum_topic.get("summary", "Nesta matéria, vais praticar conceitos essenciais através de exercícios variados.")
    st.info(f"**Introdução à matéria:** {summary}")

    active_game = progress.get("active_game")
    current_quarter = int(progress.get("current_quarter", 1))
    completed_quarters = set(progress.get("completed_quarters", []))
    total_xp = int(progress.get("total_xp", 0))
    rank_info = get_rank(total_xp)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Quarto atual", f"{current_quarter}.º Q" if active_game else "Sem partida")
    m2.metric("Quartos concluídos", f"{len(completed_quarters)} / 4")
    m3.metric("Nível", rank_info["rank"])
    m4.metric("XP acumulado", total_xp)

    if not active_game:
        st.warning("Ainda não existe uma partida ativa. Usa **Start** no placar superior para começar a sessão.")

    st.markdown("### Progresso dos quatro quartos")
    quarter_rows = []
    quarter_columns = st.columns(4)
    timeout_usage = progress.get("timeout_usage", {})
    for quarter_number, column in enumerate(quarter_columns, start=1):
        if quarter_number in completed_quarters:
            state = "Concluído"
        elif quarter_number == current_quarter and active_game:
            state = "Em curso"
        else:
            state = "Por jogar"
        used = int(timeout_usage.get(str(quarter_number), 0))
        quarter_rows.append({
            "Quarto": f"{quarter_number}.º",
            "Estado": state,
            "Timeouts usados": f"{used} / 2",
        })

    st.dataframe(
        quarter_rows,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Quarto": st.column_config.TextColumn("Quarto", width="small"),
            "Estado": st.column_config.TextColumn("Estado", width="medium"),
            "Timeouts usados": st.column_config.TextColumn("Timeouts usados", width="medium"),
        },
        height=205,
    )

    rest_phase = progress.get("rest_phase")
    if rest_phase:
        pause_minutes = int(rest_phase.get("duration_minutes", 15))
        after_quarter = int(rest_phase.get("after_quarter", current_quarter))
        st.info(f"Intervalo em curso após o {after_quarter}.º quarto: pausa de {pause_minutes} minutos.")

    st.markdown("### Mini-jogos deste quarto")

    mini_results = progress.get("mini_game_results", {}).get(str(current_quarter), {})
    mini_rows = []
    for mode in REQUIRED_SESSION_MODES:
        status, correct, incorrect, visual = _mini_status(mode, mini_results.get(mode))
        result = mini_results.get(mode)
        percentage = int(result.get("percentage", 0)) if result else 0
        points = int(result.get("points", 0)) if result else 0
        mini_rows.append({
            "Mini-jogo": mode,
            "Estado": status,
            "Acertos": correct,
            "Falhas": incorrect,
            "Aproveitamento": f"{percentage}%",
            "Pontos": points,
        })

    st.dataframe(
        mini_rows,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Mini-jogo": st.column_config.TextColumn("Mini-jogo", width="large"),
            "Estado": st.column_config.TextColumn("Estado", width="medium"),
            "Acertos": st.column_config.NumberColumn("Acertos", width="small"),
            "Falhas": st.column_config.NumberColumn("Falhas", width="small"),
            "Aproveitamento": st.column_config.TextColumn("Aproveitamento", width="medium"),
            "Pontos": st.column_config.NumberColumn("Pontos", width="small"),
        },
        height=280,
    )

    st.markdown("### Regras deste período")
    r1, r2, r3 = st.columns(3)
    r1.metric("Aproveitamento necessário", f"{int(settings.get('pass_threshold', 80))}%")
    r2.metric("Duração do quarto", f"{int(settings.get('quarter_minutes', 30))} min")
    r3.metric("Timeouts por quarto", "2")

    passed_count = sum(
        1 for mode in REQUIRED_SESSION_MODES
        if bool(mini_results.get(mode, {}).get("passed", False))
    )
    st.progress(passed_count / len(REQUIRED_SESSION_MODES), text=f"Mini-jogos aprovados neste quarto: {passed_count} / 5")

    if passed_count == len(REQUIRED_SESSION_MODES):
        st.success("Os cinco mini-jogos deste quarto estão concluídos com aproveitamento suficiente.")
    elif active_game:
        st.caption("Completa cada mini-jogo para avançar para o intervalo e para o quarto seguinte.")
