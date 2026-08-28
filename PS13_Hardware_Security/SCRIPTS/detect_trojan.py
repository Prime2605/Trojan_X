#!/usr/bin/env python3
"""
PS13 Hardware Security — Trojan Detection Script
===================================================
Run Trojan detection on extracted features.

Usage:
    python detect_trojan.py --features <features.json> [--threshold 0.6] [--output <detection.json>]
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYZER.detection.trojan_detector import TrojanDetector


def main():
    parser = argparse.ArgumentParser(
        description="Detect suspicious regions in netlist features."
    )
    parser.add_argument("--features", required=True,
                        help="Path to features JSON (from extract_features.py)")
    parser.add_argument("--threshold", type=float, default=0.6,
                        help="Suspicion score threshold (0.0-1.0, default: 0.6)")
    parser.add_argument("--output", default=None,
                        help="Output detection JSON path")
    args = parser.parse_args()

    if args.output is None:
        base_name = os.path.splitext(os.path.basename(args.features))[0]
        base_name = base_name.replace("_features", "")
        args.output = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "REPORTS", "trojan", f"{base_name}_detection.json"
        )

    print(f"[*] Loading features from: {args.features}")
    with open(args.features, 'r') as f:
        feature_data = json.load(f)

    print(f"[*] Running Trojan detection (threshold={args.threshold})...")
    detector = TrojanDetector(feature_data, threshold=args.threshold)
    suspicious = detector.detect()

    summary = detector.get_detection_summary()
    print(f"[+] Analyzed {summary['total_cells_analyzed']} cells")
    print(f"[+] Found {summary['suspicious_count']} suspicious cells")

    if suspicious:
        print(f"[!] Top suspicious cells:")
        for s in summary.get("top_suspicious", [])[:5]:
            print(f"    - {s['cell']} (score: {s['score']:.4f}, type: {s['type']})")
    else:
        print(f"[+] No suspicious cells found above threshold.")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    detector.to_json(args.output)
    print(f"[+] Saved detection results to: {args.output}")


if __name__ == "__main__":
    main()
