#!/usr/bin/env python3
"""
PS13 Hardware Security — Timing Analysis Tests
=================================================
Unit tests for the timing parser and comparison (SCA module).
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ANALYZER.sca.timing_parser import TimingParser
from ANALYZER.sca.timing_comparison import TimingComparator


# Sample Vivado timing report content (simulated)
SAMPLE_TIMING_REPORT = """
Copyright 1986-2025 Xilinx, Inc. All Rights Reserved.
------------------------------------------------------------------------------------
| Tool Version : Vivado v.2025.1
| Date         : Thu Aug 28 00:00:00 2026
------------------------------------------------------------------------------------

WNS(ns)      TNS(ns)  TNS Failing Endpoints  TNS Total Endpoints      WHS(ns)      THS(ns)  THS Failing Endpoints  THS Total Endpoints     WPWS(ns)     TPWS(ns)  TPWS Failing Endpoints  TPWS Total Endpoints  
-------      -------  ---------------------  -------------------      -------      -------  ---------------------  -------------------     --------     --------  ----------------------  --------------------  
  3.456        0.000                      0                  100        0.123        0.000                      0                  100        3.000        0.000                       0                    45  


Slack (MET)   :  3.456ns
  Source:      A[0] (port)
  Destination: Y[0] (port)
  Data Path Delay: 6.544ns
    Logic Levels: 2 (LUT2=1, FDRE=1) (logic 4.0ns net 2.544ns)

Slack (MET)   :  2.100ns
  Source:      B[3] (port)
  Destination: Y[3] (port)
  Data Path Delay: 7.900ns
    Logic Levels: 3 (LUT4=2, MUXF7=1) (logic 5.0ns net 2.900ns)

Slack (MET)   :  4.200ns
  Source:      OP[0] (port)
  Destination: carry (port)
  Data Path Delay: 5.800ns
    Logic Levels: 1 (LUT6=1) (logic 3.0ns net 2.800ns)
"""


class TestTimingSCA(unittest.TestCase):
    
    def setUp(self):
        self.parser = TimingParser()
        self.comparator = TimingComparator()
        
        # Create a temporary file with the sample report
        self.fd, self.temp_path = tempfile.mkstemp(suffix='.rpt')
        with os.fdopen(self.fd, 'w') as f:
            f.write(SAMPLE_TIMING_REPORT)

    def tearDown(self):
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)

    def test_timing_parser(self):
        """Test parsing of Vivado report."""
        data = self.parser.parse_report(self.temp_path)
        
        # Check summary
        summary = data["summary"]
        self.assertEqual(summary["WNS"], 3.456)
        self.assertEqual(summary["TNS"], 0.0)
        self.assertEqual(summary["WHS"], 0.123)
        
        # Check paths
        paths = data["critical_paths"]
        self.assertEqual(len(paths), 3)
        
        # Verify first path
        p1 = paths[0]
        self.assertEqual(p1["startpoint"], "A[0]")
        self.assertEqual(p1["endpoint"], "Y[0]")
        self.assertEqual(p1["total_delay_ns"], 6.544)
        
        # Verify second path elements
        p2 = paths[1]
        self.assertEqual(p2["startpoint"], "B[3]")
        self.assertEqual(p2["total_delay_ns"], 7.900)
        self.assertIn("LUT4", p2["path_elements"])

    def test_timing_comparison(self):
        """Test comparison logic."""
        ref_data = self.parser.parse_report(self.temp_path)
        ref_data["design"] = "CLEAN"
        
        # Create suspect data with degraded timing
        sus_data = self.parser.parse_report(self.temp_path)
        sus_data["design"] = "TROJAN"
        # Degrade WNS
        sus_data["summary"]["WNS"] = 3.000 
        # Increase delay on worst path
        sus_data["critical_paths"][1]["total_delay_ns"] = 8.356
        
        result = self.comparator.compare(ref_data, sus_data)
        
        metrics = result["metrics"]
        assessment = result["assessment"]
        
        # 8.356 - 7.900 = 0.456
        self.assertAlmostEqual(metrics["critical_delay_difference_ns"], 0.456, places=3)
        # 3.000 - 3.456 = -0.456
        self.assertAlmostEqual(metrics["slack_difference_ns"], -0.456, places=3)
        
        self.assertTrue(assessment["timing_anomaly"])
        self.assertFalse(assessment["potential_timing_leakage"])


if __name__ == '__main__':
    unittest.main()
