import streamlit as st

from services.progress import load_progress, REQUIRED_SESSION_MODES


def render_session_scoreboard() -> None:
    progress = load_progress()
    current_quarter = progress.get("current_quarter", 1)
    completed_quarters = set(progress.get("completed_quarters", []))
    quarter_modes = progress.get("quarter_modes", {})

    st.markdown('<div class="session-scoreboard">', unsafe_allow_html=True)

    columns = st.columns(4)
    for quarter_number, column in enumerate(columns, start=1):
        modes = set(quarter_modes.get(str(quarter_number), []))
        if quarter_number == current_quarter:
            modes = set(progress.get("session_modes", []))

        dots = "".join(
            '<span class="score-dot done"></span>' if mode in modes else '<span class="score-dot"></span>'
            for mode in REQUIRED_SESSION_MODES
        )

        status = "ATUAL" if quarter_number == current_quarter else ("FEITO" if quarter_number in completed_quarters else "")
        with column:
            st.markdown(
                f'<div class="quarter-board"><div class="quarter-header"><b>{quarter_number}.º Q</b><small>{status}</small></div><div class="quarter-dots">{dots}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)
