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

generos = st.sidebar.multiselect("Gênero", df["Gênero"].unique, default=df["Gênero"].unique)

st.sidebar.image("fatec_pompeia.jpg",use_container_width=True)

if generos:
    df_filtered = df_filtered[df_filtered["Gênero"].isin(generos)]

st.title("Dashboard Fatec Pompeia")