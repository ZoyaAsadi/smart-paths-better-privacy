# Smart Paths, Better Privacy  
**Graph-Optimized Cookie-Based Consent Management**

**Author:** Zoya Asadi  
**Supervisor:** Prof. Dr. Stefanie Scherzinger
**Advisor:** Prof. Dr. Harald Kosch
**University:** University of Passau  
**Year:** 2025

This repository contains the artefacts, scripts, and evaluation materials for the Master’s thesis:

> **Smart Paths, Better Privacy: Graph-Optimized Cookie-Based Consent Management**

The repository is structured to support **reproducibility**: researchers can rerun the algorithms on the consent-graph variants, regenerate outputs, and compare results with the provided evaluation data.

---

## Overview

The project implements a **Graph-Optimized Cookie-Based Consent Management** model, in which
cookie-consent interactions are represented as directed graphs. Nodes correspond to
interface states and user actions (such as *Open Modal*, *Accept All*, or *Save Settings*),
while edges represent the transitions between these states.

Five edge-removal algorithms (adapted from the approach of Konstantinidis et al.) are
applied to the graphs in order to observe how the removal of selected edges influences
user click-paths and the structure of the consent interaction flow.

The evaluation concentrates on measurable effects of these modifications, including
changes in click effort and path reachability across the different graph variants.

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
```bash
cd Tools/code/konstantinidis-team-algorithm/consent-management-in-data-workflows-main/code
```

2. Generic run pattern
```bash
python apply_on_dot.py \
  --graph ../../../artefacts/Graphs/<GRAPH>/<GRAPH>.dot \
  --algorithm <ALGORITHM_NAME> \
  --output ../../../artefacts/Graphs/<GRAPH>/<GRAPH>_<ALGORITHM_NAME>_after.dot

<GRAPH> = G0 | G1 | G1b

<ALGORITHM_NAME> =
  remove_first_edge
  remove_random_edge
  remove_min_cut
  remove_min_mc
  brute_force
```

**Example run**
```bash
python apply_on_dot.py \
  --graph ../../../artefacts/Graphs/G1/G1.dot \
  --algorithm remove_min_cut \
  --output ../../../artefacts/Graphs/G1/G1_remove_min_cut_after.dot
```

---
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

- G0 represents the baseline CMP banner–modal flow.
- G1 introduces inline quick-consent actions to reduce interaction depth.
- G1b extends G1 with auto-apply behaviour and implicit first-use consent triggers.

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

Example output files:
- artefacts/Results/clicks_summary_plus.csv
- artefacts/Results/G1_remove_min_cut_paths.csv

---

## Repository Layout

```
smart-paths-better-privacy
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
│       └── konstantinidis-team-algorithm/
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

When citing this work, please reference:

> Zoya Asadi, *Smart Paths, Better Privacy: Graph-Optimized Cookie Consent Management*,  
> Master’s Thesis, University of Passau, 2025.

### BibTeX Citation

If you use this work in academic research, please cite:

```bibtex
@mastersthesis{Asadi2025SmartPaths,
  author       = {Zoya Asadi},
  title        = {Smart Paths, Better Privacy: Graph-Optimized Cookie Consent Management},
  school       = {University of Passau},
  year         = {2025},
  supervisor   = {Prof. Dr. Stefanie Scherzinger},
  advisor      = {Prof. Dr. Harald Kosch}
}
```
---

## Acknowledgements

- Prof. Dr. Stefanie Scherzinger — supervision  
- Konstantinidis research group — algorithmic foundations  
- OpenCms & Klaro communities — CMP platform support  
- Open-source contributors to NetworkX, Graphviz, and pydot
