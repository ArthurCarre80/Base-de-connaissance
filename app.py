import streamlit as st
import pandas as pd

# Chargement du fichier Excel
@st.cache_data
def charger_donnees():
    df = pd.read_excel("Produits boutté.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = charger_donnees()

# Fonction de recherche
def recherche_inversee(terme):
    filtre = df[df.apply(lambda row: row.astype(str).str.contains(terme, case=False, na=False).any(), axis=1)]
    return filtre

# Fonction pour surligner les résultats
def surligner(val):
    return "background-color: yellow" if isinstance(val, str) and recherche.lower() in val.lower() else ""

# Interface utilisateur
st.title("🔍 Base de Connaissance - Catalogue Boutté")
recherche = st.text_input("Entrez un mot-clé à rechercher dans tout le catalogue :")

if recherche:
    resultat = recherche_inversee(recherche)
    if not resultat.empty:
        st.write(f"🎯 Résultats pour : `{recherche}`")
        styled = resultat.style.applymap(surligner)
        st.dataframe(styled, use_container_width=True)
    else:
        st.warning("Aucun résultat trouvé.")
