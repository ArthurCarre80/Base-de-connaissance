import pandas as pd

# Chargement du fichier Excel
FICHIER = "Produits boutté.xlsx"
df = pd.read_excel(FICHIER)

# Normalisation des noms de colonnes
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Fonction de recherche flexible
def rechercher(df, champ, valeur, correspondance="contient"):
    champ = champ.strip().lower().replace(" ", "_")
    if champ not in df.columns:
        print(f"Champ '{champ}' introuvable dans la base de données.")
        return pd.DataFrame()
    
    if correspondance == "exact":
        resultats = df[df[champ].astype(str).str.lower() == valeur.lower()]
    elif correspondance == "contient":
        resultats = df[df[champ].astype(str).str.lower().str.contains(valeur.lower(), na=False)]
    elif correspondance == "commence_par":
        resultats = df[df[champ].astype(str).str.lower().str.startswith(valeur.lower())]
    elif correspondance == "finit_par":
        resultats = df[df[champ].astype(str).str.lower().str.endswith(valeur.lower())]
    else:
        print("Type de correspondance non pris en charge.")
        return pd.DataFrame()
    
    return resultats

# Fonction d'affichage des résultats
def afficher_resultats(df_resultats, max_lignes=10):
    if df_resultats.empty:
        print("Aucun résultat trouvé.")
    else:
        print(df_resultats.head(max_lignes).to_string(index=False))
        if len(df_resultats) > max_lignes:
            print(f"... et {len(df_resultats) - max_lignes} autres résultats.")

# Interface utilisateur basique
def interface():
    print("=== Recherche Produits Boutté ===")
    while True:
        champ = input("Champ à rechercher (ou 'exit' pour quitter) : ")
        if champ.lower() == "exit":
            break
        valeur = input("Valeur à rechercher : ")
        correspondance = input("Type de correspondance (exact / contient / commence_par / finit_par) : ").strip().lower()
        if correspondance not in ["exact", "contient", "commence_par", "finit_par"]:
            correspondance = "contient"
        resultats = rechercher(df, champ, valeur, correspondance)
        afficher_resultats(resultats)

# Lancer l'interface si exécuté directement
if __name__ == "__main__":
    interface()
