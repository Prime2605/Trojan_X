#!/bin/bash
cd /home/prime/Trojan_X/PS13_Hardware_Security

echo "=========================================="
echo " Starting Full Hardware Security Pipeline"
echo "=========================================="

echo ">>> [1/3] Running Clean Baseline..."
bash run_clean.sh

echo ">>> [2/3] Running T1 Analysis..."
bash run_t1.sh

echo ">>> [3/3] Running T4 Super Trojan Analysis..."
bash run_t4.sh

echo "=========================================="
echo " Pipeline Complete!"
echo "=========================================="
