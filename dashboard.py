import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Conexão com o banco de dados
USER = "postgres"
PASSWORD = "senha123"   # mesma senha que usou no docker run
HOST = "localhost"
PORT = "5232"
DB = "postgres"

# Conexão com o PostgreSQL
engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

# Função para carregar dados de uma view
def load_data(view_name):
  return pd.read_sql(f"SELECT * FROM {view_name}", engine)

# Título do dashboard
st.title('Dashboard de Temperaturas IoT')

# Gráfico 1: Média de temperatura por dispositivo
st.header('Média de Temperatura por Dispositivo')
df_avg_temp = load_data('media_temperatura_por_dispositivo')
fig1 = px.bar(df_avg_temp, x='id_dispositivo', y='media_temperatura')
st.plotly_chart(fig1)

# Gráfico 2: Contagem de leituras por hora
st.header('Variacao de temperatura por dia')
df_leituras_hora = load_data('variacao_temperatura_dia')
fig2 = px.line(df_leituras_hora, x='dia', y='temperatura')
st.plotly_chart(fig2)

# # Gráfico 3: Temperaturas máximas e mínimas por dia
st.header('Media de temperatura mensal')
df_temp_max_min = load_data('variacao_temperatura_mes')
fig3 = px.line(df_temp_max_min, x='mes', y='media_temperatura')
st.plotly_chart(fig3)