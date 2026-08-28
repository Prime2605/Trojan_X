# ==============================================================================
# PS13 Hardware Security — Recovery Implementation Script
# ==============================================================================
# Compiles the restored gate-level netlist all the way to a bitstream.
# Proves that the Trojan was neutralized and the design is fully routable.
# ==============================================================================

set DESIGN_NAME "alu8_top"
set RESTORED_NETLIST "NETLISTS/T1/restored_netlist.v"
set CONSTRAINTS      "FPGA/Nexys_A7_100T/constraints/recovery_nexys.xdc"
set OUT_DIR          "REPORTS/recovery"
set TARGET_PART      "xc7a100tcsg324-1"

file mkdir $OUT_DIR

# ------------------------------------------------------------------------------
# 1. Create In-Memory Project & Load Sources
# ------------------------------------------------------------------------------
create_project -in_memory -part $TARGET_PART
set_property target_language Verilog [current_project]

# Read the restored netlist
if { [catch {read_verilog $RESTORED_NETLIST} errMsg] } {
    puts "\[ERROR\] Failed to read restored netlist: $errMsg"
    exit 1
}

# Read constraints
if { [catch {read_xdc $CONSTRAINTS} errMsg] } {
    puts "\[ERROR\] Failed to read constraints: $errMsg"
    exit 1
}

# ------------------------------------------------------------------------------
# 2. Link Design
# ------------------------------------------------------------------------------
puts "\[INFO\] Linking design..."
link_design -part $TARGET_PART -top $DESIGN_NAME

# ------------------------------------------------------------------------------
# 3. Optimize & Place
# ------------------------------------------------------------------------------
puts "\[INFO\] Running opt_design..."
opt_design
puts "\[INFO\] Running place_design..."
place_design

# ------------------------------------------------------------------------------
# 4. Route & Bitstream
# ------------------------------------------------------------------------------
puts "\[INFO\] Running route_design..."
route_design

# Generate reports to prove it routed successfully
report_utilization -file $OUT_DIR/recovery_utilization.txt
report_timing_summary -file $OUT_DIR/recovery_timing_summary.txt

puts "\[INFO\] Generating bitstream..."
write_bitstream -force $OUT_DIR/restored.bit

puts "\[INFO\] Implementation Complete. Bitstream generated at $OUT_DIR/restored.bit"
exit 0
