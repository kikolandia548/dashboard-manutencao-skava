import io
import plotly.express as px
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image

# ===== LOGO E TEMA =====
logo = Image.open("logo_musa.png")
st.image(logo, width=150)

st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .css-1d391kg, .css-1v0mbdj, .css-1offfwp {
        background-color: #333333;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# ===== LOGIN =====
name, authentication_status, username = authenticator.login('Login', 'sidebar')

usernames = ['kiko', 'gestor']
passwords = ['senha123', 'usiminas2025']

import hashlib

# Função auxiliar para gerar hashes de senhas
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Senhas já com hash direto
hashed_passwords = [
    hash_password('senha123'),
    hash_password('usiminas2025')
]


credentials = {
    "usernames": {
        "kiko": {"name": "Kiko", "password": hashed_passwords[0]},
        "gestor": {"name": "Gestor", "password": hashed_passwords[1]},
    }
}

authenticator = stauth.Authenticate(
    credentials,
    'dashboard_musa_cookie',
    'abcdef',
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status is False:
    st.error('Usuário ou senha inválido')
elif authentication_status is None:
    st.warning('Digite seu usuário e senha')
else:
    authenticator.logout('Sair', 'sidebar')
    st.sidebar.success(f'Bem-vindo, {name}')

    # ===== CARREGAMENTO DE DADOS =====
    st.title("Dashboard de Manutenção - MUSA")
    df = pd.read_excel("planilha_equipamento_musa.xlsx")

    df = df.dropna(subset=['Equipamento'])
    df['Compartimento'] = df['Compartimento'].astype(str).str.strip()
    df['DF'] = pd.to_numeric(df['DF'], errors='coerce')

    # ===== FILTROS COM 'TODOS' =====
    st.sidebar.subheader("Filtros")
    anos = sorted(df['ANO'].dropna().unique())
    ano_selecionado = st.sidebar.selectbox("Ano", ["Todos"] + list(anos))

    meses = sorted(df['MÊS'].dropna().unique())
    mes_selecionado = st.sidebar.selectbox("Mês", ["Todos"] + list(meses))

    tags_disponiveis = df['Equipamento'].dropna().unique()
    tag_selecionada = st.sidebar.selectbox("TAG do Equipamento", ["Todos"] + list(tags_disponiveis))

    df_filtrado = df.copy()
    if ano_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['ANO'] == ano_selecionado]
    if mes_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['MÊS'] == mes_selecionado]
    if tag_selecionada != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Equipamento'] == tag_selecionada]

    # ===== INDICADORES =====
    st.subheader("Indicadores Gerais")
    st.metric(label="Média DF Geral", value=f"{df_filtrado['DF'].mean():.2%}")
    st.metric(label="Total de OS", value=df_filtrado.shape[0])
    st.metric(label="Equipamento com Pior DF", value=df_filtrado.groupby('Equipamento')['DF'].mean().idxmin())

    # ===== GRÁFICO DF =====
    st.subheader("Disponibilidade Física por Equipamento")
    df_disponibilidade = df_filtrado.groupby('Equipamento')['DF'].mean().reset_index()
    df_disponibilidade = df_disponibilidade.sort_values(by='DF', ascending=False)

    fig1 = px.bar(df_disponibilidade, x='Equipamento', y='DF',
                  labels={'DF': 'Disponibilidade Física (%)'},
                  title='DF Média por Equipamento')
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1)

    # ===== PARETO =====
    st.subheader("Gráfico de Pareto - Compartimentos com Mais Ocorrências")
    df_pareto = df_filtrado['Compartimento'].value_counts().reset_index()
    df_pareto.columns = ['Compartimento', 'Ocorrências']
    df_pareto['Acumulado'] = df_pareto['Ocorrências'].cumsum()
    df_pareto['% Acumulado'] = 100 * df_pareto['Acumulado'] / df_pareto['Ocorrências'].sum()

    fig2 = px.bar(df_pareto, x='Compartimento', y='Ocorrências',
                  title='Pareto de Compartimentos')
    fig2.add_scatter(x=df_pareto['Compartimento'], y=df_pareto['% Acumulado'],
                     mode='lines+markers', name='% Acumulado', yaxis='y2')
    fig2.update_layout(
        yaxis=dict(title='Ocorrências'),
        yaxis2=dict(overlaying='y', side='right', title='% Acumulado'),
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig2)

    # ===== HISTÓRICO =====
    st.subheader("Histórico de Falhas por Equipamento")
    equipamento_selecionado = st.selectbox(
        "Selecionar Equipamento", df_filtrado['Equipamento'].unique())
    st.dataframe(df_filtrado[df_filtrado['Equipamento'] == equipamento_selecionado][[
                 'MÊS', 'ANO', 'Compartimento', 'OBS']])

    # ===== EXPORTAÇÃO =====
    st.subheader("Exportar Dados Filtrados")
    if st.button("Exportar para Excel"):
        output = io.BytesIO()
        df_filtrado.to_excel(output, index=False)
        st.download_button("Baixar Excel", data=output.getvalue(),
                           file_name="dados_filtrados.xlsx")

    st.success("Dashboard finalizado com filtros, login e layout escuro!")




# cd C:\Users\Kikolândia\Desktop\Projeto_skava\dashboard_kiko
# venv\Scripts\activate
# python -m streamlit run app.py
# dir

# git rm nome-do-arquivo-antigo.xlsx
# git commit -m "dados_equipamentos.xlsx"
# git push origin master