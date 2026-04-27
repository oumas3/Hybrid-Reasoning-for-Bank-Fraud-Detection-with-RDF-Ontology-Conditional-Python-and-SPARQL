import streamlit as st
import pandas as pd
from owlready2 import *
from rdflib import Graph
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt

FRAUDE_SPARQL = "fraude_sparql.owl"
FRAUDE_PY = "fraude_python.owl"
BANQUE_BASE = "banque_fraude.owl"

def charger_ontologie(fichier):
    try:
        onto = get_ontology(fichier).load()
        return onto
    except:
        return None

def reset_ontologie(onto):
    with onto:
        for cls in onto.classes():
            for inst in list(cls.instances()):
                destroy_entity(inst)

def ajouter_fraude(p, t, onto):
    with onto:
        if not hasattr(onto, "TransactionSuspecte"):
            class TransactionSuspecte(onto.Transaction): pass
        if not hasattr(onto, "PersonneFraudeuse"):
            class PersonneFraudeuse(onto.Personne): pass
        if onto.TransactionSuspecte not in t.is_a:
            t.is_a.append(onto.TransactionSuspecte)
        if onto.PersonneFraudeuse not in p.is_a:
            p.is_a.append(onto.PersonneFraudeuse)

def est_fraude(montant, solde, pays):
    return (montant > 13000 and pays.lower() == "iran" and solde < 10000)

def afficher_statistiques(df, titre):
    st.markdown(f"### Statistiques des transactions {titre}")
    count_normales = df[df['fraude_predite'] == 0].shape[0]
    count_fraudes = df[df['fraude_predite'] == 1].shape[0]
    st.write(f"- Nombre transactions normales : {count_normales}")
    st.write(f"- Nombre transactions frauduleuses : {count_fraudes}")

    # Camembert
    labels = ['Normales', 'Fraudes']
    sizes = [count_normales, count_fraudes]
    colors = ['#4CAF50', '#F44336']  # vert et rouge
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 14})
    ax.axis('equal')  # Cercle parfait
    st.pyplot(fig)

# --- Style CSS ---
def local_css():
    st.markdown(
        """
        <style>
        .main {
            background-color: #f7f9fc;
        }
        h1, h2, h3 {
            text-align: center;
            color: #0d3b66;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        }
        div.stButton > button {
            background-color: #0d3b66;
            color: white;
            font-weight: bold;
            width: 100%;
            height: 40px;
            border-radius: 8px;
            transition: background-color 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #144d85;
            color: #f0f0f0;
        }
        .dataframe {
            font-size: 12px;
        }
        </style>
        """, unsafe_allow_html=True
    )

local_css()

st.title("💳 Détection de Fraude Bancaire")

# Sidebar menu
st.sidebar.title("Menu")
onglet = st.sidebar.radio("Choisissez une section :", [
    "Formulaire SPARQL", "CSV SPARQL", "Évaluation SPARQL",
    "Formulaire Python", "CSV Python", "Évaluation Python"
])

help_text = {
    "Formulaire SPARQL": "Remplissez les informations pour une transaction unique via ontologie SPARQL.",
    "CSV SPARQL": "Téléchargez un fichier CSV pour analyser plusieurs transactions avec SPARQL.",
    "Évaluation SPARQL": "Évaluez vos prédictions SPARQL avec un fichier CSV d’évaluation.",
    "Formulaire Python": "Remplissez les informations pour une transaction unique via ontologie Python.",
    "CSV Python": "Téléchargez un fichier CSV pour analyser plusieurs transactions avec Python.",
    "Évaluation Python": "Évaluez vos prédictions Python avec un fichier CSV d’évaluation."
}
st.sidebar.markdown(f"**Info :** {help_text[onglet]}")

st.markdown("---")

if onglet == "Formulaire SPARQL":
    st.header("Formulaire SPARQL")
    with st.form("formulaire_sparql", clear_on_submit=True):
        prenom = st.text_input("Prénom")
        nom = st.text_input("Nom")
        pays = st.text_input("Pays")
        solde = st.number_input("Solde", min_value=0.0)
        montant = st.number_input("Montant", min_value=0.0)
        devise = st.selectbox("Devise", ["EUR", "USD", "GBP"])
        date = st.date_input("Date")
        heure = st.time_input("Heure")
        valider = st.form_submit_button("Valider")

    if valider:
        onto = charger_ontologie(FRAUDE_SPARQL)
        if onto:
            reset_ontologie(onto)
            with onto:
                pid = f"p_{prenom}_{nom}".replace(" ", "_")
                cid = f"c_{prenom}_{nom}".replace(" ", "_")
                tid = f"t_{prenom}_{nom}".replace(" ", "_")
                p = onto.Personne(pid)
                p.Prenom = [prenom]
                p.Nom = [nom]
                p.pays = [pays]
                c = onto.CompteBancaire(cid)
                c.solde = [solde]
                p.possede.append(c)
                t = onto.Transaction(tid)
                t.montant = [montant]
                t.devise = [devise]
                t.dateTransaction = [f"{date}T{heure}"]
                c.effectueTransaction.append(t)

                if est_fraude(montant, solde, pays):
                    ajouter_fraude(p, t, onto)

            onto.save(file=FRAUDE_SPARQL, format="rdfxml")

            g = Graph()
            g.parse(FRAUDE_SPARQL)
            query = """
            PREFIX : <http://www.semanticweb.org/ontologies/banque_fraude#>
            SELECT ?transaction WHERE {
                ?t a :Transaction ;
                   :montant ?montant ;
                   :devise ?devise .
                ?c a :CompteBancaire ;
                   :effectueTransaction ?t ;
                   :solde ?solde .
                ?p a :Personne ;
                   :pays ?pays ;
                   :possede ?c .
                FILTER(?montant > 13000 && ?solde < 10000 && lcase(str(?pays)) = "iran")
                BIND(str(?t) AS ?transaction)
            }
            """
            results = list(g.query(query))
            if results:
                st.error("🚨 Transaction frauduleuse détectée !")
            else:
                st.success("✅ Transaction normale")

elif onglet == "CSV SPARQL":
    st.header("Analyse CSV via SPARQL")
    fichier = st.file_uploader("Uploader un CSV avec colonnes : prenom, nom, pays, solde, montant, devise, date, heure")
    if fichier:
        try:
            df = pd.read_csv(fichier)
            df.fillna("", inplace=True)
        except Exception as e:
            st.error(f"Erreur lecture CSV : {e}")
            st.stop()

        required_cols = ['prenom', 'nom', 'pays', 'solde', 'montant', 'devise', 'date', 'heure']
        if not all(col in df.columns for col in required_cols):
            st.error("❌ Le fichier doit contenir toutes les colonnes demandées.")
            st.stop()

        onto = charger_ontologie(FRAUDE_SPARQL)
        if onto:
            reset_ontologie(onto)
            normales = []
            fraudes = []

            progress = st.progress(0, text="Traitement des transactions...")

            with onto:
                total = len(df)
                for i, row in df.iterrows():
                    try:
                        pid = f"p_{i}"
                        cid = f"c_{i}"
                        tid = f"t_{i}"
                        p = onto.Personne(pid)
                        p.Prenom = [str(row['prenom'])]
                        p.Nom = [str(row['nom'])]
                        p.pays = [str(row['pays'])]
                        c = onto.CompteBancaire(cid)
                        c.solde = [float(row['solde'])]
                        p.possede.append(c)
                        t = onto.Transaction(tid)
                        t.montant = [float(row['montant'])]
                        t.devise = [str(row['devise'])]
                        t.dateTransaction = [f"{row['date']}T{row['heure']}"]
                        c.effectueTransaction.append(t)

                        if est_fraude(float(row['montant']), float(row['solde']), row['pays']):
                            ajouter_fraude(p, t, onto)
                            row['fraude_predite'] = 1
                            fraudes.append(row)
                        else:
                            row['fraude_predite'] = 0
                            normales.append(row)

                        progress.progress((i + 1) / total, text=f"{i+1}/{total} transactions traitées")
                    except Exception as e:
                        st.warning(f"Ligne {i} ignorée : {e}")

            onto.save(file=FRAUDE_SPARQL, format="rdfxml")

            st.success(f"✅ Terminé : {len(normales)} normales, {len(fraudes)} frauduleuses")

            if normales:
                st.markdown("### ✅ Transactions normales")
                st.dataframe(pd.DataFrame(normales), use_container_width=True)
            if fraudes:
                st.markdown("### 🚨 Transactions frauduleuses")
                st.dataframe(pd.DataFrame(fraudes), use_container_width=True)

            df_eval = pd.concat([pd.DataFrame(normales), pd.DataFrame(fraudes)])
            afficher_statistiques(df_eval, "SPARQL")

elif onglet == "Évaluation SPARQL":
    st.header("Évaluation SPARQL")
    eval_file = st.file_uploader("Charger fichier CSV d'évaluation SPARQL (fraude_reelle, fraude_predite)", type=["csv"])
    if eval_file:
        df_eval = pd.read_csv(eval_file)
        if 'fraude_predite' in df_eval.columns and 'fraude_reelle' in df_eval.columns:
            y_pred = df_eval['fraude_predite']
            y_true = df_eval['fraude_reelle']

            st.markdown("#### 📈 Rapport d'évaluation")
            st.text(classification_report(y_true, y_pred, digits=3))

            acc = accuracy_score(y_true, y_pred)
            st.metric("Exactitude", f"{acc:.2%}")

            cm = confusion_matrix(y_true, y_pred)
            st.markdown("#### 📊 Matrice de confusion")
            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
            ax.set_xlabel("Prédit")
            ax.set_ylabel("Réel")
            st.pyplot(fig)
        else:
            st.error("Le fichier doit contenir les colonnes : fraude_reelle, fraude_predite")

elif onglet == "Formulaire Python":
    st.header("Formulaire Python")
    with st.form("formulaire_python", clear_on_submit=True):
        prenom_py = st.text_input("Prénom")
        nom_py = st.text_input("Nom")
        pays_py = st.text_input("Pays")
        solde_py = st.number_input("Solde", min_value=0.0)
        montant_py = st.number_input("Montant", min_value=0.0)
        devise_py = st.selectbox("Devise", ["EUR", "USD", "GBP"])
        date_py = st.date_input("Date")
        heure_py = st.time_input("Heure")
        valider_py = st.form_submit_button("Valider")

    if valider_py:
        onto_py = charger_ontologie(FRAUDE_PY)
        if onto_py:
            reset_ontologie(onto_py)
            with onto_py:
                pid = f"p_{prenom_py}_{nom_py}".replace(" ", "_")
                cid = f"c_{prenom_py}_{nom_py}".replace(" ", "_")
                tid = f"t_{prenom_py}_{nom_py}".replace(" ", "_")
                p = onto_py.Personne(pid)
                p.Prenom = [prenom_py]
                p.Nom = [nom_py]
                p.pays = [pays_py]
                c = onto_py.CompteBancaire(cid)
                c.solde = [solde_py]
                p.possede.append(c)
                t = onto_py.Transaction(tid)
                t.montant = [montant_py]
                t.devise = [devise_py]
                t.dateTransaction = [f"{date_py}T{heure_py}"]
                c.effectueTransaction.append(t)

                if est_fraude(montant_py, solde_py, pays_py):
                    ajouter_fraude(p, t, onto_py)

            onto_py.save(file=FRAUDE_PY, format="rdfxml")

            g_py = Graph()
            g_py.parse(FRAUDE_PY)
            query_py = """
            PREFIX : <http://www.semanticweb.org/ontologies/banque_fraude#>
            SELECT ?transaction WHERE {
                ?t a :Transaction ;
                   :montant ?montant ;
                   :devise ?devise .
                ?c a :CompteBancaire ;
                   :effectueTransaction ?t ;
                   :solde ?solde .
                ?p a :Personne ;
                   :pays ?pays ;
                   :possede ?c .
                FILTER(?montant > 13000 && ?solde < 10000 && lcase(str(?pays)) = "iran")
                BIND(str(?t) AS ?transaction)
            }
            """
            results_py = list(g_py.query(query_py))
            if results_py:
                st.error("🚨 Transaction frauduleuse détectée (Python) !")
            else:
                st.success("✅ Transaction normale (Python)")

elif onglet == "CSV Python":
    st.header("Analyse CSV via Python")
    fichier_py = st.file_uploader("Uploader un CSV avec colonnes : prenom, nom, pays, solde, montant, devise, date, heure")
    if fichier_py:
        try:
            df_py = pd.read_csv(fichier_py)
            df_py.fillna("", inplace=True)
        except Exception as e:
            st.error(f"Erreur lecture CSV : {e}")
            st.stop()

        required_cols = ['prenom', 'nom', 'pays', 'solde', 'montant', 'devise', 'date', 'heure']
        if not all(col in df_py.columns for col in required_cols):
            st.error("❌ Le fichier doit contenir toutes les colonnes demandées.")
            st.stop()

        onto_py = charger_ontologie(FRAUDE_PY)
        if onto_py:
            reset_ontologie(onto_py)
            normales_py = []
            fraudes_py = []

            progress_py = st.progress(0, text="Traitement des transactions...")

            with onto_py:
                total_py = len(df_py)
                for i, row in df_py.iterrows():
                    try:
                        pid = f"p_{i}"
                        cid = f"c_{i}"
                        tid = f"t_{i}"
                        p = onto_py.Personne(pid)
                        p.Prenom = [str(row['prenom'])]
                        p.Nom = [str(row['nom'])]
                        p.pays = [str(row['pays'])]
                        c = onto_py.CompteBancaire(cid)
                        c.solde = [float(row['solde'])]
                        p.possede.append(c)
                        t = onto_py.Transaction(tid)
                        t.montant = [float(row['montant'])]
                        t.devise = [str(row['devise'])]
                        t.dateTransaction = [f"{row['date']}T{row['heure']}"]
                        c.effectueTransaction.append(t)

                        if est_fraude(float(row['montant']), float(row['solde']), row['pays']):
                            ajouter_fraude(p, t, onto_py)
                            row['fraude_predite'] = 1
                            fraudes_py.append(row)
                        else:
                            row['fraude_predite'] = 0
                            normales_py.append(row)

                        progress_py.progress((i + 1) / total_py, text=f"{i+1}/{total_py} transactions traitées")
                    except Exception as e:
                        st.warning(f"Ligne {i} ignorée : {e}")

            onto_py.save(file=FRAUDE_PY, format="rdfxml")

            st.success(f"✅ Terminé : {len(normales_py)} normales, {len(fraudes_py)} frauduleuses")

            if normales_py:
                st.markdown("### ✅ Transactions normales (Python)")
                st.dataframe(pd.DataFrame(normales_py), use_container_width=True)
            if fraudes_py:
                st.markdown("### 🚨 Transactions frauduleuses (Python)")
                st.dataframe(pd.DataFrame(fraudes_py), use_container_width=True)

            df_eval_py = pd.concat([pd.DataFrame(normales_py), pd.DataFrame(fraudes_py)])
            afficher_statistiques(df_eval_py, "Python")

elif onglet == "Évaluation Python":
    st.header("Évaluation Python")
    eval_file_py = st.file_uploader("Charger fichier CSV d'évaluation Python (fraude_reelle, fraude_predite)", type=["csv"])
    if eval_file_py:
        df_eval_py = pd.read_csv(eval_file_py)
        if 'fraude_predite' in df_eval_py.columns and 'fraude_reelle' in df_eval_py.columns:
            y_pred_py = df_eval_py['fraude_predite']
            y_true_py = df_eval_py['fraude_reelle']

            st.markdown("#### 📈 Rapport d'évaluation")
            st.text(classification_report(y_true_py, y_pred_py, digits=3))

            acc_py = accuracy_score(y_true_py, y_pred_py)
            st.metric("Exactitude", f"{acc_py:.2%}")

            cm_py = confusion_matrix(y_true_py, y_pred_py)
            st.markdown("#### 📊 Matrice de confusion")
            fig_py, ax_py = plt.subplots()
            sns.heatmap(cm_py, annot=True, fmt="d", cmap="Blues", ax=ax_py)
            ax_py.set_xlabel("Prédit")
            ax_py.set_ylabel("Réel")
            st.pyplot(fig_py)
        else:
            st.error("Le fichier doit contenir les colonnes : fraude_reelle, fraude_predite")
