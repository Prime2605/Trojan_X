from typing import Dict, Any, List

class PathAnalyzer:
    """Analyzes extracted timing paths to identify structural properties."""

    def analyze_paths(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Performs analysis on the extracted timing paths."""
        paths = parsed_data.get("critical_paths", [])
        
        analysis = {
            "total_paths_analyzed": len(paths),
            "max_logic_depth": 0,
            "common_endpoints": {},
            "common_startpoints": {}
        }
        
        for p in paths:
            # Count elements for depth
            depth = len(p.get("path_elements", []))
            if depth > analysis["max_logic_depth"]:
                analysis["max_logic_depth"] = depth
                
            # Aggregate endpoints
            ep = p.get("endpoint", "unknown")
            analysis["common_endpoints"][ep] = analysis["common_endpoints"].get(ep, 0) + 1
            
            # Aggregate startpoints
            sp = p.get("startpoint", "unknown")
            analysis["common_startpoints"][sp] = analysis["common_startpoints"].get(sp, 0) + 1
            
        return analysis
