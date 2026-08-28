#!/usr/bin/env python3
"""
PS13 Hardware Security — Netlist Parser Script
================================================
Parse a gate-level Verilog netlist and save structured data to JSON.

Usage:
    python run_parser.py --netlist <path_to_netlist.v> [--output <output.json>]
"""

import argparse
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYZER.parser.netlist_parser import NetlistParser


def main():
    parser = argparse.ArgumentParser(
        description="Parse a gate-level Verilog netlist."
    )
    parser.add_argument("--netlist", required=True,
                        help="Path to the Verilog netlist file")
    parser.add_argument("--output", default=None,
                        help="Output JSON path (default: DATA/features/<name>_parsed.json)")
    args = parser.parse_args()

    # Default output path
    if args.output is None:
        base_name = os.path.splitext(os.path.basename(args.netlist))[0]
        args.output = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "DATA", "features", f"{base_name}_parsed.json"
        )

    print(f"[*] Parsing netlist: {args.netlist}")
    np = NetlistParser(args.netlist)

    if not np.parse():
        print("[ERROR] Failed to parse netlist.")
        sys.exit(1)

    # Print summary
    summary = np.get_summary()
    print(f"[+] Modules:   {summary['module_count']}")
    print(f"[+] Instances: {summary['instance_count']}")
    print(f"[+] Nets:      {summary['net_count']}")
    print(f"[+] Ports:     {summary['port_count']}")
    print(f"[+] Cell types: {summary['cell_types']}")

    # Save output
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    np.to_json(args.output)
    print(f"[+] Saved parsed data to: {args.output}")


if __name__ == "__main__":
    main()
