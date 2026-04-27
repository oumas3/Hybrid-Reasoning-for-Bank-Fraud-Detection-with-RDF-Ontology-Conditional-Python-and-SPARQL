<<<<<<< HEAD
#  Titre du projet
Détection de Fraudes Bancaires par Ontologie, Règles SWRL et Raisonnement Python

---

##  1. Description du projet

Ce projet met en œuvre une solution hybride de détection automatique des fraudes bancaires en combinant :

- Une ontologie OWL pour structurer les entités (`Personne`, `CompteBancaire`, `Transaction`)
- Des règles métier appliquées via deux méthodes :
  - Raisonnement conditionnel en Python
  - Requêtes SPARQL sur les données RDF
- La bibliothèque Owlready2 pour manipuler dynamiquement l’ontologie
- Une interface Web interactive développée avec Streamlit
- Des fichiers CSV pour l'import, l’analyse, et l’évaluation des transactions

---

##  2. Objectifs

- Détecter automatiquement les fraudes bancaires selon des critères métier
- Comparer deux méthodes de détection (Python conditionnel et SPARQL)
- Visualiser les résultats en temps réel
- Calculer des métriques d’évaluation : précision, rappel, F1-score
- Offrir une interface conviviale pour les utilisateurs non techniques

---

##  3. Structure des fichiers
fraude/
├── app.py # Interface Web Streamlit
├── banque_fraude.owl # Fichier OWL (ontologie)
├──fraude_python.owl # Fichier OWL (ontologie)
├──fraude_sparql.owl # Fichier OWL (ontologie)
├── transactions.csv # Fichier pour détection de fraude
├── test_fraude.csv # Fichier pour l’évaluation (avec colonnes Réel vs Prédit)
├── requirements.txt # Dépendances à installer
└── README.md # Ce fichier d’explication


---

## Objectif du projet


La détection repose sur une règle simple, commune aux deux approches :

> Si une `Personne` effectue une `Transaction` dont le montant > 13 000 €,  
> et que cette `Personne` est située en "Iran",  
> et que son `CompteBancaire` a un solde < 10 000 € →  
> alors la transaction est considérée comme frauduleuse.

---

## Étapes pour exécuter le projet

### 1. Installer les bibliothèques nécessaires

```bash
pip install -r requirements.txt


## Utilisation de l'application

L’application s’ouvre automatiquement dans le navigateur.

###  Onglet 1 – Entrée manuelle python

- Saisir :  
  - le pays de la Personne  
  - le solde de son CompteBancaire  
  - le montant de la Transaction  

- Le système applique la règle métier :  
  > Si montant > 13 000 €, pays = Iran, solde < 10 000 € →  fraude  

- Résultat affiché immédiatement dans l’interface.

### Onglet 2 – Analyse via fichier CSV python 

- Charger le fichier `transactions.csv`.  
  

Fonctionnalités :  
- Télécharger toutes les transactions annotées  
- Télécharger uniquement les fraudes  
- Voir des graphes (fraudes par pays)

###  Onglet 3 – Entrée manuelle python-sparql

- Saisir :  
  - le pays de la Personne  
  - le solde de son CompteBancaire  
  - le montant de la Transaction  

- Le système applique la règle métier :  
  > Si montant > 13 000 €, pays = Iran, solde < 10 000 € →  fraude  

- Résultat affiché immédiatement dans l’interface.

### Onglet 4 – Analyse via fichier CSV python-sparql

- Charger le fichier `transactions.csv`.  

Fonctionnalités :  
- Télécharger toutes les transactions annotées  
- Télécharger uniquement les fraudes  
- Voir des graphes (fraudes par pays)




### Onglet 5 – Évaluation scientifique python-sparql

- Importer le fichier `test_fraude.csv`, contenant une colonne `label_reel` ("Fraude" ou "Normale").  
- Le système applique la même règle, calcule `label_detecte`.  
- Affiche :  
  - le rapport de classification : précision, rappel, F1-score  


### Onglet 6– Évaluation scientifique python-

- Importer le fichier `test_fraude.csv`, contenant une colonne `label_reel` ("Fraude" ou "Normale").  
- Le système applique la même règle, calcule `label_detecte`.  
- Affiche :  
  - le rapport de classification : précision, rappel, F1-score  

---

## Exemple de règle de détection (en Python)

```python
if montant > 13000 and pays.lower() == "iran" and solde < 10000:
    statut = "Fraude"
else:
    statut = "Normale"

## Exemple de règle de détection (requete sparql)

```sparql
PREFIX : <http://www.semanticweb.org/ontologies/banque_fraude#>
      SELECT ?transaction 
      WHERE {
                 ?t a :Transaction ;
                         :montant ?montant ;
                         :devise ?devise .
                ?c a :CompteBancaire ;
                         :effectueTransaction ?t ;
                         :solde ?solde .
       .        ?p a :Personne ;
                         :pays ?pays ;
                         :possede ?c .
       FILTER(?montant > 13000 && ?solde < 10000 && 
                  lcase(str(?pays)) = "iran")
       BIND(str(?t) AS ?transaction)


## Auteurs

- **Khaoula El Ater** 
- **Oumaima Ouayres** 


## Encadré par

Pr. CHEKRY Abderrahman
Université Cadi Ayyad – EST Safi  
🎓 Master Science des Données Analytiques (2024–2025)

=======
# Hybrid-Reasoning-for-Bank-Fraud-Detection-with-RDF-Ontology-Conditional-Python-and-SPARQL
>>>>>>> c17ab99017054a70931a8280748c6bdb854ece7a
