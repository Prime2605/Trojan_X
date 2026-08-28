"""
PS13 Hardware Security — Analyzer Package
==========================================
Python framework for analyzing gate-level Verilog netlists to detect
hardware Trojans and perform side-channel timing analysis.

Sub-packages:
    parser          — Pyverilog-based netlist parser
    graph           — NetworkX circuit graph builder
    features        — Feature extraction (fan-in, fanout, depth, etc.)
    detection       — Trojan detection (multi-indicator scoring)
    trojan_analysis — Deep Trojan analysis (trigger, payload, impact)
    sca             — Side-channel / timing analysis
    security        — Combined security assessment
    verification    — Ground-truth verification
"""

__version__ = "0.1.0"
__project__ = "PS13 Hardware Security"
