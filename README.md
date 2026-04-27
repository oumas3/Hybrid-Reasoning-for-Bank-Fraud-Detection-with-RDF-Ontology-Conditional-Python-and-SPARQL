# Hybrid Reasoning for Bank Fraud Detection
### RDF Ontology • SPARQL • Python • Streamlit

---

## Overview
This project presents a hybrid fraud detection system combining ontology-based reasoning, SPARQL querying, and Python rule-based logic to detect suspicious banking transactions.

---

## Key Idea
Instead of relying only on machine learning, this system uses:
- RDF/OWL ontology for structured knowledge
- SPARQL for semantic pattern detection
- Python rules for flexible fraud logic

---

## Architecture
User Input (CSV / Manual)
→ Streamlit Interface
→ Python (Owlready2 Engine)
→ SPARQL + Rule-Based Reasoning
→ Fraud Detection Results

---

## Technologies
- Protégé (Ontology design)
- OWL / RDF (Knowledge modeling)
- SPARQL (Query engine)
- Python (Owlready2 reasoning)
- Streamlit (Web interface)

---

## Features
- Fraud detection using semantic rules
- Hybrid reasoning (SPARQL + Python)
- CSV upload support
- Interactive dashboard

---

## How to Run
pip install owlready2 streamlit pandas

streamlit run app.py

---

## Data
Simulated banking transactions including normal and fraudulent cases.

---

## Advantages
- Explainable AI (no black box)
- Modular design
- Easy to extend rules
- Works with semantic web standards

---

## Future Work
- Integration with machine learning
- Real-world banking datasets
- Enhanced ontology expansion

---

## Authors
- Khaoula El Ater  
- Ouayres Oumaima  
- Abderrahman Chekry  

Cadi Ayyad University, Morocco
