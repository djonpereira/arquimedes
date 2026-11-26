import time
import streamlit as st

from services.progress import (
    load_progress,
    REQUIRED_SESSION_MODES,
    start_game_record,
    finish_or_cancel_game,
    is_session_complete,
    complete_quarter_with_rest,
)
from services.settings_store import load_settings


def render_session_scoreboard(subject: str = "Português", topic: str = "") -> None:
    settings = load_settings()
    if not bool(settings.get("modo_jogo", False)):
        return
    render_timer(subject, topic)


@st.fragment(run_every=1)
def render_timer(subject: str = "Português", topic: str = "") -> None:
    progress = load_progress()
    current_quarter = progress.get("current_quarter", 1)
    completed_quarters = set(progress.get("completed_quarters", []))
    mini_game_results = progress.get("mini_game_results", {})

    duration_seconds = int(load_settings().get("quarter_minutes", 30)) * 60

    st.session_state.setdefault("timer_running", False)
    st.session_state.setdefault("timer_remaining", duration_seconds)
    st.session_state.setdefault("timer_end_epoch", None)
    st.session_state.setdefault("timer_quarter", current_quarter)
    st.session_state.setdefault("timeout_used", {1: 0, 2: 0, 3: 0, 4: 0})
    st.session_state.setdefault("timer_action", "Start")
    st.session_state.setdefault("timer_canceled", False)

    persisted_timeout_usage = progress.get("timeout_usage", {})
    st.session_state.setdefault("timeout_used", {
        1: int(persisted_timeout_usage.get("1", 0)),
        2: int(persisted_timeout_usage.get("2", 0)),
        3: int(persisted_timeout_usage.get("3", 0)),
        4: int(persisted_timeout_usage.get("4", 0)),
    })

    if st.session_state.timer_quarter != current_quarter:
        st.session_state.timer_quarter = current_quarter
        st.session_state.timer_running = False
        st.session_state.timer_remaining = duration_seconds
        st.session_state.timer_end_epoch = None
        st.session_state.timer_action = "Start"
        st.session_state.timer_canceled = False
        st.session_state.timeout_used.setdefault(current_quarter, 0)

    rest_phase = progress.get("rest_phase")

    if rest_phase:
        if st.session_state.timer_running and st.session_state.timer_end_epoch:
            remaining = max(0, int(st.session_state.timer_end_epoch - time.time()))
        elif st.session_state.timer_end_epoch:
            remaining = max(0, int(st.session_state.timer_end_epoch - time.time()))
        else:
            remaining = int(rest_phase.get("remaining_seconds", duration_seconds))
            st.session_state.timer_end_epoch = time.time() + remaining
            st.session_state.timer_running = True

        st.session_state.timer_remaining = remaining

        if remaining <= 0:
            next_quarter = int(rest_phase.get("next_quarter", current_quarter + 1))
            progress["current_quarter"] = next_quarter
            progress.pop("rest_phase", None)
            progress["session_modes"] = []
            progress.setdefault("quarter_modes", {})[str(next_quarter)] = []
            from services.progress import save_progress
            save_progress(progress)
            st.session_state.timer_quarter = next_quarter
            st.session_state.timer_remaining = duration_seconds
            st.session_state.timer_end_epoch = None
            st.session_state.timeout_used[next_quarter] = 0
            st.session_state.timer_running = False
            st.session_state.timer_action = "Start"
            st.rerun()

    elif st.session_state.timer_running and st.session_state.timer_end_epoch:
        remaining = max(0, int(st.session_state.timer_end_epoch - time.time()))
        st.session_state.timer_remaining = remaining

        if remaining <= 0:
            st.session_state.timer_running = False
            st.session_state.timer_end_epoch = None
            settings = load_settings()
            progress = complete_quarter_with_rest(
                int(settings.get("short_pause_minutes", 15)),
                int(settings.get("halftime_minutes", 30)),
            )
            rest_phase = progress.get("rest_phase")
            if rest_phase:
                rest_remaining = int(rest_phase.get("remaining_seconds", duration_seconds))
                st.session_state.timer_remaining = rest_remaining
                st.session_state.timer_end_epoch = time.time() + rest_remaining
                st.session_state.timer_action = "Restart"
            st.rerun()
    else:
        remaining = int(st.session_state.timer_remaining)

    minutes, seconds = divmod(int(remaining), 60)
    timeout_used = int(st.session_state.timeout_used.get(current_quarter, 0))

    quarter_html = []
    for quarter_number in range(1, 5):
        quarter_results = mini_game_results.get(str(quarter_number), {})
        dots = "".join(
            '<span class="score-dot done" style="background:#5d9d6b!important;border-color:#5d9d6b!important"></span>'
            if bool(quarter_results.get(mode, {}).get("passed", False))
            else '<span class="score-dot"></span>'
            for mode in REQUIRED_SESSION_MODES
        )
        status = "ATUAL" if quarter_number == current_quarter else (
            "FEITO" if quarter_number in completed_quarters else ""
        )
        used = int(st.session_state.timeout_used.get(quarter_number, 0))
        timeout_squares = "".join(
            '<span class="timeout-square used"></span>' if index <= used
            else '<span class="timeout-square"></span>'
            for index in range(1, 3)
        )
        quarter_html.append(
            f'<div class="quarter-board"><div class="quarter-header"><b>{quarter_number}.º Q</b><small>{status}</small></div>'
            f'<div class="quarter-dots">{dots}<span class="timeout-separator"></span>{timeout_squares}</div></div>'
        )

    with st.container(key="session-scoreboard"):
        action, quarters, clock = st.columns([0.72, 4.2, 0.82], gap="small")

        with action:
            stored_action = st.session_state.timer_action
            action_label = stored_action if isinstance(stored_action, str) else "Start"
            if st.button(action_label, key="timer_action_button", disabled=action_label == "Canceled", use_container_width=True):
                if action_label == "Start":
                    st.session_state.timeout_used = {1: 0, 2: 0, 3: 0, 4: 0}
                    st.session_state.timer_remaining = duration_seconds
                    st.session_state.timer_canceled = False
                    start_game_record(subject, topic)
                    if remaining <= 0:
                        st.session_state.timer_remaining = duration_seconds
                        remaining = duration_seconds
                    st.session_state.timer_running = True
                    st.session_state.timer_end_epoch = time.time() + remaining
                    st.session_state.timer_action = "Timeout"
                    st.rerun()

                elif action_label == "Timeout":
                    st.session_state.timer_remaining = max(0, int(st.session_state.timer_end_epoch - time.time()))
                    st.session_state.timer_running = False
                    st.session_state.timer_end_epoch = None
                    st.session_state.timeout_used[current_quarter] = timeout_used + 1
                    progress["timeout_usage"] = progress.get("timeout_usage", {"1": 0, "2": 0, "3": 0, "4": 0})
                    progress["timeout_usage"][str(current_quarter)] = timeout_used + 1
                    from services.progress import save_progress
                    save_progress(progress)
                    st.session_state.timer_action = "Restart"
                    st.rerun()

                elif action_label == "Restart":
                    resumed_remaining = max(1, int(st.session_state.timer_remaining))
                    st.session_state.timer_remaining = resumed_remaining
                    st.session_state.timer_running = True
                    st.session_state.timer_end_epoch = time.time() + resumed_remaining
                    if int(st.session_state.timeout_used.get(current_quarter, 0)) >= 2:
                        st.session_state.timer_action = "Cancel game"
                    else:
                        st.session_state.timer_action = "Timeout"
                    st.rerun()

                elif action_label == "Cancel game":
                    finish_or_cancel_game(cancelled=True)
                    st.session_state.timer_running = False
                    st.session_state.timer_remaining = duration_seconds
                    st.session_state.timeout_used = {1: 0, 2: 0, 3: 0, 4: 0}
                    st.session_state.timer_action = "Start"
                    st.rerun()

        with quarters:
            st.markdown('<div class="quarter-grid">' + "".join(quarter_html) + '</div>', unsafe_allow_html=True)

        with clock:
            st.markdown(f'<div class="quarter-timer">{minutes:02d}:{seconds:02d}</div>', unsafe_allow_html=True)

    if progress.get("active_game") and is_session_complete(progress) and not progress.get("rest_phase"):
        settings = load_settings()
        progress = complete_quarter_with_rest(
            int(settings.get("short_pause_minutes", 15)),
            int(settings.get("halftime_minutes", 30)),
        )
        rest_phase = progress.get("rest_phase")
        if rest_phase:
            st.session_state.timer_running = False
            st.session_state.timer_remaining = int(rest_phase.get("remaining_seconds", duration_seconds))
            st.session_state.timer_end_epoch = time.time() + int(rest_phase.get("remaining_seconds", duration_seconds))
            st.session_state.timer_action = "Restart"
            st.rerun()
