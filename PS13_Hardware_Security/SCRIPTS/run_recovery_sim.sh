#!/bin/bash
# ==============================================================================
# PS13 Hardware Security — Recovery Simulation Script
# ==============================================================================
# Runs Gate-Level Simulation (GLS) on the restored netlist using Vivado XSim.
# Verifies the Trojan payload is no longer active.
# ==============================================================================

cd /home/prime/Trojan_X/PS13_Hardware_Security
source /home/prime/2025.1/Vivado/settings64.sh

SIM_DIR="REPORTS/recovery/sim"
mkdir -p $SIM_DIR
cd $SIM_DIR

echo "[INFO] Compiling sources..."
xvlog ../../../FPGA/Nexys_A7_100T/testbench/tb_recovery.v ../../../NETLISTS/T1/restored_netlist.v /home/prime/2025.1/Vivado/data/verilog/src/glbl.v

echo "[INFO] Elaborating design with Unisim libraries..."
xelab -L unisims_ver -debug typical -top tb_recovery -top glbl -snapshot tb_recovery_snapshot

echo "[INFO] Running simulation..."
xsim tb_recovery_snapshot -R > simulation_results.log

cat simulation_results.log | grep -E "PASS|FAIL|NORMAL|TRIGGER|RECOVERED"

if grep -q "FAIL" simulation_results.log; then
    echo -e "\n[ERROR] Recovery simulation failed! Payload might still be active."
    exit 1
else
    echo -e "\n[SUCCESS] Recovery simulation passed! Trojan is neutralized."
    exit 0
fi
