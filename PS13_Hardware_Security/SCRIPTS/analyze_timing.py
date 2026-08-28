#!/usr/bin/env python3
"""
PS13 Hardware Security — Side-Channel Timing Analyzer
=======================================================
Compares Vivado STA timing reports between a Clean baseline
and a Trojan-suspect design. Outputs rich colored terminal
output with per-endpoint delay tables and statistical summary.

Usage:
    python analyze_timing.py --reference <clean.rpt> --suspect <trojan.rpt>
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from ANALYZER.sca.timing_parser import TimingParser
from ANALYZER.sca.timing_comparison import TimingComparator
from VISUALIZATION.timing_visualizer import TimingVisualizer

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
    print(f"\n{CYAN}{BOLD}{'━' * 62}{RESET}")
    print(f"{CYAN}{BOLD}  {title}{RESET}")
    print(f"{CYAN}{BOLD}{'━' * 62}{RESET}")


def print_endpoint_table(endpoint_details):
    """Print a rich per-endpoint comparison table."""
    print(f"\n  {BOLD}Per-Endpoint Delay Comparison:{RESET}")
    print(f"  {DIM}┌{'─'*24}┬{'─'*12}┬{'─'*12}┬{'─'*12}┬{'─'*12}┐{RESET}")
    print(f"  {DIM}│{RESET} {BOLD}{'Endpoint':<22s}{RESET} {DIM}│{RESET} {BOLD}{'Clean':>10s}{RESET} {DIM}│{RESET} {BOLD}{'Trojan':>10s}{RESET} {DIM}│{RESET} {BOLD}{'Δ Total':>10s}{RESET} {DIM}│{RESET} {BOLD}{'Δ Logic':>10s}{RESET} {DIM}│{RESET}")
    print(f"  {DIM}├{'─'*24}┼{'─'*12}┼{'─'*12}┼{'─'*12}┼{'─'*12}┤{RESET}")

    for ep in sorted(endpoint_details, key=lambda x: -abs(x['delay_diff_ns'])):
        name = ep['endpoint']
        if len(name) > 22:
            name = name[:19] + "..."

        diff = ep['delay_diff_ns']
        logic_diff = ep['logic_diff_ns']

        if diff > 0.01:
            diff_color = RED
        elif diff < -0.01:
            diff_color = YELLOW
        else:
            diff_color = GREEN

        logic_color = RED if logic_diff > 0.01 else (YELLOW if logic_diff < -0.01 else DIM)

        print(f"  {DIM}│{RESET} {name:<22s} {DIM}│{RESET} {ep['ref_delay_ns']:>9.3f}s {DIM}│{RESET} {ep['sus_delay_ns']:>9.3f}s {DIM}│{RESET} {diff_color}{diff:>+9.3f}s{RESET} {DIM}│{RESET} {logic_color}{logic_diff:>+9.3f}s{RESET} {DIM}│{RESET}")

    print(f"  {DIM}└{'─'*24}┴{'─'*12}┴{'─'*12}┴{'─'*12}┴{'─'*12}┘{RESET}")


def print_statistics(stats):
    """Print statistical summary of delay differences."""
    print(f"\n  {BOLD}Delay Difference Statistics:{RESET}")
    print(f"  {DIM}│{RESET} {'Mean Δ':<20s} {stats.get('mean_diff_ns', 0):>+.4f} ns")
    print(f"  {DIM}│{RESET} {'Median Δ':<20s} {stats.get('median_diff_ns', 0):>+.4f} ns")
    print(f"  {DIM}│{RESET} {'Std Dev':<20s} {stats.get('stdev_diff_ns', 0):>.4f} ns")
    print(f"  {DIM}│{RESET} {'Min Δ':<20s} {stats.get('min_diff_ns', 0):>+.4f} ns")
    print(f"  {DIM}│{RESET} {'Max Δ':<20s} {stats.get('max_diff_ns', 0):>+.4f} ns")
    print(f"  {DIM}│{RESET} {'Total Endpoints':<20s} {stats.get('total_endpoints', 0)}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze and compare Side-Channel Timing from Vivado STA reports."
    )
    parser.add_argument('--reference', required=True,
                        help="Path to the reference (clean) Vivado timing report (.rpt)")
    parser.add_argument('--suspect', required=True,
                        help="Path to the suspect (Trojan) Vivado timing report (.rpt)")
    parser.add_argument('--out-json', default="REPORTS/sca/timing_comparison.json",
                        help="Output JSON path")
    parser.add_argument('--out-vis-dir', default="REPORTS/sca/",
                        help="Output directory for visualizations")

    args = parser.parse_args()

    print_header("PS13 Hardware Security — Side-Channel Timing Analysis")

    # Parse reports
    print(f"\n{MAGENTA}[STEP 1/4]{RESET} {BOLD}Parsing timing reports...{RESET}")
    timing_parser = TimingParser()
    try:
        ref_data = timing_parser.parse_report(args.reference)
        ref_data['design'] = "ALU8_CLEAN"
        ref_paths = len(ref_data.get('critical_paths', []))
        print(f"  {DIM}│{RESET} Reference: {args.reference} ({ref_paths} paths)")
    except FileNotFoundError:
        print(f"  {RED}[ERROR] Reference report not found: {args.reference}{RESET}")
        return

    try:
        sus_data = timing_parser.parse_report(args.suspect)
        sus_data['design'] = "ALU8_TROJAN"
        sus_paths = len(sus_data.get('critical_paths', []))
        print(f"  {DIM}│{RESET} Suspect:   {args.suspect} ({sus_paths} paths)")
    except FileNotFoundError:
        print(f"  {RED}[ERROR] Suspect report not found: {args.suspect}{RESET}")
        return

    # Compare
    print(f"\n{MAGENTA}[STEP 2/4]{RESET} {BOLD}Performing timing comparison (SCA)...{RESET}")
    comparator = TimingComparator()
    comparison_results = comparator.compare(ref_data, sus_data)

    # Save JSON
    out_path = Path(args.out_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(comparison_results, f, indent=4)
    print(f"  {DIM}│{RESET} Results saved to {args.out_json}")

    # Per-endpoint table
    print(f"\n{MAGENTA}[STEP 3/4]{RESET} {BOLD}Per-endpoint analysis...{RESET}")
    endpoint_details = comparison_results.get('endpoint_details', [])
    if endpoint_details:
        print_endpoint_table(endpoint_details)
    else:
        print(f"  {YELLOW}No endpoint data available.{RESET}")

    # Statistics
    stats = comparison_results.get('delay_statistics', {})
    if stats:
        print_statistics(stats)

    # Visualizations
    print(f"\n{MAGENTA}[STEP 4/4]{RESET} {BOLD}Generating visualizations...{RESET}")
    visualizer = TimingVisualizer(output_dir=args.out_vis_dir)

    from ANALYZER.sca.delay_analysis import DelayAnalyzer
    from ANALYZER.sca.slack_analysis import SlackAnalyzer
    da = DelayAnalyzer()
    sa = SlackAnalyzer()

    ref_crit = da.analyze_delays(ref_data).get("critical_delay_ns", 0.0)
    sus_crit = da.analyze_delays(sus_data).get("critical_delay_ns", 0.0)
    visualizer.plot_delay_comparison(ref_crit, sus_crit, "Clean", "Trojan")

    ref_wns = sa.analyze_slack(ref_data).get("worst_negative_slack_ns", 0.0)
    sus_wns = sa.analyze_slack(sus_data).get("worst_negative_slack_ns", 0.0)
    visualizer.plot_slack_comparison(ref_wns, sus_wns, "Clean", "Trojan")

    print(f"  {DIM}│{RESET} Plots saved to {args.out_vis_dir}")

    # Final Verdict
    metrics = comparison_results['metrics']
    delay_diff = metrics.get('max_endpoint_delay_difference_ns', 0.0)
    anomaly_count = metrics.get('anomalies_count', 0)
    anomaly_detected = comparison_results['assessment']['timing_anomaly']
    leakage = comparison_results['assessment'].get('potential_timing_leakage', False)
    confidence = comparison_results['assessment']['confidence']

    print(f"\n{CYAN}{BOLD}{'━' * 62}{RESET}")
    print(f"{CYAN}{BOLD}  SIDE-CHANNEL TIMING ANALYSIS — RESULT SUMMARY{RESET}")
    print(f"{CYAN}{BOLD}{'━' * 62}{RESET}")
    print(f"  Reference Design:    {comparison_results['reference_design']}")
    print(f"  Suspect Design:      {comparison_results['suspect_design']}")

    delay_color = RED if delay_diff > 0.5 else (YELLOW if delay_diff > 0.01 else GREEN)
    print(f"  Max Delay Diff:      {delay_color}{BOLD}{delay_diff:+.3f} ns{RESET}")
    print(f"  Affected Endpoints:  {RED if anomaly_count > 0 else GREEN}{anomaly_count}{RESET}")
    if anomaly_count > 0:
        print(f"  Worst Endpoint:      {metrics.get('worst_affected_endpoint')}")

    print(f"{CYAN}  {'─' * 58}{RESET}")

    anomaly_str = f"{RED}{BOLD}YES{RESET}" if anomaly_detected else f"{GREEN}{BOLD}NO{RESET}"
    print(f"  Timing Anomaly:      {anomaly_str}")

    leakage_str = f"{YELLOW}{BOLD}YES{RESET}" if leakage else f"{GREEN}NO{RESET}"
    print(f"  Timing Leakage:      {leakage_str}")

    conf_color = RED if confidence == 'HIGH' else (YELLOW if confidence == 'MEDIUM' else GREEN)
    print(f"  Confidence:          {conf_color}{BOLD}{confidence}{RESET}")
    print(f"{CYAN}{BOLD}{'━' * 62}{RESET}\n")


if __name__ == "__main__":
    main()
