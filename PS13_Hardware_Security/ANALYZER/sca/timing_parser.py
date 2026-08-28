import re
import json
from pathlib import Path
from typing import Dict, Any, List

class TimingParser:
    """Parses Vivado static timing analysis reports (.rpt) into structured JSON."""

    def __init__(self):
        pass

    def parse_report(self, filepath: str) -> Dict[str, Any]:
        """Parses a Vivado report_timing_summary output file."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Timing report not found: {filepath}")

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        timing_data = {
            "source": "Vivado_STA",
            "summary": self._extract_summary(content),
            "critical_paths": self._extract_critical_paths(content)
        }
        return timing_data

    def _extract_summary(self, content: str) -> Dict[str, float]:
        """Extracts WNS, TNS, WHS, THS from the Design Timing Summary section."""
        summary = {"WNS": 0.0, "TNS": 0.0, "WHS": 0.0, "THS": 0.0}
        
        # Example Vivado format:
        # WNS(ns)      TNS(ns)  TNS Failing Endpoints  TNS Total Endpoints      WHS(ns)      THS(ns)  THS Failing Endpoints  THS Total Endpoints     WPWS(ns)     TPWS(ns)  TPWS Failing Endpoints  TPWS Total Endpoints  
        # -------      -------  ---------------------  -------------------      -------      -------  ---------------------  -------------------     --------     --------  ----------------------  --------------------  
        #   2.500        0.000                      0                  100        0.100        0.000                      0                  100        3.000        0.000                       0                    45  
        
        # We will use regex to find the line with the numbers after the dashes.
        # This is a simplified regex targeting the standard format.
        summary_regex = re.search(r'WNS\(ns\).*?\n\s*-+\s*-+.*?\n\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+\d+\s+\d+\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)', content)
        
        if summary_regex:
            summary["WNS"] = float(summary_regex.group(1))
            summary["TNS"] = float(summary_regex.group(2))
            summary["WHS"] = float(summary_regex.group(3))
            summary["THS"] = float(summary_regex.group(4))
        else:
            # Fallback for plain report_timing or different formats
            wns_match = re.search(r'Slack\s*\(VIOLATED\)\s*:\s*(-?\d+\.\d+)ns', content) or re.search(r'Slack\s*\(MET\)\s*:\s*(-?\d+\.\d+)ns', content)
            if wns_match:
                summary["WNS"] = float(wns_match.group(1))
                
        return summary

    def _extract_critical_paths(self, content: str) -> List[Dict[str, Any]]:
        """Extracts individual path details (startpoint, endpoint, delay, slack)."""
        paths = []
        
        # Split into individual path reports
        path_blocks = re.split(r'Slack\s*(?:\(.*\))?\s*:\s*', content)
        
        # The first block is the header, skip it
        for block in path_blocks[1:]:
            path_info = self._parse_single_path(block)
            if path_info:
                paths.append(path_info)
                
        return paths

    def _parse_single_path(self, block: str) -> Dict[str, Any]:
        """Parses a single timing path block."""
        path = {}
        
        # Source/Destination format in report_timing for unconstrained paths
        # Source: SW[7] (input port)
        # Destination: LED[3] (output port)
        start_match = re.search(r'Source:\s+(\S+)', block)
        end_match = re.search(r'Destination:\s+(\S+)', block)
        delay_match = re.search(r'Data Path Delay:\s+(\d+\.\d+)ns', block)
        
        # Format might be slightly different in summary vs report_timing
        logic_delay_match = re.search(r'Data Path Delay:.*\(logic\s+(\d+\.\d+)ns.*route\s+(\d+\.\d+)ns\)', block)
        
        if start_match and end_match and delay_match:
            path['startpoint'] = start_match.group(1)
            path['endpoint'] = end_match.group(1)
            path['total_delay_ns'] = float(delay_match.group(1))
            
            if logic_delay_match:
                path['logic_delay_ns'] = float(logic_delay_match.group(1))
                path['net_delay_ns'] = float(logic_delay_match.group(2))
            else:
                path['logic_delay_ns'] = 0.0
                path['net_delay_ns'] = 0.0
                
            # Extract elements on the path
            elements = []
            for line in block.split('\n'):
                # In summary format: (LUT4=2, MUXF7=1)
                # In detailed format: ...  LUT4 (Prop_lut4_I0_O) ...
                # Also handle IBUF and OBUF
                cell_matches = re.findall(r'(IBUF|OBUF|LUT\d|FDRE|FDCE|MUXF\d|CARRY\d)', line)
                for match in cell_matches:
                    if match not in elements:
                        elements.append(match)
            path['path_elements'] = elements
            
            return path
            
        return None
