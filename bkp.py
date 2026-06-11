import streamlit as st
import random

st.set_page_config(page_title="DataLearning App", page_icon="📱", layout="centered")

# Estilização baseada no WhatsApp
st.markdown("""
    <style>
    .stApp { background-color: #efeae2; }
    .chat-header {
        background-color: #005e54; color: white; padding: 15px;
        font-weight: bold; border-radius: 10px 10px 0px 0px;
        text-align: center; font-size: 18px; margin-bottom: 10px;
    }
    .msg-left {
        background-color: #ffffff; padding: 12px; border-radius: 0px 15px 15px 15px;
        margin: 8px 0px; max-width: 85%; text-align: left; color: #000000;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .msg-right {
        background-color: #e2f9cb; padding: 12px; border-radius: 15px 0px 15px 15px;
        margin: 8px 0px; float: right; min-width: 40%; max-width: 85%;
        text-align: left; color: #000000; box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .feedback-box-correct {
        background-color: #d4edda; color: #155724; padding: 15px;
        border-radius: 10px; border-left: 5px solid #28a745; margin-top: 20px; clear: both;
    }
    .feedback-box-incorrect {
        background-color: #f8d7da; color: #721c24; padding: 15px;
        border-radius: 10px; border-left: 5px solid #dc3545; margin-top: 20px; clear: both;
    }
    .clearfix { clear: both; }
    
    /* Forçar estilo limpo nas tabelas do chat */
    table { width: 100%; border-collapse: collapse; margin-top: 8px; }
    th, td { border: 1px solid #ddd; padding: 6px; text-align: left; font-size: 13px; }
    th { background-color: #f2f2f2; }
    </style>
""", unsafe_allow_html=True)

# Inicialização das variáveis de sessão
if "cenarios_ordem" not in st.session_state:
    # Embaralha a ordem dos cenários (1-5)
    cenarios_ordem = list(range(1, 6))
    random.shuffle(cenarios_ordem)
    st.session_state.cenarios_ordem = cenarios_ordem
    st.session_state.indice_pergunta = 0
    st.session_state.score = 0
    st.session_state.respostas = {}  # Rastreia acertos por pergunta

if "indice_pergunta" not in st.session_state:
    st.session_state.indice_pergunta = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "respostas" not in st.session_state:
    st.session_state.respostas = {}

if "resposta_dada" not in st.session_state:
    st.session_state.resposta_dada = None

cenarios = {
    1: {
        "contexto": "🛍️ <b>Loja de Roupas:</b><br>Preciso calcular o gasto típico dos clientes para repor o estoque de roupas de forma segura.",
        "tabela": "<table><tr><th>Cliente</th><th>Gasto</th></tr><tr><td>Cliente A</td><td>R$ 120,00</td></tr><tr><td>Cliente B</td><td>R$ 150,00</td></tr><tr><td>Cliente C</td><td>R$ 90,00</td></tr><tr><td><b>Cliente D</b></td><td><b>R$ 15.000,00</b></td></tr></table>",
        "certa": "mediana",
        "fb_sucesso": "<b>✓ Perfeito!</b> A Mediana ignorou o efeito do cliente atípico (Outlier) de R$ 15k e mostrou o comportamento real de consumo da maioria dos clientes.",
        "fb_erro": "<b>✕ Errado!</b> A Média foi puxada para cima pelo valor gigante. Ela diria que o gasto típico é de R$ 3.840 por cliente! Comprar estoque baseado nisso traria enorme prejuízo."
    },
    2: {
        "contexto": "🍔 <b>Hamburgueria Artística:</b><br>Quero prever nosso custo fixo diário aproximado com motoboys. Veja o relatório de pagamentos da última semana:",
        "tabela": "<table><tr><th>Dia da Semana</th><th>Gasto Motoboy</th></tr><tr><td>Segunda-feira</td><td>R$ 310,00</td></tr><tr><td>Terça-feira</td><td>R$ 290,00</td></tr><tr><td>Quarta-feira</td><td>R$ 300,00</td></tr><tr><td>Quinta-feira</td><td>R$ 320,00</td></tr></table>",
        "certa": "média",
        "fb_sucesso": "<b>✓ Muito bem!</b> Como os dados são extremamente estáveis e sem valores absurdos (Outliers), a Média é o cálculo mais preciso para prever o custo exato.",
        "fb_erro": "<b>✕ Incorreto!</b> Quando não existem valores atípicos nos dados, a Média é a métrica padrão ideal, pois ela aproveita e pondera o valor exato de cada dia na conta."
    },
    3: {
        "contexto": "💈 <b>Barbearia do Bairro:</b><br>Preciso estabelecer o tempo padrão de atendimento na agenda para o próximo sábado.",
        "tabela": "<table><tr><th>Atendimento</th><th>Tempo Gasto</th></tr><tr><td>Cliente 1</td><td>25 minutos</td></tr><tr><td>Cliente 2</td><td>30 minutos</td></tr><tr><td>Cliente 3</td><td>20 minutos</td></tr><tr><td><b>Cliente 4 (Passou mal)</b></td><td><b>180 minutos</b></td></tr></table>",
        "certa": "mediana",
        "fb_sucesso": "<b>✓ Exato!</b> Esse atendimento de 3 horas foi uma exceção. A Mediana blinda o seu negócio contra esses imprevistos, mantendo o tempo de agenda correto.",
        "fb_erro": "<b>✕ Agenda Travada!</b> A Média jogaria o tempo padrão para cima, fazendo parecer que cada cliente demora mais de uma hora. Sua agenda ficaria ociosa e vazia."
    },
    4: {
        "contexto": "🛒 <b>Mercado de Bairro:</b><br>Vou assinar um contrato de manutenção e preciso informar o faturamento diário típico do caixa principal:",
        "tabela": "<table><tr><th>Dia do Teste</th><th>Faturamento</th></tr><tr><td>Dia 1</td><td>R$ 4.100,00</td></tr><tr><td>Dia 2</td><td>R$ 3.950,00</td></tr><tr><td>Dia 3</td><td>R$ 4.050,00</td></tr><tr><td>Dia 4</td><td>R$ 4.000,00</td></tr></table>",
        "certa": "média",
        "fb_sucesso": "<b>✓ Perfeito!</b> Sem nenhum susto ou anomalia nos dados do caixa, a Média resume a movimentação de forma justa e matematicamente precisa.",
        "fb_erro": "<b>✕ Errado...</b> Você preferiu a Mediana, mas em distribuições uniformes e equilibradas (sem anomalias), a Média é a melhor ferramenta de análise e decisão."
    },
    5: {
        "contexto": "💰 <b>Equipe de Vendas:</b><br>Um candidato a vendedor perguntou qual é a comissão típica recebida pela nossa equipe atual para avaliar se aceita a vaga:",
        "tabela": "<table><tr><th>Colaborador</th><th>Comissão Recebida</th></tr><tr><td>Vendedor 1</td><td>R$ 1.800,00</td></tr><tr><td>Vendedor 2</td><td>R$ 2.000,00</td></tr><tr><td>Vendedor 3</td><td>R$ 1.900,00</td></tr><tr><td><b>Diretor (Vendeu Franquia)</b></td><td><b>R$ 45.000,00</b></td></tr></table>",
        "certa": "mediana",
        "fb_sucesso": "<b>✓ Excelente!</b> A Mediana mostra o ganho real de um vendedor de balcão. A super comissão isolada do diretor não enganará o novo funcionário.",
        "fb_erro": "<b>✕ Cuidado!</b> Se usar a Média, vai dizer que o ganho padrão é de mais de R$ 12.000! O candidato vai aceitar a vaga e se frustrar logo no primeiro mês ao ver a realidade."
    }
}

# Pega o cenário atual baseado na ordem embaralhada
cenario_numero = st.session_state.cenarios_ordem[st.session_state.indice_pergunta]
q = cenarios[cenario_numero]

# Renderização da tela do app
st.markdown(f'<div class="chat-header">💬 Consultor de Negócios — Pergunta {st.session_state.indice_pergunta + 1} de 5 | Pontuação: {st.session_state.score}/5 ⭐</div>', unsafe_allow_html=True)
st.markdown(f'<div class="msg-left">{q["contexto"]}<br>{q["tabela"]}</div>', unsafe_allow_html=True)

if st.session_state.resposta_dada is None:
    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Usar a Média", use_container_width=True):
            st.session_state.resposta_dada = "média"
            st.rerun()
    with col2:
        if st.button("Usar a Mediana", use_container_width=True):
            st.session_state.resposta_dada = "mediana"
            st.rerun()
else:
    st.markdown(f'<div class="msg-right"><b>Você:</b> Escolhi usar a {st.session_state.resposta_dada.capitalize()}!</div><div class="clearfix"></div>', unsafe_allow_html=True)
    
    if st.session_state.resposta_dada == q["certa"]:
        # Marcar resposta correta e incrementar score
        if st.session_state.indice_pergunta not in st.session_state.respostas:
            st.session_state.score += 1
            st.session_state.respostas[st.session_state.indice_pergunta] = "correto"
        
        st.markdown(f'<div class="feedback-box-correct">{q["fb_sucesso"]}</div>', unsafe_allow_html=True)
        st.write("")
        st.info(f"✅ +1 ponto! Score atual: {st.session_state.score}/5")
        st.write("")
        
        if st.session_state.indice_pergunta < 4:
            if st.button("➡️ Ir para a Próxima Pergunta", type="primary", use_container_width=True):
                st.session_state.indice_pergunta += 1
                st.session_state.resposta_dada = None
                st.rerun()
        else:
            # Mostrar resultado final
            st.success("🎉 Você concluiu a Fase 1!")
            st.write("")
            
            # Análise de desempenho
            percentual = (st.session_state.score / 5) * 100
            
            if st.session_state.score == 5:
                st.markdown(f'<div style="background-color: #d4edda; color: #155724; padding: 20px; border-radius: 10px; border-left: 5px solid #28a745; margin: 20px 0;">' + 
                           f'<h3>🏆 Desempenho Extraordinário!</h3>' +
                           f'<p><b>Resultado Final: {st.session_state.score}/5 pontos ({percentual:.0f}%)</b></p>' +
                           f'<p>Você domina perfeitamente os conceitos de Média e Mediana! Pronto para desafios maiores?</p>' +
                           f'</div>', unsafe_allow_html=True)
            elif st.session_state.score >= 3:
                st.markdown(f'<div style="background-color: #cfe2ff; color: #084298; padding: 20px; border-radius: 10px; border-left: 5px solid #0d6efd; margin: 20px 0;">' +
                           f'<h3>👍 Bom Desempenho!</h3>' +
                           f'<p><b>Resultado Final: {st.session_state.score}/5 pontos ({percentual:.0f}%)</b></p>' +
                           f'<p>Você tem uma boa compreensão! Revise os conceitos para consolidar ainda mais.</p>' +
                           f'</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background-color: #f8d7da; color: #721c24; padding: 20px; border-radius: 10px; border-left: 5px solid #dc3545; margin: 20px 0;">' +
                           f'<h3>📚 Continue Estudando</h3>' +
                           f'<p><b>Resultado Final: {st.session_state.score}/5 pontos ({percentual:.0f}%)</b></p>' +
                           f'<p>Você pode melhorar! Revise os conceitos de Média e Mediana e tente novamente.</p>' +
                           f'</div>', unsafe_allow_html=True)
            
            st.write("")
            st.button("🏁 Avançar para a Fase 2: Cafeteria", type="primary", use_container_width=True)
    else:
        # Resposta incorreta - não avança
        if st.session_state.indice_pergunta not in st.session_state.respostas:
            st.session_state.respostas[st.session_state.indice_pergunta] = "incorreto"
        
        st.markdown(f'<div class="feedback-box-incorrect">{q["fb_erro"]}</div>', unsafe_allow_html=True)
        st.write("")
        st.warning("❌ Resposta incorreta. Tente novamente!")
        st.write("")
        if st.button("🔄 Tentar Novamente", use_container_width=True):
            st.session_state.resposta_dada = None
            st.rerun()