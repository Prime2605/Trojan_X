# PS13 Hardware Security Project Guide
**End-to-End Guide: Hardware Trojan Detection & Side-Channel Timing Analysis**

This guide provides the complete, chronological list of commands needed to run this project entirely from scratch, including how to set up your environment, generate the Vivado projects, and run the security analyzers.

> [!IMPORTANT]
> **Command Execution Location**
> - **Vivado TCL Console:** Only use this for internal Vivado commands (like `report_timing`). 
> - **Linux Terminal:** ALL commands in this guide (including Python and Vivado batch commands) MUST be run in a standard Linux Terminal. Do not run Python scripts inside the Vivado TCL Console.

---

## 1. Environment & Setup

### A. Python Virtual Environment (venv)
To avoid conflicting with your system's Python packages or Vivado's internal Python, we will create a dedicated Virtual Environment (venv) for this project.

Open a **Linux Terminal** and run:
```bash
cd /home/prime/Trojan_X/PS13_Hardware_Security/

# Create a virtual environment named 'env' using Python 3.13
python3.13 -m venv env

# Activate the virtual environment
source env/bin/activate
```
*(You must run `source env/bin/activate` every time you open a new terminal before running the python scripts).*

### B. Install Dependencies
With the `env` activated, install the required packages:
```bash
pip install --upgrade pip
pip install networkx pyverilog matplotlib
pip install --upgrade pillow --force-reinstall
```

---

## 2. Generating the Hardware Data (Vivado)

Before running the analyzers, you must generate the hardware Netlists and Timing Reports from Vivado. 
*Note: We limit Vivado to `-jobs 2` during these steps to prevent Linux Out-Of-Memory (OOM) crashes.*

### Option A: The Automated Way (Recommended)
You can use the provided bash scripts to safely toggle Trojans and run Vivado. You must run these in the Linux Terminal.

- To run everything sequentially (Clean, T1):
  ```bash
  bash run_all.sh
  ```
- To run individual profiles:
  ```bash
  bash run_clean.sh  # Generates the reference baseline
  bash run_t1.sh     # Analyzes T1
  ```

---

## 3. Running the Security Analyzers

**WHEN TO RUN:** You can only run these scripts **AFTER** Vivado has successfully completed Synthesis and Implementation (meaning the `.v` netlists and `.rpt` timing reports exist).

### A. Structural Netlist Analyzer
This tool parses the Gate-Level Netlist into a Graph (DAG) and detects logic anomalies.
```bash
# Ensure your venv is activated first!
python SCRIPTS/run_full_analysis.py --netlist NETLISTS/T1/alu8_T1_netlist.v
```

### B. Side-Channel Timing Analyzer
This tool compares the endpoint-specific delays of the Clean Baseline against the Trojan design.
```bash
# Ensure your venv is activated first!
python SCRIPTS/analyze_timing.py --reference DATA/timing/clean/report.rpt --suspect DATA/timing/trojan/T1_report.rpt
```

---

## 4. Working in the Vivado GUI (Optional)

If you need to view the RTL schematics, run simulations, or program the Nexys A7-100T board:

```bash
source /home/prime/2025.1/Vivado/settings64.sh
vivado &
```
1. Click **Open Project**.
2. Navigate to `/home/prime/Trojan_X/PS13_Hardware_Security/FPGA/Nexys_A7_100T/vivado/ALU8/`
3. Select `ALU8.xpr`.

---

## 5. Common Errors & Troubleshooting

> [!WARNING]
> **`incremental checkpoint failed synth_1 does not exist` or `Killed`**
> **Cause:** Vivado was killed by the OS (OOM Killer) because `-jobs 4` or `-jobs 6` used too much RAM, leaving corrupted lock files.
> **Fix:** Delete the corrupted project and rebuild using the batch scripts (which have now been optimized to `-jobs 2`):
> ```bash
> rm -rf FPGA/Nexys_A7_100T/vivado/ALU8 FPGA/Nexys_A7_100T/vivado/.Xil
> ```

> [!CAUTION]
> **IDE Error: `@[current_problems]` (`Unexpected indentation` or `Could not find name`)**
> **Cause:** Your code editor (IDE) tries to dynamically evaluate partial Python snippets while the file is open, generating virtual parsing errors (`__pyrefly_virtual__`).
> **Fix:** These errors are harmless UI artifacts. The actual `.py` files on your disk are perfectly formatted and valid. You can safely ignore these warnings.

> [!WARNING]
> **`ImportError: cannot import name '_imaging' from 'PIL'`**
> **Cause:** You ran the Python script using Vivado's internal Python environment or the system Python.
> **Fix:** Create and activate the `venv` as described in Section 1, and ensure you run the script from the standard Linux Terminal.
