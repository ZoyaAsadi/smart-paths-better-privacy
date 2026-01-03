# Smart Paths, Better Privacy  
**Graph-Optimized Cookie Consent Management**

Zoya Asadi, University of Passau, 2025 — Supervisor: Prof. Dr. Stefanie Scherzinger

This repository contains the artefacts, scripts, and evaluation materials for the Master’s thesis:

> **Smart Paths, Better Privacy: Graph-Optimized Cookie Consent Management**

The repository is structured to support **reproducibility**: researchers can rerun the algorithms on the consent-graph variants, regenerate outputs, and compare results with the provided evaluation data.

---

## Overview

The project models cookie-consent interactions as **directed graphs**, where nodes represent interface states and user actions (e.g., *Open Modal*, *Accept All*, *Save Settings*), and edges represent transitions between them.  

Five **edge-removal algorithms** (adapted from Konstantinidis et al.) are applied to these graphs to study how user click-paths can be simplified while preserving privacy compliance and overall system utility.

The evaluation analyses:

- click-cost reduction after graph simplification  
- preservation / loss of reachable consent paths  
- usability–privacy trade-offs across design variants and algorithms  

The README focuses on **technical setup, execution, and artefact structure**.

---

## Getting Started

### Clone the repository

```bash
git clone https://github.com/ZoyaAsadi/smart-paths-better-privacy.git
cd smart-paths-better-privacy
```

### Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

Graph rendering requires **Graphviz** to be installed on the system.

---
### Minimal Reproduction Steps

1. Go to the algorithm folder  
   `cd Tools/code/konstantinidis-team-algorithm/consent-management-in-data-workflows-main/code`

2. Run an algorithm on a graph:
```bash
python apply_on_dot.py \
  --graph ../../../artefacts/Graphs/G1/G1.dot \
  --algorithm remove_first_edge \
  --output ../../../artefacts/Graphs/G1/G1_remove_first_edge_after.dot


## Project Architecture

### Content & Data Layer — OpenCms
- Demo “Open Library” website  
- Interaction flows across books, magazines, audiobooks, membership pages  
- User actions stored in **MySQL**, forming the basis for consent-graph modelling

### Consent Management Layer — Klaro (CMP)
- Cookie banner and modal interface  
- Cookie categories: analytics, marketing, functional, essential  
- Consent actions mapped to graph representations  
- **Custom Klaro integration and cookie configuration implemented by the author**  
  (`Klaro/klaro.js`, `Klaro/klaro-config.js`, `Klaro/klaro.jsp`)

### Graph Analysis & Algorithm Layer — Python
- Consent flows represented as `.dot` graphs (NetworkX / pydot)
- Algorithms applied to simplify graph structure and evaluate click-cost impact
- Outputs include simplified graphs, overlays, and metric tables

---

## Graph Variants

- **G0** — Baseline CMP flow  
- **G1** — Quick-Consent variant  
- **G1b** — Quick-Consent + auto-apply / implicit first-use  

---

## Input Graphs and Output Locations

Input graphs:

- `artefacts/Graphs/G0/G0.dot`
- `artefacts/Graphs/G1/G1.dot`
- `artefacts/Graphs/G1b/G1b.dot`

Algorithm outputs:

- `artefacts/Graphs/<GRAPH>/*_after.dot` — simplified graphs  
- `artefacts/Figures/*.png` — overlays and rendered figures  
- `artefacts/Results/*.csv` — click-cost metrics and comparison tables  

Existing outputs may be reused for replication.

---

## Running the Algorithms

Algorithms are executed from:

```
Tools/code/konstantinidis-team-algorithm/consent-management-in-data-workflows-main/code
```

### Generic execution pattern

```bash
python apply_on_dot.py \
  --graph ../../../artefacts/Graphs/<GRAPH>/<GRAPH>.dot \
  --algorithm <ALGORITHM_NAME> \
  --output ../../../artefacts/Graphs/<GRAPH>/<GRAPH>_<ALGORITHM_NAME>_after.dot
```

Where:

- `<GRAPH> ∈ {G0, G1, G1b}`
- `<ALGORITHM_NAME> ∈ {remove_first_edge, remove_random_edge, remove_min_cut, remove_min_mc, brute_force}`

### Example

```bash
python apply_on_dot.py \
  --graph ../../../artefacts/Graphs/G0/G0.dot \
  --algorithm remove_min_cut \
  --output ../../../artefacts/Graphs/G0/G0_remove_min_cut_after.dot
```

Parameters:

- `--graph` path to input `.dot` file  
- `--algorithm` algorithm name  
- `--output` output path for simplified graph  

---

## Evaluation Metrics

For each algorithm and graph variant, the following metrics are reported:

- total clicks before / after simplification  
- consent-path length changes  
- connectivity preservation vs. disconnection  
- characteristics of removed edges  
- structural overlays for visual comparison  

Metric files are stored in:

```
artefacts/Results/
```

---

## Repository Layout

```
Smart Path Better Privacy
│
├── artefacts/
│   ├── Graphs/
│   │   ├── G0/
│   │   ├── G1/
│   │   └── G1b/
│   ├── Figures/
│   └── Results/
│
├── Tools/
│   └── code/
│       └── Konstantinidis-team-algorithm/
│           └── consent-management-in-data-workflows-main/
│               └── code/
│
├── Klaro/
├── Thesis/
└── README.md
```

Folder names reflect the **actual repository structure**.

---

## Source Attribution

- The underlying algorithmic framework originates from  
  **Konstantinidis et al. (2021)** (referenced in the thesis).  
- **Klaro integration, cookie configuration, consent-flow mapping, graph design (G0 / G1 / G1b), artefacts in `artefacts/`, and evaluation workflow are the author’s own work.**  
- External code is reused strictly for academic-research purposes and is referenced accordingly.

---

## License & Citation

This project is released under the **MIT License**.

When citing this work:

> Zoya Asadi, *Smart Paths, Better Privacy: Graph-Optimized Cookie Consent Management*,  
> Master’s Thesis, University of Passau, 2025.

---

## Acknowledgements

- Prof. Dr. Stefanie Scherzinger — supervision  
- Konstantinidis research group — algorithmic foundations  
- OpenCms & Klaro communities — CMP platform support  
- Open-source contributors to NetworkX, Graphviz, and pydot
