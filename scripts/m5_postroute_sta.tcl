# Milestone 5: targeted post-route timing coverage, not full-chip signoff.
# Use archived routed DB + exact original SDC + SPEF; no re-placement.
set dir $::env(M5_CASE_DIR)
set output $::env(M5_AUDIT_DIR)
set width $::env(M5_WORD_WIDTH)
file mkdir $output
set platform /OpenROAD-flow-scripts/flow/platforms/nangate45
read_liberty "$platform/lib/NangateOpenCellLibrary_typical.lib"
read_db "$dir/routed.odb"
read_sdc "$dir/top.sdc"
source "$platform/setRC.tcl"
read_spef "$dir/routed.spef"
set launches [get_cells -quiet {*addrff*}]
set captures [get_cells -quiet {*capture*}]
set actual_input_ports [get_ports -quiet {addr_in* data_in* write_enable}]
set actual_output_ports [get_ports -quiet {data_out*}]
set clock_ports [get_ports -quiet clk]
if {[llength $launches] != 5} { error "Bad launch count: [llength $launches]" }
if {[llength $captures] != $width} { error "Bad capture count: [llength $captures]" }
if {[llength $actual_output_ports] != $width} { error "Bad output count: [llength $actual_output_ports]" }
if {[llength $clock_ports] != 1} { error "Bad clock port" }
if {[llength $actual_input_ports] != [expr {5+$width+1}]} { error "Unexpected input count: [llength $actual_input_ports]" }
puts "M5_COUNTS launch=[llength $launches] capture=[llength $captures] input=[llength $actual_input_ports] output=[llength $actual_output_ports]"
report_units
puts "M5_CHECK_SETUP_BEGIN"
check_setup -verbose
puts "M5_CHECK_SETUP_END"
# Reopen full extracted parasitics and generate both path classes.
report_checks -from $launches -to $captures -path_delay max -group_path_count 12 \
  -fields {input_pin net capacitance fanout slew} -digits 7 -no_line_splits > "$output/target_read.rpt"
report_checks -path_delay max -group_path_count 12 \
  -fields {input_pin net capacitance fanout slew} -digits 7 -no_line_splits > "$output/all_setup.rpt"
report_worst_slack -max > "$output/wns.rpt"
report_worst_slack -min > "$output/hold_wns.rpt"
report_tns -max > "$output/tns.rpt"
if {[file size "$output/target_read.rpt"]<300} { error "No target read setup path" }
if {[file size "$output/all_setup.rpt"]<300} { error "No complete setup path" }
set f [open "$output/provenance.txt" w]
puts $f "INPUT_ODB $dir/routed.odb"
puts $f "INPUT_SDC $dir/top.sdc"
puts $f "INPUT_SPEF $dir/routed.spef"
puts $f "OPENSTA_REPORTED check_setup -verbose on log between M5_CHECK_SETUP_BEGIN and M5_CHECK_SETUP_END"
puts $f "CAVEAT Ideal clock and no routed CTS or multi-corner signoff"
close $f
puts "M5_POSTROUTE_RECHECK_PASS dir=$dir"
