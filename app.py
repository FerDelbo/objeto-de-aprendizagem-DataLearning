import streamlit as st
import random

st.set_page_config(page_title="DataLearning App", layout="centered")

PERGUNTAS_POR_SESSAO = 5

# ==========================================================================
# BANCO DE FASES (PRÁTICA)
# Cenário 1: Interpretação Estatística -> Planilha (Média x Mediana)
# Cenário 2: Visualização de Dados -> Dashboard de Analytics (Linhas x Barras x Histograma)
# Cenário 3: Tomada de Decisão -> Dashboard Financeiro (decisão variável)
# ==========================================================================

banco_fases = {
    1: {
        "tipo": "planilha",
        "app_nome": "Planilha de Vendas",
        "header_text": "📊 Planilha do Pequeno Negócio — Módulo: Tendência Central",
        "botoes": ["📈 Usar a Média", "📊 Usar a Mediana"],
        "opcoes_chaves": ["média", "mediana"],
        "perguntas": {
            1: {
                "contexto": "🍿 <b>Pipoca do Seu Zé (Carrinho da Praça):</b><br>O Seu Zé quer saber quanto ele fatura em um dia comum para comprar os milhos e saquinhos da semana sem desperdício.",
                "tabela": "<table><tr><th>Dia</th><th>Faturamento</th></tr><tr><td>Segunda</td><td>R$ 80,00</td></tr><tr><td>Terça</td><td>R$ 95,00</td></tr><tr><td>Quarta</td><td>R$ 85,00</td></tr><tr><td><b>Quinta (Dia de Show na Praça)</b></td><td><b>R$ 3.500,00</b></td></tr></table>",
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Perfeito!</b> A Mediana ignorou o 'Show na Praça' (Outlier) e mostrou o faturamento real de um dia comum.",
                "fb_erro": "<b>✕ Errado!</b> A Média foi puxada para as nuvens pelo dia do show. Ele ia falir comprando estoque excessivo."
            },
            2: {
                "contexto": "🥟 <b>Pastelaria da Dona Maria (Feira de Domingo):</b><br>A Dona Maria quer calcular o lucro típico das barracas para convidar a irmã como sócia. Os dados foram super parelhos:",
                "tabela": "<table><tr><th>Barraca</th><th>Lucro Líquido</th></tr><tr><td>Barraca 1 (Pastel)</td><td>R$ 450,00</td></tr><tr><td>Barraca 2 (Caldo de Cana)</td><td>R$ 410,00</td></tr><tr><td>Barraca 3 (Salgados)</td><td>R$ 430,00</td></tr><tr><td>Barraca 4 (Bebidas)</td><td>R$ 440,00</td></tr></table>",
                "certa": "média",
                "fb_sucesso": "<b>✓ Muito bem!</b> Sem outliers, a Média é o cálculo mais justo para apresentar à nova sócia.",
                "fb_erro": "<b>✕ Incorreto.</b> Quando os dados não têm distorções, a Média é a melhor escolha."
            },
            3: {
                "contexto": "🥚 <b>Carro do Ovo (Seu Tião):</b><br>O Seu Tião quer anunciar quantas dúzias o cliente típico costuma levar. Qual métrica usar?",
                "tabela": "<table><tr><th>Cliente</th><th>Dúzias Compradas</th></tr><tr><td>Dona Antônia</td><td>1 dúzia</td></tr><tr><td>Seu Raimundo</td><td>2 dúzias</td></tr><tr><td>Dona Francisca</td><td>1 dúzia</td></tr><tr><td><b>Padaria do Bairro (Atacado)</b></td><td><b>100 dúzias</b></td></tr></table>",
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Exato!</b> A compra da padaria é um caso isolado. A Mediana mantém o foco nas donas de casa.",
                "fb_erro": "<b>✕ Alto-falante Maluco!</b> A Média diria que o cliente típico leva 26 dúzias de ovos!"
            },
            4: {
                "contexto": "🚲 <b>Entregas de Bicicleta (Julio da Marmita):</b><br>O Julio precisa dizer aos clientes o tempo padrão de entrega sem reclamação de atraso.",
                "tabela": "<table><tr><th>Entrega</th><th>Tempo Gasto</th></tr><tr><td>Casa 1</td><td>15 minutos</td></tr><tr><td>Casa 2</td><td>18 minutos</td></tr><tr><td>Casa 3</td><td>14 minutos</td></tr><tr><td><b>Casa 4 (Pneu Furou)</b></td><td><b>90 minutos</b></td></tr></table>",
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Excelente!</b> O pneu furado foi uma fatalidade (Outlier). A Mediana manteve a previsão realista.",
                "fb_erro": "<b>✕ Cliente com fome!</b> A Média jogaria o tempo de entrega para quase 35 minutos."
            },
            5: {
                "contexto": "🧁 <b>Dona Cida (Salgados para Festa):</b><br>Ela quer saber a quantidade típica de salgados encomendados para deixar massa pré-pronta.",
                "tabela": "<table><tr><th>Pedido</th><th>Quantidade</th></tr><tr><td>Festa 1</td><td>200 unidades</td></tr><tr><td>Festa 2</td><td>150 unidades</td></tr><tr><td>Festa 3</td><td>250 unidades</td></tr><tr><td>Festa 4</td><td>200 unidades</td></tr></table>",
                "certa": "média",
                "fb_sucesso": "<b>✓ Sensacional!</b> Sem outliers, a Média resume perfeitamente a quantidade diária de produção.",
                "fb_erro": "<b>✕ Não precisa de medo!</b> Quando os dados são uniformes, a Média é o indicador mais rico."
            },
            6: {
                "contexto": "🧃 <b>Suco Natural da Lia (Quiosque de Praia):</b><br>A Lia quer saber o consumo típico de copos por dia, mas um feriado prolongado bombou as vendas.",
                "tabela": "<table><tr><th>Dia</th><th>Copos Vendidos</th></tr><tr><td>Seg</td><td>40</td></tr><tr><td>Ter</td><td>38</td></tr><tr><td>Qua</td><td>42</td></tr><tr><td><b>Feriado</b></td><td><b>500</b></td></tr></table>",
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Isso!</b> O feriado é um Outlier. A Mediana mostra o consumo real de um dia comum.",
                "fb_erro": "<b>✕ Cuidado!</b> A Média ficaria inflada pelo feriado e faria a Lia comprar fruta demais."
            },
            7: {
                "contexto": "🧹 <b>Diarista Joana (Faxinas por Empreitada):</b><br>A Joana quer saber o valor típico cobrado por faxina para montar uma tabela de preços nova.",
                "tabela": "<table><tr><th>Cliente</th><th>Valor Cobrado</th></tr><tr><td>Casa 1</td><td>R$ 120,00</td></tr><tr><td>Casa 2</td><td>R$ 110,00</td></tr><tr><td>Casa 3</td><td>R$ 130,00</td></tr><tr><td>Casa 4</td><td>R$ 115,00</td></tr></table>",
                "certa": "média",
                "fb_sucesso": "<b>✓ Muito bem!</b> Valores parecidos, sem distorções — a Média representa bem o preço de mercado.",
                "fb_erro": "<b>✕ Incorreto.</b> Não há outliers aqui, então a Média já é a métrica mais precisa."
            },
            8: {
                "contexto": "🔧 <b>Borracharia do Edson:</b><br>O Edson quer saber o número típico de pneus trocados por dia, mas um caminhão de frota trocou todos os 18 pneus de uma vez.",
                "tabela": "<table><tr><th>Dia</th><th>Pneus Trocados</th></tr><tr><td>Seg</td><td>4</td></tr><tr><td>Ter</td><td>3</td></tr><tr><td>Qua</td><td>5</td></tr><tr><td><b>Quinta (Frota)</b></td><td><b>18</b></td></tr></table>",
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Correto!</b> O caminhão de frota é um Outlier isolado. A Mediana reflete o movimento comum da borracharia.",
                "fb_erro": "<b>✕ Errado!</b> A Média ficaria distorcida pela frota, fazendo o Edson achar que vende muito mais que o normal."
            },
            9: {
                "contexto": "🍰 <b>Confeitaria da Sônia:</b><br>A Sônia quer saber o valor típico dos bolos vendidos no mês para montar um cardápio de preços fixos.",
                "tabela": "<table><tr><th>Bolo</th><th>Valor</th></tr><tr><td>Chocolate</td><td>R$ 60,00</td></tr><tr><td>Cenoura</td><td>R$ 55,00</td></tr><tr><td>Red Velvet</td><td>R$ 65,00</td></tr><tr><td>Brigadeiro</td><td>R$ 58,00</td></tr></table>",
                "certa": "média",
                "fb_sucesso": "<b>✓ Perfeito!</b> Valores equilibrados — a Média representa bem o ticket médio dos bolos.",
                "fb_erro": "<b>✕ Quase lá!</b> Sem outliers, a Média já é suficiente e mais precisa que a Mediana aqui."
            },
            10: {
                "contexto": "🛵 <b>Motoboy Renan (Entregas por App):</b><br>O Renan quer saber quantas entregas faz num dia comum, mas a Black Friday bombou os pedidos.",
                "tabela": "<table><tr><th>Dia</th><th>Entregas</th></tr><tr><td>Seg</td><td>12</td></tr><tr><td>Ter</td><td>14</td></tr><tr><td>Qua</td><td>13</td></tr><tr><td><b>Black Friday</b></td><td><b>80</b></td></tr></table>",
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Isso!</b> A Black Friday é um pico isolado (Outlier). A Mediana mostra a rotina real do Renan.",
                "fb_erro": "<b>✕ Errado!</b> A Média super-estimaria o número de entregas diárias por causa de um único dia fora da curva."
            },
            11: {
                "contexto": "🐶 <b>Pet Shop da Carol (Banho e Tosa):</b><br>A Carol quer saber o número típico de atendimentos por dia para organizar a agenda dos tosadores.",
                "tabela": "<table><tr><th>Dia</th><th>Atendimentos</th></tr><tr><td>Seg</td><td>8</td></tr><tr><td>Ter</td><td>9</td></tr><tr><td>Qua</td><td>7</td></tr><tr><td>Qui</td><td>8</td></tr></table>",
                "certa": "média",
                "fb_sucesso": "<b>✓ Muito bem!</b> Atendimentos estáveis e parecidos — a Média representa bem a rotina do Pet Shop.",
                "fb_erro": "<b>✕ Incorreto.</b> Não há valores extremos aqui, então a Média já é a métrica certa."
            },
            12: {
                "contexto": "📦 <b>Loja Online da Patrícia:</b><br>A Patrícia quer saber o valor típico dos pedidos do mês, mas um cliente comprou em grande quantidade para revenda.",
                "tabela": "<table><tr><th>Pedido</th><th>Valor</th></tr><tr><td>Pedido 1</td><td>R$ 90,00</td></tr><tr><td>Pedido 2</td><td>R$ 110,00</td></tr><tr><td>Pedido 3</td><td>R$ 95,00</td></tr><tr><td><b>Revendedor</b></td><td><b>R$ 4.800,00</b></td></tr></table>",
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Correto!</b> O pedido do revendedor é um Outlier. A Mediana mostra o ticket real do cliente comum.",
                "fb_erro": "<b>✕ Errado!</b> A Média ficaria inflada pelo pedido gigante, escondendo o comportamento real dos clientes."
            },
            13: {
                "contexto": "🪴 <b>Viveiro de Plantas do Seu Nonato:</b><br>Ele quer saber a quantidade típica de mudas vendidas por dia para planejar a produção.",
                "tabela": "<table><tr><th>Dia</th><th>Mudas Vendidas</th></tr><tr><td>Seg</td><td>20</td></tr><tr><td>Ter</td><td>22</td></tr><tr><td>Qua</td><td>19</td></tr><tr><td>Qui</td><td>21</td></tr></table>",
                "certa": "média",
                "fb_sucesso": "<b>✓ Isso!</b> Vendas constantes e parecidas — a Média reflete bem a produção necessária.",
                "fb_erro": "<b>✕ Incorreto.</b> Sem outliers, a Média já é a métrica mais informativa aqui."
            },
            14: {
                "contexto": "🎂 <b>Buffet Infantil da Renata:</b><br>Ela quer saber o número típico de convidados por festa, mas uma festa de 15 anos teve um número bem fora do padrão.",
                "tabela": "<table><tr><th>Festa</th><th>Convidados</th></tr><tr><td>Festa 1</td><td>25</td></tr><tr><td>Festa 2</td><td>30</td></tr><tr><td>Festa 3</td><td>28</td></tr><tr><td><b>Festa de 15 Anos</b></td><td><b>300</b></td></tr></table>",
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Perfeito!</b> A festa de 15 anos é um Outlier. A Mediana representa o tamanho comum das festas.",
                "fb_erro": "<b>✕ Errado!</b> A Média ficaria inflada pela festa grande, distorcendo o planejamento de buffet."
            },
            15: {
                "contexto": "🧴 <b>Loja de Cosméticos da Bianca:</b><br>Ela quer saber o valor típico de compra para criar um programa de fidelidade justo.",
                "tabela": "<table><tr><th>Cliente</th><th>Valor Gasto</th></tr><tr><td>Cliente 1</td><td>R$ 70,00</td></tr><tr><td>Cliente 2</td><td>R$ 75,00</td></tr><tr><td>Cliente 3</td><td>R$ 68,00</td></tr><tr><td>Cliente 4</td><td>R$ 72,00</td></tr></table>",
                "certa": "média",
                "fb_sucesso": "<b>✓ Muito bem!</b> Gastos parecidos — a Média representa de forma justa o ticket médio dos clientes.",
                "fb_erro": "<b>✕ Incorreto.</b> Sem outliers, a Média já é a métrica mais precisa para o programa de fidelidade."
            }
        }
    },
    2: {
        "tipo": "dashboard_analytics",
        "app_nome": "Dashboard de Vendas",
        "header_text": "📈 Painel de Vendas — Módulo: Visualização de Dados",
        "perguntas": {
            1: {
                "contexto": "☕ <b>Carrinho de Café do Calçadão:</b><br>O fornecedor quer entender como o consumo de café varia ao longo dos meses para programar entregas.",
                "tabela": "<table><tr><th>Mês</th><th>Copos Vendidos</th></tr><tr><td>Janeiro</td><td>1.200</td></tr><tr><td>Abril</td><td>2.100</td></tr><tr><td>Julho</td><td>5.800</td></tr><tr><td>Outubro</td><td>2.400</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "linhas",
                "fb_sucesso": "<b>✓ Excelente!</b> O Gráfico de Linhas revela a sazonalidade causada pelo frio. Ideal para evolução no tempo.",
                "fb_erro": "<b>✕ Incorreto!</b> Para séries temporais (mês a mês), o Gráfico de Linhas comunica melhor a tendência contínua."
            },
            2: {
                "contexto": "👕 <b>Loja de Roupas da Bia:</b><br>A Bia quer saber qual categoria de produto vendeu mais no mês para decidir o que repor.",
                "tabela": "<table><tr><th>Categoria</th><th>Unidades</th></tr><tr><td>Camisetas</td><td>120</td></tr><tr><td>Calças</td><td>45</td></tr><tr><td>Vestidos</td><td>80</td></tr><tr><td>Acessórios</td><td>30</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "barras",
                "fb_sucesso": "<b>✓ Muito bem!</b> O Gráfico de Barras compara categorias lado a lado, mostrando Camisetas como líder.",
                "fb_erro": "<b>✕ Incorreto!</b> Categorias distintas (não sequenciais no tempo) são melhor comparadas com Barras."
            },
            3: {
                "contexto": "🍦 <b>Sorveteria do Seu Aurélio:</b><br>Ele quer visualizar como o faturamento se comportou durante a semana de calor.",
                "tabela": "<table><tr><th>Dia</th><th>Faturamento</th></tr><tr><td>Segunda</td><td>R$ 200,00</td></tr><tr><td>Terça</td><td>R$ 350,00</td></tr><tr><td>Quarta</td><td>R$ 500,00</td></tr><tr><td>Quinta</td><td>R$ 800,00</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "linhas",
                "fb_sucesso": "<b>✓ Isso!</b> O Gráfico de Linhas mostra a tendência de crescimento dia após dia com clareza.",
                "fb_erro": "<b>✕ Quase lá!</b> Para detectar uma escalada contínua, Linhas comunica melhor que Barras ou Histograma."
            },
            4: {
                "contexto": "🌮 <b>Food Truck do Marcos:</b><br>Ele quer comparar o faturamento entre os 4 pontos de venda diferentes que testou no mês.",
                "tabela": "<table><tr><th>Ponto</th><th>Faturamento</th></tr><tr><td>Praça Central</td><td>R$ 4.200,00</td></tr><tr><td>Universidade</td><td>R$ 6.100,00</td></tr><tr><td>Parque</td><td>R$ 2.800,00</td></tr><tr><td>Zona Industrial</td><td>R$ 5.300,00</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "barras",
                "fb_sucesso": "<b>✓ Perfeito!</b> O Gráfico de Barras compara pontos de venda lado a lado — Universidade é o mais rentável.",
                "fb_erro": "<b>✕ Não é o ideal!</b> Pontos de venda são categorias, não uma sequência no tempo — Barras é mais clara aqui."
            },
            5: {
                "contexto": "🌸 <b>Floricultura da Dona Eunice:</b><br>Ela quer entender como as vendas se comportaram nas últimas 4 semanas antes do Dia das Mães.",
                "tabela": "<table><tr><th>Semana</th><th>Buquês Vendidos</th></tr><tr><td>Semana 1</td><td>20</td></tr><tr><td>Semana 2</td><td>35</td></tr><tr><td>Semana 3</td><td>60</td></tr><tr><td>Semana 4</td><td>95</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "linhas",
                "fb_sucesso": "<b>✓ Ótimo!</b> O Gráfico de Linhas revela a aceleração semana a semana.",
                "fb_erro": "<b>✕ Cuidado!</b> Para perceber uma tendência de aceleração contínua, Linhas é a escolha certa."
            },
            6: {
                "contexto": "🥖 <b>Padaria do Seu Hélio:</b><br>Ele quer entender como o valor das compras dos clientes se distribui — quantos gastam pouco, médio ou muito.",
                "tabela": "<table><tr><th>Faixa de Gasto</th><th>Nº de Clientes</th></tr><tr><td>R$ 0–10</td><td>40</td></tr><tr><td>R$ 10–20</td><td>65</td></tr><tr><td>R$ 20–30</td><td>20</td></tr><tr><td>R$ 30+</td><td>5</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "histograma",
                "fb_sucesso": "<b>✓ Excelente!</b> O Histograma mostra a distribuição de frequências dos gastos, revelando o padrão de consumo.",
                "fb_erro": "<b>✕ Incorreto!</b> Quando o objetivo é ver como os valores se distribuem em faixas, o Histograma é o gráfico certo."
            },
            7: {
                "contexto": "🚗 <b>Lava-Rápido do Seu Ailton:</b><br>Ele quer entender a distribuição do tempo de lavagem dos carros para organizar a fila de espera.",
                "tabela": "<table><tr><th>Faixa de Tempo</th><th>Nº de Carros</th></tr><tr><td>10–15 min</td><td>30</td></tr><tr><td>15–20 min</td><td>50</td></tr><tr><td>20–25 min</td><td>15</td></tr><tr><td>25+ min</td><td>5</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "histograma",
                "fb_sucesso": "<b>✓ Isso!</b> O Histograma revela a distribuição dos tempos de lavagem, mostrando que a maioria fica entre 15 e 20 minutos.",
                "fb_erro": "<b>✕ Errado!</b> Para entender como um valor se distribui em faixas (não é tempo nem categoria simples), use Histograma."
            },
            8: {
                "contexto": "🛍️ <b>Brechó da Camila:</b><br>Ela quer comparar quantas peças de cada tipo (camisas, calças, vestidos, casacos) foram vendidas no mês.",
                "tabela": "<table><tr><th>Tipo de Peça</th><th>Vendidas</th></tr><tr><td>Camisas</td><td>60</td></tr><tr><td>Calças</td><td>40</td></tr><tr><td>Vestidos</td><td>75</td></tr><tr><td>Casacos</td><td>20</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "barras",
                "fb_sucesso": "<b>✓ Muito bem!</b> O Gráfico de Barras compara as categorias de peças de forma direta e clara.",
                "fb_erro": "<b>✕ Incorreto!</b> Tipos de peça são categorias distintas — Barras comunica melhor que Linhas ou Histograma."
            },
            9: {
                "contexto": "🏋️ <b>Academia da Fernanda:</b><br>Ela quer entender como as idades dos alunos se distribuem para planejar novas turmas.",
                "tabela": "<table><tr><th>Faixa de Idade</th><th>Nº de Alunos</th></tr><tr><td>15–25</td><td>30</td></tr><tr><td>26–35</td><td>55</td></tr><tr><td>36–45</td><td>25</td></tr><tr><td>46+</td><td>10</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "histograma",
                "fb_sucesso": "<b>✓ Perfeito!</b> O Histograma mostra a distribuição de idades, ajudando a planejar turmas para o público de 26–35 anos.",
                "fb_erro": "<b>✕ Errado!</b> Para visualizar a distribuição de uma variável contínua em faixas, o Histograma é ideal."
            },
            10: {
                "contexto": "📱 <b>Assistência Técnica do Diego:</b><br>Ele quer acompanhar a evolução do número de aparelhos reparados nos últimos 6 meses.",
                "tabela": "<table><tr><th>Mês</th><th>Reparos</th></tr><tr><td>Jan</td><td>30</td></tr><tr><td>Mar</td><td>45</td></tr><tr><td>Mai</td><td>70</td></tr><tr><td>Jun</td><td>90</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "linhas",
                "fb_sucesso": "<b>✓ Isso!</b> O Gráfico de Linhas mostra claramente o crescimento contínuo dos reparos mês a mês.",
                "fb_erro": "<b>✕ Cuidado!</b> Para evolução temporal, Linhas é sempre a escolha mais clara."
            },
            11: {
                "contexto": "🧺 <b>Lavanderia da Dona Iracema:</b><br>Ela quer entender como o peso das sacolas de roupa se distribui entre os clientes.",
                "tabela": "<table><tr><th>Faixa de Peso</th><th>Nº de Sacolas</th></tr><tr><td>0–3 kg</td><td>20</td></tr><tr><td>3–6 kg</td><td>50</td></tr><tr><td>6–9 kg</td><td>25</td></tr><tr><td>9+ kg</td><td>5</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "histograma",
                "fb_sucesso": "<b>✓ Muito bem!</b> O Histograma revela que a maioria das sacolas pesa entre 3 e 6 kg, ajudando a precificar melhor.",
                "fb_erro": "<b>✕ Incorreto!</b> Faixas de peso são uma distribuição contínua — o Histograma é o gráfico certo aqui."
            },
            12: {
                "contexto": "🎮 <b>Locadora de Videogame do Rafa:</b><br>Ele quer comparar quantas vezes cada console foi alugado no mês.",
                "tabela": "<table><tr><th>Console</th><th>Locações</th></tr><tr><td>PlayStation</td><td>90</td></tr><tr><td>Xbox</td><td>40</td></tr><tr><td>Switch</td><td>110</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "barras",
                "fb_sucesso": "<b>✓ Excelente!</b> O Gráfico de Barras compara os consoles de forma direta — Switch é o mais alugado.",
                "fb_erro": "<b>✕ Incorreto!</b> Consoles são categorias, não uma evolução no tempo — Barras é a escolha certa."
            },
            13: {
                "contexto": "🧁 <b>Doceria da Marta:</b><br>Ela quer acompanhar como o faturamento evoluiu ao longo dos últimos 5 meses.",
                "tabela": "<table><tr><th>Mês</th><th>Faturamento</th></tr><tr><td>Fev</td><td>R$ 1.200,00</td></tr><tr><td>Mar</td><td>R$ 1.500,00</td></tr><tr><td>Abr</td><td>R$ 1.300,00</td></tr><tr><td>Mai</td><td>R$ 1.800,00</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "linhas",
                "fb_sucesso": "<b>✓ Isso!</b> O Gráfico de Linhas mostra a evolução do faturamento mês a mês com clareza.",
                "fb_erro": "<b>✕ Errado!</b> Para ver a evolução contínua no tempo, Linhas é sempre mais indicado que Barras."
            },
            14: {
                "contexto": "🚲 <b>Bicicletaria do Seu Geraldo:</b><br>Ele quer entender como o valor dos reparos se distribui entre os clientes para criar pacotes de serviço.",
                "tabela": "<table><tr><th>Faixa de Valor</th><th>Nº de Reparos</th></tr><tr><td>R$ 0–30</td><td>35</td></tr><tr><td>R$ 30–60</td><td>50</td></tr><tr><td>R$ 60–90</td><td>10</td></tr><tr><td>R$ 90+</td><td>5</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "histograma",
                "fb_sucesso": "<b>✓ Perfeito!</b> O Histograma mostra que a maioria dos reparos custa entre R$ 30 e R$ 60, ideal para criar um pacote popular.",
                "fb_erro": "<b>✕ Incorreto!</b> Para visualizar a distribuição de valores em faixas, o Histograma é a ferramenta certa."
            },
            15: {
                "contexto": "🍕 <b>Pizzaria do Seu Vitor:</b><br>Ele quer comparar quantas pizzas de cada sabor foram vendidas no fim de semana.",
                "tabela": "<table><tr><th>Sabor</th><th>Vendidas</th></tr><tr><td>Calabresa</td><td>85</td></tr><tr><td>Margherita</td><td>50</td></tr><tr><td>Frango com Catupiry</td><td>95</td></tr></table>",
                "opcoes": ["linhas", "barras", "histograma"],
                "certa": "barras",
                "fb_sucesso": "<b>✓ Muito bem!</b> O Gráfico de Barras compara os sabores lado a lado — Frango com Catupiry é o campeão.",
                "fb_erro": "<b>✕ Incorreto!</b> Sabores são categorias distintas — Barras comunica melhor que Linhas ou Histograma."
            }
        }
    },
    3: {
        "tipo": "dashboard_financeiro",
        "app_nome": "Dashboard Financeiro",
        "header_text": "💼 Painel Financeiro — Módulo: Tomada de Decisão",
        "perguntas": {
            1: {
                "contexto": "👕 <b>Loja de Roupas da Bia:</b><br>Um cliente revendedor fez uma compra gigante essa semana. Qual decisão tomar para a próxima reposição de estoque?",
                "tabela": "<table><tr><th>Cliente</th><th>Valor</th></tr><tr><td>Cliente 1</td><td>R$ 80,00</td></tr><tr><td>Cliente 2</td><td>R$ 95,00</td></tr><tr><td>Cliente 3</td><td>R$ 85,00</td></tr><tr><td>⚠️ <b>Loja Revendedora</b></td><td><b>R$ 3.500,00</b></td></tr></table>",
                "botoes": ["📦 Repor baseado na Mediana", "📦 Repor baseado na Média"],
                "opcoes_chaves": ["mediana", "média"],
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> A Mediana mitigou o Outlier e protegeu o capital de giro do negócio.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> A Média distorcida gera compras excessivas, resultando em Prejuízo Financeiro."
            },
            2: {
                "contexto": "☕ <b>Carrinho de Café do Calçadão:</b><br>O relatório mostra um pico claro de vendas no inverno. Qual decisão tomar sobre o estoque de grãos?",
                "tabela": "<table><tr><th>Período</th><th>Tendência</th></tr><tr><td>Jan–Jun</td><td>Estável (~1.200 copos)</td></tr><tr><td>Jul–Ago</td><td>📈 Pico de até 5.800 copos</td></tr></table>",
                "botoes": ["📦 Antecipar compra de grãos", "📦 Manter o pedido padrão"],
                "opcoes_chaves": ["antecipar", "manter"],
                "certa": "antecipar",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> A Sazonalidade foi identificada. Antecipar evita falta de produto no pico.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Ignorar o padrão sazonal é Achismo, e resulta em falta de grãos no pico."
            },
            3: {
                "contexto": "🍦 <b>Sorveteria do Seu Aurélio:</b><br>O gráfico mostra que Chocolate vende muito mais que Pistache. Qual decisão tomar?",
                "tabela": "<table><tr><th>Sabor</th><th>Vendas</th></tr><tr><td>Chocolate</td><td>420 unidades</td></tr><tr><td>Pistache</td><td>35 unidades</td></tr></table>",
                "botoes": ["🍫 Investir mais em Chocolate", "🍫 Investir mais em Pistache"],
                "opcoes_chaves": ["chocolate", "pistache"],
                "certa": "chocolate",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> Investir no produto de maior demanda gera alto faturamento e estoque equilibrado.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Ignorar a Visualização de Dados gera estoque encalhado de Pistache."
            },
            4: {
                "contexto": "🌮 <b>Food Truck do Marcos:</b><br>O movimento é fortíssimo de sexta a domingo, e quase nulo de segunda a quinta. Qual decisão tomar?",
                "tabela": "<table><tr><th>Período</th><th>Faturamento Médio/Dia</th></tr><tr><td>Segunda a Quinta</td><td>R$ 60,00</td></tr><tr><td>Sexta a Domingo</td><td>R$ 850,00</td></tr></table>",
                "botoes": ["🕒 Abrir apenas de sexta a domingo", "🕒 Manter aberto todos os dias"],
                "opcoes_chaves": ["sexta_domingo", "todos_dias"],
                "certa": "sexta_domingo",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> Ajustar os dias elimina o desperdício e maximiza o lucro.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Manter aberto em dias de baixíssima frequência gera Prejuízo Financeiro."
            },
            5: {
                "contexto": "🌸 <b>Floricultura da Dona Eunice:</b><br>O painel mostra aceleração contínua nas vendas antes do Dia das Mães. Qual decisão tomar?",
                "tabela": "<table><tr><th>Semana</th><th>Buquês Vendidos</th></tr><tr><td>Semana 1</td><td>20</td></tr><tr><td>Semana 2</td><td>35</td></tr><tr><td>Semana 3</td><td>60</td></tr><tr><td>Semana 4</td><td>95</td></tr></table>",
                "botoes": ["🌷 Aumentar pedido de flores frescas", "🌷 Manter o pedido de sempre"],
                "opcoes_chaves": ["aumentar", "manter"],
                "certa": "aumentar",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> A tendência de crescimento mostra que aumentar o pedido evita perda de vendas.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Ignorar a tendência é Achismo e gera falta de flores no dia mais importante."
            },
            6: {
                "contexto": "🥖 <b>Padaria do Seu Hélio:</b><br>O histograma mostra que a maioria dos clientes gasta entre R$ 10 e R$ 20. Qual decisão tomar sobre as promoções?",
                "tabela": "<table><tr><th>Faixa de Gasto</th><th>Nº de Clientes</th></tr><tr><td>R$ 0–10</td><td>40</td></tr><tr><td>R$ 10–20</td><td>65</td></tr><tr><td>R$ 20–30</td><td>20</td></tr></table>",
                "botoes": ["🎯 Criar promoção focada na faixa R$10-20", "🎯 Criar promoção para compras acima de R$30"],
                "opcoes_chaves": ["faixa_comum", "faixa_rara"],
                "certa": "faixa_comum",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> Focar na faixa mais frequente atinge a maioria dos clientes reais, maximizando o impacto da promoção.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Focar numa faixa rara de gasto desperdiça o investimento em marketing."
            },
            7: {
                "contexto": "🚗 <b>Lava-Rápido do Seu Ailton:</b><br>O histograma mostra que a maior parte dos carros leva entre 15 e 20 minutos para lavar. Qual decisão tomar sobre o número de vagas?",
                "tabela": "<table><tr><th>Faixa de Tempo</th><th>Nº de Carros</th></tr><tr><td>10–15 min</td><td>30</td></tr><tr><td>15–20 min</td><td>50</td></tr><tr><td>20–25 min</td><td>15</td></tr></table>",
                "botoes": ["🚙 Dimensionar vagas para o tempo mais comum (15-20min)", "🚙 Dimensionar vagas para o pior caso (25min+)"],
                "opcoes_chaves": ["tempo_comum", "pior_caso"],
                "certa": "tempo_comum",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> Planejar pelo tempo mais frequente otimiza o uso das vagas no dia a dia real.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Planejar pelo pior caso deixa vagas ociosas na maior parte do tempo, gerando ineficiência."
            },
            8: {
                "contexto": "📦 <b>Loja Online da Patrícia:</b><br>Um pedido de revenda distorceu a Média de valor dos pedidos. Qual decisão tomar para o frete grátis?",
                "tabela": "<table><tr><th>Pedido</th><th>Valor</th></tr><tr><td>Pedido 1</td><td>R$ 90,00</td></tr><tr><td>Pedido 2</td><td>R$ 110,00</td></tr><tr><td>Pedido 3</td><td>R$ 95,00</td></tr><tr><td>⚠️ <b>Revendedor</b></td><td><b>R$ 4.800,00</b></td></tr></table>",
                "botoes": ["🚚 Definir frete grátis baseado na Mediana (R$95)", "🚚 Definir frete grátis baseado na Média (inflada)"],
                "opcoes_chaves": ["mediana", "média"],
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> Usar a Mediana evita um valor de frete grátis inalcançável para clientes comuns.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Usar a Média distorcida pelo Outlier afasta os clientes reais da loja."
            },
            9: {
                "contexto": "🎂 <b>Buffet Infantil da Renata:</b><br>Uma festa de 15 anos teve um número de convidados bem fora do padrão. Qual decisão tomar para o pacote padrão do buffet?",
                "tabela": "<table><tr><th>Festa</th><th>Convidados</th></tr><tr><td>Festa 1</td><td>25</td></tr><tr><td>Festa 2</td><td>30</td></tr><tr><td>Festa 3</td><td>28</td></tr><tr><td>⚠️ <b>Festa de 15 Anos</b></td><td><b>300</b></td></tr></table>",
                "botoes": ["🎈 Criar pacote padrão baseado na Mediana (~28 convidados)", "🎈 Criar pacote padrão baseado na Média (inflada)"],
                "opcoes_chaves": ["mediana", "média"],
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> O pacote baseado na Mediana atende à maioria real das festas, evitando desperdício.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Um pacote baseado na Média ficaria caro e desproporcional para festas comuns."
            },
            10: {
                "contexto": "🛵 <b>Motoboy Renan (Entregas por App):</b><br>A Black Friday bombou os pedidos, distorcendo a rotina normal. Qual decisão tomar sobre a contratação de mais motoboys?",
                "tabela": "<table><tr><th>Dia</th><th>Entregas</th></tr><tr><td>Seg</td><td>12</td></tr><tr><td>Ter</td><td>14</td></tr><tr><td>Qua</td><td>13</td></tr><tr><td>⚠️ <b>Black Friday</b></td><td><b>80</b></td></tr></table>",
                "botoes": ["🛵 Manter equipe baseada na rotina comum (Mediana)", "🛵 Contratar equipe permanente baseada na Black Friday"],
                "opcoes_chaves": ["mediana", "pico"],
                "certa": "mediana",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> Contratar pela rotina comum evita custo fixo desnecessário; reforços pontuais cobrem picos como a Black Friday.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Contratar equipe permanente baseada num pico isolado gera custo fixo alto sem necessidade real."
            },
            11: {
                "contexto": "🛍️ <b>Brechó da Camila:</b><br>O gráfico de barras mostra Vestidos como a categoria mais vendida. Qual decisão tomar para as próximas compras de peças?",
                "tabela": "<table><tr><th>Tipo de Peça</th><th>Vendidas</th></tr><tr><td>Camisas</td><td>60</td></tr><tr><td>Calças</td><td>40</td></tr><tr><td>Vestidos</td><td>75</td></tr><tr><td>Casacos</td><td>20</td></tr></table>",
                "botoes": ["🛍️ Priorizar compra de mais Vestidos", "🛍️ Priorizar compra de mais Casacos"],
                "opcoes_chaves": ["vestidos", "casacos"],
                "certa": "vestidos",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> Priorizar a categoria de maior demanda maximiza o giro de estoque e o faturamento.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Investir na categoria de menor demanda (Casacos) é Achismo e gera estoque parado."
            },
            12: {
                "contexto": "🏋️ <b>Academia da Fernanda:</b><br>O histograma mostra que a maioria dos alunos tem entre 26 e 35 anos. Qual decisão tomar sobre as novas turmas?",
                "tabela": "<table><tr><th>Faixa de Idade</th><th>Nº de Alunos</th></tr><tr><td>15–25</td><td>30</td></tr><tr><td>26–35</td><td>55</td></tr><tr><td>36–45</td><td>25</td></tr></table>",
                "botoes": ["🏋️ Criar turma focada em 26-35 anos", "🏋️ Criar turma focada em 46+ anos"],
                "opcoes_chaves": ["faixa_comum", "faixa_rara"],
                "certa": "faixa_comum",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> Criar uma turma para a faixa mais numerosa atende a maior parte dos alunos reais.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Focar numa faixa etária pouco representada na academia desperdiça recursos."
            },
            13: {
                "contexto": "📱 <b>Assistência Técnica do Diego:</b><br>O gráfico de linhas mostra crescimento contínuo nos reparos nos últimos meses. Qual decisão tomar sobre a contratação de técnicos?",
                "tabela": "<table><tr><th>Mês</th><th>Reparos</th></tr><tr><td>Jan</td><td>30</td></tr><tr><td>Mar</td><td>45</td></tr><tr><td>Mai</td><td>70</td></tr><tr><td>Jun</td><td>90</td></tr></table>",
                "botoes": ["🛠️ Contratar mais um técnico para acompanhar o crescimento", "🛠️ Manter a equipe atual"],
                "opcoes_chaves": ["contratar", "manter"],
                "certa": "contratar",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> A tendência clara de crescimento justifica reforçar a equipe antes que o atendimento fique sobrecarregado.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Ignorar a tendência de crescimento é Achismo e pode gerar atrasos e clientes insatisfeitos."
            },
            14: {
                "contexto": "🧺 <b>Lavanderia da Dona Iracema:</b><br>O histograma mostra que a maioria das sacolas pesa entre 3 e 6 kg. Qual decisão tomar sobre o pacote de preço fixo?",
                "tabela": "<table><tr><th>Faixa de Peso</th><th>Nº de Sacolas</th></tr><tr><td>0–3 kg</td><td>20</td></tr><tr><td>3–6 kg</td><td>50</td></tr><tr><td>6–9 kg</td><td>25</td></tr></table>",
                "botoes": ["🧺 Criar pacote fixo para a faixa 3-6 kg", "🧺 Criar pacote fixo para a faixa 6-9 kg"],
                "opcoes_chaves": ["faixa_comum", "faixa_rara"],
                "certa": "faixa_comum",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> O pacote baseado na faixa mais frequente atende a maioria das sacolas reais dos clientes.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Um pacote pensado para a faixa menos comum deixa a maioria dos clientes pagando mais do que deveriam."
            },
            15: {
                "contexto": "🍕 <b>Pizzaria do Seu Vitor:</b><br>O gráfico de barras mostra Frango com Catupiry como o sabor mais vendido. Qual decisão tomar sobre os ingredientes do estoque?",
                "tabela": "<table><tr><th>Sabor</th><th>Vendidas</th></tr><tr><td>Calabresa</td><td>85</td></tr><tr><td>Margherita</td><td>50</td></tr><tr><td>Frango com Catupiry</td><td>95</td></tr></table>",
                "botoes": ["🧀 Priorizar estoque de Frango e Catupiry", "🧀 Priorizar estoque de Margherita"],
                "opcoes_chaves": ["frango_catupiry", "margherita"],
                "certa": "frango_catupiry",
                "fb_sucesso": "<b>✓ Decisão Correta!</b> Priorizar o ingrediente do sabor mais vendido evita falta de estoque no produto-chave.",
                "fb_erro": "<b>✕ Decisão Incorreta!</b> Priorizar o sabor menos vendido (Margherita) é Achismo e pode causar falta do ingrediente mais demandado."
            }
        }
    }
}

# ==========================================================================
# BANCO DE CONCEITOS (TEORIA)
# ==========================================================================

banco_conceitos = {
    1: {
        "titulo": "📚 Interpretação Estatística",
        "cor": "#0f9d6e",
        "cor_clara": "#e3f7ee",
        "explanatorio": (
            "Quando você soma os valores de venda e divide pela quantidade de dias ou clientes, "
            "você calcula a <b>Média</b>. Ela funciona bem quando os números são parecidos entre si.<br><br>"
            "Mas e quando aparece um cliente fora da curva — uma compra gigante, um dia de evento especial? "
            "Esse valor estranho se chama <b>Outlier</b>, e ele pode distorcer a Média, fazendo parecer que o "
            "negócio fatura muito mais (ou muito menos) do que o normal.<br><br>"
            "Nesses casos, a <b>Mediana</b> — o valor do meio quando você organiza os números em ordem — "
            "é mais confiável, porque ela ignora os extremos e mostra o que é realmente típico no seu negócio."
        ),
        "pilulas": ["Média", "Mediana", "Outliers"],
        "finalidade": "Ajudar a proteger o caixa do negócio contra decisões enviesadas por clientes ou eventos atípicos.",
        "fase_pratica": 1
    },
    2: {
        "titulo": "📚 Visualização de Dados",
        "cor": "#1d63d6",
        "cor_clara": "#e7f0fd",
        "explanatorio": (
            "Os números de uma planilha escondem informações que só aparecem quando você os transforma em imagem.<br><br>"
            "O <b>Gráfico de Linhas</b> é ideal para mostrar como algo muda <b>ao longo do tempo</b> — vendas por mês, "
            "faturamento por semana. Ele revela tendências de subida, queda e sazonalidade.<br><br>"
            "O <b>Gráfico de Barras</b> é ideal para <b>comparar categorias</b> diferentes entre si — qual produto vende mais, "
            "qual ponto de venda é mais rentável.<br><br>"
            "Já o <b>Histograma</b> mostra como os valores se <b>distribuem em faixas</b> — por exemplo, quantos clientes gastam "
            "pouco, médio ou muito — ajudando a enxergar o padrão geral por trás dos números."
        ),
        "pilulas": ["Gráfico de Linhas", "Gráfico de Barras", "Histograma"],
        "finalidade": "Permitir enxergar tendências, sazonalidade e distribuições que os números brutos escondem.",
        "fase_pratica": 2
    },
    3: {
        "titulo": "📚 Tomada de Decisão",
        "cor": "#7c3aed",
        "cor_clara": "#f1ebfd",
        "explanatorio": (
            "Decidir baseado em <b>Achismo</b> é confiar na sensação, sem checar os números. Isso costuma levar a "
            "<b>Prejuízo Financeiro</b>: comprar estoque errado, manter horários que não funcionam, investir no produto errado.<br><br>"
            "Uma <b>Decisão segura</b> nasce da combinação entre Estatística (Média, Mediana, Outliers) e "
            "Visualização (Linhas, Barras, Histograma). Quando você identifica <b>Padrões</b> nos dados — uma tendência "
            "de crescimento, uma sazonalidade, um produto que vende mais — você tem uma base sólida para decidir.<br><br>"
            "O objetivo final é simples: usar o que os dados mostram para que o <b>Empreendimento</b> seja mais "
            "rentável e seguro, sob pressão real do dia a dia."
        ),
        "pilulas": ["Achismo", "Decisão segura", "Padrões"],
        "finalidade": "Aplicar estatística e visualização juntas para evitar Achismo e Prejuízo Financeiro, tomando a decisão mais rentável.",
        "fase_pratica": 3
    }
}

# ==========================================================================
# ESTADO DA SESSÃO
# ==========================================================================

if "tela" not in st.session_state:
    st.session_state.tela = "hub"

if "placares" not in st.session_state:
    st.session_state.placares = {1: None, 2: None, 3: None}

if "conceitos_vistos" not in st.session_state:
    st.session_state.conceitos_vistos = {1: False, 2: False, 3: False}


def inicializar_fase(numero_fase):
    fase_info = banco_fases[numero_fase]
    todos_indices = list(fase_info["perguntas"].keys())
    qtd = min(PERGUNTAS_POR_SESSAO, len(todos_indices))
    indices_sorteados = random.sample(todos_indices, qtd)
    st.session_state.fase_atual = numero_fase
    st.session_state.ordem_perguntas = indices_sorteados
    st.session_state.indice_pergunta = 0
    st.session_state.score = 0
    st.session_state.respostas_computadas = {}
    st.session_state.resposta_dada = None
    st.session_state.exibir_transicao = False


def ir_para(tela, **kwargs):
    st.session_state.tela = tela
    for chave, valor in kwargs.items():
        st.session_state[chave] = valor
    st.rerun()


# ==========================================================================
# ESTILOS — TEMA CLARO FIXO, VISUAL EDUCACIONAL/GAMIFICADO
# ==========================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Nunito:wght@400;600;700;800&display=swap');

html, body, .stApp {
    background-color: #f7f8fb !important;
    color: #20232b !important;
}
* { font-family: 'Nunito', sans-serif; }
h1, h2, h3, h4 { font-family: 'Baloo 2', cursive !important; color: #20232b !important; }

[data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
    background-color: #f7f8fb !important;
}
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span { color: #20232b !important; }

/* ---------- Hub ---------- */
.hub-header {
    background: linear-gradient(135deg, #ffb238 0%, #ff7a59 100%);
    color: #ffffff !important; padding: 26px; border-radius: 20px;
    text-align: center; margin-bottom: 24px; box-shadow: 0 6px 18px rgba(255,122,89,0.25);
}
.hub-header h2, .hub-header p { color: #ffffff !important; margin: 0; }

.hub-card-title { font-size: 18px; font-weight: 800; margin-bottom: 2px; }
.hub-card-status { font-size: 13px; color: #6b7280 !important; font-weight: 700; }
.badge-feito {
    display: inline-block; background-color: #d6f5e3; color: #0f7a4d !important;
    padding: 3px 10px; border-radius: 14px; font-size: 12px; font-weight: 800; margin-right: 6px;
}
.badge-pendente {
    display: inline-block; background-color: #f1f2f6; color: #8a8f9c !important;
    padding: 3px 10px; border-radius: 14px; font-size: 12px; font-weight: 700; margin-right: 6px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #ffffff !important; border-radius: 18px !important;
    border: 2px solid #e9ebf0 !important; box-shadow: 0 3px 10px rgba(20,20,40,0.05);
}
div[data-testid="stVerticalBlockBorderWrapper"] * { color: #20232b !important; }

/* ---------- Conceito ---------- */
.conceito-header {
    color: #ffffff !important; padding: 20px; border-radius: 18px 18px 0px 0px;
    font-weight: 800; font-size: 21px; text-align: center;
}
.conceito-body {
    background-color: #ffffff !important; padding: 24px; border-radius: 0px 0px 18px 18px;
    line-height: 1.7; font-size: 15px; color: #20232b !important; border: 2px solid #e9ebf0; border-top: none;
}
.conceito-body * { color: #20232b !important; }
.conceito-finalidade {
    background-color: #fff6e0 !important; border-left: 6px solid #ffb238; padding: 14px;
    margin-top: 18px; border-radius: 10px; font-size: 14px; color: #7a4d00 !important;
}
.conceito-finalidade * { color: #7a4d00 !important; }
.pilula {
    display: inline-block; padding: 7px 16px; border-radius: 24px;
    font-size: 13px; font-weight: 800; margin: 4px 4px 4px 0px;
}

/* ---------- Planilha (Prática 1) ---------- */
.planilha-header {
    background: linear-gradient(135deg, #1bbf8a 0%, #0f9d6e 100%);
    color: #ffffff !important; padding: 16px; font-weight: 800;
    border-radius: 18px 18px 0px 0px; text-align: center; font-size: 17px;
}
.planilha-toolbar {
    background-color: #e3f7ee !important; padding: 9px 16px; font-size: 12px;
    color: #0f5c41 !important; font-weight: 700; border-bottom: 2px solid #b9ecd8;
}
.planilha-body {
    background-color: #ffffff !important; padding: 18px; border: 2px solid #e3f7ee;
    border-radius: 0px 0px 18px 18px; color: #20232b !important;
}
.planilha-body * { color: #20232b !important; }

/* ---------- Dashboard Analytics (Prática 2) ---------- */
.analytics-header {
    background: linear-gradient(135deg, #4d8df0 0%, #1d63d6 100%);
    color: #ffffff !important; padding: 16px; font-weight: 800;
    border-radius: 18px 18px 0px 0px; text-align: center; font-size: 17px;
}
.analytics-body {
    background-color: #ffffff !important; padding: 18px; border: 2px solid #dde9fb;
    border-radius: 0px 0px 18px 18px; color: #20232b !important;
}
.analytics-body * { color: #20232b !important; }
.analytics-kpi {
    display: inline-block; background-color: #e7f0fd !important; color: #1d4fb0 !important;
    padding: 5px 12px; border-radius: 8px; font-size: 12px; font-weight: 700; margin-bottom: 10px;
}

/* ---------- Dashboard Financeiro (Prática 3) ---------- */
.financeiro-header {
    background: linear-gradient(135deg, #9b6df0 0%, #7c3aed 100%);
    color: #ffffff !important; padding: 16px; font-weight: 800;
    border-radius: 18px 18px 0px 0px; text-align: center; font-size: 17px;
}
.financeiro-body {
    background-color: #ffffff !important; padding: 18px; border: 2px solid #ece2fc;
    border-radius: 0px 0px 18px 18px; color: #20232b !important;
}
.financeiro-body * { color: #20232b !important; }
.financeiro-alerta {
    background-color: #fff6e0 !important; color: #7a4d00 !important; padding: 10px 14px;
    border-radius: 8px; font-size: 13px; margin-top: 12px; border-left: 5px solid #ffb238;
    font-weight: 600;
}

/* ---------- Comum: Feedback ---------- */
.feedback-box-correct {
    background-color: #e2f7e9 !important; color: #166534 !important; padding: 16px;
    border-radius: 12px; border-left: 6px solid #22c55e; margin-top: 18px; font-weight: 600;
}
.feedback-box-correct * { color: #166534 !important; }
.feedback-box-incorrect {
    background-color: #fde8ea !important; color: #9f1239 !important; padding: 16px;
    border-radius: 12px; border-left: 6px solid #f43f5e; margin-top: 18px; font-weight: 600;
}
.feedback-box-incorrect * { color: #9f1239 !important; }

table { width: 100%; border-collapse: collapse; margin-top: 10px; }
th, td { border: 1px solid #e9ebf0; padding: 7px; text-align: left; font-size: 13px; color: #20232b !important; }
th { background-color: #f1f2f6 !important; font-weight: 700; }

/* ---------- Resultados ---------- */
.resultado-card {
    background-color: #ffffff !important; border: 2px solid #e9ebf0; border-radius: 14px;
    padding: 18px; margin-bottom: 14px; color: #20232b !important;
}
.resultado-card * { color: #20232b !important; }
.resultado-classificacao {
    background: linear-gradient(135deg, #ffd166 0%, #ffb238 100%);
    border-left: 6px solid #d97706; padding: 18px; border-radius: 12px;
    font-size: 17px; font-weight: 800; text-align: center; color: #5c3a00 !important;
}
.resultado-classificacao * { color: #5c3a00 !important; }

/* botões com cara de jogo educacional */
.stButton button {
    border-radius: 12px !important; font-weight: 800 !important;
    border: 2px solid #e9ebf0 !important; color: #20232b !important;
    background-color: #ffffff !important; transition: transform 0.08s ease;
}
.stButton button:hover { transform: translateY(-1px); border-color: #ffb238 !important; }
.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #ffb238 0%, #ff7a59 100%) !important;
    color: #ffffff !important; border: none !important;
}
</style>
""", unsafe_allow_html=True)


# ==========================================================================
# TELA: HUB (Navegação principal)
# ==========================================================================

def tela_hub():
    st.markdown(
        '<div class="hub-header"><h2>📊 DataLearning</h2>'
        '<p>Como Tomar Melhores Decisões para seu Negócio e Ganhar Dinheiro?</p></div>',
        unsafe_allow_html=True
    )

    for num in [1, 2, 3]:
        conceito = banco_conceitos[num]
        placar = st.session_state.placares[num]
        visto = st.session_state.conceitos_vistos[num]

        badge_conceito = '<span class="badge-feito">✅ Conceito visto</span>' if visto else '<span class="badge-pendente">⬜ Conceito não visto</span>'
        badge_pratica = f'<span class="badge-feito">✅ Praticado — {placar}/{PERGUNTAS_POR_SESSAO}</span>' if placar is not None else '<span class="badge-pendente">⬜ Não praticado</span>'

        with st.container(border=True):
            st.markdown(
                f'<div class="hub-card-title" style="color:{conceito["cor"]}">{conceito["titulo"]}</div>'
                f'<div class="hub-card-status">{badge_conceito}{badge_pratica}</div>',
                unsafe_allow_html=True
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📖 Ver Conceito", key=f"hub_conceito_{num}", use_container_width=True):
                    st.session_state.conceitos_vistos[num] = True
                    ir_para("conceito", conceito_atual=num)
            with col2:
                if st.button("🎮 Ir para Prática", key=f"hub_pratica_{num}", use_container_width=True):
                    inicializar_fase(num)
                    ir_para("pratica")

    st.write("")
    if st.button("🏁 Ver Resultados Gerais", use_container_width=True, type="primary"):
        ir_para("resultados")


# ==========================================================================
# TELA: CONCEITO
# ==========================================================================

def tela_conceito():
    num = st.session_state.conceito_atual
    c = banco_conceitos[num]
    st.session_state.conceitos_vistos[num] = True

    if st.button("← Voltar ao início"):
        ir_para("hub")

    st.markdown(f'<div class="conceito-header" style="background-color:{c["cor"]}">{c["titulo"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="conceito-body">{c["explanatorio"]}', unsafe_allow_html=True)

    st.write("")
    pilulas_html = "".join(
        f'<span class="pilula" style="background-color:{c["cor_clara"]}; color:{c["cor"]} !important;">{p}</span>'
        for p in c["pilulas"]
    )
    st.markdown(pilulas_html, unsafe_allow_html=True)

    st.markdown(f'<div class="conceito-finalidade"><b>🎯 Finalidade:</b> {c["finalidade"]}</div></div>', unsafe_allow_html=True)

    st.write("")
    if st.button(f"🎮 Ir para Prática: {banco_fases[c['fase_pratica']]['app_nome']}", use_container_width=True, type="primary"):
        inicializar_fase(c["fase_pratica"])
        ir_para("pratica")


# ==========================================================================
# TELA: PRÁTICA
# ==========================================================================

def tela_pratica():
    fase_info = banco_fases[st.session_state.fase_atual]
    id_pergunta_atual = st.session_state.ordem_perguntas[st.session_state.indice_pergunta]
    q = fase_info["perguntas"][id_pergunta_atual]

    col_voltar1, col_voltar2 = st.columns(2)
    with col_voltar1:
        if st.button("← Início"):
            ir_para("hub")
    with col_voltar2:
        if st.button("📖 Ver Conceito"):
            num_conceito = next(
                n for n, c in banco_conceitos.items() if c["fase_pratica"] == st.session_state.fase_atual
            )
            st.session_state.conceitos_vistos[num_conceito] = True
            ir_para("conceito", conceito_atual=num_conceito)

    if st.session_state.exibir_transicao:
        st.markdown('<div class="financeiro-header">🏁 MÓDULO CONCLUÍDO!</div>', unsafe_allow_html=True)
        total = len(st.session_state.ordem_perguntas)
        st.success(f"🏆 Excelente! Você concluiu o módulo {fase_info['app_nome']} com {st.session_state.score}/{total} acertos!")
        st.session_state.placares[st.session_state.fase_atual] = st.session_state.score
        st.write("")
        if st.button("🏠 Voltar ao Início", use_container_width=True, type="primary"):
            ir_para("hub")
        if st.button("🏁 Ver Resultados Gerais", use_container_width=True):
            ir_para("resultados")
        return

    progresso = f"Desafio {st.session_state.indice_pergunta + 1} de {len(st.session_state.ordem_perguntas)} | Placar: {st.session_state.score} ⭐"

    # ---------------- CENÁRIO 1: PLANILHA ----------------
    if fase_info["tipo"] == "planilha":
        st.markdown(f'<div class="planilha-header">📊 {fase_info["header_text"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="planilha-toolbar">{progresso}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="planilha-body">{q["contexto"]}{q["tabela"]}</div>', unsafe_allow_html=True)
        botoes, chaves = fase_info["botoes"], fase_info["opcoes_chaves"]

    # ---------------- CENÁRIO 2: DASHBOARD ANALYTICS (3 opções, com Histograma) ----------------
    elif fase_info["tipo"] == "dashboard_analytics":
        st.markdown(f'<div class="analytics-header">{fase_info["header_text"]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="analytics-body"><span class="analytics-kpi">{progresso}</span>{q["contexto"]}{q["tabela"]}</div>',
            unsafe_allow_html=True
        )
        nomes_opcoes = {"linhas": "📈 Gráfico de Linhas", "barras": "📊 Gráfico de Barras", "histograma": "📉 Histograma"}
        chaves = q["opcoes"]
        botoes = [nomes_opcoes[k] for k in chaves]

    # ---------------- CENÁRIO 3: DASHBOARD FINANCEIRO ----------------
    else:
        st.markdown(f'<div class="financeiro-header">{fase_info["header_text"]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="financeiro-body">{progresso}<br><br>{q["contexto"]}{q["tabela"]}'
            f'<div class="financeiro-alerta">⚠️ Use os dados acima para tomar a decisão mais segura para o negócio.</div></div>',
            unsafe_allow_html=True
        )
        botoes, chaves = q["botoes"], q["opcoes_chaves"]

    # ---------------- INTERAÇÃO ----------------
    if st.session_state.resposta_dada is None:
        st.write("")
        if len(botoes) == 3:
            cols = st.columns(3)
        else:
            cols = st.columns(2)

        for i, col in enumerate(cols):
            with col:
                if st.button(botoes[i], use_container_width=True, key=f"btn_opcao_{i}"):
                    st.session_state.resposta_dada = chaves[i]
                    st.rerun()
    else:
        if st.session_state.resposta_dada == q["certa"]:
            if st.session_state.indice_pergunta not in st.session_state.respostas_computadas:
                st.session_state.score += 1
                st.session_state.respostas_computadas[st.session_state.indice_pergunta] = "correto"
            st.markdown(f'<div class="feedback-box-correct">{q["fb_sucesso"]}</div>', unsafe_allow_html=True)
            st.write("")
            if st.session_state.indice_pergunta < (len(st.session_state.ordem_perguntas) - 1):
                if st.button("➡️ Próximo Desafio", type="primary", use_container_width=True):
                    st.session_state.indice_pergunta += 1
                    st.session_state.resposta_dada = None
                    st.rerun()
            else:
                st.session_state.exibir_transicao = True
                st.rerun()
        else:
            if st.session_state.indice_pergunta not in st.session_state.respostas_computadas:
                st.session_state.respostas_computadas[st.session_state.indice_pergunta] = "incorreto"
            st.markdown(f'<div class="feedback-box-incorrect">{q["fb_erro"]}</div>', unsafe_allow_html=True)
            st.write("")
            if st.button("🔄 Analisar os dados novamente", use_container_width=True):
                st.session_state.resposta_dada = None
                st.rerun()


# ==========================================================================
# TELA: RESULTADOS GERAIS
# ==========================================================================

def tela_resultados():
    if st.button("← Voltar ao início"):
        ir_para("hub")

    st.markdown(
        '<div class="hub-header"><h2>🏁 Resultados Gerais</h2>'
        '<p>Consolidação do seu desempenho nos 3 módulos</p></div>',
        unsafe_allow_html=True
    )

    placares = st.session_state.placares
    cenarios_praticados = [n for n in [1, 2, 3] if placares[n] is not None]

    if not cenarios_praticados:
        st.markdown(
            '<div class="resultado-card">Você ainda não praticou nenhum módulo. '
            'Volte ao início e escolha um cenário para começar!</div>',
            unsafe_allow_html=True
        )
        return

    total_acertos = sum(placares[n] for n in cenarios_praticados)
    total_perguntas = len(cenarios_praticados) * PERGUNTAS_POR_SESSAO
    percentual = round((total_acertos / total_perguntas) * 100)

    with st.container(border=True):
        st.markdown("#### 📊 Pontuação Geral")
        st.progress(percentual / 100)
        st.markdown(f"**{total_acertos} de {total_perguntas} acertos ({percentual}%)**")

    st.write("")
    st.markdown("#### 📋 Acertos e Erros por Cenário")
    for num in [1, 2, 3]:
        conceito = banco_conceitos[num]
        nome_app = banco_fases[num]["app_nome"]
        if placares[num] is not None:
            st.markdown(
                f'<div class="resultado-card"><b style="color:{conceito["cor"]} !important;">{conceito["titulo"]}</b> '
                f'({nome_app}) — {placares[num]}/{PERGUNTAS_POR_SESSAO} acertos</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="resultado-card" style="opacity:0.6;"><b>{conceito["titulo"]}</b> '
                f'({nome_app}) — ainda não praticado</div>',
                unsafe_allow_html=True
            )

    st.write("")
    st.markdown("#### 🏆 Classificação do Empreendedor")
    if len(cenarios_praticados) < 3:
        classificacao = "Complete os 3 módulos para receber sua classificação final!"
    elif percentual >= 80:
        classificacao = "🌟 Mestre do Empreendimento — Você domina a tomada de decisão baseada em dados!"
    elif percentual >= 50:
        classificacao = "👀 Visão Limpa — Você já enxerga os dados, mas ainda pode refinar suas decisões."
    else:
        classificacao = "🎲 No Achismo — Reforce os conceitos e pratique mais para proteger seu negócio."
    st.markdown(f'<div class="resultado-classificacao">{classificacao}</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 💡 Dicas Práticas")
    st.markdown(
        '<div class="resultado-card">'
        "- Antes de calcular a Média, verifique se há um Outlier que possa distorcer o resultado.<br>"
        "- Para decisões ao longo do tempo, use Gráfico de Linhas; para comparar categorias, use Barras; "
        "para distribuições, use Histograma.<br>"
        "- Sempre que for decidir algo importante no negócio, busque confirmar com os dados antes de confiar só na intuição."
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")
    if st.button("🔄 Reiniciar todos os módulos", use_container_width=True):
        st.session_state.placares = {1: None, 2: None, 3: None}
        st.session_state.conceitos_vistos = {1: False, 2: False, 3: False}
        ir_para("hub")


# ==========================================================================
# ROTEADOR PRINCIPAL
# ==========================================================================

if st.session_state.tela == "hub":
    tela_hub()
elif st.session_state.tela == "conceito":
    tela_conceito()
elif st.session_state.tela == "pratica":
    tela_pratica()
elif st.session_state.tela == "resultados":
    tela_resultados()