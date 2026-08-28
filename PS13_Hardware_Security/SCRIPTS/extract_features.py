#!/usr/bin/env python3
"""
PS13 Hardware Security — Feature Extraction Script
=====================================================
Load parsed netlist data, build circuit graph, extract features.

Usage:
    python extract_features.py --parsed <parsed.json> [--output <features.json>]
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYZER.graph.circuit_graph import CircuitGraph
from ANALYZER.features.feature_extractor import FeatureExtractor


def main():
    parser = argparse.ArgumentParser(
        description="Extract structural features from parsed netlist data."
    )
    parser.add_argument("--parsed", required=True,
                        help="Path to parsed netlist JSON (from run_parser.py)")
    parser.add_argument("--output", default=None,
                        help="Output features JSON path")
    args = parser.parse_args()

    if args.output is None:
        base_name = os.path.splitext(os.path.basename(args.parsed))[0]
        base_name = base_name.replace("_parsed", "")
        args.output = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "DATA", "features", f"{base_name}_features.json"
        )

    print(f"[*] Building circuit graph from: {args.parsed}")
    cg = CircuitGraph()
    cg.build_from_json(args.parsed)

    graph_summary = cg.get_summary()
    print(f"[+] Nodes: {graph_summary['total_nodes']}")
    print(f"[+] Edges: {graph_summary['total_edges']}")
    print(f"[+] Max depth: {graph_summary['max_logic_depth']}")
    print(f"[+] DAG: {graph_summary['is_dag']}")

    print(f"[*] Extracting features...")
    fe = FeatureExtractor(cg)
    features = fe.extract_all()

    print(f"[+] Cell features extracted for {len(features['cell_features'])} cells")
    print(f"[+] Design features: {features['design_features']}")

    # Check for anomalies
    anomalies = fe.get_anomalous_cells()
    if anomalies:
        print(f"[!] Found {len(anomalies)} anomalous cells:")
        for a in anomalies[:5]:
            print(f"    - {a['cell']}: {', '.join(a['anomaly_reasons'])}")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    fe.to_json(args.output)
    print(f"[+] Saved features to: {args.output}")


if __name__ == "__main__":
    main()
