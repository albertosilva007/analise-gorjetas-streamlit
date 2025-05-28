import streamlit as st
import pandas as pd
import altair as alt

# Título da sua aplicação
st.title("Análise de Gorjetas com Streamlit 📊")

# Carregar os dados do arquivo CSV
# Certifique-se de que o arquivo 'tip.csv' está na mesma pasta que o seu script Python,
# ou forneça o caminho completo para o arquivo.
try:
    df_tips = pd.read_csv("tip.csv")
except FileNotFoundError:
    st.error("Arquivo 'tip.csv' não encontrado. Por favor, coloque-o na mesma pasta do script ou ajuste o caminho.")
    st.stop() # Impede a execução do restante do script se o arquivo não for encontrado

# Mostrar uma amostra dos dados
if st.checkbox("Mostrar dados brutos (primeiras 5 linhas)"):
    st.subheader("Amostra dos Dados")
    st.write(df_tips.head())

st.markdown("---")

# --- Gráfico 1: Histograma da Conta Total ---
st.header("Distribuição da Conta Total")
if 'total_bill' in df_tips.columns:
    hist_total_bill = alt.Chart(df_tips).mark_bar().encode(
        alt.X('total_bill:Q', bin=alt.Bin(maxbins=20), title='Conta Total ($)'),
        alt.Y('count()', title='Frequência'),
        tooltip=[alt.X('total_bill:Q', bin=alt.Bin(maxbins=20), title='Intervalo da Conta'), 'count()']
    ).properties(
        title='Histograma da Conta Total'
    )
    st.altair_chart(hist_total_bill, use_container_width=True)
else:
    st.warning("Coluna 'total_bill' não encontrada no CSV.")

st.markdown("---")

# --- Gráfico 2: Gorjeta Média por Dia da Semana ---
st.header("Gorjeta Média por Dia da Semana")
if 'day' in df_tips.columns and 'tip' in df_tips.columns:
    # Ordenar os dias da semana (opcional, mas melhora a visualização)
    day_order = ['Thur', 'Fri', 'Sat', 'Sun'] # Ajuste se os nomes dos dias forem diferentes
    df_tips['day'] = pd.Categorical(df_tips['day'], categories=day_order, ordered=True)

    bar_tip_by_day = alt.Chart(df_tips).mark_bar().encode(
        alt.X('day:O', title='Dia da Semana', sort=day_order), # :O indica ordinal
        alt.Y('average(tip):Q', title='Gorjeta Média ($)'),
        tooltip=['day:O', alt.Y('average(tip):Q', title='Gorjeta Média', format="$.2f")]
    ).properties(
        title='Gorjeta Média por Dia da Semana'
    )
    st.altair_chart(bar_tip_by_day, use_container_width=True)
else:
    st.warning("Colunas 'day' ou 'tip' não encontradas no CSV.")

st.markdown("---")

# --- Gráfico 3: Relação entre Conta Total e Gorjeta (Gráfico de Dispersão) ---
st.header("Relação entre Conta Total e Gorjeta")
if 'total_bill' in df_tips.columns and 'tip' in df_tips.columns:
    scatter_bill_tip = alt.Chart(df_tips).mark_circle(size=60).encode(
        alt.X('total_bill:Q', title='Conta Total ($)', scale=alt.Scale(zero=False)),
        alt.Y('tip:Q', title='Gorjeta ($)', scale=alt.Scale(zero=False)),
        tooltip=['total_bill', 'tip', 'size' if 'size' in df_tips.columns else 'total_bill'] # Adiciona 'size' ao tooltip se existir
    ).properties(
        title='Conta Total vs. Gorjeta'
    ).interactive() # Permite zoom e pan no gráfico
    st.altair_chart(scatter_bill_tip, use_container_width=True)
else:
    st.warning("Colunas 'total_bill' ou 'tip' não encontradas no CSV.")

st.markdown("---")

# --- Opção para mais gráficos (exemplo com filtro) ---
st.sidebar.header("Opções de Filtro")
if 'smoker' in df_tips.columns:
    smoker_filter = st.sidebar.selectbox(
        "Filtrar por Fumante:",
        options=['Todos', 'Sim', 'Não'],
        index=0
    )

    df_filtered = df_tips.copy()
    if smoker_filter == 'Sim':
        df_filtered = df_tips[df_tips['smoker'] == 'Yes'] # Ajuste 'Yes' se o valor for diferente
    elif smoker_filter == 'Não':
        df_filtered = df_tips[df_tips['smoker'] == 'No']  # Ajuste 'No' se o valor for diferente

    if smoker_filter != 'Todos':
        st.header(f"Análise para Fumantes: {smoker_filter}")

    if 'time' in df_filtered.columns and 'tip' in df_filtered.columns:
        bar_tip_by_time_filtered = alt.Chart(df_filtered).mark_bar().encode(
            alt.X('time:N', title='Horário'), # :N indica nominal
            alt.Y('average(tip):Q', title='Gorjeta Média ($)'),
            color='time:N',
            tooltip=['time:N', alt.Y('average(tip):Q', title='Gorjeta Média', format="$.2f")]
        ).properties(
            title=f'Gorjeta Média por Horário (Fumantes: {smoker_filter})'
        )
        st.altair_chart(bar_tip_by_time_filtered, use_container_width=True)
    elif smoker_filter != 'Todos':
        st.warning("Colunas 'time' ou 'tip' não encontradas para o gráfico filtrado.")

else:
    st.sidebar.info("Coluna 'smoker' não encontrada para adicionar filtro.")


st.write("Fim da análise. Experimente com outras colunas e tipos de gráficos! ✨")