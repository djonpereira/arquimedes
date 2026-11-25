import streamlit as st

from services.content_requests import load_requests, save_request


def render_content_suggestions() -> None:
    st.markdown('<span class="eyebrow">Novo conteúdo • pedido para revisão humana</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="lesson-title">Sugerir mais questões</h1>', unsafe_allow_html=True)
    st.info("Escreve livremente: podes pedir temas, livros, frases, exercícios ou dificuldades. O pedido não altera o banco nem o progresso.")

    request_text = st.text_area(
        "O que queres adicionar ou mudar?",
        placeholder="Escreve aqui qualquer pedido...",
        height=220,
    )

    if st.button("Guardar pedido", type="primary", use_container_width=True):
        if len(request_text.strip()) < 3:
            st.warning("Escreve pelo menos uma sugestão antes de guardar.")
        else:
            saved = save_request(
                subject="Livre",
                topic="Livre",
                activity_type="Livre",
                difficulty="Livre",
                request_text=request_text,
            )
            st.success("Pedido guardado para revisão humana!")
            st.caption(f"Referência: {saved['id']}")

    st.divider()
    st.markdown("### Pedidos recentes")
    requests = load_requests()
    if not requests:
        st.caption("Ainda não existem pedidos.")
    else:
        for request in reversed(requests[-8:]):
            st.markdown(
                f'<div class="study-card blue"><h3>{request["id"]}</h3><p>{request["request"]}<br><small>{request["status"]}</small></p></div>',
                unsafe_allow_html=True,
            )
