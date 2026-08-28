"""
PS13 Hardware Security — Feature Extractor
============================================
Extracts per-cell and per-net structural features from the circuit graph
for use in Trojan detection scoring.

Features extracted:
  - Cell-level: type, fan-in, fan-out, logic depth, cone size
  - Net-level: driver count, sink count, width
  - Design-level: total cells, nets, max depth, type distribution
  - Statistical: mean/std/max fanout, depth distribution
"""

import json
import statistics
from typing import Dict, List, Any, Optional


class FeatureExtractor:
    """
    Extract structural features from a CircuitGraph for Trojan detection.

    The features capture topological and connectivity characteristics
    that differ between clean and Trojan-infected designs.
    """

    def __init__(self, circuit_graph):
        """
        Initialize with a built CircuitGraph.

        Args:
            circuit_graph: A CircuitGraph instance (already built).
        """
        self.cg = circuit_graph
        self.cell_features = {}   # cell_name -> feature dict
        self.design_features = {} # aggregate design features
        self._extracted = False

    def extract_all(self) -> Dict[str, Any]:
        """
        Extract all features and return combined feature set.

        Returns:
            Dictionary containing cell_features and design_features.
        """
        self._extract_cell_features()
        self._extract_design_features()
        self._extracted = True
        return {
            "cell_features": self.cell_features,
            "design_features": self.design_features
        }

    def _extract_cell_features(self) -> None:
        """Extract per-cell features from the circuit graph."""
        cell_nodes = self.cg.get_cell_nodes()
        depths = self.cg.get_logic_depth()

        for cell_name in cell_nodes:
            attrs = self.cg.graph.nodes[cell_name]
            fan_in = self.cg.get_fanin(cell_name)
            fan_out = self.cg.get_fanout(cell_name)
            logic_cone = self.cg.get_logic_cone(cell_name)
            influence_cone = self.cg.get_influence_cone(cell_name)

            self.cell_features[cell_name] = {
                "cell_type": attrs.get("cell_type", "unknown"),
                "fan_in": fan_in,
                "fan_out": fan_out,
                "logic_depth": depths.get(cell_name, 0),
                "logic_cone_size": len(logic_cone),
                "influence_cone_size": len(influence_cone),
                "predecessor_count": len(self.cg.get_predecessors(cell_name)),
                "successor_count": len(self.cg.get_successors(cell_name)),
            }

    def _extract_design_features(self) -> None:
        """Extract aggregate design-level features."""
        summary = self.cg.get_summary()
        all_fanout = self.cg.get_all_fanout()
        all_fanin = self.cg.get_all_fanin()

        # Cell type distribution
        cell_type_counts = {}
        for cell_name, features in self.cell_features.items():
            ct = features["cell_type"]
            cell_type_counts[ct] = cell_type_counts.get(ct, 0) + 1

        # Fanout statistics (cells only)
        cell_fanouts = [all_fanout[n] for n in self.cg.get_cell_nodes()
                        if n in all_fanout]
        cell_fanins = [all_fanin[n] for n in self.cg.get_cell_nodes()
                       if n in all_fanin]

        self.design_features = {
            "total_cells": summary["cell_count"],
            "total_ports": summary["port_count"],
            "total_nodes": summary["total_nodes"],
            "total_edges": summary["total_edges"],
            "max_logic_depth": summary["max_logic_depth"],
            "connected_components": summary["connected_components"],
            "is_dag": summary["is_dag"],
            "cell_type_distribution": cell_type_counts,
            "fanout_stats": self._compute_stats(cell_fanouts),
            "fanin_stats": self._compute_stats(cell_fanins),
        }

    def _compute_stats(self, values: List[int]) -> Dict[str, float]:
        """Compute basic statistics for a list of values."""
        if not values:
            return {"mean": 0, "median": 0, "stdev": 0, "min": 0, "max": 0}
        return {
            "mean": round(statistics.mean(values), 3),
            "median": round(statistics.median(values), 3),
            "stdev": round(statistics.stdev(values), 3) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values),
        }

    def get_anomalous_cells(self, fanout_threshold: float = 2.0,
                             depth_threshold: float = 2.0) -> List[Dict]:
        """
        Identify cells with anomalous features.

        A cell is flagged if its fan-out or logic depth exceeds
        mean + threshold * stdev for the design.

        Args:
            fanout_threshold: Number of standard deviations above mean.
            depth_threshold:  Number of standard deviations above mean.

        Returns:
            List of dicts describing anomalous cells and their features.
        """
        if not self._extracted:
            self.extract_all()

        anomalies = []
        fo_stats = self.design_features["fanout_stats"]
        fo_cutoff = fo_stats["mean"] + fanout_threshold * fo_stats["stdev"]

        depths = [f["logic_depth"] for f in self.cell_features.values()]
        depth_mean = statistics.mean(depths) if depths else 0
        depth_stdev = statistics.stdev(depths) if len(depths) > 1 else 0
        depth_cutoff = depth_mean + depth_threshold * depth_stdev

        for cell_name, features in self.cell_features.items():
            reasons = []
            if features["fan_out"] > fo_cutoff and fo_cutoff > 0:
                reasons.append(f"high_fanout ({features['fan_out']} > {fo_cutoff:.1f})")
            if features["logic_depth"] > depth_cutoff and depth_cutoff > 0:
                reasons.append(f"high_depth ({features['logic_depth']} > {depth_cutoff:.1f})")
            if reasons:
                anomalies.append({
                    "cell": cell_name,
                    "features": features,
                    "anomaly_reasons": reasons
                })

        return anomalies

    def to_json(self, output_path: str) -> None:
        """Export features to JSON."""
        if not self._extracted:
            self.extract_all()
        data = {
            "cell_features": self.cell_features,
            "design_features": self.design_features
        }
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
