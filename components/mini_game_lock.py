import streamlit as st

from services.progress import get_mini_game_result


def show_locked_result(mode: str) -> bool:
    result = get_mini_game_result(mode)
    if not result:
        return False

    status = "Aprovado" if result["passed"] else "Recomeçar necessário"
    st.markdown('<span class="eyebrow">Mini-jogo fechado neste quarto</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="lesson-title">Resultado do mini-jogo</h1>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Estado", status)
    c2.metric("Aproveitamento", f'{result["percentage"]}%')
    c3.metric("Pontos ganhos", result["points"])
    st.progress(result["percentage"] / 100)

    if result["passed"]:
        st.success("Este mini-jogo já está concluído neste quarto. Continua para o próximo.")
    else:
        st.error("O aproveitamento ficou abaixo do limite. Este resultado fica guardado até mudar de quarto.")

    st.caption("O resultado só fica disponível para novo jogo no próximo quarto.")
    return True
