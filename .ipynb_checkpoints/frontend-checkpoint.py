{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "5a6f1a65-89f4-4d28-a94a-f30ff56de961",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'streamlit'",
     "output_type": "error",
     "traceback": [
      "\u001b[31m---------------------------------------------------------------------------\u001b[39m",
      "\u001b[31mModuleNotFoundError\u001b[39m                       Traceback (most recent call last)",
      "\u001b[36mCell\u001b[39m\u001b[36m \u001b[39m\u001b[32mIn[1]\u001b[39m\u001b[32m, line 3\u001b[39m\n\u001b[32m      1\u001b[39m \u001b[38;5;66;03m# frontend.py\u001b[39;00m\n\u001b[32m----> \u001b[39m\u001b[32m3\u001b[39m \u001b[38;5;28;01mimport\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[34;01mstreamlit\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mas\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[34;01mst\u001b[39;00m\n\u001b[32m      4\u001b[39m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[34;01mowlready2\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m *\n\u001b[32m      6\u001b[39m \u001b[38;5;66;03m# Charger l'ontologie\u001b[39;00m\n",
      "\u001b[31mModuleNotFoundError\u001b[39m: No module named 'streamlit'"
     ]
    }
   ],
   "source": [
    "# frontend.py\n",
    "\n",
    "import streamlit as st\n",
    "from owlready2 import *\n",
    "\n",
    "# Charger l'ontologie\n",
    "onto = get_ontology(\"banque_fraude.owl\").load()\n",
    "\n",
    "st.set_page_config(page_title=\"Détection de Fraude Bancaire\", page_icon=\"💳\")\n",
    "\n",
    "st.title(\"💳 Système de Détection de Fraudes Bancaires\")\n",
    "\n",
    "st.write(\"Veuillez entrer les informations du client et de la transaction :\")\n",
    "\n",
    "# Formulaire utilisateur\n",
    "with st.form(\"formulaire_fraude\"):\n",
    "    pays = st.text_input(\"Pays du client\", placeholder=\"ex: France, Iran, etc.\")\n",
    "    solde = st.number_input(\"Solde du compte (€)\", min_value=0.0, format=\"%.2f\")\n",
    "    montant = st.number_input(\"Montant de la transaction (€)\", min_value=0.0, format=\"%.2f\")\n",
    "    devise = st.selectbox(\"Devise\", options=[\"EUR\", \"USD\", \"GBP\", \"Autre\"])\n",
    "    date = st.date_input(\"Date de la transaction\")\n",
    "    heure = st.time_input(\"Heure de la transaction\")\n",
    "    \n",
    "    bouton_envoyer = st.form_submit_button(\"Vérifier la Transaction\")\n",
    "\n",
    "# Traitement après clic\n",
    "if bouton_envoyer:\n",
    "    with onto:\n",
    "        # Créer un nouveau client\n",
    "        client = onto.Personne(f\"client_{pays}_{solde}\")\n",
    "        client.pays = pays\n",
    "        \n",
    "        # Créer un compte bancaire\n",
    "        compte = onto.CompteBancaire(f\"compte_{pays}_{solde}\")\n",
    "        compte.solde = solde\n",
    "        client.possede.append(compte)\n",
    "        \n",
    "        # Créer une transaction\n",
    "        transaction = onto.Transaction(f\"transaction_{pays}_{montant}\")\n",
    "        transaction.montant = montant\n",
    "        transaction.devise = devise\n",
    "        datetime_iso = f\"{date}T{heure}\"\n",
    "        transaction.dateTransaction = datetime_iso\n",
    "        compte.effectueTransaction.append(transaction)\n",
    "\n",
    "    # Détection de fraude selon les règles de l'article\n",
    "    fraude = False\n",
    "    if (transaction.montant > 13000) and (client.pays.lower() == \"iran\") and (compte.solde < 10000):\n",
    "        fraude = True\n",
    "\n",
    "    # Résultat\n",
    "    st.subheader(\"🔎 Résultat de l'analyse :\")\n",
    "    if fraude:\n",
    "        st.error(\"⚠️ Transaction suspecte détectée selon les critères de fraude !\")\n",
    "    else:\n",
    "        st.success(\"✅ Transaction normale.\")\n",
    "\n",
    "    # Sauvegarder les modifications\n",
    "    onto.save(file=\"banque_fraude_modified.owl\", format=\"rdfxml\")\n",
    "    st.info(\"Ontologie mise à jour et sauvegardée sous 'banque_fraude_modified.owl'.\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9b115871-0df0-4e7b-bfb0-80ba83f48d4f",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
