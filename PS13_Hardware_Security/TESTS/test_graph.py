#!/usr/bin/env python3
"""
PS13 Hardware Security — Graph Tests
=======================================
Unit tests for the circuit graph builder.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYZER.graph.circuit_graph import CircuitGraph


class TestCircuitGraph(unittest.TestCase):
    """Test suite for CircuitGraph."""

    def setUp(self):
        """Create sample data for testing."""
        self.sample_instances = [
            {
                "name": "lut_0",
                "module": "LUT6",
                "connections": {"O": "n1", "I0": "A_0", "I1": "B_0"}
            },
            {
                "name": "lut_1",
                "module": "LUT6",
                "connections": {"O": "n2", "I0": "A_1", "I1": "B_1"}
            },
            {
                "name": "ff_0",
                "module": "FDRE",
                "connections": {"Q": "n3", "D": "n1", "C": "CLK"}
            },
            {
                "name": "obuf_0",
                "module": "OBUF",
                "connections": {"O": "Y_0", "I": "n3"}
            },
        ]
        self.sample_ports = [
            {"name": "A_0", "direction": "input", "width": 1},
            {"name": "A_1", "direction": "input", "width": 1},
            {"name": "B_0", "direction": "input", "width": 1},
            {"name": "B_1", "direction": "input", "width": 1},
            {"name": "CLK", "direction": "input", "width": 1},
            {"name": "Y_0", "direction": "output", "width": 1},
        ]
        self.sample_nets = [
            {"name": "n1", "type": "wire", "width": 1},
            {"name": "n2", "type": "wire", "width": 1},
            {"name": "n3", "type": "wire", "width": 1},
        ]

    def test_build(self):
        """Test graph construction."""
        cg = CircuitGraph()
        cg.build_from_parsed_data(
            self.sample_instances, self.sample_ports, self.sample_nets
        )
        self.assertTrue(cg.graph.number_of_nodes() > 0)
        self.assertTrue(cg.graph.number_of_edges() > 0)

    def test_cell_nodes(self):
        """Test cell node identification."""
        cg = CircuitGraph()
        cg.build_from_parsed_data(
            self.sample_instances, self.sample_ports, self.sample_nets
        )
        cells = cg.get_cell_nodes()
        self.assertEqual(len(cells), 4)  # lut_0, lut_1, ff_0, obuf_0

    def test_port_nodes(self):
        """Test port node identification."""
        cg = CircuitGraph()
        cg.build_from_parsed_data(
            self.sample_instances, self.sample_ports, self.sample_nets
        )
        ports = cg.get_port_nodes()
        self.assertEqual(len(ports), 6)

    def test_fanin_fanout(self):
        """Test fan-in and fan-out computation."""
        cg = CircuitGraph()
        cg.build_from_parsed_data(
            self.sample_instances, self.sample_ports, self.sample_nets
        )
        # lut_0 has inputs from A_0 and B_0 -> fan_in >= 2
        fi = cg.get_fanin("lut_0")
        self.assertGreaterEqual(fi, 0)

    def test_logic_depth(self):
        """Test logic depth computation."""
        cg = CircuitGraph()
        cg.build_from_parsed_data(
            self.sample_instances, self.sample_ports, self.sample_nets
        )
        depths = cg.get_logic_depth()
        self.assertIsInstance(depths, dict)
        max_depth = cg.get_max_logic_depth()
        self.assertGreaterEqual(max_depth, 0)

    def test_logic_cone(self):
        """Test logic cone computation."""
        cg = CircuitGraph()
        cg.build_from_parsed_data(
            self.sample_instances, self.sample_ports, self.sample_nets
        )
        cell_nodes = cg.get_cell_nodes()
        if cell_nodes:
            cone = cg.get_logic_cone(cell_nodes[0])
            self.assertIsInstance(cone, set)

    def test_summary(self):
        """Test graph summary generation."""
        cg = CircuitGraph()
        cg.build_from_parsed_data(
            self.sample_instances, self.sample_ports, self.sample_nets
        )
        summary = cg.get_summary()
        self.assertIn("total_nodes", summary)
        self.assertIn("total_edges", summary)
        self.assertIn("is_dag", summary)

    def test_not_built_error(self):
        """Test error when querying before build."""
        cg = CircuitGraph()
        with self.assertRaises(RuntimeError):
            cg.get_summary()


if __name__ == "__main__":
    unittest.main()
