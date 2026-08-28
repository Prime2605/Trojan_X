import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, List
import os

class TimingVisualizer:
    """Generates visualizations for timing comparisons (Clean vs Trojan)."""

    def __init__(self, output_dir: str = "REPORTS/sca/"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def plot_delay_comparison(self, ref_delay: float, sus_delay: float, ref_name: str, sus_name: str, filename: str = "delay_comparison.png"):
        """Plots a bar chart comparing the critical path delays."""
        labels = [ref_name, sus_name]
        delays = [ref_delay, sus_delay]
        
        plt.figure(figsize=(8, 6))
        bars = plt.bar(labels, delays, color=['blue', 'red'])
        
        plt.title('Critical Path Delay Comparison')
        plt.ylabel('Delay (ns)')
        
        # Add values on top of bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 3), ha='center', va='bottom')
            
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()

    def plot_slack_comparison(self, ref_slack: float, sus_slack: float, ref_name: str, sus_name: str, filename: str = "slack_comparison.png"):
        """Plots a bar chart comparing the Worst Negative Slack."""
        labels = [ref_name, sus_name]
        slacks = [ref_slack, sus_slack]
        
        plt.figure(figsize=(8, 6))
        bars = plt.bar(labels, slacks, color=['green', 'orange'])
        
        plt.title('Worst Negative Slack (WNS) Comparison')
        plt.ylabel('Slack (ns)')
        
        # Add values on top of bars
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05 if yval >= 0 else yval - 0.15, round(yval, 3), ha='center', va='bottom')
            
        plt.axhline(0, color='black', linewidth=1)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()
