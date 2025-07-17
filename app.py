import streamlit as st
import pandas as pd
import re

@st.cache_data
def charger_donnees():
    df = pd.read_excel("Produits boutté.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = charger_donnees()

# Construction automatique d'alias pour les champs
def generer_alias(df):
    alias = {}
    for col in df.columns:
        alias_simple = col.lower()
        alias_simple = alias_simple.replace("_", " ")
        alias_simple = re.sub(r"[^a-z0-9 ]", "", alias_simple)
        mots = alias_simple.split()
        for mot in mots:
            if mot not in alias:
                alias[mot] = col
    return alias

alias_champs = generer_alias(df)

# Extraction du champ demandé
def extraire_champ(question):
    question = question.lower()
    for mot in question.split():
        mot_clean = re.sub(r"[^a-z0-9]", "", mot)
        if mot_clean in alias_champs:
            return alias_champs[mot_clean]
    return None

# Extraction du libellé recherché
def extraire_produit(question, champ_detecte):
    champ_clean = champ_detecte.replace("_", " ")
    question_sans_champ = re.sub(rf"\b{champ_clean}\b", "", question, flags=re.I)
    mots = re.findall(r"\w{3,}", question_sans_champ.lower())
    return " ".join(mots)

# Interface Streamlit
st.title("🧠 Assistant Catalogue Boutté — questions naturelles")
question = st.text_input("Exemples : Quel est le GTIN du bouchon 20x27 ? | Quelle est la matière du nez de robinet ?")

if question:
    champ = extraire_champ(question)
    if not champ:
        st.error("❌ Je n’ai pas reconnu le champ demandé. Reformule ta question.")
    else:
        produit_texte = extraire_produit(question, champ)
        resultat = df[df["libellé_du_produit_(libre)"].str.contains(produit_texte, case=False, na=False)]

        if resultat.empty:
            st.warning(f"Aucun produit trouvé correspondant à : `{produit_texte}`")
        else:
            valeur = resultat[champ].values[0]
            libelle = resultat['libellé_du_produit_(libre)'].values[0]
            st.success(f"✅ **{champ.replace('_', ' ').capitalize()}** pour **{libelle}** : `{valeur}`")
