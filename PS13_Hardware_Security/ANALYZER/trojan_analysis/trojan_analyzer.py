"""
PS13 Hardware Security — Trojan Analyzer
==========================================
Deep analysis of suspicious regions identified by TrojanDetector.

Analyzes:
  - Trigger characterization (input conditions, activation paths)
  - Payload characterization (affected outputs, corruption type)
  - Logic cone analysis (what the Trojan can see and affect)
  - Propagation paths (how the Trojan effect reaches outputs)
  - Impact assessment (which outputs are compromised)
"""

import json
from typing import Dict, List, Any, Optional


class TrojanAnalyzer:
    """
    Perform deep analysis on detected suspicious cells to characterize
    potential Trojan trigger and payload structures.
    """

    def __init__(self, circuit_graph, suspicious_cells: List[Dict]):
        """
        Initialize with circuit graph and detected suspicious cells.

        Args:
            circuit_graph:    A built CircuitGraph instance.
            suspicious_cells: Output from TrojanDetector.detect().
        """
        self.cg = circuit_graph
        self.suspicious = suspicious_cells
        self.analysis_results = []
        self._analyzed = False

    def analyze(self) -> List[Dict]:
        """
        Analyze all suspicious cells and characterize potential Trojans.

        Returns:
            List of analysis results for each suspicious region.
        """
        self.analysis_results = []

        for cell_data in self.suspicious:
            cell_name = cell_data["cell"]
            result = self._analyze_cell(cell_name, cell_data)
            self.analysis_results.append(result)

        self._analyzed = True
        return self.analysis_results

    def _analyze_cell(self, cell_name: str, cell_data: Dict) -> Dict:
        """Perform deep analysis on a single suspicious cell."""
        # Logic cone analysis
        logic_cone = self.cg.get_logic_cone(cell_name)
        influence_cone = self.cg.get_influence_cone(cell_name)

        # Identify input ports in the logic cone (potential trigger inputs)
        trigger_inputs = []
        for node in logic_cone:
            attrs = self.cg.graph.nodes.get(node, {})
            if attrs.get("node_type") == "port" and attrs.get("direction") == "input":
                trigger_inputs.append(node.replace("PORT_", ""))

        # Identify output ports in the influence cone (affected outputs)
        affected_outputs = []
        for node in influence_cone:
            attrs = self.cg.graph.nodes.get(node, {})
            if attrs.get("node_type") == "port" and attrs.get("direction") == "output":
                affected_outputs.append(node.replace("PORT_", ""))

        # Categorize cells in the logic cone by type
        cone_cell_types = {}
        for node in logic_cone:
            attrs = self.cg.graph.nodes.get(node, {})
            if attrs.get("node_type") == "cell":
                ct = attrs.get("cell_type", "unknown")
                cone_cell_types[ct] = cone_cell_types.get(ct, 0) + 1

        # Check for sequential elements (FFs) in the cone
        sequential_elements = []
        ff_types = {"FDRE", "FDSE", "FDCE", "FDPE", "FD", "FDE", "LDCE", "LDPE"}
        for node in logic_cone | influence_cone:
            attrs = self.cg.graph.nodes.get(node, {})
            if attrs.get("cell_type", "").upper() in ff_types:
                sequential_elements.append(node)

        # Classify as trigger-like or payload-like
        classification = self._classify_role(
            cell_name, cell_data, trigger_inputs, affected_outputs,
            sequential_elements
        )

        return {
            "cell": cell_name,
            "cell_type": cell_data.get("cell_type", "unknown"),
            "suspicion_score": cell_data.get("total_score", 0),
            "classification": classification,
            "trigger_analysis": {
                "potential_trigger_inputs": trigger_inputs,
                "trigger_input_count": len(trigger_inputs),
                "logic_cone_size": len(logic_cone),
                "cone_cell_types": cone_cell_types,
            },
            "payload_analysis": {
                "affected_outputs": affected_outputs,
                "affected_output_count": len(affected_outputs),
                "influence_cone_size": len(influence_cone),
            },
            "sequential_analysis": {
                "has_sequential_elements": len(sequential_elements) > 0,
                "sequential_count": len(sequential_elements),
                "sequential_cells": sequential_elements[:10],  # Limit output
            },
            "impact_assessment": {
                "severity": self._assess_severity(affected_outputs),
                "trojan_type_estimate": self._estimate_type(
                    sequential_elements, trigger_inputs
                ),
            }
        }

    def _classify_role(self, cell_name: str, cell_data: Dict,
                       trigger_inputs: List, affected_outputs: List,
                       sequential_elements: List) -> str:
        """Classify cell as likely trigger, payload, or intermediate."""
        fan_in = cell_data.get("features", {}).get("fan_in", 0)
        fan_out = cell_data.get("features", {}).get("fan_out", 0)

        # Trigger cells: high fan-in (many inputs), low fan-out
        if fan_in > fan_out and len(trigger_inputs) > 2:
            return "likely_trigger"
        # Payload cells: low fan-in, high fan-out to outputs
        elif fan_out > fan_in and len(affected_outputs) > 0:
            return "likely_payload"
        else:
            return "intermediate"

    def _assess_severity(self, affected_outputs: List) -> str:
        """Assess severity based on number of affected outputs."""
        count = len(affected_outputs)
        if count == 0:
            return "none"
        elif count <= 2:
            return "low"
        elif count <= 4:
            return "medium"
        else:
            return "high"

    def _estimate_type(self, sequential_elements: List,
                       trigger_inputs: List) -> str:
        """Estimate Trojan type based on structural characteristics."""
        if sequential_elements:
            return "sequential (state-based trigger)"
        elif len(trigger_inputs) >= 8:
            return "combinational (wide trigger — rare condition)"
        elif len(trigger_inputs) >= 4:
            return "combinational (moderate trigger)"
        else:
            return "combinational (simple trigger)"

    def get_summary(self) -> Dict[str, Any]:
        """Return analysis summary."""
        if not self._analyzed:
            self.analyze()
        return {
            "total_suspicious": len(self.suspicious),
            "analyzed_count": len(self.analysis_results),
            "classifications": {
                r["classification"]: sum(
                    1 for x in self.analysis_results
                    if x["classification"] == r["classification"]
                )
                for r in self.analysis_results
            },
            "estimated_types": [
                r["impact_assessment"]["trojan_type_estimate"]
                for r in self.analysis_results
            ]
        }

    def to_json(self, output_path: str) -> None:
        """Export analysis results to JSON."""
        if not self._analyzed:
            self.analyze()
        data = {
            "summary": self.get_summary(),
            "analysis": self.analysis_results
        }
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
