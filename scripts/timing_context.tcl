# Reopen unchanged physical block and vary ONLY external STA boundary assumptions.
set variant $::env(ORRAM_VARIANT)
set context $::env(ORRAM_CONTEXT)
set out $::env(ORRAM_OUTPUT_DIR)
set platform /OpenROAD-flow-scripts/flow/platforms/nangate45
set root "/study/results/$variant"
file mkdir $out
read_liberty "$platform/lib/NangateOpenCellLibrary_typical.lib"
read_db "$root/ram.odb"
source "$platform/setRC.tcl"
estimate_parasitics -placement
create_clock -name clk -period 2.000 [get_ports clk]
set_input_delay 0.10 -clock clk [get_ports {D*}]
set_input_delay 0.10 -clock clk [get_ports {we*}]
set addr_all [get_ports {addr_rw*}]
set addr_low {}
set addr_high {}
foreach port $addr_all {
  set port_name [get_full_name $port]
  puts "ORRAM_CONTEXT_PORT: $port_name"
  if {[regexp {^addr_rw\[[01]\]$} $port_name]} {lappend addr_low $port}
  if {[regexp {^addr_rw\[[34]\]$} $port_name]} {lappend addr_high $port}
}
if {[llength $addr_all] != 5 || [llength $addr_low] != 2 || [llength $addr_high] != 2} {
  error "Address-bit selections invalid all=[llength $addr_all] low=[llength $addr_low] high=[llength $addr_high]"
}
set_input_delay 0.10 -clock clk $addr_all
set_output_delay 0.10 -clock clk [get_ports {Q*}]
set_load 0.005 [get_ports {Q*}]
switch -- $context {
  reference { }
  late_addr_lowbits {set_input_delay 0.65 -clock clk $addr_low}
  late_addr_highbits {set_input_delay 0.65 -clock clk $addr_high}
  heavy_outputs {set_load 0.050 [get_ports {Q*}]}
  tight_output {set_output_delay 0.75 -clock clk [get_ports {Q*}]}
  default {error "Unexpected context $context"}
}
report_checks -from $addr_all -to [get_ports {Q*}] -path_delay max -group_path_count 4 \
  -fields {input_pin net capacitance fanout slew} -digits 5 -no_line_splits > "$out/read_path.rpt"
report_checks -path_delay max -group_path_count 4 -digits 5 -no_line_splits > "$out/overall.rpt"
report_worst_slack -max > "$out/overall_worst_slack.rpt"
write_sdc "$out/assumptions.sdc"
if {[file size "$out/read_path.rpt"] == 0} {error "Empty read-path report"}
puts "Completed STA $variant $context"