import streamlit as st


def render_game_rules() -> None:
    st.markdown('<span class="eyebrow">Manual do jogador</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="lesson-title">Regras do Jogo</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p>O Arquimedes transforma o estudo de Português num jogo composto por uma partida de quatro quartos. '
        'Cada decisão, resposta ou frase contribui para o teu progresso.</p>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 1. Como começa uma sessão")
        st.markdown(
            '<div class="study-card blue"><p>Premir <b>Start</b> no placar superior cria uma nova partida. '
            'A partida começa no 1.º quarto e o temporizador passa a contar a duração configurada em Definições.</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown("### 2. Os quatro quartos")
        st.markdown(
            '<div class="study-card"><p>A partida está dividida em quatro períodos. '
            'Em cada quarto é necessário concluir os cinco mini-jogos definidos pela aplicação:</p>'
            '<ul><li>Escolha Múltipla</li><li>Missão Quiz</li><li>Liga as Ideias</li><li>Problema em Campo</li>'
            '<li>Laboratório de Escrita</li></ul></div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("### 3. Semelhança com timeouts")
        st.markdown(
            '<div class="study-card blue"><p>Os <b>timeouts</b> funcionam como pequenas paragens pedagógicas:'
            '<br><br><b>Timeout</b> — pausa o cronómetro no momento atual.'
            '<br><b>Restart</b> — retoma exatamente o tempo que estava a contar.'
            '<br><b>Cancel game</b> — aparece após o segundo timeout e permite cancelar a partida.</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown("### 4. Limite de timeouts")
        st.markdown(
            '<div class="study-card"><p>Existem dois espaços de timeout por quarto. '
            'Quando os dois são usados, a próxima ação disponível é cancelar a partida. '
            'Os timeouts são reiniciados ao avançar para um novo quarto.</p></div>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown("### 5. Ritmo dos períodos e intervalos")

    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="study-card"><h3>Quarto</h3><p>O temporizador usa a duração configurada em Definições.</p></div>', unsafe_allow_html=True)
    c2.markdown('<div class="study-card blue"><h3>Pausa curta</h3><p>Depois do 1.º e do 3.º quarto existe uma pausa curta configurável.</p></div>', unsafe_allow_html=True)
    c3.markdown('<div class="study-card"><h3>Intervalo</h3><p>Após o 2.º quarto existe o intervalo principal, definido em Definições.</p></div>', unsafe_allow_html=True)

    st.markdown("### 6. Conclusão de um quarto")
    st.markdown(
        '<div class="study-card blue"><p>Um quarto só avança quando todos os cinco mini-jogos estão concluídos com '
        'o aproveitamento necessário. Quando termina o tempo normal, o sistema inicia automaticamente o período de pausa.</p></div>',
        unsafe_allow_html=True,
    )

    st.markdown("### 7. Como funciona cada mini-jogo")

    game1, game2 = st.columns(2)
    with game1:
        st.markdown(
            '<div class="study-card"><h3>Escolha Múltipla</h3><p>Bloco de dez questões. '
            'Pode haver uma resposta ou várias respostas corretas.</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="study-card blue"><h3>Missão Quiz</h3><p>Dez jogadas rápidas com XP, streak e feedback imediato. '
            'Uma resposta correta mantém ou aumenta a sequência.</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="study-card"><h3>Laboratório de Escrita</h3><p>O aluno cria frases, identifica relações sintáticas ou encontra excertos literários nos livros carregados.</p></div>',
            unsafe_allow_html=True,
        )

    with game2:
        st.markdown(
            '<div class="study-card blue"><h3>Liga as Ideias</h3><p>Associar uma expressão à relação correspondente, '
            'como adição, oposição, causa, tempo ou finalidade.</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="study-card"><h3>Problema em Campo</h3><p>Escolher a reformulação que mantém melhor o sentido '
            'ou representar corretamente a relação sintática.</p></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="study-card blue"><h3>Fecho do mini-jogo</h3><p>Depois de aprovado ou reprovado, o mini-jogo fica fechado neste quarto. '
            'Só poderá ser novamente realizado no quarto seguinte.</p></div>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown("### 8. Pontuação, aproveitamento e XP")

    p1, p2, p3 = st.columns(3)
    p1.metric("Resposta correta", "+20 XP em vários jogos")
    p2.metric("Aproveitamento", "Definido em Definições")
    p3.metric("Níveis", "Rookie → MVP")

    st.markdown(
        '<div class="study-card"><p>A aprovação depende da percentagem configurada em Definições, por defeito <b>80%</b>. '
        'Os pontos ganhos por quarto são somados na pontuação da partida e podem influenciar o ranking e os níveis do utilizador.</p></div>',
        unsafe_allow_html=True,
    )

    st.markdown("### 9. Dificuldade")
    st.markdown(
        '<div class="study-card blue"><p>Em Definições podes escolher <b>Misturada, Fácil, Média ou Difícil</b> para cada mini-jogo. '
        'O nível selecionado determina a dificuldade das questões disponíveis nesse jogo.</p></div>',
        unsafe_allow_html=True,
    )

    st.markdown("### 10. Navegação durante o jogo")
    st.markdown(
        '<div class="study-card"><p>Enquanto o cronómetro está a contar, a barra lateral apresenta apenas os cinco mini-jogos. '
        'Durante um timeout, também pode estar disponível o Resumo da Matéria. '
        'Definições e outras páginas de administração ficam fora do fluxo ativo para não interferirem com a partida.</p></div>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.success("Objetivo: completar os cinco mini-jogos em cada quarto, usar bem os timeouts e terminar os quatro quartos com o melhor desempenho possível.")
