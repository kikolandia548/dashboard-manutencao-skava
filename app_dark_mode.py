
import io
import pandas as pd
import streamlit as st
import plotly.express as px
import streamlit_authenticator as stauth
from PIL import Image

# Logo
logo = Image.open("logo_musa.png")
st.image(logo, width=150)

# Login
credentials = {
    "usernames": {
        "kiko": {
            "name": "Kiko",
            "password": stauth.Hasher(["senha123"]).generate()[0]
        },
        "gestor": {
            "name": "Gestor",
            "password": stauth.Hasher(["usiminas2025"]).generate()[0]
        }
    }
}

authenticator = stauth.Authenticate(credentials, "dashboard_cookie", "abcdef", cookie_expiry_days=1)
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Usuário ou senha inválido")
elif authentication_status is None:
    st.warning("Digite seu usuário e senha")
else:
    authenticator.logout("Sair", "sidebar")
    st.sidebar.success(f"Bem-vindo, {name}")

    st.title("Dashboard de Manutenção - MUSA")

    df = pd.read_excel("planilha_equipamento_musa.xlsx")
    df = df.dropna(subset=['Equipamento'])
    df['Compartimento'] = df['Compartimento'].astype(str).str.strip()
    df['DF'] = pd.to_numeric(df['DF'], errors='coerce')

    anos = sorted(df['ANO'].dropna().unique())
    ano_selecionado = st.selectbox("Escolha o Ano", anos)

    meses = sorted(df[df['ANO'] == ano_selecionado]['MÊS'].dropna().unique())
    mes_selecionado = st.selectbox("Escolha o Mês", meses)

    df_mes = df[(df['ANO'] == ano_selecionado) & (df['MÊS'] == mes_selecionado)]

    equipamentos = ['Todos'] + sorted(df_mes['Equipamento'].unique())
    equipamento_sel = st.selectbox("Filtrar por Equipamento", equipamentos)

    if equipamento_sel != 'Todos':
        df_filtrado = df_mes[df_mes['Equipamento'] == equipamento_sel]
    else:
        df_filtrado = df_mes

    st.subheader("Indicadores Gerais")
    st.metric("Média DF", f"{df_filtrado['DF'].mean():.2%}")
    st.metric("Total de OS", df_filtrado.shape[0])
    st.metric("Pior Equipamento", df_filtrado.groupby('Equipamento')['DF'].mean().idxmin())

    st.subheader("DF por Equipamento")
    df_disp = df_filtrado.groupby('Equipamento')['DF'].mean().reset_index()
    fig1 = px.bar(df_disp, x='Equipamento', y='DF', title='DF Média por Equipamento')
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1)

    st.subheader("Pareto de Defeitos")
    pareto = df_filtrado['Compartimento'].value_counts().reset_index()
    pareto.columns = ['Compartimento', 'Ocorrências']
    pareto['Acumulado'] = pareto['Ocorrências'].cumsum()
    pareto['% Acumulado'] = 100 * pareto['Acumulado'] / pareto['Ocorrências'].sum()
    fig2 = px.bar(pareto, x='Compartimento', y='Ocorrências', title='Pareto de Compartimentos')
    fig2.add_scatter(x=pareto['Compartimento'], y=pareto['% Acumulado'], mode='lines+markers', name='% Acumulado', yaxis='y2')
    fig2.update_layout(yaxis=dict(title='Ocorrências'), yaxis2=dict(overlaying='y', side='right', title='% Acumulado'), xaxis_tickangle=-45)
    st.plotly_chart(fig2)

    st.subheader("Histórico de Falhas")
    eq_sel = st.selectbox("Selecionar Equipamento", df_filtrado['Equipamento'].unique())
    st.dataframe(df_filtrado[df_filtrado['Equipamento'] == eq_sel][['MÊS', 'ANO', 'Compartimento', 'OBS']])

    st.subheader("Exportar Dados")
    if st.button("Exportar para Excel"):
        output = io.BytesIO()
        df_filtrado.to_excel(output, index=False)
        st.download_button("Baixar Excel", data=output.getvalue(), file_name="dados_filtrados.xlsx")

    st.markdown("""
        <style>
            .stApp {
                background-color: #1e1e1e;
                color: white;
            }
            .css-18e3th9 {
                padding-top: 2rem;
            }
            .block-container {
                padding: 2rem 1rem;
            }
        </style>
    """, unsafe_allow_html=True)
