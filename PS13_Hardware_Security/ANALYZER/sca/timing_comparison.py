from typing import Dict, Any, List
import statistics
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
        
        # Map worst delay per endpoint with logic/route breakdown
        def map_endpoints(paths):
            ep_map = {}
            for p in paths:
                ep = p.get("endpoint")
                delay = p.get("total_delay_ns", 0.0)
                if ep not in ep_map or delay > ep_map[ep]["delay"]:
                    ep_map[ep] = {
                        "delay": delay,
                        "logic_delay": p.get("logic_delay_ns", 0.0),
                        "net_delay": p.get("net_delay_ns", 0.0),
                        "elements": p.get("path_elements", []),
                        "startpoint": p.get("startpoint", "?"),
                    }
            return ep_map
            
        ref_ep_map = map_endpoints(ref_paths)
        sus_ep_map = map_endpoints(sus_paths)
        
        # Per-endpoint comparison
        endpoint_details = []
        anomalies = []
        all_diffs = []
        max_diff = 0.0
        max_diff_ep = None
        
        # Merge all endpoints from both designs
        all_endpoints = sorted(set(list(ref_ep_map.keys()) + list(sus_ep_map.keys())))
        
        for ep in all_endpoints:
            ref_info = ref_ep_map.get(ep)
            sus_info = sus_ep_map.get(ep)
            
            ref_delay = ref_info["delay"] if ref_info else 0.0
            sus_delay = sus_info["delay"] if sus_info else 0.0
            diff = sus_delay - ref_delay
            all_diffs.append(diff)
            
            ref_logic = ref_info["logic_delay"] if ref_info else 0.0
            sus_logic = sus_info["logic_delay"] if sus_info else 0.0
            ref_route = ref_info["net_delay"] if ref_info else 0.0
            sus_route = sus_info["net_delay"] if sus_info else 0.0
            
            detail = {
                "endpoint": ep,
                "startpoint": (sus_info or ref_info or {}).get("startpoint", "?"),
                "ref_delay_ns": round(ref_delay, 3),
                "sus_delay_ns": round(sus_delay, 3),
                "delay_diff_ns": round(diff, 3),
                "ref_logic_ns": round(ref_logic, 3),
                "sus_logic_ns": round(sus_logic, 3),
                "logic_diff_ns": round(sus_logic - ref_logic, 3),
                "ref_route_ns": round(ref_route, 3),
                "sus_route_ns": round(sus_route, 3),
                "route_diff_ns": round(sus_route - ref_route, 3),
                "in_ref": ref_info is not None,
                "in_sus": sus_info is not None,
            }
            endpoint_details.append(detail)
            
            if abs(diff) > abs(max_diff):
                max_diff = diff
                max_diff_ep = ep
                
            if diff > 0.01:
                anomalies.append({
                    "endpoint": ep,
                    "delay_diff_ns": round(diff, 3),
                    "logic_diff_ns": round(sus_logic - ref_logic, 3),
                    "route_diff_ns": round(sus_route - ref_route, 3),
                    "suspect_elements": (sus_info or {}).get("elements", [])
                })
        
        # Statistical summary of delay differences
        delay_stats = {}
        if all_diffs:
            delay_stats = {
                "mean_diff_ns": round(statistics.mean(all_diffs), 4),
                "median_diff_ns": round(statistics.median(all_diffs), 4),
                "stdev_diff_ns": round(statistics.stdev(all_diffs), 4) if len(all_diffs) > 1 else 0.0,
                "min_diff_ns": round(min(all_diffs), 4),
                "max_diff_ns": round(max(all_diffs), 4),
                "total_endpoints": len(all_diffs),
            }
        
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
            "delay_statistics": delay_stats,
            "endpoint_details": endpoint_details,
            "assessment": {
                "timing_anomaly": timing_anomaly,
                "potential_timing_leakage": timing_anomaly and max_diff > 0.5,
                "confidence": "HIGH" if timing_anomaly else "INCONCLUSIVE"
            }
        }
        
        if timing_anomaly:
            result["assessment"]["note"] = f"Endpoint-specific structural delay penalty detected on {len(anomalies)} endpoint(s). Max delta = {max_diff:.3f} ns."
            
        return result
