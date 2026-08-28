#!/usr/bin/env python3
"""
PS13 Hardware Security — Feature Extraction Tests
====================================================
Unit tests for the feature extractor module.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYZER.graph.circuit_graph import CircuitGraph
from ANALYZER.features.feature_extractor import FeatureExtractor


class TestFeatureExtractor(unittest.TestCase):
    """Test suite for FeatureExtractor."""

    def setUp(self):
        """Build a test circuit graph."""
        self.instances = [
            {"name": "lut_0", "module": "LUT6",
             "connections": {"O": "n1", "I0": "a0", "I1": "b0"}},
            {"name": "lut_1", "module": "LUT4",
             "connections": {"O": "n2", "I0": "a1", "I1": "b1"}},
            {"name": "lut_2", "module": "LUT6",
             "connections": {"O": "n3", "I0": "n1", "I1": "n2"}},
            {"name": "obuf_0", "module": "OBUF",
             "connections": {"O": "y0", "I": "n3"}},
        ]
        self.ports = [
            {"name": "a0", "direction": "input", "width": 1},
            {"name": "a1", "direction": "input", "width": 1},
            {"name": "b0", "direction": "input", "width": 1},
            {"name": "b1", "direction": "input", "width": 1},
            {"name": "y0", "direction": "output", "width": 1},
        ]
        self.nets = [
            {"name": "n1", "type": "wire", "width": 1},
            {"name": "n2", "type": "wire", "width": 1},
            {"name": "n3", "type": "wire", "width": 1},
        ]
        self.cg = CircuitGraph()
        self.cg.build_from_parsed_data(self.instances, self.ports, self.nets)

    def test_extract_all(self):
        """Test feature extraction returns expected structure."""
        fe = FeatureExtractor(self.cg)
        features = fe.extract_all()
        self.assertIn("cell_features", features)
        self.assertIn("design_features", features)

    def test_cell_features_content(self):
        """Test that cell features contain expected keys."""
        fe = FeatureExtractor(self.cg)
        features = fe.extract_all()
        for cell_name, cf in features["cell_features"].items():
            self.assertIn("cell_type", cf)
            self.assertIn("fan_in", cf)
            self.assertIn("fan_out", cf)
            self.assertIn("logic_depth", cf)
            self.assertIn("logic_cone_size", cf)

    def test_design_features_content(self):
        """Test that design features contain expected keys."""
        fe = FeatureExtractor(self.cg)
        features = fe.extract_all()
        df = features["design_features"]
        self.assertIn("total_cells", df)
        self.assertIn("fanout_stats", df)
        self.assertIn("cell_type_distribution", df)

    def test_anomalous_cells(self):
        """Test anomaly detection works without error."""
        fe = FeatureExtractor(self.cg)
        fe.extract_all()
        anomalies = fe.get_anomalous_cells()
        self.assertIsInstance(anomalies, list)


if __name__ == "__main__":
    unittest.main()
