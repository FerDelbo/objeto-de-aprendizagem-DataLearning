import streamlit as st
import random

st.set_page_config(page_title="DataLearning App", layout="centered")

banco_fases = {
    1: {
        "app_nome": "WhatsApp",
        "header_bg": "#005e54",  # Verde clássico do WhatsApp
        "header_text": "💬 WhatsApp do Seu Zé — Módulo: Tendência Central",
        "msg_bg_esquerda": "#ffffff",
        "msg_bg_direita": "#e2f9cb",
        "botoes": ["📈 Usar a Média", "📊 Usar a Mediana"],
        "opcoes_chaves": ["média", "mediana"],
        "perguntas": {
            1: {
                "contexto": "🍿 <b>Pipoca do Seu Zé (Carrinho da Praça):</b><br>O Seu Zé quer saber quanto ele fatura em um dia comum para comprar os milhos e saquinhos da semana sem desperdício. Olhando as vendas dele, o que devemos calcular?",
                "tabela": "<table><tr><th>Dia</th><th>Faturamento</th></tr><tr><td>Segunda</td><td>R$ 80,00</td></tr><tr><td>Terça</td><td>R$ 95,00</td></tr><tr><td>Quarta</td><td>R$ 85,00</td></tr><tr><td>⚠️ <b>Quinta (Dia de Show na Praça)</b></td><td><b>R$ 3.500,00</b></td></tr></table>",
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Perfeito!</b> A Mediana ignorou o 'Show na Praça' (Outlier) e mostrou o faturamento real de um dia comum. Se o Seu Zé usasse a média, compraria milho para um batalhão e estragaria tudo!",
                "fb_erro": "<b>✕ Errado!</b> A Média foi puxada para as nuvens pelo dia do show. Ela diria que o Seu Zé ganha quase R$ 1.000 por dia comum! Ele ia falir comprando estoque excessivo."
            },
            2: {
                "contexto": "🥟 <b>Pastelaria da Dona Maria (Feira de Domingo):</b><br>A Dona Maria quer calcular o lucro típico das barracas dela para convidar a irmã para ser sócia. Os dados da última feira foram super parelhos e estáveis:",
                "tabela": "<table><tr><th>Barraca</th><th>Lucro Líquido</th></tr><tr><td>Barraca 1 (Pastel)</td><td>R$ 450,00</td></tr><tr><td>Barraca 2 (Caldo de Cana)</td><td>R$ 410,00</td></tr><tr><td>Barraca 3 (Salgados)</td><td>R$ 430,00</td></tr><tr><td>Barraca 4 (Bebidas)</td><td>R$ 440,00</td></tr></table>",
                "certa": "média",
                "fb_sucesso": "<b>✓ Muito bem!</b> Como o lucro das barracas é equilibrado e não tem nenhuma 'barraca maluca' com valor gigante (Outlier), a Média é o cálculo mais justo para apresentar à nova sócia.",
                "fb_erro": "<b>✕ Incorreto.</b> Quando os dados não têm distorções ou anomalias, a Média é sempre a melhor escolha porque ela calcula a divisão exata considerando o peso real de cada centavo."
            },
            3: {
                "contexto": "🥚 <b>Carro do Ovo (Seu Tião):</b><br>O Seu Tião quer colocar uma gravação nova no alto-falante dizendo quantas dúzias o cliente típico costuma levar para incentivar o pessoal a comprar mais. Qual métrica usar?",
                "tabela": "<table><tr><th>Cliente</th><th>Dúzias Compradas</th></tr><tr><td>Dona Antônia</td><td>1 dúzia</td></tr><tr><td>Seu Raimundo</td><td>2 dúzias</td></tr><tr><td>Dona Francisca</td><td>1 dúzia</td></tr><tr><td>⚠️ <b>Padaria do Bairro (Atacado)</b></td><td><b>100 dúzias</b></td></tr></table>",
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Exato!</b> A compra gigante da padaria é um caso isolado. A Mediana mantém o foco nas donas de casa. O Seu Tião vai anunciar que o cliente típico leva 1 ou 2 dúzias, o que faz sentido!",
                "fb_erro": "<b>✕ Alto-falante Maluco!</b> A Média diria que o cliente típico leva 26 dúzias de ovos! Nenhuma dona de casa vai comprar isso e a gravação do carro ia virar piada no bairro."
            },
            4: {
                "contexto": "🚲 <b>Entregas de Bicicleta (Julio da Marmita):</b><br>O Julio faz entregas de marmitex na comunidade. Ele precisa dizer para os clientes o tempo padrão que leva para a comida chegar quentinha sem que eles reclamem de atraso.",
                "tabela": "<table><tr><th>Entrega</th><th>Tempo Gasto</th></tr><tr><td>Casa 1</td><td>15 minutos</td></tr><tr><td>Casa 2</td><td>18 minutos</td></tr><tr><td>Casa 3</td><td>14 MINUTOS</td></tr><tr><td>⚠️ <b>Casa 4 (Pneu Furou na Subida)</b></td><td><b>90 minutos</b></td></tr></table>",
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Excelente!</b> O pneu furado foi uma fatalidade (Outlier). A Mediana manteve a previsão realista de 15 minutos. O Julio protege a reputação das marmitas dele!",
                "fb_erro": "<b>✕ Cliente com fome!</b> A Média jogaria o tempo de entrega para quase 35 minutos. Os clientes iam achar que demora demais e pediriam no concorrente."
            },
            5: {
                "contexto": "🧼 <b>Dona Cida (Salgados para Festa):</b><br>A Dona Cida faz coxinha e frito por encomenda. Ela quer saber a quantidade típica de salgados que as pessoas encomendam para deixar a massa pré-pronta no congelador.",
                "tabela": "<table><tr><th>Pedido</th><th>Quantidade de Salgados</th></tr><tr><td>Festa 1 (Aniversário infantil)</td><td>200 unidades</td></tr><tr><td>Festa 2 (Reunião de amigos)</td><td>150 unidades</td></tr><tr><td>Festa 3 (Chá de bebê)</td><td>250 unidades</td></tr><tr><td>Festa 4 (Batizado)</td><td>200 unidades</td></tr></table>",
                "certa": "média",
                "fb_sucesso": "<b>✓ Sensacional!</b> Como os pedidos de salgados das festas de bairro mantêm sempre o mesmo padrão (entre 150 e 250), a Média resume perfeitamente a quantidade diária de produção.",
                "fb_erro": "<b>✕ Não precisa de medo!</b> Você escolheu a Mediana, mas lembre-se: se a distribuição é uniforme e os dados são comportados, a Média é estatisticamente o indicador mais rico."
            }
        }
    },
    2: {
        "app_nome": "E-mail de Negócios",
        "header_bg": "#4285f4",  # Azul corporativo (Estilo Gmail)
        "header_text": "📩 Caixa de Entrada — Módulo: Séries Temporais (Visualização)",
        "msg_bg_esquerda": "#f1f3f4", # Cinza claro de e-mail
        "msg_bg_direita": "#e8f0fe",
        "botoes": ["🍕 Usar Gráfico de Pizza", "📈 Usar Gráfico de Linhas"],
        "opcoes_chaves": ["pizza", "linhas"],
        "perguntas": {
            1: {
                "contexto": "☕ <b>Carrinho de Café do Calçadão:</b><br>E-mail recebido do seu fornecedor: 'Preciso descobrir os meses de pico de vendas para entender quando o inverno faz o consumo disparar e programar as entregas de grãos.' Para ver a variação do tempo, qual gráfico anexar?",
                "tabela": "<table><tr><th>Mês</th><th>Copos de Café Vendidos</th></tr><tr><td>Janeiro (Verão)</td><td>1.200 copos</td></tr><tr><td>Julho (Inverno)</td><td>5.800 copos</td></tr><tr><td>Dezembro (Verão)</td><td>1.500 copos</td></tr></table>",
                "certa": "linhas",
                "fb_sucesso": "<b>✓ Excelente!</b> O Gráfico de Linhas conecta os meses em ordem, expondo perfeitamente a subida e a descida da <b>Sazonalidade</b> causada pelo frio.",
                "fb_erro": "<b>✕ Incorreto!</b> O Gráfico de Pizza corta os meses em pedaços isolados, o que impede o fornecedor de enxergar a linha do tempo e a tendência de crescimento das estações."
            }
        }
    }
}

if "fase_atual" not in st.session_state:
    st.session_state.fase_atual = 1

def inicializar_fase():
    fase_info = banco_fases[st.session_state.fase_atual]
    lista_indices = list(fase_info["perguntas"].keys())
    random.shuffle(lista_indices)
    
    st.session_state.ordem_perguntas = lista_indices
    st.session_state.indice_pergunta = 0
    st.session_state.score = 0
    st.session_state.respostas_computadas = {} # Evita ganhar pontos repetidos ao errar e tentar de novo
    st.session_state.resposta_dada = None
    st.session_state.exibir_transicao = False

if "ordem_perguntas" not in st.session_state or "indice_pergunta" not in st.session_state:
    inicializar_fase()
if "exibir_transicao" not in st.session_state:
    st.session_state.exibir_transicao = False

fase_info = banco_fases[st.session_state.fase_atual]
id_pergunta_atual = st.session_state.ordem_perguntas[st.session_state.indice_pergunta]
q = fase_info["perguntas"][id_pergunta_atual]

st.markdown(f"""
    <style>
    .stApp {{ background-color: #efeae2; }}
    .chat-header {{
        background-color: {fase_info['header_bg']}; color: white; padding: 15px;
        font-weight: bold; border-radius: 10px 10px 0px 0px;
        text-align: center; font-size: 16px; margin-bottom: 10px;
    }}
    .msg-left {{
        background-color: {fase_info['msg_bg_esquerda']}; padding: 12px; border-radius: 0px 15px 15px 15px;
        margin: 8px 0px; max-width: 85%; text-align: left; color: #000000;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    .msg-right {{
        background-color: {fase_info['msg_bg_direita']}; padding: 12px; border-radius: 15px 0px 15px 15px;
        margin: 8px 0px; float: right; min-width: 40%; max-width: 85%;
        text-align: left; color: #000000; box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    .feedback-box-correct {{
        background-color: #d4edda; color: #155724; padding: 15px;
        border-radius: 10px; border-left: 5px solid #28a745; margin-top: 20px; clear: both;
    }}
    .feedback-box-incorrect {{
        background-color: #f8d7da; color: #721c24; padding: 15px;
        border-radius: 10px; border-left: 5px solid #dc3545; margin-top: 20px; clear: both;
    }}
    .clearfix {{ clear: both; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
    th, td {{ border: 1px solid #ddd; padding: 6px; text-align: left; font-size: 13px; }}
    th {{ background-color: #f2f2f2; }}
    
    /* Botão Laranja de Mudança de Ambiente (Inspirado no projeto referência) */
    div.stButton > button.btn-laranja {{
        background-color: #ff9800 !important; color: white !important;
        font-weight: bold !important; font-size: 16px !important;
        border-radius: 10px !important; border: none !important; padding: 12px !important;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }}
    </style>
""", unsafe_allow_html=True)

if st.session_state.exibir_transicao:
    st.markdown('<div class="chat-header">🏁 MÓDULO CONCLUÍDO!</div>', unsafe_allow_html=True)
    st.success(f"🏆 Excelente! Você ajudou os pequenos comércios no {fase_info['app_nome']}!")
    
    prox_fase = st.session_state.fase_atual + 1
    nome_prox_app = banco_fases[prox_fase]["app_nome"]
    
    st.write(f"Você provou que entende de Média e Mediana! Agora, novos desafios chegaram. Você mudará do **{fase_info['app_nome']}** e precisará gerenciar a empresa analisando relatórios visuais no **{nome_prox_app}**.")
    
    st.write("")
    if st.button(f"➡ Próxima Fase: Abrir o {nome_prox_app}", key="btn_laranja", use_container_width=True):
        st.session_state.fase_atual += 1
        inicializar_fase()
        st.rerun()

else:
    st.markdown(f'<div class="chat-header">📱 {fase_info["header_text"]} | Desafio {st.session_state.indice_pergunta + 1} de {len(st.session_state.ordem_perguntas)} | Placar: {st.session_state.score} ⭐</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="msg-left">{q["contexto"]}<br>{q["tabela"]}</div>', unsafe_allow_html=True)

    if st.session_state.resposta_dada is None:
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(fase_info["botoes"][0], use_container_width=True):
                st.session_state.resposta_dada = fase_info["opcoes_chaves"][0]
                st.rerun()
        with col2:
            if st.button(fase_info["botoes"][1], use_container_width=True):
                st.session_state.resposta_dada = fase_info["opcoes_chaves"][1]
                st.rerun()
    else:
        label_escolhido = fase_info["botoes"][0] if st.session_state.resposta_dada == fase_info["opcoes_chaves"][0] else fase_info["botoes"][1]
        st.markdown(f'<div class="msg-right"><b>Você:</b> Escolhi {label_escolhido}!</div><div class="clearfix"></div>', unsafe_allow_html=True)
        
        if st.session_state.resposta_dada == q["certa"]:
            if st.session_state.indice_pergunta not in st.session_state.respostas_computadas:
                st.session_state.score += 1
                st.session_state.respostas_computadas[st.session_state.indice_pergunta] = "correto"
                
            st.markdown(f'<div class="feedback-box-correct">{q["fb_sucesso"]}</div>', unsafe_allow_html=True)
            st.write("")
            
            if st.session_state.indice_pergunta < (len(st.session_state.ordem_perguntas) - 1):
                if st.button("➡️ Próximo Pequeno Negócio", type="primary", use_container_width=True):
                    st.session_state.indice_pergunta += 1
                    st.session_state.resposta_dada = None
                    st.rerun()
            else:
                if st.session_state.fase_atual < len(banco_fases):
                    st.session_state.exibir_transicao = True
                    st.rerun()
                else:
                    st.balloons()
                    st.success("🏆 FIM DO SIMULADOR! Você ajudou o comércio popular a prosperar usando a Ciência de Dados!")
        else:
            if st.session_state.indice_pergunta not in st.session_state.respostas_computadas:
                st.session_state.respostas_computadas[st.session_state.indice_pergunta] = "incorreto"
                
            st.markdown(f'<div class="feedback-box-incorrect">{q["fb_erro"]}</div>', unsafe_allow_html=True)
            st.write("")
            if st.button("🔄 Analisar os dados novamente", use_container_width=True):
                st.session_state.resposta_dada = None
                st.rerun()