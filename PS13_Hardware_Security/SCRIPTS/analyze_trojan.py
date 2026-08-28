#!/usr/bin/env python3
"""
PS13 Hardware Security — Trojan Analysis Script
==================================================
Deep-analyze detected suspicious regions.

Usage:
    python analyze_trojan.py --parsed <parsed.json> --detection <detection.json> [--output <analysis.json>]
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYZER.graph.circuit_graph import CircuitGraph
from ANALYZER.trojan_analysis.trojan_analyzer import TrojanAnalyzer


def main():
    parser = argparse.ArgumentParser(
        description="Analyze detected suspicious regions in depth."
    )
    parser.add_argument("--parsed", required=True,
                        help="Path to parsed netlist JSON")
    parser.add_argument("--detection", required=True,
                        help="Path to detection results JSON")
    parser.add_argument("--output", default=None,
                        help="Output analysis JSON path")
    args = parser.parse_args()

    if args.output is None:
        base_name = os.path.splitext(os.path.basename(args.detection))[0]
        base_name = base_name.replace("_detection", "")
        args.output = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "REPORTS", "trojan", f"{base_name}_analysis.json"
        )

    print(f"[*] Building circuit graph from: {args.parsed}")
    cg = CircuitGraph()
    cg.build_from_json(args.parsed)

    print(f"[*] Loading detection results from: {args.detection}")
    with open(args.detection, 'r') as f:
        detection_data = json.load(f)

    suspicious = detection_data.get("suspicious_cells", [])
    print(f"[*] Analyzing {len(suspicious)} suspicious cells...")

    analyzer = TrojanAnalyzer(cg, suspicious)
    results = analyzer.analyze()

    summary = analyzer.get_summary()
    print(f"[+] Analysis complete:")
    print(f"    Classifications: {summary.get('classifications', {})}")
    print(f"    Estimated types: {summary.get('estimated_types', [])}")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    analyzer.to_json(args.output)
    print(f"[+] Saved analysis to: {args.output}")


if __name__ == "__main__":
    main()
