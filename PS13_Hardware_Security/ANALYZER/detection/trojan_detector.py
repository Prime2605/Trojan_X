"""
PS13 Hardware Security — Trojan Detector
==========================================
Multi-indicator scoring system for identifying suspicious regions
in a gate-level netlist. Combines structural features to flag cells
that may be part of a hardware Trojan.

Detection uses a weighted composite score — NOT a single hard-coded rule.
Indicators include:
  - Anomalous fan-out / fan-in
  - Unusual logic depth
  - Atypical connectivity patterns
  - Rare cell types
  - Logic cone anomalies
"""

import json
from typing import Dict, List, Any, Optional


class TrojanDetector:
    """
    Detect suspicious regions in a circuit using multi-indicator scoring.

    Each cell receives a suspicion score based on weighted combination
    of structural indicators. Cells exceeding the threshold are flagged
    as potentially Trojan-related.
    """

    # Default indicator weights
    DEFAULT_WEIGHTS = {
        "fanout_anomaly":     0.25,
        "fanin_anomaly":      0.20,
        "depth_anomaly":      0.15,
        "cone_size_anomaly":  0.20,
        "rare_cell_type":     0.10,
        "connectivity_ratio": 0.10,
    }

    def __init__(self, feature_data: Dict[str, Any],
                 weights: Optional[Dict[str, float]] = None,
                 threshold: float = 0.6):
        """
        Initialize detector with extracted feature data.

        Args:
            feature_data: Output from FeatureExtractor.extract_all().
            weights:      Optional custom indicator weights.
            threshold:    Suspicion score threshold (0.0 to 1.0).
        """
        self.cell_features = feature_data.get("cell_features", {})
        self.design_features = feature_data.get("design_features", {})
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
        self.threshold = threshold
        self.scores = {}        # cell_name -> score dict
        self.suspicious = []    # list of flagged cells
        self._detected = False

    def detect(self) -> List[Dict]:
        """
        Run detection on all cells and return suspicious regions.

        Returns:
            List of dicts for cells exceeding the suspicion threshold.
        """
        self._compute_scores()
        self.suspicious = [
            cell_data for cell_data in self.scores.values()
            if cell_data["total_score"] >= self.threshold
        ]
        # Sort by score descending
        self.suspicious.sort(key=lambda x: x["total_score"], reverse=True)
        self._detected = True
        return self.suspicious

    def _compute_scores(self) -> None:
        """Compute suspicion score for each cell."""
        fo_stats = self.design_features.get("fanout_stats", {})
        fi_stats = self.design_features.get("fanin_stats", {})

        # Pre-compute design statistics for normalization
        fo_mean = fo_stats.get("mean", 1)
        fo_stdev = fo_stats.get("stdev", 1) or 1
        fi_mean = fi_stats.get("mean", 1)
        fi_stdev = fi_stats.get("stdev", 1) or 1

        # Logic depth stats
        depths = [f["logic_depth"] for f in self.cell_features.values()]
        depth_mean = sum(depths) / len(depths) if depths else 0
        depth_stdev = self._stdev(depths) if len(depths) > 1 else 1

        # Cone size stats
        cone_sizes = [f["logic_cone_size"] for f in self.cell_features.values()]
        cone_mean = sum(cone_sizes) / len(cone_sizes) if cone_sizes else 0
        cone_stdev = self._stdev(cone_sizes) if len(cone_sizes) > 1 else 1

        # Cell type frequency (rare types get higher scores)
        type_dist = self.design_features.get("cell_type_distribution", {})
        total_cells = sum(type_dist.values()) if type_dist else 1

        for cell_name, features in self.cell_features.items():
            indicators = {}

            # 1. Fan-out anomaly (z-score)
            fo_z = (features["fan_out"] - fo_mean) / fo_stdev if fo_stdev else 0
            indicators["fanout_anomaly"] = min(max(fo_z / 3.0, 0), 1.0)

            # 2. Fan-in anomaly (z-score)
            fi_z = (features["fan_in"] - fi_mean) / fi_stdev if fi_stdev else 0
            indicators["fanin_anomaly"] = min(max(fi_z / 3.0, 0), 1.0)

            # 3. Depth anomaly
            d_z = (features["logic_depth"] - depth_mean) / depth_stdev if depth_stdev else 0
            indicators["depth_anomaly"] = min(max(d_z / 3.0, 0), 1.0)

            # 4. Cone size anomaly
            c_z = (features["logic_cone_size"] - cone_mean) / cone_stdev if cone_stdev else 0
            indicators["cone_size_anomaly"] = min(max(c_z / 3.0, 0), 1.0)

            # 5. Rare cell type (inverse frequency)
            cell_type = features["cell_type"]
            type_freq = type_dist.get(cell_type, 1) / total_cells
            indicators["rare_cell_type"] = 1.0 - type_freq

            # 6. Connectivity ratio (fan_in * fan_out relative to design)
            max_product = (fo_stats.get("max", 1)) * (fi_stats.get("max", 1))
            product = features["fan_in"] * features["fan_out"]
            indicators["connectivity_ratio"] = product / max_product if max_product else 0

            # Weighted composite score
            total_score = sum(
                self.weights.get(key, 0) * value
                for key, value in indicators.items()
            )

            self.scores[cell_name] = {
                "cell": cell_name,
                "cell_type": features["cell_type"],
                "indicators": indicators,
                "total_score": round(total_score, 4),
                "features": features
            }

    def get_scores(self) -> Dict[str, Dict]:
        """Return all cell scores."""
        if not self.scores:
            self._compute_scores()
        return self.scores

    def get_suspicious_region(self) -> List[Dict]:
        """Return flagged suspicious cells."""
        if not self._detected:
            self.detect()
        return self.suspicious

    def get_detection_summary(self) -> Dict[str, Any]:
        """Return summary of detection results."""
        if not self._detected:
            self.detect()
        return {
            "total_cells_analyzed": len(self.cell_features),
            "suspicious_count": len(self.suspicious),
            "threshold": self.threshold,
            "weights": self.weights,
            "top_suspicious": [
                {"cell": s["cell"], "score": s["total_score"],
                 "type": s["cell_type"]}
                for s in self.suspicious[:10]
            ]
        }

    def to_json(self, output_path: str) -> None:
        """Export detection results to JSON."""
        if not self._detected:
            self.detect()
        data = {
            "summary": self.get_detection_summary(),
            "suspicious_cells": self.suspicious,
            "all_scores": {k: v["total_score"] for k, v in self.scores.items()}
        }
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def _stdev(values: List[float]) -> float:
        """Compute standard deviation."""
        n = len(values)
        if n < 2:
            return 0
        mean = sum(values) / n
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        return variance ** 0.5
