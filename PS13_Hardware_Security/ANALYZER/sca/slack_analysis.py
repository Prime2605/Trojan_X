from typing import Dict, Any

class SlackAnalyzer:
    """Analyzes worst negative slack (WNS) and total negative slack (TNS)."""

    def analyze_slack(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts slack metrics and checks for timing violations."""
        summary = parsed_data.get("summary", {})
        wns = summary.get("WNS", 0.0)
        tns = summary.get("TNS", 0.0)
        
        analysis = {
            "worst_negative_slack_ns": wns,
            "total_negative_slack_ns": tns,
            "timing_met": wns >= 0.0
        }
        
        if not analysis["timing_met"]:
            analysis["note"] = "Timing requirements are violated (WNS < 0)."
            
        return analysis
