import streamlit as st
import pandas as pd

st.set_page_config(page_title="Catalogue Boutté", layout="wide")

@st.cache_data
def charger_donnees():
    return pd.read_excel("Produits boutté.xlsx")

df = charger_donnees()

st.title("🔍 Catalogue Boutté - Recherche Produits")

recherche = st.text_input("🔎 Rechercher (valeur présente dans n'importe quelle colonne)")

if recherche:
    # Filtrer
    mask = df.apply(lambda row: row.astype(str).str.contains(recherche, case=False, na=False).any(), axis=1)
    resultats = df[mask].copy()

    # Surlignage
    def surligner(val):
        val_str = str(val)
        if recherche.lower() in val_str.lower():
            return f"background-color: yellow"
        return ""

    styled = resultats.style.applymap(surligner)
    st.write(f"🔍 Résultats pour : `{recherche}`")
    st.dataframe(styled, use_container_width=True)
else:
    st.dataframe(df.head(50), use_container_width=True)
