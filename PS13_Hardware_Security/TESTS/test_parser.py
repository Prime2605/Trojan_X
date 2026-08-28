#!/usr/bin/env python3
"""
PS13 Hardware Security — Parser Tests
========================================
Unit tests for the netlist parser module.
"""

import os
import sys
import json
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYZER.parser.netlist_parser import NetlistParser


# Sample gate-level netlist for testing
SAMPLE_NETLIST = """
module alu8_test (
    input  [7:0] A,
    input  [7:0] B,
    input  [2:0] OP,
    output [7:0] Y,
    output       carry,
    output       zero
);

    wire n1, n2, n3, n4;
    wire [7:0] add_result;

    LUT6 #(.INIT(64'hAAAA5555)) lut_0 (.O(n1), .I0(A[0]), .I1(B[0]), .I2(OP[0]), .I3(1'b0), .I4(1'b0), .I5(1'b0));
    LUT6 #(.INIT(64'hFF00FF00)) lut_1 (.O(n2), .I0(A[1]), .I1(B[1]), .I2(OP[0]), .I3(OP[1]), .I4(1'b0), .I5(1'b0));
    FDRE #(.INIT(1'b0)) ff_0 (.Q(n3), .C(CLK), .CE(1'b1), .D(n1), .R(1'b0));
    OBUF obuf_0 (.O(Y[0]), .I(n3));

endmodule
"""


class TestNetlistParser(unittest.TestCase):
    """Test suite for NetlistParser."""

    def setUp(self):
        """Create a temporary netlist file for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.netlist_path = os.path.join(self.temp_dir, "test_netlist.v")
        with open(self.netlist_path, 'w') as f:
            f.write(SAMPLE_NETLIST)

    def test_parser_creation(self):
        """Test parser can be instantiated."""
        parser = NetlistParser(self.netlist_path)
        self.assertIsNotNone(parser)
        self.assertEqual(parser.netlist_path, os.path.abspath(self.netlist_path))

    def test_parse_succeeds(self):
        """Test parsing completes without error."""
        parser = NetlistParser(self.netlist_path)
        result = parser.parse()
        self.assertTrue(result)

    def test_file_not_found(self):
        """Test proper error on missing file."""
        parser = NetlistParser("/nonexistent/file.v")
        with self.assertRaises(FileNotFoundError):
            parser.parse()

    def test_instances_extracted(self):
        """Test that cell instances are extracted."""
        parser = NetlistParser(self.netlist_path)
        parser.parse()
        instances = parser.get_instances()
        self.assertIsInstance(instances, list)
        # Should find LUT6, FDRE, OBUF instances
        instance_types = [i["module"] for i in instances]
        self.assertTrue(len(instances) > 0, "Should extract at least one instance")

    def test_cell_types(self):
        """Test cell type counting."""
        parser = NetlistParser(self.netlist_path)
        parser.parse()
        cell_types = parser.get_cell_types()
        self.assertIsInstance(cell_types, dict)

    def test_summary(self):
        """Test summary generation."""
        parser = NetlistParser(self.netlist_path)
        parser.parse()
        summary = parser.get_summary()
        self.assertIn("module_count", summary)
        self.assertIn("instance_count", summary)
        self.assertIn("net_count", summary)

    def test_json_export(self):
        """Test JSON export."""
        parser = NetlistParser(self.netlist_path)
        parser.parse()
        output_path = os.path.join(self.temp_dir, "output.json")
        parser.to_json(output_path)
        self.assertTrue(os.path.exists(output_path))
        with open(output_path, 'r') as f:
            data = json.load(f)
        self.assertIn("instances", data)
        self.assertIn("summary", data)

    def test_not_parsed_error(self):
        """Test error when accessing data before parsing."""
        parser = NetlistParser(self.netlist_path)
        with self.assertRaises(RuntimeError):
            parser.get_modules()


if __name__ == "__main__":
    unittest.main()
