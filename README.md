# Hybrid Reasoning for Bank Fraud Detection

A Python and Streamlit research prototype that represents people, accounts, and transactions in an OWL ontology and flags suspicious transactions using explicit conditions. The project explores ontology modeling, RDF serialization, and SPARQL querying alongside a usable interface for manual entry, CSV processing, and evaluation.

![Python](https://img.shields.io/badge/Python-3D314A?style=flat-square&logo=python&logoColor=FFD9E2)
![Streamlit](https://img.shields.io/badge/Streamlit-B76E79?style=flat-square&logo=streamlit&logoColor=white)
![Ontology](https://img.shields.io/badge/OWL_%2F_RDF_%2F_SPARQL-8E5572?style=flat-square)

[Application](app.py) · [Ontology](banque_fraude.owl) · [Published article](https://www.scimetech.com/issues/vol2/issue2/V2I2A2.html)

## What the application offers

- Manual transaction forms and CSV upload through a French-language Streamlit interface.
- Ontology instances linking people, bank accounts, and transactions with Owlready2.
- Suspicious-transaction annotations and RDF/XML serialization.
- SPARQL queries for manual transaction checks.
- Batch tables, transaction counts, and pie charts.
- Precision, recall, F1, accuracy, and confusion matrices for uploaded labels and predictions.

This is a symbolic reasoning prototype: the current application does not train or serve a machine-learning model.

## How it works

Transaction input is converted into ontology instances. The application applies a fixed condition, annotates matching instances, saves the ontology, and presents the result.

The implemented condition requires **all three** criteria:

```python
montant > 13000 and pays.lower() == "iran" and solde < 10000
```

These are demonstration parameters, not validated fraud indicators or a compliance policy. Values are compared numerically without currency conversion.

| Interface mode | Current decision path |
| --- | --- |
| Formulaire SPARQL | Python annotations followed by an RDFLib SPARQL query |
| Formulaire Python | Python annotations followed by the same SPARQL query for the displayed verdict |
| CSV SPARQL | Python `est_fraude` condition determines batch predictions; ontology is saved |
| CSV Python | The same Python condition determines batch predictions; ontology is saved |
| Évaluation SPARQL / Python | Metrics from uploaded `fraude_reelle` and `fraude_predite`; predictions are not regenerated |

The menu labels therefore do not represent two fully independent detection implementations. OWL classes and relationships organize the knowledge, while procedural code and queries determine the displayed decisions; `app.py` does not invoke an OWL reasoner.

## Run locally

Run these commands from the repository root in a Python environment:

```bash
python -m pip install -r requirements.txt
python -m pip install rdflib
python -m streamlit run app.py
```

`rdflib` is imported by the application but is not explicitly listed in the current requirements file. The commands above address that missing direct dependency. Package versions are not pinned, and a fresh full installation and interactive run have not been verified.

Keep `fraude_sparql.owl` and `fraude_python.owl` in the working directory. The application clears ontology instances and saves these files during processing, so run from a disposable working copy if you want to retain their original contents.

## Input examples

Both CSV analysis modes require these columns:

```csv
prenom,nom,pays,solde,montant,devise,date,heure
Demo,Person,Iran,8000,15000,EUR,2025-06-24,12:00
Demo,Person2,France,12000,3000,EUR,2025-06-24,12:00
```

This synthetic example produces rule predictions of `1` and `0`, respectively, assuming successful input parsing and ontology processing. A flag means the example matches the configured condition; it is not evidence of actual fraud.

Use [test_fraude.csv](test_fraude.csv) for an existing file with the required transaction columns. [transactions_simulees.csv](transactions_simulees.csv) lacks `prenom` and `nom`, so it cannot be uploaded unchanged to the current batch interface.

For an evaluation tab, upload a file containing both columns:

```csv
fraude_reelle,fraude_predite
1,1
1,0
0,0
```

[transactions.csv](transactions.csv) contains both evaluation columns. [evaluation_sparql.csv](evaluation_sparql.csv) contains predictions only and cannot be used unchanged for the current evaluation tabs.

## Evaluation evidence

Recomputing metrics from the **stored labels and predictions in the 30-row `transactions.csv`** gives:

| Class | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| Normal (0) | 0.923 | 1.000 | 0.960 | 24 |
| Fraud (1) | 1.000 | 0.667 | 0.800 | 6 |

Accuracy is **93.33%**, with 24 true negatives, 4 true positives, 2 false negatives, and no false positives. These figures evaluate saved predictions, not a fresh end-to-end application run. Applying the current Python condition to the same transaction fields flags all six labeled fraud rows, so the saved predictions do not match the current rule on two rows.

The article reports the same rounded class metrics but describes 100 transactions and 19 detected frauds. The repository artifacts inspected here do not establish a matching 100-row evaluation:

| Repository file | Rows | Evidence available |
| --- | ---: | --- |
| `transactions.csv` | 30 | Ground truth and saved predictions; reproduces the reported class metrics |
| `test_fraude.csv` | 119 | Required transaction columns; current Python condition flags 19 rows; no ground-truth column |
| `transactions_simulees.csv` | 200 | Current condition flags 6 rows; no ground-truth column; incomplete upload schema |
| `evaluation_sparql.csv` | 25 | Predictions only; no ground truth |

These files are distinct artifacts. The 19 rule matches in the 119-row file do not verify the article's stated 100-transaction experiment. Synthetic results also do not establish performance on real banking data or superiority over machine-learning baselines.

## Limitations and next steps

- One hard-coded condition; no learned detector, temporal patterns, currency normalization, or real-world banking validation.
- CSV modes currently share the Python prediction path rather than independently evaluating SPARQL detection.
- Evaluation accepts precomputed predictions, and the saved predictions need reconciliation with the current rule.
- Ontology files are shared mutable state; concurrent sessions and persistent history are not managed.
- Some malformed CSV rows may be skipped, and ontology-loading failures are suppressed.
- No pinned environment, automated tests, or verified hosted demo was found in the inspected repository.

Focused future work: unify the documented dataset and evaluation outputs, make both reasoning paths independently testable, validate input schemas, isolate session state, and document a reproducible environment. Machine-learning integration remains a future extension.

## Publication and attribution

The article is listed in **Sciences Methods and Technologies International Journal (SciMeTech), Volume 2, Issue 2, pages 7–13**. See the [publisher's article page](https://www.scimetech.com/issues/vol2/issue2/V2I2A2.html).

Authors, in the order credited by the publication: **Khaoula El Ater, Ouayres Oumaima, and Abderrahman Chekry**, Cadi Ayyad University, Morocco. This is collaborative work; individual implementation responsibilities are not specified in the inspected materials.

The article cites Auger et al.'s *Construction of an ontology in the financial domain for fraud detection* (INFORSID 2022) as prior work. The implementation uses Owlready2, RDFLib, Streamlit, pandas, scikit-learn, Matplotlib, and Seaborn.

The previous README stated “Academic Use Only,” but no standalone license file was found. This documentation update does not grant a new license or change reuse permissions.
