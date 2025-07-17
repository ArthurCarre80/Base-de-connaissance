import streamlit as st
import pandas as pd

st.set_page_config(page_title="Catalogue Boutté", layout="wide")

@st.cache_data
def charger_donnees():
    return pd.read_excel("Produits boutté.xlsx")

df = charger_donnees()
colonnes = df.columns.str.lower()

st.title("🔍 Recherche inversée - Catalogue Boutté")

recherche = st.text_input("Tapez une valeur connue + le champ souhaité (ex : '000651 libellé', 'Lance 20x27 référence')")

def recherche_inversee(input_text):
    mots = input_text.lower().strip().split()
    if not mots:
        return pd.DataFrame()
    
    champ_cible = None
    # Identifier si un des mots correspond à une colonne
    for mot in mots:
        if mot in colonnes.values:
            champ_cible = mot
            mots.remove(mot)
            break
    
    filtre = df[df.apply(lambda row: all(any(mot in str(val).lower() for val in row) for mot in mots), axis=1)]
    
    if champ_cible:
        if champ_cible in colonnes.values:
            return filtre[[champ_cible]]
    return filtre

if recherche:
    resultat = recherche_inversee(recherche)
    if not resultat.empty:
        st.write(f"🎯 Résultat pour : `{recherche}`")
        st.dataframe(resultat, use_container_width=True)
    else:
        st.warning("Aucun résultat trouvé.")
else:
    st.info("🔎 Exemple : `000651 libellé` ou `Lance 20x27 référence`")
