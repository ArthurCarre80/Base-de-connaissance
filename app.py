
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Catalogue Boutté", layout="wide")

@st.cache_data
def charger_donnees():
    return pd.read_excel("Produits boutté.xlsx")

df = charger_donnees()

st.title("🔍 Catalogue Boutté - Recherche Produits")

recherche = st.text_input("Rechercher un produit par libellé, code EAN ou référence")

if recherche:
    filtre = df[df.apply(lambda row: row.astype(str).str.contains(recherche, case=False).any(), axis=1)]
    st.dataframe(filtre)
else:
    st.dataframe(df.head(50))
