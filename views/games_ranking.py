import streamlit as st

from services.progress import load_progress


def render_games_ranking() -> None:
    st.markdown('<span class="eyebrow">Registo de partidas</span>', unsafe_allow_html=True)
    st.markdown("# Games Rankings")

    progress = load_progress()
    records = progress.get("game_rankings", [])

    if not records:
        st.info("Ainda não existe nenhuma partida registada. Clica em **Start** para criar a primeira entrada.")
        return

    rows = []
    for record in reversed(records):
        quarter_points = record.get("quarter_points", {})
        partial = " • ".join(
            f"{quarter}.º Q: {int(quarter_points.get(str(quarter), 0))}"
            for quarter in range(1, 5)
        )
        status = "Em curso" if record.get("status") == "running" else (
            "Cancelada" if record.get("status") == "cancelled" else "Terminada"
        )
        rows.append({
            "Data de início": record.get("start_date", ""),
            "Disciplina": record.get("subject", ""),
            "Matéria": record.get("topic", ""),
            "Pontos parciais": partial,
            "Pontos finais": int(record.get("final_points", 0)),
            "Nível": record.get("level", "Rookie"),
            "Estado": status,
        })

    rows = rows[:15]
    while len(rows) < 15:
        rows.append({
            "Data de início": "—",
            "Disciplina": "—",
            "Matéria": "—",
            "Pontos parciais": "—",
            "Pontos finais": 0,
            "Nível": "—",
            "Estado": "—",
        })

    st.dataframe(rows, use_container_width=True, hide_index=True, height=560)
