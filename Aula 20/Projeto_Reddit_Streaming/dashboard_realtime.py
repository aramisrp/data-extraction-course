import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime
from confluent_kafka import Consumer, KafkaError
import plotly.express as px

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Reddit Real-Time Analytics",
    page_icon="📊",
    layout="wide"
)

# Estilização CSS para visual premium (Dark Mode Accent e Glassmorphism)
st.markdown("""
    <style>
    .main {
        background-color: #0f1116;
        color: #f0f2f6;
    }
    .metric-card {
        background-color: #1b1e26;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #2d3139;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #ff4500; /* Laranja clássico do Reddit */
    }
    .metric-label {
        font-size: 0.9rem;
        color: #8892b0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# ANÁLISE DE SENTIMENTO DIDÁTICA (Regra de Palavras)
# ----------------------------------------------------
def analisar_sentimento_pt(texto):
    """
    Função didática de análise de sentimento para o Português.
    Varre o texto contando ocorrências de termos positivos e negativos.
    """
    texto = str(texto).lower()
    
    palavras_positivas = [
        'bom', 'boa', 'ótimo', 'otimo', 'excelente', 'maravilhoso', 'gosto', 'gostei', 'legal', 
        'lindo', 'feliz', 'parabéns', 'parabens', 'concordo', 'amor', 'melhor', 'sucesso', 'top',
        'sensacional', 'show', 'interessante', 'ajuda', 'obrigado', 'valeu'
    ]
    
    palavras_negativas = [
        'ruim', 'péssimo', 'pessimo', 'horrível', 'horrivel', 'odeio', 'odiei', 'triste', 
        'erro', 'errado', 'pior', 'bosta', 'merda', 'lixo', 'difícil', 'dificil', 'fracasso', 
        'discordo', 'fake', 'mentira', 'corrupção', 'roubo', 'crime', 'violência', 'violencia',
        'absurdo', 'pobreza', 'tristeza', 'crise', 'problema', 'bizarro'
    ]
    
    score = 0
    # Conta palavras positivas
    for p in palavras_positivas:
        score += texto.count(p)
    # Subtrai palavras negativas
    for p in palavras_negativas:
        score -= texto.count(p)
        
    if score > 0:
        return 'Positivo', score
    elif score < 0:
        return 'Negativo', score
    else:
        return 'Neutro', 0

# ----------------------------------------------------
# CONFIGURAÇÃO DO KAFKA
# ----------------------------------------------------
def criar_consumidor(bootstrap_servers, topic):
    conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'streamlit-reddit-dashboard',
        'auto.offset.reset': 'latest',  # Lemos apenas as mais recentes ao iniciar o Dashboard
        'enable.auto.commit': True
    }
    try:
        consumer = Consumer(conf)
        consumer.subscribe([topic])
        return consumer
    except Exception as e:
        st.error(f"Erro ao conectar no Kafka Broker: {e}")
        return None

# ----------------------------------------------------
# INTERFACE DO USUÁRIO (SIDEBAR & HEADER)
# ----------------------------------------------------
st.title("📊 Reddit Live Stream Dashboard")
st.caption("Disciplina: Extração de Dados (IBMEC) - Monitoramento em Tempo Real do Reddit via Apache Kafka")

# Sidebar de Configurações
st.sidebar.image("https://www.redditstatic.com/desktop2x/img/favicon/apple-icon-120x120.png", width=60)
st.sidebar.header("Configurações do Stream")
kafka_broker = st.sidebar.text_input("Kafka Broker", "localhost:9092")
kafka_topic = st.sidebar.text_input("Tópico Kafka", "reddit-stream")
max_history = st.sidebar.slider("Limite de Histórico na Tela", 50, 1000, 200)

# Botões de controle no Sidebar
iniciar_stream = st.sidebar.button("▶️ Iniciar Monitoramento", use_container_width=True)
parar_stream = st.sidebar.button("⏸️ Pausar", use_container_width=True)
limpar_dados = st.sidebar.button("🧹 Limpar Histórico", use_container_width=True)

# Inicialização do Histórico em Session State
if 'comentarios' not in st.session_state or limpar_dados:
    st.session_state['comentarios'] = []

# Exibe quantidade atual de mensagens na memória do Streamlit
st.sidebar.markdown(f"**Mensagens na memória:** `{len(st.session_state['comentarios'])}`")

# ----------------------------------------------------
# COMPONENTES DE TELA DINÂMICOS (PLACEHOLDERS)
# ----------------------------------------------------
# 1. KPIs (Cards superiores)
kpi_placeholder = st.empty()

st.write("---")

# 2. Área de Gráficos (Lado a Lado)
col_graf1, col_graf2 = st.columns(2)
grafico1_placeholder = col_graf1.empty()
grafico2_placeholder = col_graf2.empty()

st.write("---")

# 3. Tabela de Feed em Tempo Real
feed_placeholder = st.empty()

# ----------------------------------------------------
# LOOP DE STREAMING
# ----------------------------------------------------
if iniciar_stream:
    # Conecta ao Kafka
    consumer = criar_consumidor(kafka_broker, kafka_topic)
    
    if consumer:
        st.sidebar.success("Conectado ao Kafka com sucesso!")
        
        # Loop contínuo de consumo
        try:
            while True:
                # Tenta consumir mensagem (timeout de 0.5s para não travar a tela)
                msg = consumer.poll(0.5)
                
                # Se pausou, interrompe o loop
                # (Observação: Streamlit roda de cima a baixo ao clicar nos botões,
                # para controle fino de loop no Streamlit, verificamos o estado)
                
                if msg is None:
                    # Mesmo sem mensagens novas, atualizamos as visualizações com o histórico existente
                    pass
                elif msg.error():
                    if msg.error().code() != KafkaError._PARTITION_EOF:
                        st.sidebar.error(f"Erro no Kafka: {msg.error()}")
                else:
                    # Sucesso ao receber mensagem
                    try:
                        payload = json.loads(msg.value().decode('utf-8'))
                        
                        # Aplica classificação de sentimentos didática
                        sentimento, score = analisar_sentimento_pt(payload.get('body', ''))
                        
                        # Adiciona metadados extras para visualização
                        payload['sentiment'] = sentimento
                        payload['sentiment_score'] = score
                        payload['received_at'] = datetime.now().strftime("%H:%M:%S")
                        
                        # Insere no início da lista (para o feed mostrar os mais novos no topo)
                        st.session_state['comentarios'].insert(0, payload)
                        
                        # Controla o tamanho do buffer na memória
                        if len(st.session_state['comentarios']) > max_history:
                            st.session_state['comentarios'].pop()
                            
                    except Exception as parse_error:
                        st.sidebar.error(f"Erro ao parsear JSON: {parse_error}")

                # ----------------------------------------------------
                # ATUALIZAÇÃO DA TELA (RENDERING)
                # ----------------------------------------------------
                if st.session_state['comentarios']:
                    # Transforma o histórico atual em DataFrame
                    df_feed = pd.DataFrame(st.session_state['comentarios'])
                    
                    # 1. Renderiza KPIs
                    total_comentarios = len(df_feed)
                    sentimentos_counts = df_feed['sentiment'].value_counts()
                    
                    pos_pct = (sentimentos_counts.get('Positivo', 0) / total_comentarios) * 100
                    neu_pct = (sentimentos_counts.get('Neutro', 0) / total_comentarios) * 100
                    neg_pct = (sentimentos_counts.get('Negativo', 0) / total_comentarios) * 100
                    
                    autor_mais_ativo = df_feed['author'].mode()[0] if not df_feed['author'].empty else "N/A"
                    
                    with kpi_placeholder.container():
                        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
                        
                        kpi_col1.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-value">{total_comentarios}</div>
                                <div class="metric-label">Total de Comentários</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        kpi_col2.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-value" style="color: #2ecc71;">{pos_pct:.1f}%</div>
                                <div class="metric-label">Sentimento Positivo</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        kpi_col3.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-value" style="color: #95a5a6;">{neu_pct:.1f}%</div>
                                <div class="metric-label">Sentimento Neutro</div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        kpi_col4.markdown(f"""
                            <div class="metric-card">
                                <div class="metric-value" style="color: #e74c3c;">{neg_pct:.1f}%</div>
                                <div class="metric-label">Sentimento Negativo</div>
                            </div>
                        """, unsafe_allow_html=True)

                    # 2. Renderiza Gráfico 1: Sentimento (Plotly)
                    with grafico1_placeholder.container():
                        df_sent_count = df_feed['sentiment'].value_counts().reset_index()
                        df_sent_count.columns = ['Sentimento', 'Quantidade']
                        
                        cores_sentimento = {'Positivo': '#2ecc71', 'Neutro': '#95a5a6', 'Negativo': '#e74c3c'}
                        fig1 = px.bar(
                            df_sent_count, 
                            x='Sentimento', 
                            y='Quantidade',
                            color='Sentimento',
                            color_discrete_map=cores_sentimento,
                            title="Distribuição de Sentimentos (Tempo Real)"
                        )
                        fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                        st.plotly_chart(fig1, use_container_width=True)

                    # 3. Renderiza Gráfico 2: Autores Ativos
                    with grafico2_placeholder.container():
                        df_autores = df_feed['author'].value_counts().reset_index().head(8)
                        df_autores.columns = ['Autor', 'Comentários']
                        
                        fig2 = px.bar(
                            df_autores, 
                            x='Comentários', 
                            y='Autor',
                            orientation='h',
                            title="Top 8 Autores Mais Ativos",
                            color_discrete_sequence=['#ff4500']
                        )
                        fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                        fig2.update_yaxes(categoryorder="total ascending")
                        st.plotly_chart(fig2, use_container_width=True)

                    # 4. Renderiza Feed de Comentários
                    with feed_placeholder.container():
                        st.subheader("💬 Feed ao Vivo - Últimos Comentários")
                        
                        # Exibe em formato de tabela estilizada ou cards
                        for idx, row in df_feed.head(10).iterrows():
                            # Define cores baseadas no sentimento
                            sent_label = row['sentiment']
                            if sent_label == 'Positivo':
                                border_color = '#2ecc71'
                                bg_color = '#142c1e'
                            elif sent_label == 'Negativo':
                                border_color = '#e74c3c'
                                bg_color = '#311818'
                            else:
                                border_color = '#95a5a6'
                                bg_color = '#202227'
                                
                            st.markdown(f"""
                                <div style="border-left: 5px solid {border_color}; background-color: {bg_color}; padding: 12px; margin-bottom: 8px; border-radius: 4px;">
                                    <strong>/u/{row['author']}</strong> <small style='color: #8892b0;'>às {row['received_at']}</small><br/>
                                    <p style="margin: 6px 0; font-size: 0.95rem;">{row['body']}</p>
                                    <span style="font-size: 0.8rem; background-color: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 3px;">Sentimento: {sent_label} (Score: {row['sentiment_score']})</span>
                                </div>
                            """, unsafe_allow_html=True)
                
                # Pequena pausa para evitar sobrecarga de CPU na renderização do app
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()
            st.sidebar.warning("Monitoramento encerrado.")
else:
    st.info("💡 Clique no botão **'Iniciar Monitoramento'** na barra lateral para começar a escutar as mensagens do Kafka em tempo real!")
    
    # Se já houver dados na memória de sessões anteriores, renderiza os gráficos estaticamente
    if st.session_state['comentarios']:
        df_feed = pd.DataFrame(st.session_state['comentarios'])
        st.subheader("Histórico Carregado em Memória")
        st.dataframe(df_feed[['received_at', 'author', 'sentiment', 'body']].head(20), use_container_width=True)
