#!/usr/bin/env python3
"""
PS13 Hardware Security — Combined Analysis Report
====================================================
Runs BOTH structural trojan detection AND side-channel timing
analysis, then cross-references results into a unified verdict.

Usage:
    python run_combined_report.py \\
        --netlist NETLISTS/T1/alu8_T1_netlist.v \\
        --reference DATA/timing/clean/report.rpt \\
        --suspect DATA/timing/trojan/T1_report.rpt
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYZER.parser.netlist_parser import NetlistParser
from ANALYZER.graph.circuit_graph import CircuitGraph
from ANALYZER.features.feature_extractor import FeatureExtractor
from ANALYZER.detection.trojan_detector import TrojanDetector
from ANALYZER.trojan_analysis.trojan_analyzer import TrojanAnalyzer
from ANALYZER.security.security_report import SecurityReporter
from ANALYZER.sca.timing_parser import TimingParser
from ANALYZER.sca.timing_comparison import TimingComparator

# ANSI
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'

BANNER = f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════════════╗
║          PS13 HARDWARE SECURITY — COMBINED ANALYSIS          ║
║          Structural + Side-Channel Timing Detection          ║
╚══════════════════════════════════════════════════════════════╝{RESET}
"""


def section(title):
    print(f"\n{MAGENTA}{BOLD}▸ {title}{RESET}")
    print(f"  {DIM}{'─' * 56}{RESET}")


def main():
    parser = argparse.ArgumentParser(description="PS13 Combined Structural + Timing Analysis")
    parser.add_argument("--netlist", required=True, help="Gate-level Verilog netlist")
    parser.add_argument("--reference", required=True, help="Clean timing report (.rpt)")
    parser.add_argument("--suspect", required=True, help="Trojan timing report (.rpt)")
    parser.add_argument("--threshold", type=float, default=0.45, help="Detection threshold")
    parser.add_argument("--design-name", default="ALU8", help="Design name")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "REPORTS", "final")
    os.makedirs(output_dir, exist_ok=True)

    print(BANNER)

    # ─── PART 1: STRUCTURAL ANALYSIS ──────────────────────────────────
    section("STRUCTURAL TROJAN DETECTION")

    print(f"  Parsing netlist: {args.netlist}")
    np = NetlistParser(args.netlist)
    if not np.parse():
        print(f"  {RED}[ERROR] Failed to parse netlist.{RESET}")
        sys.exit(1)
    summary = np.get_summary()
    print(f"  Modules: {summary['module_count']}, "
          f"Instances: {summary['instance_count']}, "
          f"Nets: {summary['net_count']}")

    print(f"  Building circuit graph...")
    cg = CircuitGraph()
    cg.build_from_parsed_data(np.get_instances(), np.get_ports(), np.get_nets())
    gs = cg.get_summary()
    print(f"  Nodes: {gs['total_nodes']}, Edges: {gs['total_edges']}, "
          f"Depth: {gs['max_logic_depth']}")

    print(f"  Extracting features & running detection (threshold={args.threshold})...")
    fe = FeatureExtractor(cg)
    features = fe.extract_all()

    detector = TrojanDetector(features, threshold=args.threshold)
    suspicious = detector.detect()
    det_summary = detector.get_detection_summary()
    scores = detector.get_scores()

    struct_count = det_summary['suspicious_count']
    struct_total = det_summary['total_cells_analyzed']

    # Show top 5 cells
    all_sorted = sorted(scores.values(), key=lambda x: -x['total_score'])
    print(f"\n  {BOLD}Top 5 cells by suspicion score:{RESET}")
    for i, cell in enumerate(all_sorted[:5]):
        sc = cell['total_score']
        flag = f" {RED}⚠ FLAGGED{RESET}" if sc >= args.threshold else ""
        sc_color = RED if sc >= args.threshold else (YELLOW if sc >= args.threshold * 0.7 else GREEN)
        print(f"    {i+1}. {cell['cell'][:40]:<40s}  {sc_color}{sc:.4f}{RESET}{flag}")

    # Generate report
    analyzer = TrojanAnalyzer(cg, suspicious)
    analysis_results = analyzer.analyze()
    reporter = SecurityReporter(design_name=args.design_name)
    reporter.set_structural_results(features)
    reporter.set_trojan_results(det_summary, analysis_results)
    report = reporter.generate()
    reporter.to_json(os.path.join(output_dir, "security_report.json"))
    reporter.to_text(os.path.join(output_dir, "security_report.txt"))

    struct_verdict = report["overall_verdict"]["verdict"]
    struct_risk = report["overall_verdict"]["risk_level"]

    # ─── PART 2: SIDE-CHANNEL TIMING ANALYSIS ─────────────────────────
    section("SIDE-CHANNEL TIMING ANALYSIS (SCA)")

    timing_parser = TimingParser()
    timing_ok = True

    try:
        ref_data = timing_parser.parse_report(args.reference)
        ref_data['design'] = "ALU8_CLEAN"
        ref_paths = len(ref_data.get('critical_paths', []))
        print(f"  Reference: {ref_paths} paths parsed")
    except FileNotFoundError:
        print(f"  {RED}[ERROR] Reference report not found: {args.reference}{RESET}")
        timing_ok = False

    try:
        sus_data = timing_parser.parse_report(args.suspect)
        sus_data['design'] = "ALU8_TROJAN"
        sus_paths = len(sus_data.get('critical_paths', []))
        print(f"  Suspect:   {sus_paths} paths parsed")
    except FileNotFoundError:
        print(f"  {RED}[ERROR] Suspect report not found: {args.suspect}{RESET}")
        timing_ok = False

    timing_anomaly = False
    timing_leakage = False
    timing_confidence = "N/A"
    delay_diff = 0.0
    anomaly_count = 0

    if timing_ok:
        comparator = TimingComparator()
        comparison = comparator.compare(ref_data, sus_data)

        sca_json = os.path.join(project_root, "REPORTS", "sca", "timing_comparison.json")
        os.makedirs(os.path.dirname(sca_json), exist_ok=True)
        with open(sca_json, 'w') as f:
            json.dump(comparison, f, indent=4)

        metrics = comparison['metrics']
        delay_diff = metrics.get('max_endpoint_delay_difference_ns', 0.0)
        anomaly_count = metrics.get('anomalies_count', 0)
        timing_anomaly = comparison['assessment']['timing_anomaly']
        timing_leakage = comparison['assessment'].get('potential_timing_leakage', False)
        timing_confidence = comparison['assessment']['confidence']

        stats = comparison.get('delay_statistics', {})
        print(f"  Max delay diff:  {delay_diff:+.3f} ns")
        print(f"  Mean delay diff: {stats.get('mean_diff_ns', 0):+.4f} ns")
        print(f"  Affected paths:  {anomaly_count}")

        # Show top anomalies
        anomalies = metrics.get('anomalies', [])
        if anomalies:
            print(f"\n  {BOLD}Anomalous endpoints:{RESET}")
            for a in anomalies[:5]:
                print(f"    • {a['endpoint']:<22s}  Δ={RED}{a['delay_diff_ns']:+.3f} ns{RESET}  "
                      f"(logic: {a.get('logic_diff_ns', 0):+.3f}, route: {a.get('route_diff_ns', 0):+.3f})")

    # ─── PART 3: COMBINED VERDICT ─────────────────────────────────────
    print(f"\n{CYAN}{BOLD}{'═' * 62}{RESET}")
    print(f"{CYAN}{BOLD}  COMBINED SECURITY VERDICT{RESET}")
    print(f"{CYAN}{BOLD}{'═' * 62}{RESET}")

    # Structural result
    s_color = RED if 'SUSPICIOUS' in struct_verdict else GREEN
    print(f"  {BOLD}Structural Analysis:{RESET}  {s_color}{struct_verdict}{RESET}  ({struct_count}/{struct_total} flagged)")

    # Timing result
    t_str = f"{RED}ANOMALY DETECTED{RESET}" if timing_anomaly else f"{GREEN}NO ANOMALY{RESET}"
    print(f"  {BOLD}Timing Analysis:{RESET}     {t_str}  (Δ={delay_diff:+.3f} ns, {anomaly_count} endpoints)")

    # Cross-referenced combined verdict
    print(f"\n{CYAN}  {'─' * 56}{RESET}")

    struct_positive = 'SUSPICIOUS' in struct_verdict or struct_count > 0
    timing_positive = timing_anomaly

    if struct_positive and timing_positive:
        combined = f"{RED}{BOLD}TROJAN DETECTED — BOTH ANALYSES CONFIRM{RESET}"
        risk = f"{RED}{BOLD}CRITICAL{RESET}"
    elif not struct_positive and timing_positive:
        combined = f"{YELLOW}{BOLD}EVASIVE TROJAN — Timing anomaly but structurally hidden{RESET}"
        risk = f"{YELLOW}{BOLD}HIGH{RESET}"
    elif struct_positive and not timing_positive:
        combined = f"{YELLOW}{BOLD}SUSPICIOUS STRUCTURE — No timing impact detected{RESET}"
        risk = f"{YELLOW}{BOLD}MEDIUM{RESET}"
    else:
        combined = f"{GREEN}{BOLD}CLEAN — No anomalies detected by either method{RESET}"
        risk = f"{GREEN}{BOLD}NONE{RESET}"

    print(f"  {BOLD}Combined Verdict:{RESET}    {combined}")
    print(f"  {BOLD}Risk Level:{RESET}          {risk}")
    print(f"{CYAN}{BOLD}{'═' * 62}{RESET}\n")


if __name__ == "__main__":
    main()
