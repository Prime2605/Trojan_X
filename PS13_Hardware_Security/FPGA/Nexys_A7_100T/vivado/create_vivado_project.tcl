#============================================================================
# PS13 Hardware Security — Vivado Project Creation Script
#============================================================================
# Usage: In Vivado Tcl console:
#   cd /path/to/PS13_Hardware_Security/FPGA/Nexys_A7_100T/vivado
#   source create_vivado_project.tcl
#
# This creates the ALU8 Vivado project with all sources, constraints,
# and simulation files properly configured.
#============================================================================

# Project settings
set project_name "ALU8"
set project_dir  [file normalize [file dirname [info script]]]
set rtl_dir      [file normalize "$project_dir/../rtl"]
set tb_dir       [file normalize "$project_dir/../testbench"]
set xdc_dir      [file normalize "$project_dir/../constraints"]
set part_name    "xc7a100tcsg324-1"

# Remove existing project if it exists
if {[file exists "$project_dir/$project_name"]} {
    file delete -force "$project_dir/$project_name"
}

# Create project
create_project $project_name "$project_dir/$project_name" -part $part_name

# Set board part (optional — Nexys A7-100T)
# set_property board_part digilentinc.com:nexys-a7-100t:part0:1.4 [current_project]

# Add RTL design sources
add_files -norecurse [list \
    "$rtl_dir/alu8.v" \
    "$rtl_dir/alu8_top.v" \
    "$rtl_dir/trojan_alu8.v" \
]

# Set top module
set_property top alu8_top [current_fileset]

# Add constraints
add_files -fileset constrs_1 -norecurse "$xdc_dir/nexys_a7_100t.xdc"

# Add simulation sources
add_files -fileset sim_1 -norecurse "$tb_dir/tb_alu8.v"
set_property top tb_alu8 [get_filesets sim_1]

# Set simulation properties
set_property -name {xsim.simulate.runtime} -value {1000ns} -objects [get_filesets sim_1]

# Update compile order
update_compile_order -fileset sources_1
update_compile_order -fileset sim_1

# Print summary
puts "============================================================"
puts "  Vivado project '$project_name' created successfully!"
puts "============================================================"
puts "  Part:        $part_name"
puts "  RTL dir:     $rtl_dir"
puts "  TB dir:      $tb_dir"
puts "  XDC dir:     $xdc_dir"
puts "  Top module:  alu8_top"
puts "  Sim top:     tb_alu8"
puts "============================================================"
puts ""
puts "  Next steps:"
puts "    1. Run Simulation:  launch_simulation"
puts "    2. Run Synthesis:   launch_runs synth_1 -jobs 4"
puts "    3. Run Implement:   launch_runs impl_1 -jobs 4"
puts "    4. Generate Bitstream: (after impl completes)"
puts "       write_bitstream -force $project_dir/$project_name.bit"
puts ""
puts "  Export gate-level netlist (after synthesis):"
puts "    open_run synth_1"
puts "    write_verilog -mode funcsim ../../../NETLISTS/clean/alu8_clean_netlist.v"
puts "============================================================"
