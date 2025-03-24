import streamlit as st #transformar em página web
import pandas as pd #manipulação de dados
import plotly.express as px #gráficos dinamicos

# configuração layout 
st.set_page_config(layout="wide")
# leitura da base da dados de um arquivo .csv
df = pd.read_csv("vendas.csv", sep=";", decimal=",")

#converter a coluna Data para o formato de data
df["Data"]= pd.to_datetime(df["Data"])
df = df.sort_values("Data") #ordena pela data 

df["Mês"] = df["Data"].apply(lambda x: str(x.year) + "-" + str(x.month))

#cria um select box dentro de uma sidebar
month = st.sidebar.selectbox("Mês", df["Mês"].unique())
df_filtered = df[df["Mês"] == month]

generos = st.sidebar.multiselect("Gênero", df["Gênero"].unique(), default=df["Gênero"].unique())

st.sidebar.image("fatec_pompeia.jpg",use_container_width=True)

if generos:
    df_filtered = df_filtered[df_filtered["Gênero"].isin(generos)]

st.title("Dashboard Fatec Pompeia")

st.write("Projeto Integrador")

st.markdown("## Resumo")

total_faturamento = df_filtered["Total"].sum()
total_vendas = df_filtered.shape[0]
avaliacao_media = df_filtered["Rating"].mean()
total_produtos = df_filtered["Quantidade"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1: 
    st.metric(label="Total faturamento", value=f"R${total_faturamento:.2f}".replace(".",","))

with col2: 
    st.metric(label="Total vendas", value=total_vendas)

with col3: 
    st.metric(label="Total produtos vendidos", value=total_produtos)

with col4:
    st.metric(label="Avaliação Média", value=f"R${avaliacao_media:.2f}".replace(".",","))

col1, col2 = st.columns(2)

col3, col4, col5 = st.columns(3)

fig_date = px.bar(df_filtered, x="Data", y="Total", color="Cidade", title="faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

fig_prod = px.bar(df_filtered, x="Data", y="Linha de produto", color="Cidade", title="Faturamento por tipo de produto", orientation="h")
col2.plotly_chart(fig_prod,use_container_width=True )

city_total = df_filtered.groupby("Cidade")[["Total"]].sum().reset_index()

fig_city = px.bar(city_total, x="Cidade", y="Total", title="Faturamento por cidade")
col3.plotly_chart(fig_city, use_container_width=True)

fig_kindy = px.pie(df_filtered, values="Total", names="Pagamento", title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kindy, use_container_width=True)

fig_rating = px.bar(df_filtered, y="Rating", x="Cidade", title="Avaliação média")

col5.plotly_chart(fig_rating, use_container_width=True)