# Smart Paths, Better Privacy  
**Graph-Optimized Cookie Consent Management**

Zoya Asadi, University of Passau, 2025 — Supervisor: Prof. Dr. Stefanie Scherzinger

This repository contains the artefacts, scripts, and evaluation materials for the Master’s thesis:

> **Smart Paths, Better Privacy: Graph-Optimized Cookie Consent Management**

<<<<<<< HEAD
The repository is structured to support **reproducibility**: researchers can rerun the algorithms on the consent-graph variants, regenerate outputs, and compare results with the provided evaluation data.
=======

## Overview
This project explores how graph-based modeling can improve the efficiency and transparency of cookie consent systems.  
Modern websites often require users to make multiple consent choices (for analytics, personalization, payments, etc.), leading to long and repetitive click paths.  
To address this, the project represents the consent interaction flow as a **directed graph**, where nodes represent user actions (e.g., “Accept All”, “Open Modal”, “Save Settings”) and edges represent transitions between those actions.

Based on this model, five **edge-removal algorithms** (from Konstantinidis et al.) are applied to simplify the graph while preserving compliance and usability.  
Each algorithm represents a different strategy for optimizing the consent journey—from random pruning to privacy-aware structural reduction.

The evaluation measures:
- How many user clicks can be saved after simplification,  
- Which paths remain reachable (i.e., compliant with GDPR defaults),  
- And how the system’s usability and privacy trade-offs change across design variants.

By combining **graph theory** and **consent management principles**, this work provides a reproducible framework for analysing and optimizing user consent flows, helping to design systems that are both privacy-preserving and user-friendly.


------------------


## Architecture
The system is organized into three main layers that together form the experimental setup for the graph-based cookie consent evaluation.

### 2.1 Content and Data Layer — *OpenCms*
OpenCms provides the content management backbone of the system.  
It hosts the demo website (“Open Library”) that includes multiple content types such as articles, digital magazines, audiobooks, and membership pages.  
User interactions (e.g., visiting pages, logging in, or managing cookies) are stored in a **MySQL** database, forming the basis for consent graph extraction.

### 2.2 Consent Management Layer — *Klaro (CMP)*
Klaro serves as the cookie consent management platform integrated into OpenCms.  
It displays the banner and modal dialogs where users can choose which cookies to accept or decline (Analytics, Marketing, Functional, Essential).  
Each interaction event (accept, decline, manage, toggle) is recorded and later mapped into the graph representation used for evaluation.

### 2.3 Graph Analysis and Algorithm Layer — *Python Scripts*
This layer performs the computational analysis.  
Using **Python 3.11**, **Graphviz**, **pydot**, and **networkx**, user consent flows are represented as directed graphs (`.dot` files).  
Five algorithms (`RemoveFirstEdge`, `RemoveRandomEdge`, `RemoveMinCut`, `RemoveMinMC`, `BruteForce`) are applied to simplify the graph and measure user click-cost before and after optimization.  
Outputs include modified graphs (`*_after.dot`), visual overlays (`*_overlay.png`), and quantitative metrics (CSV/JSON).

### 2.4 Integration
All layers are connected as follows:
- **OpenCms + Klaro:** generate consent data from user interactions.  
- **Python scripts:** extract, model, and evaluate the data as graphs.  
- Results are visualized using Graphviz to show structural changes and user path simplifications.


------------------


 ## Graphs and design variants
- **G0**: Baseline CMP flow (banner → modal → toggles → save / accept-all).
- **G1**: Quick-Consent (inline ‘allow’ prompts).
- **G1b**: Quick-Consent + auto-apply & implicit first-use.

------------------


##  Algorithms
The evaluation applies five graph-reduction algorithms originally proposed by Konstantinidis et al.  
Each algorithm removes selected edges from the consent graph to simulate different strategies for simplifying user journeys while maintaining privacy compliance.

###  A1 — RemoveFirstEdge
A deterministic baseline that removes the first available edge in traversal order until the graph satisfies minimal connectivity under consent semantics.  
It represents predictable and reproducible simplification without randomness or optimization bias.

###  A2 — RemoveRandomEdge
Introduces randomness into edge deletion.  
At each step, a random edge is removed to study the stochastic impact of arbitrary consent-path removals.  
This approach highlights how non-targeted deletions can disrupt reachability or increase user effort unpredictably.

###  A3
— BruteForce
Performs an exhaustive search across all possible edge-removal combinations to identify the configuration that minimizes user click-cost.  
Although computationally expensive, this algorithm provides the **ground-truth optimum** against which all other heuristics are evaluated. 

###  A4 — RemoveMinCut
Targets the weakest structural links — the minimal sets of edges whose removal least affects overall connectivity.  


###  A5 — RemoveMinMC
A multi-criteria version of the MinCut strategy that balances between connectivity, privacy, and click-cost.  
It removes the minimum number of edges required to satisfy multiple constraints simultaneously, providing a near-optimal trade-off between usability and data protection.

###  Outputs
Each algorithm generates three types of artefacts:
- `*_after.dot` — the simplified graph after edge removal  
- `*_overlay.png` — visualization highlighting removed edges (red dashed lines)  
- CSV files in `artefacts/results/` — containing per-path and per-algorithm click-cost metrics

All generated results can be directly visualized using **Graphviz** or analyzed in **Python** notebooks to compare before/after performance across algorithms.

------------------
##  Evaluation
The evaluation systematically measures how graph simplifications affect the structure and usability of the consent flow.  
All experiments are performed on the baseline graph **G₀** and its design variants (**G₁**), using the five algorithms described earlier.

### Objective
To quantify how many user clicks can be saved through graph simplification while maintaining connectivity between consent start nodes (e.g., banner interactions) and outcome nodes (e.g., service access).
>>>>>>> a2cfbf0 (Folder cleanup and file changes according to supervisor feedback)

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
cd "Smart Path Better Privacy"
```

### Create and activate a virtual environment

<<<<<<< HEAD
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
Tools/code/Konstantinidis Teams Algorithm/consent-management-in-data-workflows-main/code
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
=======
## Repository layout
Smart-Paths-Better-Privacy/
│
├── README.md
│   └── Project overview, architecture, algorithms, evaluation setup
>>>>>>> a2cfbf0 (Folder cleanup and file changes according to supervisor feedback)
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
│       └── Konstantinidis Teams Algorithm/
│           └── consent-management-in-data-workflows-main/
│               └── code/
│
├── Klaro/
├── Thesis/
└── README.md
```

<<<<<<< HEAD
Folder names reflect the **actual repository structure**.
=======



## License & Credits

This repository is part of the Master’s thesis:

> **Smart Paths, Better Privacy: Graph-Optimized Cookie Consent Management**  
> Author: **Zoya Asadi**  
> Supervisor: **Prof. Dr. Stefanie Scherzinger**  
> University of Passau — Faculty of Informatics and Mathematics  
> Submission date: **October 2025**
>>>>>>> a2cfbf0 (Folder cleanup and file changes according to supervisor feedback)

---

## Source Attribution

- The underlying algorithmic framework originates from  
  **Konstantinidis et al. (2021)** (referenced in the thesis)  
- Graph modelling, dataset preparation, evaluation workflow, metric computation,  
  and produced artefacts in this repository are **author’s own work**

External code is used only where referenced and for academic-research purposes.

---

## License & Citation

This project is released under the **MIT License**.

When citing this work:

> Zoya Asadi, *Smart Paths, Better Privacy: Graph-Optimized Cookie Consent Management*,  
> Master’s Thesis, University of Passau, 2025.

---

## Acknowledgements

- Prof. Dr. Stefanie Scherzinger — supervision and feedback  
- Konstantinidis research group — algorithmic foundations  
- OpenCms & Klaro communities — CMP platform support  
- Open-source contributors to NetworkX, Graphviz, and pydot
