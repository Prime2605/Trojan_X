import argparse
import json
import sys
from pathlib import Path

# Add the project root to the python path so we can import the ANALYZER and VISUALIZATION modules
sys.path.append(str(Path(__file__).resolve().parent.parent))

from ANALYZER.sca.timing_parser import TimingParser
from ANALYZER.sca.timing_comparison import TimingComparator
from VISUALIZATION.timing_visualizer import TimingVisualizer

def main():
    parser = argparse.ArgumentParser(description="Analyze and compare Side-Channel Timing Leakage from Vivado STA reports.")
    parser.add_argument('--reference', required=True, help="Path to the reference (clean) Vivado timing summary report (.rpt)")
    parser.add_argument('--suspect', required=True, help="Path to the suspect (Trojan) Vivado timing summary report (.rpt)")
    parser.add_argument('--out-json', default="REPORTS/sca/timing_comparison.json", help="Output JSON path")
    parser.add_argument('--out-vis-dir', default="REPORTS/sca/", help="Output directory for visualizations")
    
    args = parser.parse_args()
    
    print(f"[*] Parsing Reference Timing Report: {args.reference}")
    timing_parser = TimingParser()
    try:
        ref_data = timing_parser.parse_report(args.reference)
        ref_data['design'] = "ALU8_CLEAN" # Assign logical names
    except FileNotFoundError:
        print(f"[!] Error: Reference report not found: {args.reference}")
        print("    Please run Vivado Synthesis and export report_timing_summary.")
        return
        
    print(f"[*] Parsing Suspect Timing Report: {args.suspect}")
    try:
        sus_data = timing_parser.parse_report(args.suspect)
        sus_data['design'] = "ALU8_TROJAN"
    except FileNotFoundError:
        print(f"[!] Error: Suspect report not found: {args.suspect}")
        print("    Please run Vivado Synthesis and export report_timing_summary.")
        return

    print("[*] Performing Timing Comparison (SCA)")
    comparator = TimingComparator()
    comparison_results = comparator.compare(ref_data, sus_data)
    
    # Save JSON
    out_path = Path(args.out_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(comparison_results, f, indent=4)
    print(f"[+] Saved comparison results to {args.out_json}")
    
    # Visualizations
    print("[*] Generating Visualizations")
    visualizer = TimingVisualizer(output_dir=args.out_vis_dir)
    
    # Re-extract critical delay for plotting since it's not directly in the comparison result root
    # but we can get it from the delay analyzer again, or just pass the objects
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
    
    print(f"[+] Saved visualizations to {args.out_vis_dir}")
    
    # Print Summary with ANSI Colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    print(f"\n{CYAN}{BOLD}===================================================={RESET}")
    print(f"{CYAN}{BOLD} SIDE-CHANNEL TIMING ANALYSIS (STA) RESULT SUMMARY{RESET}")
    print(f"{CYAN}{BOLD}===================================================={RESET}")
    print(f" Reference Design: {comparison_results['reference_design']}")
    print(f" Suspect Design:   {comparison_results['suspect_design']}")
    
    metrics = comparison_results['metrics']
    delay_diff = metrics.get('max_endpoint_delay_difference_ns', 0.0)
    delay_color = RED if delay_diff > 0.01 else GREEN
    print(f" Max Delay Diff:   {delay_color}{delay_diff} ns{RESET}")
    print(f" Affected Endpoints: {metrics.get('anomalies_count', 0)}")
    if metrics.get('anomalies_count', 0) > 0:
        print(f" Worst Endpoint:   {metrics.get('worst_affected_endpoint')}")
        
    print(f"{CYAN}----------------------------------------------------{RESET}")
    
    anomaly_detected = comparison_results['assessment']['timing_anomaly']
    anomaly_str = f"{RED}YES{RESET}" if anomaly_detected else f"{GREEN}NO{RESET}"
    print(f" Timing Anomaly Detected: {BOLD}{anomaly_str}{RESET}")
    
    leakage = comparison_results['assessment']['potential_timing_leakage']
    leakage_str = f"{YELLOW}YES{RESET}" if leakage else f"{GREEN}NO{RESET}"
    print(f" Potential Timing Leakage: {leakage_str}")
    
    confidence = comparison_results['assessment']['confidence']
    conf_color = RED if confidence == 'HIGH' else (YELLOW if confidence == 'MEDIUM' else GREEN)
    print(f" Confidence: {conf_color}{confidence}{RESET}")
    print(f"{CYAN}{BOLD}===================================================={RESET}\n")

if __name__ == "__main__":
    main()
