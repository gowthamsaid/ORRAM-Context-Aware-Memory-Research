# Library-based, no routed RAM target, registered address cone STA, no new memory placement.
set design $::env(PRODUCER_DESIGN)
set out $::env(PRODUCER_STA_OUT)
file mkdir $out
set platform /OpenROAD-flow-scripts/flow/platforms/nangate45
read_liberty "$platform/lib/NangateOpenCellLibrary_typical.lib"
read_lef "$platform/lef/NangateOpenCellLibrary.tech.lef"
read_lef "$platform/lef/NangateOpenCellLibrary.macro.lef"
read_verilog $design
link_design producer_top
create_clock -period 4.0 -name clk [get_ports clk]
set_input_delay 0.1 -clock clk [get_ports {addr_in*}]
set_output_delay 0.1 -clock clk [get_ports {addr_mem*}]
set_load -pin_load 30.0 [get_ports {addr_mem*}]
set_clock_uncertainty -setup 0.05 [get_clocks clk]
for {set i 0} {$i < 5} {incr i} {
 set port_name [format {addr_mem[%d]} $i]
 set port [get_ports -quiet $port_name]
 if {[llength $port]!=1} {error "No address output port $port_name"}
 report_checks -to $port -path_delay max -group_path_count 1 \
  -fields {input_pin net capacitance fanout slew} \
  -digits 7 -no_line_splits > "$out/addr_$i.rpt"
 if {[file size "$out/addr_$i.rpt"]<200} {error "Missing preplacement STA path $i"}
}
report_units
puts "PRODUCER_PREPLACEMENT_STA_PASS $design"
