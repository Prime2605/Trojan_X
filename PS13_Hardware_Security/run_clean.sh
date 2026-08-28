#!/bin/bash
cd /home/prime/Trojan_X/PS13_Hardware_Security

echo "Enabling Clean Baseline (Disabling Trojans)..."
python3.13 -c "
import re
with open('FPGA/Nexys_A7_100T/rtl/trojan_alu8.v', 'r') as f: c=f.read()
c = re.sub(r'^\s*`define ENABLE_T1', '// `define ENABLE_T1', c, flags=re.M)
with open('FPGA/Nexys_A7_100T/rtl/trojan_alu8.v', 'w') as f: f.write(c)
"

echo "Starting Clean Baseline Generation..."
rm -rf FPGA/Nexys_A7_100T/vivado/ALU8 FPGA/Nexys_A7_100T/vivado/.Xil
source /home/prime/2025.1/Vivado/settings64.sh
vivado -mode batch -source FPGA/Nexys_A7_100T/vivado/run_clean_batch.tcl

echo "Clean Baseline Generated."
