from typing import Dict, Any
from .delay_analysis import DelayAnalyzer
from .slack_analysis import SlackAnalyzer
from .critical_path import CriticalPathAnalyzer

class TimingComparator:
    """Compares the timing profiles of a Reference (Clean) and Suspect (Trojan) design."""

    def __init__(self):
        self.delay_analyzer = DelayAnalyzer()
        self.slack_analyzer = SlackAnalyzer()
        self.critical_path_analyzer = CriticalPathAnalyzer()

    def compare(self, reference_data: Dict[str, Any], suspect_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compares two parsed timing reports and assesses potential leakage per endpoint."""
        ref_paths = reference_data.get("critical_paths", [])
        sus_paths = suspect_data.get("critical_paths", [])
        
        # Map worst delay per endpoint
        def map_endpoints(paths):
            ep_map = {}
            for p in paths:
                ep = p.get("endpoint")
                delay = p.get("total_delay_ns", 0.0)
                # report_timing lists worst path first per group usually, but let's take max
                if ep not in ep_map or delay > ep_map[ep]["delay"]:
                    ep_map[ep] = {"delay": delay, "elements": p.get("path_elements", [])}
            return ep_map
            
        ref_ep_map = map_endpoints(ref_paths)
        sus_ep_map = map_endpoints(sus_paths)
        
        anomalies = []
        max_diff = 0.0
        max_diff_ep = None
        
        for ep, sus_info in sus_ep_map.items():
            ref_info = ref_ep_map.get(ep)
            if not ref_info:
                # New endpoint entirely (unlikely but possible)
                continue
                
            diff = sus_info["delay"] - ref_info["delay"]
            if diff > max_diff:
                max_diff = diff
                max_diff_ep = ep
                
            # Threshold for structural delay insertion (e.g. adding a LUT adds ~0.2ns logic + routing)
            # We use 0.01ns just to be extremely sensitive to any static routing change
            if diff > 0.01:
                anomalies.append({
                    "endpoint": ep,
                    "delay_diff_ns": round(diff, 3),
                    "suspect_elements": sus_info["elements"]
                })
        
        timing_anomaly = len(anomalies) > 0
        
        result = {
            "reference_design": reference_data.get("design", "CLEAN"),
            "suspect_design": suspect_data.get("design", "SUSPECT"),
            "metrics": {
                "max_endpoint_delay_difference_ns": round(max_diff, 3),
                "worst_affected_endpoint": max_diff_ep,
                "anomalies_count": len(anomalies),
                "anomalies": anomalies
            },
            "assessment": {
                "timing_anomaly": timing_anomaly,
                "potential_timing_leakage": False, # Requires observable physical data
                "confidence": "HIGH" if timing_anomaly else "INCONCLUSIVE"
            }
        }
        
        if timing_anomaly:
            result["assessment"]["note"] = f"Endpoint-specific structural delay penalty detected on {len(anomalies)} endpoint(s). True side-channel exploitability requires physical observability."
            
        return result
