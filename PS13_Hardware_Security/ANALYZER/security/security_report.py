"""
PS13 Hardware Security — Security Report Generator
=====================================================
Combines structural analysis and timing/SCA analysis into a unified
security assessment report.

Produces both JSON data and human-readable text reports.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional


class SecurityReporter:
    """
    Generate a comprehensive security report combining all analysis results.
    """

    def __init__(self, design_name: str = "unknown"):
        """
        Initialize reporter.

        Args:
            design_name: Name of the design being analyzed.
        """
        self.design_name = design_name
        self.structural_results = None
        self.trojan_results = None
        self.timing_results = None
        self.report = None

    def set_structural_results(self, data: Dict) -> None:
        """Set structural analysis results (from FeatureExtractor)."""
        self.structural_results = data

    def set_trojan_results(self, detection: Dict, analysis: List[Dict]) -> None:
        """Set Trojan detection and analysis results."""
        self.trojan_results = {
            "detection": detection,
            "analysis": analysis
        }

    def set_timing_results(self, data: Dict) -> None:
        """Set timing/SCA comparison results."""
        self.timing_results = data

    def generate(self) -> Dict[str, Any]:
        """
        Generate the combined security report.

        Returns:
            Complete security assessment as a dictionary.
        """
        self.report = {
            "metadata": {
                "design": self.design_name,
                "generated_at": datetime.now().isoformat(),
                "framework": "PS13 Hardware Security Analyzer",
                "version": "0.1.0"
            },
            "overall_verdict": self._compute_verdict(),
            "structural_summary": self._summarize_structural(),
            "trojan_summary": self._summarize_trojan(),
            "timing_summary": self._summarize_timing(),
            "confidence": self._compute_confidence(),
            "recommendations": self._generate_recommendations()
        }
        return self.report

    def _compute_verdict(self) -> Dict[str, Any]:
        """Compute overall security verdict."""
        has_trojan_evidence = False
        has_timing_anomaly = False

        if self.trojan_results:
            detection = self.trojan_results.get("detection", {})
            if detection.get("suspicious_count", 0) > 0:
                has_trojan_evidence = True

        if self.timing_results:
            anomalies = self.timing_results.get("anomalies", [])
            if len(anomalies) > 0:
                has_timing_anomaly = True

        if has_trojan_evidence and has_timing_anomaly:
            verdict = "SUSPICIOUS — structural and timing anomalies detected"
            level = "HIGH"
        elif has_trojan_evidence:
            verdict = "SUSPICIOUS — structural anomalies detected"
            level = "MEDIUM"
        elif has_timing_anomaly:
            verdict = "WARNING — timing anomalies detected"
            level = "LOW"
        else:
            verdict = "CLEAN — no anomalies detected"
            level = "NONE"

        return {"verdict": verdict, "risk_level": level}

    def _summarize_structural(self) -> Optional[Dict]:
        """Summarize structural analysis results."""
        if not self.structural_results:
            return None
        df = self.structural_results.get("design_features", {})
        return {
            "total_cells": df.get("total_cells", 0),
            "total_edges": df.get("total_edges", 0),
            "max_logic_depth": df.get("max_logic_depth", 0),
            "cell_type_distribution": df.get("cell_type_distribution", {})
        }

    def _summarize_trojan(self) -> Optional[Dict]:
        """Summarize Trojan detection/analysis results."""
        if not self.trojan_results:
            return None
        detection = self.trojan_results.get("detection", {})
        analysis = self.trojan_results.get("analysis", [])
        return {
            "suspicious_cells_found": detection.get("suspicious_count", 0),
            "top_suspects": detection.get("top_suspicious", []),
            "trojan_type_estimates": [
                a.get("impact_assessment", {}).get("trojan_type_estimate", "unknown")
                for a in analysis
            ],
            "affected_outputs": list(set(
                out
                for a in analysis
                for out in a.get("payload_analysis", {}).get("affected_outputs", [])
            ))
        }

    def _summarize_timing(self) -> Optional[Dict]:
        """Summarize timing/SCA results."""
        if not self.timing_results:
            return None
        return {
            "delay_comparison": self.timing_results.get("delay_comparison", {}),
            "anomaly_count": len(self.timing_results.get("anomalies", [])),
            "anomalies": self.timing_results.get("anomalies", [])[:5]
        }

    def _compute_confidence(self) -> Dict[str, Any]:
        """Compute confidence levels for each analysis component."""
        confidence = {}
        if self.structural_results:
            confidence["structural"] = "available"
        else:
            confidence["structural"] = "not_run"
        if self.trojan_results:
            confidence["trojan_detection"] = "available"
        else:
            confidence["trojan_detection"] = "not_run"
        if self.timing_results:
            confidence["timing_sca"] = "available"
        else:
            confidence["timing_sca"] = "not_run"
        return confidence

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on findings."""
        recs = []
        verdict = self._compute_verdict()

        if verdict["risk_level"] == "HIGH":
            recs.append("CRITICAL: Manually inspect flagged cells in Vivado")
            recs.append("Compare flagged region against known Trojan patterns")
            recs.append("Verify timing paths through affected regions")
        elif verdict["risk_level"] == "MEDIUM":
            recs.append("Review structural anomalies in detail")
            recs.append("Run timing analysis if not already done")
            recs.append("Compare against clean reference netlist")
        elif verdict["risk_level"] == "LOW":
            recs.append("Investigate timing anomalies — may be synthesis artifacts")
            recs.append("Run structural analysis if not already done")
        else:
            recs.append("Design appears clean — no immediate action required")
            recs.append("Consider periodic re-analysis if design evolves")

        return recs

    def to_json(self, output_path: str) -> None:
        """Export report to JSON."""
        if self.report is None:
            self.generate()
        with open(output_path, 'w') as f:
            json.dump(self.report, f, indent=2)

    def to_text(self, output_path: str) -> None:
        """Export report as human-readable text."""
        if self.report is None:
            self.generate()

        lines = []
        lines.append("=" * 70)
        lines.append("  PS13 HARDWARE SECURITY ANALYSIS REPORT")
        lines.append("=" * 70)
        lines.append(f"  Design:    {self.report['metadata']['design']}")
        lines.append(f"  Generated: {self.report['metadata']['generated_at']}")
        lines.append("")

        v = self.report["overall_verdict"]
        lines.append(f"  VERDICT:    {v['verdict']}")
        lines.append(f"  RISK LEVEL: {v['risk_level']}")
        lines.append("")
        lines.append("-" * 70)

        if self.report.get("structural_summary"):
            s = self.report["structural_summary"]
            lines.append("  STRUCTURAL ANALYSIS")
            lines.append(f"    Total cells:      {s.get('total_cells', 'N/A')}")
            lines.append(f"    Total edges:      {s.get('total_edges', 'N/A')}")
            lines.append(f"    Max logic depth:  {s.get('max_logic_depth', 'N/A')}")
            lines.append("")

        if self.report.get("trojan_summary"):
            t = self.report["trojan_summary"]
            lines.append("  TROJAN ANALYSIS")
            lines.append(f"    Suspicious cells: {t.get('suspicious_cells_found', 0)}")
            if t.get("top_suspects"):
                for s in t["top_suspects"][:5]:
                    lines.append(f"      - {s['cell']} (score: {s['score']:.4f})")
            lines.append("")

        lines.append("  RECOMMENDATIONS")
        for rec in self.report.get("recommendations", []):
            lines.append(f"    • {rec}")

        lines.append("")
        lines.append("=" * 70)

        with open(output_path, 'w') as f:
            f.write("\n".join(lines))
