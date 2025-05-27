import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Título do app
st.title("Dashboard de Manutenção - MUSA")

# Carregar a planilha atualizada
df = pd.read_excel("planilha_equipamento_musa.xlsx")

# Limpeza e preparo dos dados
df = df.dropna(subset=['Equipamento'])
df['Compartimento'] = df['Compartimento'].astype(str).str.strip()
df['DF'] = pd.to_numeric(df['DF'], errors='coerce')

# Filtros por Ano e Mês
anos = sorted(df['ANO'].dropna().unique())
ano_selecionado = st.selectbox("Escolha o Ano", anos)
meses = sorted(df[df['ANO'] == ano_selecionado]['MÊS'].dropna().unique())
mes_selecionado = st.selectbox("Escolha o Mês", meses)

df_filtrado = df[(df['ANO'] == ano_selecionado) &
                 (df['MÊS'] == mes_selecionado)]

# Indicadores
st.subheader("Indicadores Gerais")
st.metric(label="Média DF Geral", value=f"{df_filtrado['DF'].mean():.2%}")
st.metric(label="Total de OS", value=df_filtrado.shape[0])
st.metric(label="Equipamento com Pior DF", value=df_filtrado.groupby(
    'Equipamento')['DF'].mean().idxmin())

# Seção de Disponibilidade Física
st.subheader("Disponibilidade Física por Equipamento")
df_disponibilidade = df_filtrado.groupby(
    'Equipamento')['DF'].mean().reset_index()
df_disponibilidade = df_disponibilidade.sort_values(by='DF', ascending=False)

fig1 = px.bar(df_disponibilidade, x='Equipamento', y='DF',
              labels={'DF': 'Disponibilidade Física (%)'},
              title='DF Média por Equipamento')
fig1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig1)

# Seção de Pareto dos Defeitos
st.subheader("Gráfico de Pareto - Compartimentos com Mais Ocorrências")
df_pareto = df_filtrado['Compartimento'].value_counts().reset_index()
df_pareto.columns = ['Compartimento', 'Ocorrências']
df_pareto['Acumulado'] = df_pareto['Ocorrências'].cumsum()
df_pareto['% Acumulado'] = 100 * \
    df_pareto['Acumulado'] / df_pareto['Ocorrências'].sum()

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

# Histórico por Equipamento
st.subheader("Histórico de Falhas por Equipamento")
equipamento_selecionado = st.selectbox(
    "Selecionar Equipamento", df_filtrado['Equipamento'].unique())
st.dataframe(df_filtrado[df_filtrado['Equipamento'] == equipamento_selecionado][[
             'MÊS', 'ANO', 'Compartimento', 'OBS']])

# Exportar dados filtrados
st.subheader("Exportar Dados Filtrados")
if st.button("Exportar para Excel"):
    output = io.BytesIO()
    df_filtrado.to_excel(output, index=False)
    st.download_button("Baixar Excel", data=output.getvalue(),
                       file_name="dados_filtrados.xlsx")

st.success("Dashboard atualizado com filtros, indicadores e exportação de dados!")


# Seção de Disponibilidade Física
st.subheader("Disponibilidade Física por Equipamento")
df_disponibilidade = df.groupby('Equipamento')['DF'].mean().reset_index()
df_disponibilidade = df_disponibilidade.sort_values(by='DF', ascending=False)

fig1 = px.bar(df_disponibilidade, x='Equipamento', y='DF',
              labels={'DF': 'Disponibilidade Física (%)'},
              title='DF Média por Equipamento')
fig1.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig1)

# Seção de Pareto dos Defeitos
st.subheader("Gráfico de Pareto - Compartimentos com Mais Ocorrências")
df_pareto = df['Compartimento'].value_counts().reset_index()
df_pareto.columns = ['Compartimento', 'Ocorrências']
df_pareto['Acumulado'] = df_pareto['Ocorrências'].cumsum()
df_pareto['% Acumulado'] = 100 * \
    df_pareto['Acumulado'] / df_pareto['Ocorrências'].sum()

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

st.success(
    "Dashboard carregado com sucesso usando os dados da planilha_equipamento_musa.xlsx")


# cd C:\Users\Kikolândia\Desktop\Projeto_skava\dashboard_kiko
# venv\Scripts\activate
# python -m streamlit run app.py
# dir

# git rm nome-do-arquivo-antigo.xlsx
# git commit -m "dados_equipamentos.xlsx"
# git push origin master
