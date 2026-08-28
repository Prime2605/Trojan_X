# run_t4_batch.tcl — In-memory flow (no run management)
set project_dir "/home/prime/Trojan_X/PS13_Hardware_Security/FPGA/Nexys_A7_100T/vivado"
set rtl_dir     [file normalize "$project_dir/../rtl"]
set xdc_dir     [file normalize "$project_dir/../constraints"]
set part_name   "xc7a100tcsg324-1"

# 1. Read source files
read_verilog [glob $rtl_dir/*.v]
read_xdc $xdc_dir/nexys_a7_100t.xdc

# 2. Synthesize in-memory
synth_design -top alu8_top -part $part_name
write_verilog -force /home/prime/Trojan_X/PS13_Hardware_Security/NETLISTS/T4/alu8_T4_netlist.v
puts "Netlist exported to NETLISTS/T4/"

# 3. Implement in-memory
opt_design
place_design
route_design

# 4. Export Timing Reports
report_timing_summary -file /home/prime/Trojan_X/PS13_Hardware_Security/DATA/timing/trojan/T4_report_summary.rpt
report_timing -from [get_ports -filter {NAME =~ SW* || NAME =~ BTN*}] -to [get_ports -filter {NAME =~ LED*}] -max_paths 200 -sort_by group -file /home/prime/Trojan_X/PS13_Hardware_Security/DATA/timing/trojan/T4_report.rpt
puts "Timing report exported to DATA/timing/trojan/"

puts "ALL T4 BATCH OPERATIONS COMPLETE!"
