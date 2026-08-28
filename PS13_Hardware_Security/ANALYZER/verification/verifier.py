"""
PS13 Hardware Security — Verifier
====================================
Compares analyzer output against known ground truth to evaluate
detection accuracy. Computes precision, recall, and F1 score.

Ground truth is loaded from DATA/ground_truth/ JSON files and is
HIDDEN from the analyzer during blind detection — used only here.
"""

import json
from typing import Dict, List, Any, Optional


class Verifier:
    """
    Verify Trojan detection results against known ground truth.
    """

    def __init__(self, ground_truth_path: str):
        """
        Initialize with ground truth data.

        Args:
            ground_truth_path: Path to ground truth JSON file.
        """
        with open(ground_truth_path, 'r') as f:
            self.ground_truth = json.load(f)
        self.verification_result = None

    def verify(self, detected_cells: List[str],
               analysis_results: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Compare detected suspicious cells against ground truth.

        Args:
            detected_cells:   List of cell names flagged by the detector.
            analysis_results: Optional analysis results from TrojanAnalyzer.

        Returns:
            Verification metrics and detailed comparison.
        """
        gt_cells = set(
            self.ground_truth.get("ground_truth_cells", {})
            .get("trojan_trigger_cells", []) +
            self.ground_truth.get("ground_truth_cells", {})
            .get("trojan_payload_cells", [])
        )
        detected_set = set(detected_cells)

        # True positives, false positives, false negatives
        true_positives = detected_set & gt_cells
        false_positives = detected_set - gt_cells
        false_negatives = gt_cells - detected_set

        # Metrics
        precision = (len(true_positives) / len(detected_set)
                     if detected_set else 0)
        recall = (len(true_positives) / len(gt_cells)
                  if gt_cells else 1.0)  # If no GT cells, recall is trivially 1
        f1 = (2 * precision * recall / (precision + recall)
              if (precision + recall) > 0 else 0)

        self.verification_result = {
            "ground_truth": {
                "design": self.ground_truth.get("design", "unknown"),
                "trojan_type": self.ground_truth.get("trojan_type", "unknown"),
                "known_trojan_cells": list(gt_cells),
                "known_cell_count": len(gt_cells),
            },
            "detection_results": {
                "detected_cells": detected_cells,
                "detected_count": len(detected_cells),
            },
            "metrics": {
                "true_positives": list(true_positives),
                "false_positives": list(false_positives),
                "false_negatives": list(false_negatives),
                "tp_count": len(true_positives),
                "fp_count": len(false_positives),
                "fn_count": len(false_negatives),
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1_score": round(f1, 4),
            },
            "trigger_analysis_match": self._check_trigger_match(analysis_results),
            "payload_analysis_match": self._check_payload_match(analysis_results),
        }

        return self.verification_result

    def _check_trigger_match(self, analysis: Optional[List[Dict]]) -> Dict:
        """Check if analyzer correctly identified trigger characteristics."""
        if not analysis:
            return {"status": "not_available"}

        gt_trigger = self.ground_truth.get("trigger", {})
        for result in analysis:
            trigger_info = result.get("trigger_analysis", {})
            gt_signals = set(gt_trigger.get("signals", []))
            detected_inputs = set(trigger_info.get("potential_trigger_inputs", []))

            overlap = gt_signals & detected_inputs
            if overlap:
                return {
                    "status": "partial_match" if overlap != gt_signals else "full_match",
                    "matched_signals": list(overlap),
                    "missed_signals": list(gt_signals - overlap),
                }

        return {"status": "no_match"}

    def _check_payload_match(self, analysis: Optional[List[Dict]]) -> Dict:
        """Check if analyzer correctly identified payload/affected outputs."""
        if not analysis:
            return {"status": "not_available"}

        gt_payload = self.ground_truth.get("payload", {})
        gt_outputs = set(gt_payload.get("affected_outputs", []))

        for result in analysis:
            payload_info = result.get("payload_analysis", {})
            detected_outputs = set(payload_info.get("affected_outputs", []))

            overlap = gt_outputs & detected_outputs
            if overlap:
                return {
                    "status": "partial_match" if overlap != gt_outputs else "full_match",
                    "matched_outputs": list(overlap),
                    "missed_outputs": list(gt_outputs - overlap),
                }

        return {"status": "no_match"}

    def to_json(self, output_path: str) -> None:
        """Export verification results to JSON."""
        if self.verification_result is None:
            raise RuntimeError("Run verify() first.")
        with open(output_path, 'w') as f:
            json.dump(self.verification_result, f, indent=2)
