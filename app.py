<<<<<<< HEAD
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dash do Kiko 🚜", layout="wide")

# Cabeçalho estilizado com markdown e HTML para tamanho

st.markdown("""
<div style='text-align: center'>
    <span style='font-size:2.7em; font-weight: bold;'>DASHBOARD KIKO</span> <br>
    <span style='font-size:1.5em;'>Manutenção Eskava Minas</span>
</div>
""", unsafe_allow_html=True)


@st.cache_data
def carregar_dados():
    df = pd.read_excel("dados_equipamentos.xlsx")
    df["Tag_Equipamento"] = df["Tag_Equipamento"].str.strip().str.upper()
    df["Data_Entrada"] = pd.to_datetime(df["Data_Entrada"], errors='coerce')
    df["Mês"] = df["Data_Entrada"].dt.strftime('%Y-%m')
    return df


try:
    df = carregar_dados()
except Exception as e:
    st.error(f"Erro ao ler o Excel: {e}")
    st.stop()

# ==== FILTROS ====
meses = sorted(df["Mês"].dropna().unique())
equipamentos = sorted(df["Tag_Equipamento"].dropna().unique())

col_filtro1, col_filtro2, col_filtro3 = st.columns([2, 4, 1])
with col_filtro1:
    mes_sel = st.selectbox("Selecione o mês:", ["Todos"] + meses)
with col_filtro2:
    eq_sel = st.selectbox("Selecione o equipamento:", ["Todos"] + equipamentos)
with col_filtro3:
    filtrar = st.button("Filtrar")

# ==== APLICA FILTROS ====
df_filtro = df.copy()
if filtrar or True:  # True deixa filtrado sempre, pode trocar pra "if filtrar:" se quiser só com botão
    if mes_sel != "Todos":
        df_filtro = df_filtro[df_filtro["Mês"] == mes_sel]
    if eq_sel != "Todos":
        df_filtro = df_filtro[df_filtro["Tag_Equipamento"] == eq_sel]

# ==== CARDS ====
col1, col2, col3, col4 = st.columns(4)
col1.metric("Equipamentos cadastrados", df_filtro["Tag_Equipamento"].nunique())
col2.metric("Total de defeitos", df_filtro["Defeito"].notna().sum())
col3.metric("Registros totais", len(df_filtro))
hm = df_filtro["Horimetro_Entrada"].mean(
) if df_filtro["Horimetro_Entrada"].notna().sum() > 0 else 0
col4.metric("Horímetro Médio", f"{hm:.0f}")

st.divider()

# ==== GRÁFICOS ====
gr1, gr2 = st.columns([2, 2])

with gr1:
    # Defeitos por dia
    if not df_filtro.empty and "Data_Entrada" in df_filtro.columns:
        defeitos_dia = df_filtro.groupby("Data_Entrada")[
            "Defeito"].count().reset_index()
        fig_bar = px.bar(defeitos_dia, x="Data_Entrada", y="Defeito", title="Defeitos por Dia",
                         color_discrete_sequence=["#0099ff"])
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Sem dados para gráfico de defeitos por dia.")

with gr2:
    # Defeitos recorrentes (pizza)
    if not df_filtro.empty and "Defeito" in df_filtro.columns:
        defeitos = df_filtro["Defeito"].value_counts().reset_index()
        defeitos.columns = ["Defeito", "Quantidade"]
        fig_pie = px.pie(defeitos, values="Quantidade", names="Defeito",
                         title="Defeitos Recorrentes",
                         color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Sem dados para gráfico de defeitos.")

st.divider()

# ==== GRÁFICO EXTRA (EXEMPLO: MANUTENÇÕES POR TIPO) ====
with st.container():
    if not df_filtro.empty and "Tag_Equipamento" in df_filtro.columns:
        top_defeitos = df_filtro["Tag_Equipamento"].value_counts(
        ).reset_index().head(5)
        top_defeitos.columns = ["Equipamento", "Defeitos"]
        fig_top = px.bar(top_defeitos, x="Defeitos", y="Equipamento",
                         orientation="h", title="Top 5 Equipamentos com Mais Defeitos",
                         color="Equipamento", color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.info("Sem dados para o gráfico de equipamentos com mais defeitos.")


st.divider()
st.subheader("Tabela Detalhada dos Dados Filtrados")
st.dataframe(df_filtro, use_container_width=True)
=======
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dash do Kiko 🚜", layout="wide")

# Cabeçalho estilizado com markdown e HTML para tamanho

st.markdown("""
<div style='text-align: center'>
    <span style='font-size:2.7em; font-weight: bold;'>DASHBOARD KIKO</span> <br>
    <span style='font-size:1.5em;'>Manutenção Eskava Minas</span>
</div>
""", unsafe_allow_html=True)


@st.cache_data
def carregar_dados():
    df = pd.read_excel("dados_equipamentos.xlsx")
    df["Tag_Equipamento"] = df["Tag_Equipamento"].str.strip().str.upper()
    df["Data_Entrada"] = pd.to_datetime(df["Data_Entrada"], errors='coerce')
    df["Mês"] = df["Data_Entrada"].dt.strftime('%Y-%m')
    return df


try:
    df = carregar_dados()
except Exception as e:
    st.error(f"Erro ao ler o Excel: {e}")
    st.stop()

# ==== FILTROS ====
meses = sorted(df["Mês"].dropna().unique())
equipamentos = sorted(df["Tag_Equipamento"].dropna().unique())

col_filtro1, col_filtro2, col_filtro3 = st.columns([2, 4, 1])
with col_filtro1:
    mes_sel = st.selectbox("Selecione o mês:", ["Todos"] + meses)
with col_filtro2:
    eq_sel = st.selectbox("Selecione o equipamento:", ["Todos"] + equipamentos)
with col_filtro3:
    filtrar = st.button("Filtrar")

# ==== APLICA FILTROS ====
df_filtro = df.copy()
if filtrar or True:  # True deixa filtrado sempre, pode trocar pra "if filtrar:" se quiser só com botão
    if mes_sel != "Todos":
        df_filtro = df_filtro[df_filtro["Mês"] == mes_sel]
    if eq_sel != "Todos":
        df_filtro = df_filtro[df_filtro["Tag_Equipamento"] == eq_sel]

# ==== CARDS ====
col1, col2, col3, col4 = st.columns(4)
col1.metric("Equipamentos cadastrados", df_filtro["Tag_Equipamento"].nunique())
col2.metric("Total de defeitos", df_filtro["Defeito"].notna().sum())
col3.metric("Registros totais", len(df_filtro))
hm = df_filtro["Horimetro_Entrada"].mean(
) if df_filtro["Horimetro_Entrada"].notna().sum() > 0 else 0
col4.metric("Horímetro Médio", f"{hm:.0f}")

st.divider()

# ==== GRÁFICOS ====
gr1, gr2 = st.columns([2, 2])

with gr1:
    # Defeitos por dia
    if not df_filtro.empty and "Data_Entrada" in df_filtro.columns:
        defeitos_dia = df_filtro.groupby("Data_Entrada")[
            "Defeito"].count().reset_index()
        fig_bar = px.bar(defeitos_dia, x="Data_Entrada", y="Defeito", title="Defeitos por Dia",
                         color_discrete_sequence=["#0099ff"])
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Sem dados para gráfico de defeitos por dia.")

with gr2:
    # Defeitos recorrentes (pizza)
    if not df_filtro.empty and "Defeito" in df_filtro.columns:
        defeitos = df_filtro["Defeito"].value_counts().reset_index()
        defeitos.columns = ["Defeito", "Quantidade"]
        fig_pie = px.pie(defeitos, values="Quantidade", names="Defeito",
                         title="Defeitos Recorrentes",
                         color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Sem dados para gráfico de defeitos.")

st.divider()

# ==== GRÁFICO EXTRA (EXEMPLO: MANUTENÇÕES POR TIPO) ====
with st.container():
    if not df_filtro.empty and "Tag_Equipamento" in df_filtro.columns:
        top_defeitos = df_filtro["Tag_Equipamento"].value_counts(
        ).reset_index().head(5)
        top_defeitos.columns = ["Equipamento", "Defeitos"]
        fig_top = px.bar(top_defeitos, x="Defeitos", y="Equipamento",
                         orientation="h", title="Top 5 Equipamentos com Mais Defeitos",
                         color="Equipamento", color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.info("Sem dados para o gráfico de equipamentos com mais defeitos.")


st.divider()
st.subheader("Tabela Detalhada dos Dados Filtrados")
st.dataframe(df_filtro, use_container_width=True)
>>>>>>> b9a0b602f708e93251853e881fdf24c9cb3f1bc3
