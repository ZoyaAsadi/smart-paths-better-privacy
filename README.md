# Smart Paths, Better Privacy  
**Cookie Consent Management**

This repository contains artefacts and evaluation materials for the Master’s thesis:

> **Smart Paths, Better Privacy: Graph-Optimized Cookie Consent Management**  
> University:Passau, Supervisor: Prof. Dr. Stefanie Scherzinger, Author: Zoya Asadi, Year:2025

------------------


1.## Overview
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


2.## Architecture
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


3. ## Graphs and design variants
- **G0**: Baseline CMP flow (banner → modal → toggles → save / accept-all).
- **G1**: Quick-Consent (inline ‘allow’ prompts).
- **G1b**: Quick-Consent + auto-apply & implicit first-use.

------------------


4. ##  Algorithms
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
5. ##  Evaluation
The evaluation systematically measures how graph simplifications affect the structure and usability of the consent flow.  
All experiments are performed on the baseline graph **G₀** and its design variants (**G₁**), using the five algorithms described earlier.

### Objective
To quantify how many user clicks can be saved through graph simplification while maintaining connectivity between consent start nodes (e.g., banner interactions) and outcome nodes (e.g., service access).

---

###  Metrics
For each algorithm and design variant, the following metrics are recorded:

- **Click-cost metrics:** total and consent-related clicks before/after simplification.  
- **Connectivity:** which start→outcome pairs remain connected or become disconnected.  
- **Path deltas:** changes in shortest paths, identifying improvements, regressions, or neutral cases.  
- **Edge deletions:** number and type of edges removed (random, minimal cut, multi-criteria, etc.).  
- **Visual overlays:** highlight which journey segments were affected.

All data are saved as:
- `clicks_detail.csv` — per-path costs before and after simplification  
- `clicks_summary_plus.csv` — aggregate summaries per algorithm  
- `clicks_baseline_compare__G1*.csv` — design comparison between G₀, G₁, and G₁b

---

###  Experimental Setup
All experiments were executed locally using:
- **Python 3.11** with `networkx`, `pydot`, `graphviz`, `pandas`  
- **macOS 15.1 (Apple Silicon M2, 8 GB RAM)**  
- Fixed random seed: `PYTHONHASHSEED=0` for reproducibility  

Graphs were generated in `.dot` format and validated using `pydot`:
```python
import pydot, networkx as nx
pd = pydot.graph_from_dot_file('artefacts/graphs/G0.dot')[0]
G = nx.drawing.nx_pydot.from_pydot(pd)
# confirms nodes/edges and exports JSON reports



6.## Repository layout
Smart-Paths-Better-Privacy/
│
├── README.md
│   └── Project overview, architecture, algorithms, evaluation setup
│
├── artefacts/
│   ├── graphs/
│   │   ├── G0.dot              # Baseline consent graph
│   │   ├── G1.dot              # Quick-Consent variant
│   │   ├── G1b.dot             # Quick-Consent + Auto-Apply variant
│   │   └──  *_after.dot         # Graphs after algorithmic reduction
│   │   
│   │
│   ├── figures/
│   │   ├── *.png / *.jpg       # Rendered figures for thesis
│   │
│   └── results/
│       ├── clicks_detail.csv           # Per-path click-cost before/after
│       ├── clicks_summary_plus.csv     # Aggregated statistics per algorithm
│       ├── clicks_baseline_compare__G0/G1.csv  # Comparison between G₀ and G₁
│       ├── clicks_baseline_compare__G1b.csv # Comparison between G₀ and G₁b
│       └── G0_G1_pairs.csv       # Edge-removal logs and reports
│        
│
├── tools/
│   ├── run_konstantin.py        # Main runner script for executing algorithms
│   └── konstantin_adapter.py    # Interface between Python and algorithm logic
│         
│         
│
├── klaro/
│   ├── klaro.js                 # CMP configuration (cookie categories)
│   ├── klaro-config.js          # Consent options for OpenCms site
│   └── klaro.jsp.jsp            # UI integration within OpenCms templates
│
│
│   
│
└── thesis/
    └── latex/                   # LaTeX source files for Master’s thesis
                        
                   




7.## License & Credits

This repository is part of the Master’s thesis:

> **Smart Paths, Better Privacy: Graph-Optimized Cookie Consent Management**  
> Author: **Zoya Asadi**  
> Supervisor: **Prof. Dr. Stefanie Scherzinger**  
> University of Passau — Faculty of Informatics and Mathematics  
> Submission date: **October 2025**

---

###  Academic Context
This work investigates how **graph-theoretic path elimination algorithms** can improve  
user experience in **cookie consent management systems (CMPs)** while preserving privacy compliance.  
It builds upon the graph simplification algorithms introduced by **Konstantinidis et al. (2021)**,  
applied to real-world consent data modeled within **OpenCms** and **Klaro**.

All code and results are provided for academic and non-commercial research purposes only.

---

###  License
This project is distributed under the **MIT License** (open and reusable with attribution).  
You are free to use, modify, and cite this work, provided that proper credit is given to the author  
and the original source is referenced as:

> Zoya Asadi, *Smart Paths, Better Privacy: Graph-Optimized Cookie Consent Management*,  
> Master’s Thesis, University of Passau, 2025.

---

###  Acknowledgements
Special thanks to:
- **Prof. Dr. Stefanie Scherzinger** — for supervision and detailed feedback.  
- The **University of Passau** for providing the academic environment and resources.  
- The **Konstantinidis research team** for the original algorithmic framework.  
- The **OpenCms development team** for their continuous efforts in maintaining and improving the open-source CMS, and for their helpful responses to my technical inquiries.
- The open-source developers of **Graphviz**, **NetworkX**, and **Klaro**,  
  whose tools made this research possible.
