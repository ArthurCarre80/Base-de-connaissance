import streamlit as st
import pandas as pd
import re

@st.cache_data
def charger_donnees():
    df = pd.read_excel("Produits boutté.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = charger_donnees()
champs_disponibles = df.columns.tolist()

# Extraction automatique du champ demandé
def extraire_champ(question):
    question_lower = question.lower()
    for champ in champs_disponibles:
        champ_simplifie = champ.replace("_", " ").replace("(", "").replace(")", "")
        if any(mot in question_lower for mot in champ_simplifie.split()):
            return champ
    return None

# Nettoyage du libellé produit supposé
def extraire_terme_recherche(question, champ_detecte):
    nettoyé = re.sub(rf"\b({champ_detecte.replace('_', ' ')})\b", "", question, flags=re.I)
    mots = re.findall(r"\w{3,}", nettoyé.lower())
    return " ".join(mots)

# Interface
st.title("🔎 Assistant Catalogue Boutté — langage naturel")
question = st.text_input("Pose une question comme : « Quel est le code EAN du nez de robinet 15x21 ? »")

if question:
    champ = extraire_champ(question)
    if not champ:
        st.warning("Je n’ai pas compris quel champ tu recherches. Reformule ou sois plus précis.")
    else:
        lib_recherche = extraire_terme_recherche(question, champ)
        resultat = df[df["libellé_du_produit_(libre)"].str.contains(lib_recherche, case=False, na=False)]

        if resultat.empty:
            st.warning(f"Aucun produit trouvé contenant : `{lib_recherche}`")
        else:
            valeur = resultat[champ].values[0]
            produit = resultat["libellé_du_produit_(libre)"].values[0]
            st.success(f"🔍 **{champ.replace('_', ' ').capitalize()}** pour **{produit}** : `{valeur}`")
