#!/bin/bash
cd /home/prime/Trojan_X/PS13_Hardware_Security

echo "Enabling T4 in RTL..."
python3.13 -c "
import re
with open('FPGA/Nexys_A7_100T/rtl/trojan_alu8.v', 'r') as f: c=f.read()
c = re.sub(r'^\s*`define ENABLE_T1', '// `define ENABLE_T1', c, flags=re.M)
c = re.sub(r'^\s*//\s*`define ENABLE_T4', '`define ENABLE_T4', c, flags=re.M)
with open('FPGA/Nexys_A7_100T/rtl/trojan_alu8.v', 'w') as f: f.write(c)
"

echo "Starting T4 Super Trojan Generation..."
rm -rf FPGA/Nexys_A7_100T/vivado/ALU8 FPGA/Nexys_A7_100T/vivado/.Xil
source /home/prime/2025.1/Vivado/settings64.sh
vivado -mode batch -source FPGA/Nexys_A7_100T/vivado/run_t4_batch.tcl

echo "Running Analyzers..."
mkdir -p NETLISTS/T4
python3.13 SCRIPTS/run_full_analysis.py --netlist NETLISTS/T4/alu8_T4_netlist.v
python3.13 SCRIPTS/analyze_timing.py --reference DATA/timing/clean/report.rpt --suspect DATA/timing/trojan/T4_report.rpt
