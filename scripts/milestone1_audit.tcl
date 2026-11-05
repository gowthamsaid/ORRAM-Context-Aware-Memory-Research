# Milestone 1: probe actual STA boundary loads and the integration interface.
# Reuses archived post-route databases; no new placement or routing.
set arch $::env(ORRAM_VARIANT)
if {$arch ni {row word}} {error "invalid architecture $arch"}
set platform /OpenROAD-flow-scripts/flow/platforms/nangate45
set out "/study/audit/$arch"
file mkdir $out
read_liberty "$platform/lib/NangateOpenCellLibrary_typical.lib"
read_db "/study/archive/results/$arch/ram.odb"
source "$platform/setRC.tcl"
report_units > "$out/units.rpt"
create_clock -name clk -period 2.0 [get_ports clk]
set_input_delay 0.1 -clock clk [get_ports {addr_rw*}]
set_input_delay 0.1 -clock clk [get_ports {D*}]
set_input_delay 0.1 -clock clk [get_ports {we*}]
set_output_delay 0.1 -clock clk [get_ports {Q*}]
set inputs [get_ports {addr_rw*}]
set outputs [get_ports {Q*}]
set q0 [get_ports {Q[0]}]
if {[llength $inputs]!=5 || [llength $outputs]!=8 || [llength $q0]!=1} {
  error "Invalid interface: addr=[llength $inputs] Q=[llength $outputs] Q0=[llength $q0]"
}
estimate_parasitics -placement

# This is a fixed physical checkpoint. Changes in timing must therefore
# come from input/output boundary assumptions, not a new placement.
foreach load {0.005 0.050 0.500 5.000} {
  set_load -pin_load $load $outputs
  report_checks -from $inputs -to $outputs -path_delay max \
    -group_path_count 1 -fields {input_pin net capacitance fanout slew} \
    -digits 7 -no_line_splits > "$out/load_function () { [native code] }_worst.rpt"
  report_checks -from $inputs -to $q0 -path_delay max \
    -group_path_count 1 -fields {input_pin net capacitance fanout slew} \
    -digits 7 -no_line_splits > "$out/load_function () { [native code] }_q0.rpt"
  write_sdc "$out/load_function () { [native code] }.sdc"
  puts "M1_LOAD arch=$arch value=$load bytes=[file size $out/load_function () { [native code] }_q0.rpt]"
}

# Export technology-mapped gates and physical block as distinct integration options.
if {[catch {
  write_verilog -remove_cells {FILLCELL_X1 FILLCELL_X2 FILLCELL_X4 FILLCELL_X8} "$out/ram_structural.v"
} err]} {
  puts "M1_EXPORT remove_cells failed: $err"
  write_verilog "$out/ram_structural.v"
}
if {[file size "$out/ram_structural.v"]==0} {error "structural netlist is empty"}
set f [open "$out/export_status.txt" w]
puts $f "gate_netlist_written"
close $f

# Attempt true routed-parasitics timing rather than quietly calling placement
# estimates 'post-route'. Record the exact extraction failure if unsupported.
set rcfile "$platform/rcx_patterns.rules"
if {[file exists $rcfile]} {
  if {[catch {extract_parasitics -ext_model_file $rcfile} result]} {
    set f [open "$out/extraction_status.txt" w]
    puts $f "EXTRACTION_FAILED: $result"
    close $f
  } else {
    write_spef "$out/ram.spef"
    set_load -pin_load 0.050 $outputs
    report_checks -from $inputs -to $outputs -path_delay max \
      -group_path_count 1 -fields {input_pin net capacitance fanout slew} \
      -digits 7 -no_line_splits > "$out/routed_rc_worst.rpt"
    set f [open "$out/extraction_status.txt" w]
    puts $f "EXTRACTION_SUCCEEDED"
    close $f
  }
} else {
  set f [open "$out/extraction_status.txt" w]
  puts $f "EXTRACTION_BLOCKED: rcx_patterns.rules missing"
  close $f
}
puts "M1_AUDIT complete arch=$arch"