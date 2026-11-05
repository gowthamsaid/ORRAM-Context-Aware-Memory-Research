# Reproducible, read-only critical path mechanism audit of archived routed wrapper designs.
# Reread the original routed ODB, SDC, extracted SPEF (not placement RC estimates).
set root $::env(ORRAM_INTEGRATION_OUT)
set audit $::env(ORRAM_AUDIT_OUT)
file mkdir $audit
set platform /OpenROAD-flow-scripts/flow/platforms/nangate45
read_liberty "$platform/lib/NangateOpenCellLibrary_typical.lib"
read_db "$root/routed.odb"
read_sdc "$root/top.sdc"
source "$platform/setRC.tcl"
read_spef "$root/routed.spef"
report_units > "$audit/units.txt"
set starts [get_cells -quiet {*addrff*}]
set ends [get_cells -quiet {*capture*}]
puts "MECHANISM_AUDIT endpoint_count launch=[llength $starts] capture=[llength $ends]"
if {[llength $starts] != 5 || [llength $ends] < 8} {
 error "Unexpected launch or capture register count"
}
set rpt_fields {input_pin net capacitance fanout slew}
report_checks -from $starts -to $ends -path_delay max  -group_path_count 12 -fields $rpt_fields -digits 7 -no_line_splits > "$audit/top12.rpt"
report_checks -path_delay max -group_path_count 8  -fields $rpt_fields -digits 7 -no_line_splits > "$audit/overall8.rpt"
report_worst_slack -max > "$audit/worst_slack.rpt"
check_setup -verbose > "$audit/setup_check.rpt"
for {set i 0} {$i < 5} {incr i} {
 set pin [get_cells -quiet "u_addrff_$i"]
 if {[llength $pin] != 1} {error "Cannot resolve launch cell $i"}
 report_checks -from $pin -to $ends -path_delay max   -group_path_count 1 -fields $rpt_fields -digits 7 -no_line_splits > "$audit/launch_$i.rpt"
 if {[file size "$audit/launch_$i.rpt"] < 150} {error "Empty timing path for launch $i"}
}
# Report timing through all launch FFs when available; path-level analysis is read-only.
set f [open "$audit/provenance.txt" w]
puts $f "INPUT_DB $root/routed.odb"
puts $f "INPUT_SDC $root/top.sdc"
puts $f "INPUT_SPEF $root/routed.spef"
puts $f "ORIGINAL_ENDPOINTS launch=[llength $starts] capture=[llength $ends]"
close $f
puts "MECHANISM_AUDIT_PASS $root"
