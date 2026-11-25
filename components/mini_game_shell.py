import streamlit as st


def render_mini_game_status(label: str, index: int, total: int, percentage: int, threshold: int, xp: int = 0) -> None:
    st.progress((index + 1) / total, text=f"{label} {index + 1} de {total}")
    st.progress(percentage / 100, text=f"Aproveitamento: {percentage}% • limite: {threshold}%")
    if percentage >= threshold:
        st.success("Limite atingido.")
    else:
        st.caption("Limite ainda não atingido.")
    if xp:
        st.caption(f"XP ganho nesta jogada: {xp}")


def render_mini_game_card(item_id: str, difficulty: str, topic: str, title: str, prompt: str) -> None:
    st.markdown(
        f'<div class="quiz-card"><span class="eyebrow">ID: {item_id}</span><br>'
        f'<span class="eyebrow">{difficulty} • {topic}</span>'
        f'<h2>{title}</h2><p>{prompt}</p></div>',
        unsafe_allow_html=True,
    )


def render_mini_game_feedback(correct: bool, explanation: str, xp: int = 20) -> None:
    if correct:
        st.success(f"Resposta correta! +{xp} XP")
        st.info(explanation)
    else:
        st.error("Quase. Revê a relação apresentada antes da próxima jogada.")
        st.info(explanation)
