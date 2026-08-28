#!/usr/bin/env python3
"""
PS13 Hardware Security — Netlist Restoration Tool
===================================================
Uses Gate-Level Path Retracing to recover a Trojan-infected netlist.
Isolates flagged cells, neutralizes payload triggers by tying them
to logic 0, and regenerates a clean Verilog netlist.

Usage:
    python run_recovery.py --netlist <infected.v> --detection <detection.json> --out <restored.v>
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYZER.parser.netlist_parser import NetlistParser
from ANALYZER.recovery.netlist_restorer import NetlistRestorer

# ANSI
RED = '\033[91m'
GREEN = '\033[92m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'

def main():
    parser = argparse.ArgumentParser(description="PS13 Netlist Restoration via Path Retracing")
    parser.add_argument("--netlist", required=True, help="Infected Gate-level Verilog netlist")
    parser.add_argument("--detection", required=True, help="Path to detection.json from Structural Analysis")
    parser.add_argument("--out", required=True, help="Path to output the restored netlist")
    args = parser.parse_args()

    print(f"\n{CYAN}{BOLD}{'━' * 62}{RESET}")
    print(f"{CYAN}{BOLD}  PS13 Hardware Security — Trojan Recovery{RESET}")
    print(f"{CYAN}{BOLD}{'━' * 62}{RESET}")

    print(f"\n{MAGENTA}[STEP 1/3]{RESET} {BOLD}Parsing Infected Netlist...{RESET}")
    np = NetlistParser(args.netlist)
    if not np.parse():
        print(f"  {RED}[ERROR] Failed to parse netlist.{RESET}")
        sys.exit(1)
        
    print(f"  {GREEN}[OK]{RESET} AST built successfully.")

    print(f"\n{MAGENTA}[STEP 2/3]{RESET} {BOLD}Loading Detection Results...{RESET}")
    if not os.path.exists(args.detection):
        print(f"  {RED}[ERROR] Detection file not found: {args.detection}{RESET}")
        sys.exit(1)
        
    with open(args.detection, 'r') as f:
        det_data = json.load(f)
        
    suspicious = det_data.get("suspicious_cells", [])
    if not suspicious:
        print(f"  {GREEN}[OK]{RESET} No suspicious cells found. Netlist is already clean.")
        # Just copy file
        import shutil
        shutil.copy2(args.netlist, args.out)
        sys.exit(0)
        
    print(f"  {GREEN}[OK]{RESET} Loaded {len(suspicious)} flagged cells.")

    print(f"\n{MAGENTA}[STEP 3/3]{RESET} {BOLD}Executing Gate-Level Path Retracing & Restoration...{RESET}")
    restorer = NetlistRestorer(np, suspicious)
    success = restorer.restore()
    
    if success:
        out_dir = os.path.dirname(args.out)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            
        restorer.generate_verilog(args.out)
        print(f"\n{CYAN}{BOLD}{'━' * 62}{RESET}")
        print(f"  {GREEN}{BOLD}RECOVERY SUCCESSFUL!{RESET}")
        print(f"  Restored netlist saved to: {args.out}")
        print(f"  Payload triggers have been zeroed. Run synthesis to eliminate dead code.")
        print(f"{CYAN}{BOLD}{'━' * 62}{RESET}\n")
    else:
        print(f"\n  {RED}{BOLD}RECOVERY FAILED.{RESET} No modifications were made.\n")

if __name__ == "__main__":
    main()
