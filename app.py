import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


passwords = ['senha123', 'usiminas2025']
hashed_passwords = stauth.Hasher(passwords).generate()

print(hashed_passwords)


# --------------------- CONFIGURAÇÃO DE PÁGINA ---------------------
st.set_page_config(page_title="Dashboard de Manutenção - MUSA", layout="wide", initial_sidebar_state="expanded")

# --------------------- TEMA ESCURO MANUAL -------------------------
dark_style = """
<style>
    body {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .css-1v0mbdj, .css-ffhzg2 {
        background-color: #262730 !important;
        color: white;
    }
    .css-1d391kg {
        color: white;
    }
</style>
"""
st.markdown(dark_style, unsafe_allow_html=True)

# --------------------- AUTENTICAÇÃO -------------------------------
import streamlit_authenticator as stauth

names = ['Administrador', 'Supervisor']
usernames = ['admin', 'supervisor']
hashed_passwords = [
    'cole-o-hash-1-aqui',
    'cole-o-hash-2-aqui'
]

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    'dashboard_musa_cookie',
    'abcdef',
    cookie_expiry_days=1
)

)

name, authentication_status, username = authenticator.login('Login', 'sidebar')

if authentication_status is False:
    st.error('Usuário ou senha inválido')
elif authentication_status is None:
    st.warning('Por favor, insira seu usuário e senha')
elif authentication_status:
    authenticator.logout('Sair', 'sidebar')
    st.title("Dashboard de Manutenção - MUSA")

    # --------------------- IMPORTAÇÃO DE DADOS ---------------------
    df = pd.read_excel("dados_manutencao.xlsx")

    # --------------------- TRATAMENTO DE DADOS ---------------------
    df['ANO'] = df['DATA'].dt.year
    df['MÊS'] = df['DATA'].dt.month_name()
    df['TAG'] = df['EQUIPAMENTO'].str.extract(r'(\b[A-Z]+\d+\b)', expand=False)

    # --------------------- FILTROS ---------------------
    anos_disponiveis = sorted(df['ANO'].dropna().unique(), reverse=True)
    meses_disponiveis = ['Todos'] + list(df['MÊS'].dropna().unique())
    tags_disponiveis = ['Todos'] + sorted(df['TAG'].dropna().unique())

    col1, col2, col3 = st.columns(3)

    ano_selecionado = col1.selectbox("Ano", anos_disponiveis)
    mes_selecionado = col2.selectbox("Mês", meses_disponiveis)
    tag_selecionada = col3.selectbox("TAG do Equipamento", tags_disponiveis)

    df_filtrado = df[df['ANO'] == ano_selecionado]

    if mes_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['MÊS'] == mes_selecionado]
    if tag_selecionada != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['TAG'] == tag_selecionada]

    # --------------------- VISUALIZAÇÃO ---------------------
    st.subheader("Tabela de Ocorrências")
    st.dataframe(df_filtrado)

    st.subheader("Gráfico de Ocorrências por Tipo de Defeito")
    defeitos = df_filtrado['DEFEITO'].value_counts().reset_index()
    defeitos.columns = ['Defeito', 'Ocorrências']
    st.bar_chart(defeitos.set_index('Defeito'))

    st.subheader("Gráfico de Pareto - Compartimentos com Mais Ocorrências")
    compartimentos = df_filtrado['COMPARTIMENTO'].value_counts().reset_index()
    compartimentos.columns = ['Compartimento', 'Ocorrências']
    compartimentos['Acumulado'] = compartimentos['Ocorrências'].cumsum()
    compartimentos['% Acumulado'] = 100 * compartimentos['Acumulado'] / compartimentos['Ocorrências'].sum()
    st.line_chart(compartimentos.set_index('Compartimento')['% Acumulado'])





# cd C:\Users\Kikolândia\Desktop\Projeto_skava\dashboard_kiko
# venv\Scripts\activate
# python -m streamlit run app.py
# dir

# git rm nome-do-arquivo-antigo.xlsx
# git commit -m "dados_equipamentos.xlsx"
# git push origin master