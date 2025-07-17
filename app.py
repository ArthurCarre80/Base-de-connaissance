import streamlit as st
import pandas as pd

st.set_page_config(page_title="Catalogue Boutté", layout="wide")

@st.cache_data
def charger_donnees():
    return pd.read_excel("Produits boutté.xlsx")

df = charger_donnees()
colonnes = df.columns.str.lower().str.strip()

st.title("🔍 Catalogue Boutté - Recherche intelligente")

recherche = st.text_input("Exemples : 'code interne 3160140100316', 'poids 1220', 'PVC gris', 'référence 000651'")

def filtrer_lignes(query, data):
    mots = query.lower().strip().split()
    masque = pd.Series([True] * len(data))
    for mot in mots:
        present = data.astype(str).apply(lambda col: col.str.lower().str.contains(mot, na=False))
        masque &= present.any(axis=1)
    return data[masque]

if recherche:
    resultats = filtrer_lignes(recherche, df)
    st.write(f"🔍 {len(resultats)} résultat(s) pour : `{recherche}`")
    st.dataframe(resultats, use_container_width=True)
else:
    st.dataframe(df.head(50), use_container_width=True)
