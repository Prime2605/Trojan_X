from typing import Dict, Any, List
import statistics

class DelayAnalyzer:
    """Computes statistical metrics for path delays."""

    def analyze_delays(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates min, max, mean, and median delays from critical paths."""
        paths = parsed_data.get("critical_paths", [])
        
        if not paths:
            return {"error": "No paths available for delay analysis"}
            
        delays = [p.get("total_delay_ns", 0.0) for p in paths]
        
        analysis = {
            "min_delay_ns": min(delays),
            "max_delay_ns": max(delays),
            "critical_delay_ns": max(delays)
        }
        
        if len(delays) > 1:
            analysis["mean_delay_ns"] = statistics.mean(delays)
            analysis["median_delay_ns"] = statistics.median(delays)
            analysis["delay_spread_ns"] = max(delays) - min(delays)
        else:
            analysis["note"] = "Single path provided; statistical metrics not meaningful."
            
        return analysis
