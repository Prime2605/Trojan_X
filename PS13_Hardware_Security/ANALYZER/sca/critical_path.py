from typing import Dict, Any, List

class CriticalPathAnalyzer:
    """Isolates and analyzes the worst-case timing path."""

    def identify_critical_path(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Finds the path with the worst (lowest) slack or highest delay."""
        paths = parsed_data.get("critical_paths", [])
        
        if not paths:
            return {"error": "No paths available to determine critical path"}
            
        # Assuming the parser preserves Vivado's ordering (worst slack first)
        # We can just take the first path, or sort to be sure
        
        # Sort by slack ascending
        sorted_paths = sorted(paths, key=lambda x: x.get("slack_ns", 0.0))
        critical_path = sorted_paths[0]
        
        return {
            "startpoint": critical_path.get("startpoint"),
            "endpoint": critical_path.get("endpoint"),
            "total_delay_ns": critical_path.get("total_delay_ns"),
            "slack_ns": critical_path.get("slack_ns"),
            "path_elements": critical_path.get("path_elements", [])
        }
