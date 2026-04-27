# Hybrid Reasoning for Bank Fraud Detection

---

## Research Tags
[Paper] Hybrid Reasoning for Fraud Detection  
[Model] Ontology + Rule-Based Hybrid System  
[Framework] Owlready2 + SPARQL + Streamlit  
[Dataset] Simulated Banking Transactions Dataset  
[Task] Fraud Detection / Classification / Knowledge Reasoning  
[Domain] Financial Security / Semantic Web / AI Systems  
[License] Academic Use Only  

---

## Abstract
This project proposes a hybrid reasoning framework for detecting fraudulent banking transactions using ontology-based modeling, semantic querying, and rule-based Python logic. The system emphasizes interpretability and modularity compared to traditional machine learning approaches.

---

## Problem Statement
Traditional fraud detection systems often rely on black-box models that lack interpretability and are difficult to adapt. This project addresses these limitations through a symbolic reasoning approach combining semantic and rule-based techniques.

---

## Methodology

The system integrates three layers:

1. Ontology Layer  
   - OWL-based financial knowledge representation  

2. Semantic Layer  
   - SPARQL queries for pattern detection  

3. Reasoning Layer  
   - Python-based rule engine for dynamic fraud detection  

---

## System Architecture

User Input (Manual / CSV)
→ Streamlit Interface
→ Python Engine (Owlready2)
→ SPARQL + Rule-Based Reasoning
→ Fraud Detection Output

---

## Technologies

- Protégé (Ontology modeling)
- OWL / RDF (Knowledge representation)
- SPARQL (Semantic querying)
- Python (Reasoning engine)
- Owlready2 (Ontology integration)
- Streamlit (Web interface)

---

## Ontology Design

Core entities:
- Person
- Bank Account
- Transaction

Relationships:
- ownership relations
- transaction execution
- transfer relationships

Constraints ensure semantic consistency and logical integrity.

---

## Fraud Detection Strategy

### SPARQL-Based Detection
- Semantic query patterns
- Constraint-based filtering
- Knowledge graph reasoning

### Rule-Based Detection
- Conditional Python logic
- Threshold-based fraud detection
- Business rule adaptation

---

## Evaluation
The system is tested using a simulated dataset of banking transactions containing both normal and fraudulent cases.

---

## Key Contributions

- Hybrid symbolic reasoning framework
- Explainable fraud detection system
- Integration of ontology + rule-based reasoning
- Lightweight Python implementation

---

## Limitations

- Requires manual rule definition
- Sensitive to threshold configuration
- Evaluated on simulated dataset only

---

## Future Work

- Integration with machine learning models
- Real-world banking dataset evaluation
- Expansion of ontology with regulatory compliance rules
- Hybrid neuro-symbolic fraud detection

---

## Installation

pip install owlready2 streamlit pandas

---

## Execution

streamlit run app.py

---

## Authors

Khaoula El Ater  
Ouayres Oumaima  
Abderrahman Chekry  

Cadi Ayyad University, Morocco
