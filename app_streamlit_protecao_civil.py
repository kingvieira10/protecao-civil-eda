import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import geopandas as gpd
from pathlib import Path

# ================================
# CONFIGURAÇÃO GLOBAL
# ================================
st.set_page_config(page_title="Proteção Civil – EDA", layout="wide")

mpl.rcParams.update({
    "figure.figsize": (3.5, 2.8),
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
})

sns.set_style("whitegrid")

st.title("🚨 Análise de Ocorrências – Proteção Civil (2016–2020)")
st.markdown("Aplicação académica – Fundamentos de Ciência de Dados")
st.markdown("Hélder Vieira nº23678    Bruno Barros nº3547")

# ================================
# ESTADO DA APLICAÇÃO
# ================================
if "active_tab" not in st.session_state:
    st.session_state.active_tab = 0

# ================================
# CAMINHO DOS DADOS
# ================================
DATA_DIR = Path(r"C:/Users/Daniel/Desktop/projetofcd/data")

# ================================
# CARREGAMENTO DOS DADOS
# ================================
@st.cache_data
def carregar_dados(pasta):
    dfs = []
    for f in pasta.glob("*.csv"):
        df = pd.read_csv(f, low_memory=False)

        df["DataOcorrencia"] = pd.to_datetime(
            df["DataOcorrencia"], dayfirst=True, errors="coerce"
        )

        for col in ["Latitude", "Longitude"]:
            df[col] = (
                df[col].astype(str)
                .str.replace(",", ".", regex=False)
                .astype(float)
            )

        for col in [
            "NumeroOperacionaisTerrestresEnvolvidos",
            "NumeroMeiosTerrestresEnvolvidos",
            "NumeroOperacionaisAereosEnvolvidos",
            "NumeroMeiosAereosEnvolvidos",
        ]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        dfs.append(df)

    df = pd.concat(dfs, ignore_index=True)
    df = df.dropna(subset=["DataOcorrencia"])
    df["Ano"] = df["DataOcorrencia"].dt.year
    df["Mes"] = df["DataOcorrencia"].dt.month
    df["Hora"] = df["DataOcorrencia"].dt.hour
    return df


df = carregar_dados(DATA_DIR)
st.success(f"Dados carregados: {len(df)} ocorrências")

# ================================
# MAPA BASE PORTUGAL
# ================================
@st.cache_data
def carregar_mapa_portugal():
    url = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
    world = gpd.read_file(url)
    return world[world["NAME"] == "Portugal"]


mapa_pt = carregar_mapa_portugal()

# ================================
# TABS (COM ESTADO)
# ================================
tab_labels = [
    "📊 Temporal",
    "🗺️ Geografia",
    "🌡️ Mapa de Calor",
    "🔥 Incêndios",
    "🏋️ Esforço",
    "📌 Conclusões",
]

tabs = st.tabs(tab_labels)

# ================================
# TAB TEMPORAL
# ================================
with tabs[0]:
    st.session_state.active_tab = 0
    st.subheader("Análise Temporal")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        sns.countplot(x="Ano", data=df, ax=ax)
        ax.set_title("Ocorrências por Ano")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        sns.countplot(x="Mes", data=df, ax=ax)
        ax.set_title("Ocorrências por Mês")
        st.pyplot(fig)

    col3, col4 = st.columns(2)

    with col3:
        fig, ax = plt.subplots()
        sns.histplot(df["Hora"], bins=24, ax=ax)
        ax.set_title("Distribuição Horária")
        st.pyplot(fig)

    with col4:
        st.empty()

    st.markdown("### Evolução das Ocorrências por Distrito e Ano")

    tabela = df.groupby(["Distrito", "Ano"]).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(tabela, cmap="Reds", annot=True, fmt="d", linewidths=0.4, ax=ax)
    st.pyplot(fig)

# ================================
# TAB GEOGRAFIA
# ================================
with tabs[1]:
    st.session_state.active_tab = 1
    st.subheader("Distribuição Geográfica")

    ano_sel = st.selectbox("Ano", sorted(df["Ano"].unique()), key="geo_ano")
    nat_sel = st.selectbox(
        "Tipo de Ocorrência",
        sorted(df["Natureza"].dropna().unique()),
        key="geo_nat"
    )

    df_f = df[(df["Ano"] == ano_sel) & (df["Natureza"] == nat_sel)]
    top20 = df_f["Concelho"].value_counts().head(20)

    fig, ax = plt.subplots()
    sns.barplot(x=top20.values, y=top20.index, ax=ax)
    ax.set_title(f"Top 20 Concelhos – {nat_sel} ({ano_sel})")
    st.pyplot(fig)

# ================================
# TAB MAPA DE CALOR
# ================================
with tabs[2]:
    st.session_state.active_tab = 2
    st.subheader("Mapa de Calor")

    anos = sorted(df["Ano"].unique())
    opcoes = anos + [f"Total {a}" for a in anos]

    ano_heat = st.selectbox("Ano", opcoes, key="heat_ano")
    nat_heat = st.selectbox(
        "Tipo de Ocorrência",
        sorted(df["Natureza"].dropna().unique()),
        key="heat_nat"
    )

    if isinstance(ano_heat, str):
        ano_num = int(ano_heat.split()[-1])
        geo = df[df["Ano"] == ano_num]
        titulo = f"Total de Ocorrências – {ano_num}"
    else:
        geo = df[(df["Ano"] == ano_heat) & (df["Natureza"] == nat_heat)]
        titulo = f"{nat_heat} – {ano_heat}"

    geo = geo[
        geo["Latitude"].between(36, 43) &
        geo["Longitude"].between(-10, -6)
    ]

    fig, ax = plt.subplots(figsize=(4.5, 6))
    mapa_pt.plot(ax=ax, color="whitesmoke", edgecolor="black")
    ax.scatter(geo["Longitude"], geo["Latitude"], s=2, alpha=0.3, color="red")
    ax.set_title(titulo)
    ax.set_aspect("equal")
    st.pyplot(fig)

# ================================
# TAB INCÊNDIOS
# ================================
with tabs[3]:
    st.session_state.active_tab = 3
    st.subheader("Incêndios")

    df_inc = df[df["Natureza"].str.contains("Incêndio", case=False, na=False)]

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        top_inc = df_inc["Distrito"].value_counts().head(10)
        sns.barplot(x=top_inc.values, y=top_inc.index, ax=ax)
        ax.set_title("Top 10 Distritos – Incêndios")
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        top_ops = (
            df_inc.groupby("Distrito")["NumeroOperacionaisTerrestresEnvolvidos"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )
        sns.barplot(x=top_ops.values, y=top_ops.index, ax=ax)
        ax.set_title("Top 10 Distritos – Operacionais")
        st.pyplot(fig)

# ================================
# TAB ESFORÇO
# ================================
with tabs[4]:
    st.session_state.active_tab = 4
    st.subheader("Esforço Operacional")

    top5_cat = (
        df.groupby("Natureza")["NumeroOperacionaisTerrestresEnvolvidos"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    st.dataframe(top5_cat, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        sns.barplot(
            x=top5_cat["NumeroOperacionaisTerrestresEnvolvidos"],
            y=top5_cat["Natureza"],
            ax=ax
        )
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        intensidade = (
            df.groupby("Natureza")["NumeroOperacionaisTerrestresEnvolvidos"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
        )
        sns.barplot(x=intensidade.values, y=intensidade.index, ax=ax)
        st.pyplot(fig)

    fig, ax = plt.subplots()
    sns.heatmap(
        df[
            [
                "NumeroMeiosTerrestresEnvolvidos",
                "NumeroOperacionaisTerrestresEnvolvidos",
                "NumeroMeiosAereosEnvolvidos",
                "NumeroOperacionaisAereosEnvolvidos",
            ]
        ].corr(),
        annot=True,
        cmap="coolwarm",
        ax=ax,
    )
    st.pyplot(fig)

# ================================
# TAB CONCLUSÕES
# ================================
with tabs[5]:
    st.session_state.active_tab = 5
    st.subheader("Conclusões")

    st.markdown("""
    - Existem padrões temporais claros ao longo dos anos, meses e horas.
    - Os incêndios representam o maior esforço operacional.
    - A distribuição territorial é fortemente desigual.
    - Os mapas de calor identificam zonas críticas de intervenção.
    - A correlação entre meios e operacionais confirma a complexidade das ocorrências.
    """)

