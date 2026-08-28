#!/usr/bin/env python3
"""
PS13 Hardware Security — Full Structural Analysis Pipeline
============================================================
Runs the complete analysis pipeline on a netlist with rich,
colored terminal output:
  1. Parse netlist
  2. Build circuit graph
  3. Extract features
  4. Detect Trojans (8-indicator weighted scoring)
  5. Analyze suspicious regions
  6. Generate security report

Usage:
    python run_full_analysis.py --netlist <path.v> [--threshold 0.45]
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

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'


def print_header(title):
    """Print a styled section header."""
    print(f"\n{CYAN}{BOLD}{'━' * 62}{RESET}")
    print(f"{CYAN}{BOLD}  {title}{RESET}")
    print(f"{CYAN}{BOLD}{'━' * 62}{RESET}")


def print_step(step_num, total, description):
    """Print a step indicator."""
    print(f"\n{MAGENTA}[STEP {step_num}/{total}]{RESET} {BOLD}{description}{RESET}")


def print_table_row(label, value, color=WHITE):
    """Print a key-value row."""
    print(f"  {DIM}│{RESET} {label:<32s} {color}{value}{RESET}")


def print_cell_type_distribution(dist):
    """Print cell type distribution as a table."""
    print(f"\n  {BOLD}Cell Type Distribution:{RESET}")
    print(f"  {DIM}┌{'─'*20}┬{'─'*8}┬{'─'*30}┐{RESET}")
    print(f"  {DIM}│{RESET} {BOLD}{'Cell Type':<18s}{RESET} {DIM}│{RESET} {BOLD}{'Count':>6s}{RESET} {DIM}│{RESET} {BOLD}{'Bar':<28s}{RESET} {DIM}│{RESET}")
    print(f"  {DIM}├{'─'*20}┼{'─'*8}┼{'─'*30}┤{RESET}")
    total = sum(dist.values()) or 1
    for ct, count in sorted(dist.items(), key=lambda x: -x[1]):
        bar_len = int(28 * count / max(dist.values()))
        bar = '█' * bar_len
        pct = 100 * count / total
        print(f"  {DIM}│{RESET} {ct:<18s} {DIM}│{RESET} {count:>6d} {DIM}│{RESET} {GREEN}{bar:<28s}{RESET} {DIM}│{RESET} {DIM}{pct:5.1f}%{RESET}")
    print(f"  {DIM}└{'─'*20}┴{'─'*8}┴{'─'*30}┘{RESET}")


def print_suspicious_table(scores, threshold):
    """Print a detailed suspicious cells table."""
    # Get all cells sorted by score
    all_cells = sorted(scores.values(), key=lambda x: -x["total_score"])
    top_cells = all_cells[:15]  # Show top 15

    indicator_names = ["fanout", "fanin", "depth", "cone", "rare", "conn", "out_prox", "in_div"]
    indicator_keys = [
        "fanout_anomaly", "fanin_anomaly", "depth_anomaly", "cone_size_anomaly",
        "rare_cell_type", "connectivity_ratio", "output_proximity", "input_diversity"
    ]

    print(f"\n  {BOLD}Top Cells by Suspicion Score (threshold={threshold}):{RESET}")
    # Header
    hdr = f"  {DIM}│{RESET} {'Cell':<28s} {DIM}│{RESET} {'Score':>5s} {DIM}│{RESET}"
    for name in indicator_names:
        hdr += f" {name:>7s} {DIM}│{RESET}"
    print(f"  {DIM}┌{'─'*30}┬{'─'*7}┬{'─'*73}┐{RESET}")
    print(hdr)
    print(f"  {DIM}├{'─'*30}┼{'─'*7}┼{'─'*73}┤{RESET}")

    for cell_data in top_cells:
        score = cell_data["total_score"]
        name = cell_data["cell"]
        if len(name) > 27:
            name = name[:24] + "..."

        score_color = RED if score >= threshold else (YELLOW if score >= threshold * 0.7 else GREEN)
        flag = " ⚠" if score >= threshold else "  "

        row = f"  {DIM}│{RESET} {name:<28s} {DIM}│{RESET} {score_color}{score:5.3f}{RESET}{flag}{DIM}│{RESET}"
        indicators = cell_data.get("indicators", {})
        for key in indicator_keys:
            val = indicators.get(key, 0.0)
            val_color = RED if val > 0.5 else (YELLOW if val > 0.2 else DIM)
            row += f" {val_color}{val:7.3f}{RESET} {DIM}│{RESET}"
        print(row)

    print(f"  {DIM}└{'─'*30}┴{'─'*7}┴{'─'*73}┘{RESET}")

    flagged = sum(1 for c in all_cells if c["total_score"] >= threshold)
    print(f"  {BOLD}Flagged:{RESET} {RED if flagged > 0 else GREEN}{flagged}{RESET} / {len(all_cells)} cells exceed threshold")


def main():
    parser = argparse.ArgumentParser(
        description="Run the complete PS13 structural analysis pipeline."
    )
    parser.add_argument("--netlist", required=True,
                        help="Path to the gate-level Verilog netlist")
    parser.add_argument("--design-name", default="ALU8",
                        help="Name of the design (for report)")
    parser.add_argument("--threshold", type=float, default=0.40,
                        help="Detection threshold (0.0-1.0)")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory for all results")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if args.output_dir is None:
        args.output_dir = os.path.join(project_root, "REPORTS", "final")
    os.makedirs(args.output_dir, exist_ok=True)

    print_header("PS13 Hardware Security — Structural Trojan Analysis")

    # Step 1: Parse netlist
    print_step(1, 6, f"Parsing netlist: {args.netlist}")
    np = NetlistParser(args.netlist)
    if not np.parse():
        print(f"  {RED}[ERROR] Failed to parse netlist. Aborting.{RESET}")
        sys.exit(1)
    summary = np.get_summary()
    print_table_row("Modules", str(summary['module_count']))
    print_table_row("Instances", str(summary['instance_count']))
    print_table_row("Nets", str(summary['net_count']))
    np.to_json(os.path.join(args.output_dir, "parsed.json"))

    # Step 2: Build circuit graph
    print_step(2, 6, "Building circuit graph...")
    cg = CircuitGraph()
    cg.build_from_parsed_data(np.get_instances(), np.get_ports(), np.get_nets())
    gs = cg.get_summary()
    print_table_row("Nodes", str(gs['total_nodes']))
    print_table_row("Edges", str(gs['total_edges']))
    print_table_row("Max Logic Depth", str(gs['max_logic_depth']))
    print_table_row("Connected Components", str(gs['connected_components']))
    print_table_row("Is DAG", str(gs['is_dag']), GREEN if gs['is_dag'] else RED)
    cg.to_json(os.path.join(args.output_dir, "graph.json"))

    # Step 3: Extract features
    print_step(3, 6, "Extracting features...")
    fe = FeatureExtractor(cg)
    features = fe.extract_all()
    cell_count = len(features['cell_features'])
    print_table_row("Cell features extracted", str(cell_count))
    print_cell_type_distribution(features['design_features'].get('cell_type_distribution', {}))
    fe.to_json(os.path.join(args.output_dir, "features.json"))

    # Step 4: Detect Trojans
    print_step(4, 6, f"Running Trojan detection (threshold={args.threshold})...")
    detector = TrojanDetector(features, threshold=args.threshold)
    suspicious = detector.detect()
    scores = detector.get_scores()
    det_summary = detector.get_detection_summary()
    print_suspicious_table(scores, args.threshold)
    detector.to_json(os.path.join(args.output_dir, "detection.json"))

    # Step 5: Analyze suspicious regions
    print_step(5, 6, "Analyzing suspicious regions...")
    analyzer = TrojanAnalyzer(cg, suspicious)
    analysis_results = analyzer.analyze()
    print_table_row("Regions analyzed", str(len(analysis_results)))
    analyzer.to_json(os.path.join(args.output_dir, "analysis.json"))

    # Step 6: Generate security report
    print_step(6, 6, "Generating security report...")
    reporter = SecurityReporter(design_name=args.design_name)
    reporter.set_structural_results(features)
    reporter.set_trojan_results(det_summary, analysis_results)
    report = reporter.generate()
    reporter.to_json(os.path.join(args.output_dir, "security_report.json"))
    reporter.to_text(os.path.join(args.output_dir, "security_report.txt"))

    # Final Verdict
    verdict = report["overall_verdict"]
    v_text = verdict['verdict']
    risk = verdict['risk_level']

    if 'SUSPICIOUS' in v_text or 'TROJAN' in v_text:
        v_color = RED
    elif 'CLEAN' in v_text:
        v_color = GREEN
    else:
        v_color = YELLOW

    risk_color = RED if risk in ('HIGH', 'CRITICAL') else (YELLOW if risk == 'MEDIUM' else GREEN)

    print(f"\n{CYAN}{BOLD}{'━' * 62}{RESET}")
    print(f"  {BOLD}STRUCTURAL VERDICT:{RESET}  {v_color}{BOLD}{v_text}{RESET}")
    print(f"  {BOLD}RISK LEVEL:{RESET}          {risk_color}{BOLD}{risk}{RESET}")
    print(f"{CYAN}{BOLD}{'━' * 62}{RESET}")
    print(f"\n  Reports saved to: {args.output_dir}/")
    print(f"    - security_report.json / .txt")
    print(f"    - parsed.json, graph.json, features.json")
    print(f"    - detection.json, analysis.json\n")


if __name__ == "__main__":
    main()
