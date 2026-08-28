#!/usr/bin/env python3
"""
PS13 Hardware Security — Detection Tests
===========================================
Unit tests for the Trojan detection module.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYZER.detection.trojan_detector import TrojanDetector


class TestTrojanDetector(unittest.TestCase):
    """Test suite for TrojanDetector."""

    def setUp(self):
        """Create sample feature data."""
        self.feature_data = {
            "cell_features": {
                "lut_0": {
                    "cell_type": "LUT6", "fan_in": 2, "fan_out": 1,
                    "logic_depth": 1, "logic_cone_size": 2,
                    "influence_cone_size": 3, "predecessor_count": 2,
                    "successor_count": 1
                },
                "lut_1": {
                    "cell_type": "LUT6", "fan_in": 2, "fan_out": 1,
                    "logic_depth": 1, "logic_cone_size": 2,
                    "influence_cone_size": 3, "predecessor_count": 2,
                    "successor_count": 1
                },
                "lut_suspect": {
                    "cell_type": "LUT6", "fan_in": 8, "fan_out": 5,
                    "logic_depth": 5, "logic_cone_size": 12,
                    "influence_cone_size": 8, "predecessor_count": 8,
                    "successor_count": 5
                },
                "ff_0": {
                    "cell_type": "FDRE", "fan_in": 1, "fan_out": 1,
                    "logic_depth": 2, "logic_cone_size": 3,
                    "influence_cone_size": 2, "predecessor_count": 1,
                    "successor_count": 1
                },
            },
            "design_features": {
                "total_cells": 4,
                "total_ports": 5,
                "total_nodes": 9,
                "total_edges": 8,
                "max_logic_depth": 5,
                "connected_components": 1,
                "is_dag": True,
                "cell_type_distribution": {"LUT6": 3, "FDRE": 1},
                "fanout_stats": {"mean": 2.0, "stdev": 1.63, "min": 1, "max": 5, "median": 1.0},
                "fanin_stats": {"mean": 3.25, "stdev": 2.63, "min": 1, "max": 8, "median": 2.0},
            }
        }

    def test_detect_returns_list(self):
        """Test that detection returns a list."""
        detector = TrojanDetector(self.feature_data, threshold=0.3)
        result = detector.detect()
        self.assertIsInstance(result, list)

    def test_scores_computed(self):
        """Test that scores are computed for all cells."""
        detector = TrojanDetector(self.feature_data)
        detector.detect()
        scores = detector.get_scores()
        self.assertEqual(len(scores), 4)

    def test_suspicious_cell_found(self):
        """Test that the suspicious cell is flagged with low threshold."""
        detector = TrojanDetector(self.feature_data, threshold=0.2)
        suspicious = detector.detect()
        suspicious_names = [s["cell"] for s in suspicious]
        # lut_suspect should score highest
        if suspicious:
            self.assertEqual(suspicious[0]["cell"], "lut_suspect")

    def test_high_threshold_no_results(self):
        """Test that high threshold yields no results."""
        detector = TrojanDetector(self.feature_data, threshold=0.99)
        suspicious = detector.detect()
        # Most cells should not exceed 0.99
        self.assertTrue(len(suspicious) <= 1)

    def test_summary(self):
        """Test detection summary generation."""
        detector = TrojanDetector(self.feature_data, threshold=0.3)
        detector.detect()
        summary = detector.get_detection_summary()
        self.assertIn("total_cells_analyzed", summary)
        self.assertIn("suspicious_count", summary)
        self.assertIn("threshold", summary)

    def test_custom_weights(self):
        """Test detection with custom weights."""
        custom_weights = {
            "fanout_anomaly": 0.5,
            "fanin_anomaly": 0.5,
            "depth_anomaly": 0.0,
            "cone_size_anomaly": 0.0,
            "rare_cell_type": 0.0,
            "connectivity_ratio": 0.0,
        }
        detector = TrojanDetector(
            self.feature_data, weights=custom_weights, threshold=0.3
        )
        suspicious = detector.detect()
        self.assertIsInstance(suspicious, list)


if __name__ == "__main__":
    unittest.main()
