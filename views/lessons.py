import streamlit as st


def _colored_card(title: str, text: str, color: str) -> None:
    st.markdown(
        f'<div class="study-card {color}"><h3>{title}</h3><p>{text}</p></div>',
        unsafe_allow_html=True,
    )


def render_lessons(subject: str = "Português", topic: str = "Coordenação e subordinação") -> None:
    st.markdown('<span class="eyebrow">Mapa visual da matéria • 9.º ano</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="lesson-title">Rafael, entende primeiro a estrutura.</h1>', unsafe_allow_html=True)
    st.markdown(f'<span class="eyebrow">{subject} • {topic}</span>', unsafe_allow_html=True)

    st.markdown("""
    <div class="structure-map">
      <div class="structure-main"><span>FRASE COMPLEXA</span><b>Tem 2 ou mais orações</b></div>
      <div class="structure-arrow">↓</div>
      <div class="structure-options">
        <div><span>COORDENAÇÃO</span><b>Oração 1 + Oração 2</b><small>Mesma independência</small></div>
        <div><span>SUBORDINAÇÃO</span><b>Principal + Subordinada</b><small>Uma depende da outra</small></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "1. Coordenação",
        "2. Subordinação",
        "3. Casos especiais",
        "4. Plano final",
    ])

    with tab1:
        st.markdown("## Oração coordenada")
        st.markdown("As orações coordenadas são **sintaticamente independentes**. Podes sublinhá-las separadamente; nenhuma funciona como complemento ou modificador da outra.")

        c1, c2 = st.columns([1.15, 1])
        with c1:
            st.markdown("### 5 tipos que tens de dominar")
            _colored_card("COPULATIVA", "Ideia de adição ou soma.  <br><b>Conectores:</b> e; nem; não só… mas também", "green")
            _colored_card("ADVERSATIVA", "Ideia de oposição ou contraste.  <br><b>Conectores:</b> mas; porém; todavia; contudo", "orange")
            _colored_card("DISJUNTIVA", "Ideia de alternativa ou escolha.  <br><b>Conectores:</b> ou; ora…ora; ou…ou", "blue")
            _colored_card("CONCLUSIVA", "Ideia de conclusão ou consequência.  <br><b>Conectores:</b> logo; portanto; por isso; assim", "purple")
            _colored_card("EXPLICATIVA", "Justifica uma afirmação anterior.  <br><b>Conectores:</b> pois; porque; que", "pink")
        with c2:
            st.markdown("### Exemplos em contexto")
            st.markdown("<div class='example-card'><b>O Rafael treinou.</b><br><span>Copulativa:</span> O Rafael treinou <mark>e</mark> estudou.<br><small>Há soma de ações.</small></div>", unsafe_allow_html=True)
            st.markdown("<div class='example-card'><b>O Rafael treinou muito.</b><br><span>Adversativa:</span> Treinou muito, <mark>mas</mark> errou no teste.<br><small>Há contraste.</small></div>", unsafe_allow_html=True)
            st.markdown("<div class='example-card'><b>Há uma alternativa.</b><br><mark>Ou</mark> começa agora, <mark>ou</mark> perde tempo.<br><small>Há escolha.</small></div>", unsafe_allow_html=True)
            st.markdown("<div class='example-card'><b>Há uma conclusão.</b><br>Estudou três dias, <mark>logo</mark> está preparado.<br><small>Há conclusão.</small></div>", unsafe_allow_html=True)

        st.markdown("### Assindética ou sindética?")
        a, b = st.columns(2)
        with a:
            st.success("**Sindética:** usa conjunção coordenativa.\n\n“Fui ao treino **mas** esqueci-me da garrafa.”")
        with b:
            st.info("**Assindética:** não usa conjunção; usa-se, normalmente, vírgula ou ponto e vírgula.\n\n“Fui ao treino, esqueci-me da garrafa.”")

    with tab2:
        st.markdown("## Oração subordinada")
        st.markdown("Uma subordinada desempenha uma função dentro da oração subordinante. Se a retirarmos, a frase principal pode ficar incompleta ou mudar de sentido.")

        st.markdown("""
        <div class="dependency-map">
          <div class="principal-node">ORAÇÃO SUBORDINANTE<br><b>Contém o núcleo da mensagem</b></div>
          <div class="dependency-arrow">↔ depende de</div>
          <div class="subordinate-node">ORAÇÃO SUBORDINADA<br><b>Completa ou modifica a principal</b></div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            _colored_card("SUBSTANTIVAS / COMPLETIVAS", "Fazem a função de sujeito, complemento direto, complemento oblíquo ou nome.  <br><b>Pequena pista:</b> substitui por «isso».", "purple")
            st.code("Quero que o Rafael estude.\n→ Quero isso.", language="text")
        with c2:
            _colored_card("ADJETIVAS / RELATIVAS", "Modificam um nome e começam, frequentemente, por que, quem, o qual.  <br><b>Pequena pista:</b> caracteriza alguém ou algo.", "orange")
            st.code("Vi o jogador que marcou o ponto.\n→ O «que» identifica o jogador.", language="text")
        with c3:
            _colored_card("ADVERBIAIS", "Exprimem circunstância: tempo, causa, fim, condição, concessão, comparação, consequencia ou modo.", "blue")
            st.code("Treinei porque queria melhorar.\n→ indica causa.", language="text")

        st.markdown("### As subordinadas adverbiais — tabela rápida")
        table = {
            "Tipo": ["Temporal", "Causal", "Final", "Condicional", "Concessiva", "Comparativa", "Consecutiva", "Consecutiva"],
            "Pergunta": ["Quando?", "Porquê?", "Para quê?", "Com que condição?", "Apesar de quê?", "Como quem?", "Com que resultado?", "Com que resultado?"],
            "Conectores": ["quando, enquanto, logo que", "porque, como, visto que", "para que, a fim de que", "se, caso", "embora, conquanto", "como, assim como", "de modo que, de forma que", "tanto…que"],
        }
        st.dataframe(table, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("## Atenção aos casos que confundem")

        c1, c2 = st.columns(2)
        with c1:
            _colored_card("QUE: conetivo coordenativo ou subordinativo?", "O «que» pode introduzir explicação, conclusão ou subordinação. Observa a relação:  <br>• Coord. explicativa: “Estuda, que vais melhorar.”  <br>• Substantiva: “Quero que estudes.”", "pink")
            _colored_card("POIS: explicação ou conclusão?", "• Antes do verbo ou início da oração: explicativo — “Estuda, pois vais ser aprovado.”  <br>• Depois do verbo: conclusivo — “Vais ser aprovado, pois estudaste.”", "orange")
        with c2:
            _colored_card("QUE RELATIVO VS. QUE CONJUNÇÃO", "O relativo substitui um nome anterior: “O jogador que marcou…”  <br>A conjunção integra uma completiva: “Disse que estava cansado.”", "green")
            _colored_card("COORDENADA VS. FRASE SEPARADA", "Quando as orações têm sujeito próprio mas nenhuma depende da outra, continua a haver coordenação. A vírgula não muda essa relação.", "blue")

        st.markdown("### Análise passo a passo")
        st.markdown("<div class='example-card'><b>Frase:</b> “O Rafael entrou em campo, mas não marcou, porque estava cansado.”</div>", unsafe_allow_html=True)
        a, b, c = st.columns(3)
        a.metric("Oração 1", "O Rafael entrou em campo")
        b.metric("Oração 2", "mas não marcou")
        c.metric("Oração 3", "porque estava cansado")
        st.markdown("- `mas não marcou` → coordenação **adversativa**.\n- `porque estava cansado` → subordinação **causal**.")

    with tab4:
        st.markdown("## Checklist antes de entregar o teste")

        checklist = [
            "Encontrei todos os verbos?",
            "Separei as orações pelos conectores?",
            "Alguma oração completa outra?",
            "Perguntei quando, porquê, para quê ou com que condição?",
            "Identifiquei se a conjunção coordena ou subordina?",
            "Escrevi a classificação completa?",
        ]
        for item in checklist:
            st.checkbox(item, key=f"lesson_check_{item}")

        st.markdown("### Erros que custam pontos")
        e1, e2, e3 = st.columns(3)
        e1.warning("**Não confundir oração com palavra.** Uma oração precisa de verbo.")
        e2.warning("**Não usar só o conector.** Explica a relação entre as ideias.")
        e3.warning("**Não dividir por vírgula à pressa.** A vírgula pode separar coordenadas ou marcar subordinação.")

        st.success("**Frase-modelo:** “O jogador treinou muito, mas perdeu o jogo, porque estava lesionado.”\n\nResposta: `mas perdeu o jogo` é coordenada adversativa; `porque estava lesionado` é subordinada adverbial causal.")
