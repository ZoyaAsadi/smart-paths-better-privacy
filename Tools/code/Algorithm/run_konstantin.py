# tools/run_konstantin.py
from __future__ import annotations

import argparse
import json

from .konstantin_adapter import run_algorithm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--algo",
        required=True,
        help=(
            "Algorithm name. Examples: "
            "'Remove Random Edge', 'Remove First Edge', 'Remove Min-Cut', "
            "'Remove MinMC', 'Brute Force' "
            "or legacy ones like 'random_edge', 'first_edge', 'st_cut', "
            "'optimisation_approx', 'matrix_bruteforce', 'bruteforce'"
        ),
    )
    parser.add_argument("--graph", required=True, help="Path to graph JSON")
    parser.add_argument("--out", required=True, help="Output directory (kept for compatibility)")
    args = parser.parse_args()

    #    konstantin_adapter  
    res = run_algorithm(args.graph, args.algo, args.out)
    print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

