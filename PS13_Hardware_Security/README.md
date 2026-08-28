# PS13 — Hardware Trojan Detection & Side-Channel Timing Leakage Analysis

## Project Overview

This project implements a complete hardware security analysis framework targeting
an 8-bit ALU design on the **Digilent Nexys A7-100T** FPGA board (Xilinx Artix-7
XC7A100T-1CSG324C).

### Architecture

```
8-bit ALU (clean reference)
   ├── Trojan Injection → Trojan-infected ALU ─┐
   └── SCA/Timing experiment ──────────────────┤
                                                ▼
                                      Vivado Synthesis
                                                ▼
                        Gate-level structural Verilog netlist
                                                ▼
                                 OUR ANALYZER (Python)
      1. Netlist parser → 2. AST/DAG → 3. Circuit graph (NetworkX)
      → 4. Feature extraction (fan-in, fanout, depth, cell type)
      → 5. Trojan identification (suspicious regions, scored)
      → 6. Trojan analysis (trigger / payload / affected output)
      → 7. SCA/Timing analysis (Vivado timing reports)
      → 8. Security analysis (combine structural + timing evidence)
      → 9. Verification (vs known ground truth)
      → 10. Final report generator
```

### Trojan Benchmarks

| Trojan | Type | Trigger | Analyzer Features Exercised |
|--------|------|---------|---------------------------|
| T1 | Rare-combination combinational | Rare input combo | connectivity, fan-in/out, logic cone |
| T2 | Complex combinational | Less obvious trigger/payload | topology, connectivity, path analysis |
| T3 | Sequential | State/time dependent | FFs, sequential paths, state analysis |

## Hardware Platform

- **Board**: Digilent Nexys A7-100T
- **FPGA**: Xilinx Artix-7 XC7A100T-1CSG324C
- **Tool**: AMD Vivado 2025.1
- **Clock**: 100 MHz (pin E3)

### I/O Mapping

| Signal | Nexys A7 Resource | Description |
|--------|-------------------|-------------|
| A[7:0] | SW[7:0] | Operand A (8-bit) |
| B[7:0] | SW[15:8] | Operand B (8-bit) |
| OP[2:0] | BTNU/BTND/BTNL/BTNR/BTNC | ALU opcode (button-encoded) |
| Y[7:0] | LED[7:0] | ALU result |
| carry | LED[13] | Carry flag |
| zero | LED[14] | Zero flag |
| overflow | LED[15] | Overflow flag |
| reset | CPU_RESETN | Active-low reset |

## Setup

### Prerequisites

```bash
# Vivado 2025.1 (already installed)
# Python 3.13
sudo apt install python3.13 python3.13-venv python3.13-dev

# Optional: Icarus Verilog for quick simulation
sudo apt install iverilog
```

### Python Environment

```bash
cd PS13_Hardware_Security
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Vivado Project

```bash
# In Vivado Tcl console:
cd /path/to/PS13_Hardware_Security/FPGA/Nexys_A7_100T/vivado
source create_vivado_project.tcl
```

## Directory Structure

```
PS13_Hardware_Security/
├── FPGA/           → Verilog RTL, testbench, constraints, Vivado project
├── NETLISTS/       → Synthesized gate-level netlists (clean, T1, T2, T3)
├── ANALYZER/       → Python analysis framework (8 sub-packages)
├── DATA/           → Feature data, timing data, ground truth
├── REPORTS/        → Generated analysis reports
├── SCRIPTS/        → Pipeline entry-point scripts
└── TESTS/          → Unit tests
```

## Usage

### 1. FPGA Flow (Vivado)

```
RTL → Simulate → Synthesize → Implement → Bitstream → Nexys A7
```

### 2. Analysis Flow (Python)

```bash
# Full pipeline
python SCRIPTS/run_full_analysis.py --netlist NETLISTS/T1/alu8_T1_netlist.v

# Individual steps
python SCRIPTS/run_parser.py --netlist NETLISTS/clean/alu8_clean_netlist.v
python SCRIPTS/extract_features.py --data DATA/features/
python SCRIPTS/detect_trojan.py --features DATA/features/
python SCRIPTS/analyze_trojan.py --detection DATA/features/
python SCRIPTS/analyze_timing.py --timing DATA/timing/
```

### 3. Run Tests

```bash
python -m pytest TESTS/ -v
```

## Development Order

1. ✅ System architecture locked
2. Clean ALU RTL
3. Nexys A7 implementation (XDC)
4. Simulate clean ALU
5. Synthesize clean ALU
6. Build T1 Trojan RTL
7. Synthesize T1 → export netlist
8. Build netlist parser
9. Build circuit graph
10. Extract features
11. Trojan detection
12. Trojan analysis
13. SCA/Timing module
14. Report generator
15. Verification
16. Add T2, T3

## License

Academic project — PS13 Hardware Security course.
