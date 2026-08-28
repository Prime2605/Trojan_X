<div align="center">

# 🔐 TROJAN_X

### Hardware Trojan Detection & Side-Channel Analysis Platform

[![Vivado](https://img.shields.io/badge/Vivado-2025.1-FF6F00?style=for-the-badge&logo=amd&logoColor=white)](https://www.xilinx.com/products/design-tools/vivado.html)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FPGA](https://img.shields.io/badge/FPGA-Nexys_A7--100T-00979D?style=for-the-badge&logo=digilent&logoColor=white)](https://digilent.com/reference/programmable-logic/nexys-a7/start)
[![License](https://img.shields.io/badge/License-Academic-purple?style=for-the-badge)](LICENSE)

[![Verilog](https://img.shields.io/badge/HDL-Verilog-blue?style=flat-square&logo=verilog)](https://en.wikipedia.org/wiki/Verilog)
[![NetworkX](https://img.shields.io/badge/Graph-NetworkX-orange?style=flat-square)](https://networkx.org/)
[![Matplotlib](https://img.shields.io/badge/Viz-Matplotlib-11557c?style=flat-square&logo=matplotlib)](https://matplotlib.org/)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

<br>

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          ████████╗██████╗  ██████╗      ██╗ █████╗ ███╗  ██╗ ║
║          ╚══██╔══╝██╔══██╗██╔═══██╗     ██║██╔══██╗████╗ ██║ ║
║             ██║   ██████╔╝██║   ██║     ██║███████║██╔██╗██║ ║
║             ██║   ██╔══██╗██║   ██║██   ██║██╔══██║██║╚████║ ║
║             ██║   ██║  ██║╚██████╔╝╚█████╔╝██║  ██║██║ ╚███║ ║
║             ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ║
║                     ═══  X  ═══                              ║
║           Hardware Security Research Platform                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

<br>

> *"The most dangerous hardware trojans are the ones you can't see — until it's too late."*

---

</div>

## 🎯 What is Trojan_X?

**Trojan_X** is a complete hardware security research platform that demonstrates **hardware trojan injection**, **structural detection**, and **side-channel timing analysis** on a real FPGA. Built around an **8-bit ALU** deployed on the **Digilent Nexys A7-100T** board, it provides:

| Feature | Description |
|:---:|:---|
| 🧬 | **Trojan Injection** — Physically triggerable combinational trojan with `BTNC + BTND` cheat code |
| 🔍 | **Structural Analysis** — Graph-based DAG analysis with 8 weighted detection indicators |
| ⏱️ | **Side-Channel Analysis** — Endpoint-specific timing comparison (SCA) against clean baseline |
| 📊 | **Combined Verdict** — Cross-referenced dual-analysis with 4-tier risk classification |
| 🤖 | **Full Automation** — One-command Vivado synthesis → implementation → analysis pipeline |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        TROJAN_X PLATFORM                        │
├─────────────────────────┬───────────────────────────────────────┤
│   🔧 HARDWARE LAYER     │           📊 ANALYSIS LAYER           │
│                         │                                       │
│  ┌───────────────────┐  │  ┌─────────────┐  ┌───────────────┐  │
│  │   alu8_top.v      │  │  │  Netlist     │  │   Timing      │  │
│  │   ┌─────────────┐ │  │  │  Parser      │  │   Parser      │  │
│  │   │trojan_alu8.v│ │──┤  │  (pyverilog) │  │   (regex)     │  │
│  │   │ ┌─────────┐ │ │  │  └──────┬──────┘  └───────┬───────┘  │
│  │   │ │   T1    │ │ │  │         ▼                  ▼          │
│  │   │ │ TROJAN  │ │ │  │  ┌─────────────┐  ┌───────────────┐  │
│  │   │ └─────────┘ │ │  │  │  Circuit     │  │   Delay       │  │
│  │   └─────────────┘ │  │  │  Graph (DAG) │  │   Comparator  │  │
│  └───────────────────┘  │  │  (NetworkX)  │  │   (per-path)  │  │
│                         │  └──────┬──────┘  └───────┬───────┘  │
│  ┌───────────────────┐  │         ▼                  ▼          │
│  │  Nexys A7-100T    │  │  ┌─────────────┐  ┌───────────────┐  │
│  │  xc7a100tcsg324-1 │  │  │  Feature     │  │   Statistical │  │
│  │                   │  │  │  Extractor   │  │   Summary     │  │
│  │  SW[15:0] → A,B   │  │  └──────┬──────┘  └───────┬───────┘  │
│  │  BTN → OP,TRIGGER │  │         ▼                  ▼          │
│  │  LED[15:0] → Y    │  │  ┌──────────────────────────────────┐ │
│  └───────────────────┘  │  │    🎯 COMBINED SECURITY VERDICT   │ │
│                         │  │    Cross-referenced 4-tier risk   │ │
├─────────────────────────┤  └──────────────────────────────────┘ │
│  ⚡ Vivado Batch Flow   │                                       │
│  synth → impl → export  │  8 Indicators · Per-endpoint SCA     │
└─────────────────────────┴───────────────────────────────────────┘
```

---

## 🧬 The Trojan — T1

<div align="center">

| Property | Value |
|:---|:---|
| **Type** | Combinational (purely logic — no state) |
| **Trigger Code** | `11` → Press **BTNC** + **BTND** simultaneously |
| **Payload** | `Y = alu_y ^ A` — XORs the ALU result with operand A |
| **Side Effect** | Carry flag is also inverted |
| **Visibility** | LEDs display wrong mathematical answer |
| **Deactivation** | Release either button → instantly returns to normal |

</div>

### 💡 How It Works

```verilog
// TRIGGER: Both buttons pressed = cheat code "11"
wire t1_trigger = BTNC & BTND;

// PAYLOAD: Corrupt the ALU output with operand A
assign Y     = t1_trigger ? (alu_y ^ A) : alu_y;    // ← Wrong answer!
assign carry = t1_trigger ? ~alu_carry  : alu_carry; // ← Flipped carry!
```

### 🎮 Physical Trigger on Board

```
    ┌──────────────────────────────┐
    │         Nexys A7-100T        │
    │                              │
    │         [BTNU] OP[2]         │
    │                              │
    │  [BTNL]   [BTNC]   [BTNR]   │
    │   OP[1]  TRIGGER    OP[0]   │
    │                              │
    │         [BTND]               │
    │        TRIGGER               │
    │                              │
    │  SW[7:0] = Operand A         │
    │  SW[15:8] = Operand B        │
    │  LED[7:0] = Result Y         │
    │  LED[13] = Carry             │
    │  LED[14] = Zero              │
    │  LED[15] = Overflow          │
    └──────────────────────────────┘

    Press BTNC + BTND together → Trojan activates! 💀
```

---

## 📊 Detection Results

<div align="center">

### Structural Analysis
| Metric | Value |
|:---|:---|
| Cells Analyzed | 167 |
| Suspicious Cells Flagged | **10** ⚠️ |
| Detection Threshold | 0.45 |
| Verdict | 🔴 **SUSPICIOUS** |

### Side-Channel Timing Analysis
| Metric | Value |
|:---|:---|
| Max Delay Difference | **+1.076 ns** |
| Affected Endpoints | **9 / 11** |
| Worst Endpoint | `LED[13]` (Carry flag) |
| Mean Δ | +0.3655 ns |
| Verdict | 🔴 **ANOMALY DETECTED** |

### 🎯 Combined Verdict
```
╔══════════════════════════════════════════════════════════════╗
║  COMBINED VERDICT:  🔴 TROJAN DETECTED — BOTH CONFIRM       ║
║  RISK LEVEL:        🔴 CRITICAL                             ║
╚══════════════════════════════════════════════════════════════╝
```

</div>

---

## 🚀 Quick Start

### Prerequisites

| Tool | Version | Purpose |
|:---|:---|:---|
| Vivado | 2025.1 | FPGA Synthesis & Implementation |
| Python | 3.13 | Analysis Scripts |
| Nexys A7-100T | — | Target FPGA Board |

### 1️⃣ Clone & Setup

```bash
git clone https://github.com/Prime2605/Trojan_X.git
cd Trojan_X/PS13_Hardware_Security

# Create Python virtual environment
python3.13 -m venv env
source env/bin/activate
pip install networkx pyverilog matplotlib
```

### 2️⃣ Run the Full Pipeline

```bash
# Source Vivado
source /path/to/Vivado/settings64.sh

# Run everything: Clean baseline → T1 Trojan → Analysis
bash run_all.sh
```

### 3️⃣ View the Combined Report

```bash
python SCRIPTS/run_combined_report.py \
    --netlist NETLISTS/T1/alu8_T1_netlist.v \
    --reference DATA/timing/clean/report.rpt \
    --suspect DATA/timing/trojan/T1_report.rpt
```

---

## 📁 Project Structure

```
Trojan_X/
├── PS13_Hardware_Security/
│   ├── ANALYZER/                    # 🔍 Detection Engine
│   │   ├── detection/               #    8-indicator weighted scoring
│   │   ├── features/                #    Per-cell feature extraction
│   │   ├── graph/                   #    NetworkX DAG builder
│   │   ├── parser/                  #    Pyverilog netlist parser
│   │   ├── sca/                     #    Side-channel timing analysis
│   │   ├── security/                #    Report generation
│   │   └── trojan_analysis/         #    Region analysis
│   │
│   ├── DATA/                        # 📦 Timing Reports
│   │   ├── timing/clean/            #    Clean baseline reports
│   │   └── timing/trojan/           #    Trojan-infected reports
│   │
│   ├── FPGA/Nexys_A7_100T/          # 🔧 Hardware Design
│   │   ├── rtl/                     #    Verilog source (ALU + Trojan)
│   │   ├── testbench/               #    36-test verification suite
│   │   ├── constraints/             #    Nexys A7 pin assignments
│   │   └── vivado/                  #    TCL batch scripts
│   │
│   ├── NETLISTS/                    # 📄 Gate-Level Netlists
│   │   ├── clean/                   #    Reference baseline
│   │   └── T1/                      #    Trojan-infected netlist
│   │
│   ├── REPORTS/                     # 📊 Analysis Output
│   │   ├── final/                   #    Structural reports (JSON + TXT)
│   │   └── sca/                     #    Timing comparison + plots
│   │
│   ├── SCRIPTS/                     # 🤖 Automation
│   │   ├── run_full_analysis.py     #    Structural pipeline
│   │   ├── analyze_timing.py        #    SCA pipeline
│   │   └── run_combined_report.py   #    ⭐ Unified combined report
│   │
│   ├── run_all.sh                   #    Master automation script
│   ├── run_clean.sh                 #    Clean baseline generation
│   ├── run_t1.sh                    #    T1 trojan generation
│   ├── Guide.md                     #    Complete setup guide
│   └── README.md                    #    Project documentation
│
├── Requirements/                    # 📋 Board specs & context
└── .gitignore
```

---

## 🔬 Detection Indicators

The structural analyzer uses **8 weighted indicators** to score each cell:

| # | Indicator | Weight | Description |
|:-:|:---|:-:|:---|
| 1 | `fanout_anomaly` | 20% | Abnormally high fan-out (z-score) |
| 2 | `fanin_anomaly` | 15% | Abnormally high fan-in (z-score) |
| 3 | `depth_anomaly` | 10% | Unusual logic depth position |
| 4 | `cone_size_anomaly` | 15% | Large logic cone (many upstream cells) |
| 5 | `rare_cell_type` | 10% | Infrequently used cell type |
| 6 | `connectivity_ratio` | 10% | Fan-in × fan-out product |
| 7 | `output_proximity` | 10% | Directly drives an output port |
| 8 | `input_diversity` | 10% | Inputs from many different source ports |

Cells scoring above **0.45** are flagged as suspicious.

---

## 🎓 ALU Operations

The 8-bit ALU supports 8 operations controlled by physical buttons:

| Opcode | Buttons | Operation | Description |
|:-:|:---|:---|:---|
| `000` | *None* | `A + B` | Addition |
| `001` | BTNR | `A - B` | Subtraction |
| `010` | BTNL | `A & B` | Bitwise AND |
| `011` | BTNL + BTNR | `A \| B` | Bitwise OR |
| `100` | BTNU | `A ^ B` | Bitwise XOR |
| `101` | BTNU + BTNR | `~A` | Bitwise NOT |
| `110` | BTNU + BTNL | `A + 1` | Increment |
| `111` | BTNU + BTNL + BTNR | `A - 1` | Decrement |

---

<div align="center">

## 📜 Academic Context

This project was developed as part of **PS13: Hardware Security** coursework, exploring hardware trojan injection, detection methodologies, and side-channel analysis on real FPGA hardware.

---

**Made with 🔐 by [Prime2605](https://github.com/Prime2605)**

[![GitHub](https://img.shields.io/badge/GitHub-Prime2605-181717?style=for-the-badge&logo=github)](https://github.com/Prime2605)

</div>
