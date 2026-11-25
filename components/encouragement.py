import random
import streamlit as st


ENCOURAGEMENTS = [
    ("patinho.svg", "Patinho", "Boa, parça! Um passe limpo e o campo abre-se."),
    ("cardadeiro.svg", "Cardadeiro", "Boa leitura de jogo. Repara na relação antes de responder."),
    ("salvador.svg", "Salvador", "Brother, foi um bom lance. Agora sobe outra jogada."),
    ("fradique.svg", "Fradique", "Fradique confirma: treino consistente ganha partidas."),
    ("luis.svg", "Luís", "Mantém a cabeça fria. A próxima jogada é tua."),
    ("ferrage.svg", "Ferrage", "Ajusta a posição e volta a tentar. O erro também ensina."),
    ("pops.svg", "Pops", "Bom trabalho. 30 minutos de foco valem uma boa pausa depois."),
    ("itamar.svg", "Itamar", "Cesto limpo! Agora prepara o próximo ataque."),
    ("adriana.svg", "Adriana", "Boa resposta. Vamos para a próxima jogada."),
    ("zeezinho.svg", "Zezinho Dino", "Era isso! Mantém o ritmo, colega."),
    ("leo.svg", "Léo", "Boa visão de campo. Continua assim."),
    ("rafael.svg", "Rafael", "Eu consigo — uma jogada certa de cada vez."),
    ("wemby.svg", "Wemby", "Bloqueio fechado, leitura limpa. Sobe o nível."),
    ("mano.svg", "Mano", "É assim, parça. Pequenos passos dão XP."),
    ("mae.svg", "Mãe", "Estou orgulhosa do teu esforço. Continua com calma."),
]


FAILURES = [
    ("patinho.svg", "Patinho", "Falháste esta jogada, mas não perdes o jogo. Ajusta e volta."),
    ("cardadeiro.svg", "Cardadeiro", "Falha de leitura, não falha de capacidade. Revê a pista."),
    ("salvador.svg", "Salvador", "Brother, esta não entrou. Faz o passe outra vez."),
    ("fradique.svg", "Fradique", "Falháste? Treina a jogada outra vez. Erros dão experiência."),
    ("luis.svg", "Luís", "Mantém a calma. Uma falha é só uma jogada corrigida."),
    ("ferrage.svg", "Ferrage", "Falháste, mas tens hipótese de arrumar a resposta. Volta ao essencial."),
    ("pops.svg", "Pops", "Não desistas. Lê a explicação e tenta uma jogada melhor."),
    ("itamar.svg", "Itamar", "Esta não entrou, mas a próxima pode ser tua."),
    ("adriana.svg", "Adriana", "A jogada falhou; a aprendizagem continua. Lê com atenção."),
    ("zeezinho.svg", "Zezinho Dino", "Falha na resposta, não falha no esforço. Recomeça."),
    ("leo.svg", "Léo", "Revê a pista e prepara outra jogada."),
    ("rafael.svg", "Rafael", "Ainda consigo. Vou corrigir esta jogada e subir de novo."),
    ("wemby.svg", "Wemby", "Um bloqueio não acaba o jogo. Ajusta a posição."),
    ("mano.svg", "Mano", "Falháste, parça. Aprende com esta e tenta outra vez."),
    ("mae.svg", "Mãe", "Está bem falhar. O importante é perceber o que corrigir."),
]


def encouragement(message_type: str = "correct") -> None:
    if message_type == "correct":
        image_name, name, message = random.choice(ENCOURAGEMENTS)
    else:
        image_name, name, message = random.choice(FAILURES)
    image_column, text_column = st.columns([0.25, 2])
    with image_column:
        st.image(f"assets/characters/{image_name}", use_container_width=True)
    with text_column:
        card_type = "made" if message_type == "correct" else "missed"
        st.markdown(f'<div class="encourage-card {card_type}"><b>{name}</b><span>{message}</span></div>', unsafe_allow_html=True)
