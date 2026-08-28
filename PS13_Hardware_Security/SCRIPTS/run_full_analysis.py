#!/usr/bin/env python3
"""
PS13 Hardware Security — Full Analysis Pipeline
==================================================
Runs the complete analysis pipeline on a netlist:
  1. Parse netlist
  2. Build circuit graph
  3. Extract features
  4. Detect Trojans
  5. Analyze suspicious regions
  6. Generate security report

Usage:
    python run_full_analysis.py --netlist <path.v> --design-name <name> [--threshold 0.6]
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYZER.parser.netlist_parser import NetlistParser
from ANALYZER.graph.circuit_graph import CircuitGraph
from ANALYZER.features.feature_extractor import FeatureExtractor
from ANALYZER.detection.trojan_detector import TrojanDetector
from ANALYZER.trojan_analysis.trojan_analyzer import TrojanAnalyzer
from ANALYZER.security.security_report import SecurityReporter


def main():
    parser = argparse.ArgumentParser(
        description="Run the complete PS13 analysis pipeline."
    )
    parser.add_argument("--netlist", required=True,
                        help="Path to the gate-level Verilog netlist")
    parser.add_argument("--design-name", default="ALU8",
                        help="Name of the design (for report)")
    parser.add_argument("--threshold", type=float, default=0.6,
                        help="Detection threshold (0.0-1.0)")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory for all results")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if args.output_dir is None:
        args.output_dir = os.path.join(project_root, "REPORTS", "final")
    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 60)
    print("  PS13 Hardware Security — Full Analysis Pipeline")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Step 1: Parse netlist
    # ------------------------------------------------------------------
    print(f"\n[STEP 1/6] Parsing netlist: {args.netlist}")
    np = NetlistParser(args.netlist)
    if not np.parse():
        print("[ERROR] Failed to parse netlist. Aborting.")
        sys.exit(1)
    summary = np.get_summary()
    print(f"  Modules: {summary['module_count']}, "
          f"Instances: {summary['instance_count']}, "
          f"Nets: {summary['net_count']}")

    parsed_json = os.path.join(args.output_dir, "parsed.json")
    np.to_json(parsed_json)

    # ------------------------------------------------------------------
    # Step 2: Build circuit graph
    # ------------------------------------------------------------------
    print(f"\n[STEP 2/6] Building circuit graph...")
    cg = CircuitGraph()
    cg.build_from_parsed_data(np.get_instances(), np.get_ports(), np.get_nets())
    gs = cg.get_summary()
    print(f"  Nodes: {gs['total_nodes']}, Edges: {gs['total_edges']}, "
          f"Max depth: {gs['max_logic_depth']}")

    graph_json = os.path.join(args.output_dir, "graph.json")
    cg.to_json(graph_json)

    # ------------------------------------------------------------------
    # Step 3: Extract features
    # ------------------------------------------------------------------
    print(f"\n[STEP 3/6] Extracting features...")
    fe = FeatureExtractor(cg)
    features = fe.extract_all()
    print(f"  Cell features: {len(features['cell_features'])}")
    print(f"  Design features: {json.dumps(features['design_features'], indent=4)[:200]}...")

    features_json = os.path.join(args.output_dir, "features.json")
    fe.to_json(features_json)

    # ------------------------------------------------------------------
    # Step 4: Detect Trojans
    # ------------------------------------------------------------------
    print(f"\n[STEP 4/6] Running Trojan detection (threshold={args.threshold})...")
    detector = TrojanDetector(features, threshold=args.threshold)
    suspicious = detector.detect()
    det_summary = detector.get_detection_summary()
    print(f"  Suspicious cells: {det_summary['suspicious_count']}")
    for s in det_summary.get("top_suspicious", [])[:5]:
        print(f"    - {s['cell']} (score: {s['score']:.4f})")

    detection_json = os.path.join(args.output_dir, "detection.json")
    detector.to_json(detection_json)

    # ------------------------------------------------------------------
    # Step 5: Analyze suspicious regions
    # ------------------------------------------------------------------
    print(f"\n[STEP 5/6] Analyzing suspicious regions...")
    analyzer = TrojanAnalyzer(cg, suspicious)
    analysis_results = analyzer.analyze()
    print(f"  Analyzed: {len(analysis_results)} regions")

    analysis_json = os.path.join(args.output_dir, "analysis.json")
    analyzer.to_json(analysis_json)

    # ------------------------------------------------------------------
    # Step 6: Generate security report
    # ------------------------------------------------------------------
    print(f"\n[STEP 6/6] Generating security report...")
    reporter = SecurityReporter(design_name=args.design_name)
    reporter.set_structural_results(features)
    reporter.set_trojan_results(det_summary, analysis_results)
    report = reporter.generate()

    report_json = os.path.join(args.output_dir, "security_report.json")
    reporter.to_json(report_json)

    report_txt = os.path.join(args.output_dir, "security_report.txt")
    reporter.to_text(report_txt)

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    verdict = report["overall_verdict"]
    print(f"\n{'=' * 60}")
    print(f"  VERDICT:    {verdict['verdict']}")
    print(f"  RISK LEVEL: {verdict['risk_level']}")
    print(f"{'=' * 60}")
    print(f"\n  Reports saved to: {args.output_dir}/")
    print(f"    - security_report.json")
    print(f"    - security_report.txt")
    print(f"    - parsed.json, graph.json, features.json")
    print(f"    - detection.json, analysis.json")


if __name__ == "__main__":
    main()
