# Memory-address boundary path audit using immutable routed register-integrated ORRAM.
# The boundary pin is the final XOR output driving flattened addr_mem[bit].
# Constrained FF-to-FF paths through that pin are used to measure suffix delay.
set root $::env(ORRAM_INTEGRATION_OUT)
set audit $::env(ORRAM_AUDIT_OUT)
set mode $::env(ORRAM_WRAPPER)
set size $::env(ORRAM_SIZE)
if {$mode ni {balanced late_low}} {error "Invalid context $mode"}
if {$size ni {32x8 32x16}} {error "Invalid memory size $size"}
set nout [expr {$size eq "32x8" ? 8 : 16}]
file mkdir $audit
set platform /OpenROAD-flow-scripts/flow/platforms/nangate45
read_liberty "$platform/lib/NangateOpenCellLibrary_typical.lib"
read_db "$root/routed.odb"
read_sdc "$root/top.sdc"
source "$platform/setRC.tcl"
read_spef "$root/routed.spef"
set starts [get_cells -quiet {*addrff*}]
set captures [get_cells -quiet {*capture*}]
if {[llength $starts]!=5 || [llength $captures]!=$nout} {
 error "Unexpected launch or capture register count: [llength $starts] / [llength $captures]"
}
set fields {input_pin net capacitance fanout slew}
report_worst_slack -max > "$audit/overall_slack.rpt"
set fh [open "$audit/boundary_inventory.csv" w]
puts $fh "bit,driver_pin,memory_address_net"
for {set bit 0} {$bit<5} {incr bit} {
 set last_stage [expr {$mode eq "late_low" && $bit<2 ? 2 : 0}]
 set driver_name [format {u_mix_%d_%d/Z} $bit $last_stage]
 set driver [get_pins -quiet $driver_name]
 if {[llength $driver]!=1} {
   error "RAM address driver pin $driver_name: expected 1, got [llength $driver]"
 }
 puts $fh [format {%d,%s,addr_mem[%d]} $bit $driver_name $bit]
 report_checks -through $driver -to $captures -path_delay max \
   -group_path_count 8 -fields $fields -digits 7 -no_line_splits \
   > "$audit/address_$bit_worst.rpt"
 if {[file size "$audit/address_$bit_worst.rpt"]<350} {
   error "No constrained path through $driver_name"
 }
 set targets {0 7}
 if {$nout==16} {lappend targets 14}
 foreach q $targets {
   set capture [get_cells -quiet "u_capture_$q"]
   if {[llength $capture]!=1} {error "No capture FF $q"}
   report_checks -through $driver -to $capture -path_delay max \
     -group_path_count 1 -fields $fields -digits 7 -no_line_splits \
     > "$audit/address_$bit_q$q.rpt"
   if {[file size "$audit/address_$bit_q$q.rpt"]<350} {
     error "No constrained path through $driver_name to output Q$q"
   }
 }
}
close $fh
set fh [open "$audit/provenance.txt" w]
puts $fh "Physical: $root/routed.odb"
puts $fh "SDC: $root/top.sdc"
puts $fh "Extracted RC: $root/routed.spef (read_spef)"
puts $fh "Boundary: last XOR driver Z connected to each addr_mem bit (not a hierarchical macro port)"
puts $fh "Downstream suffix: capture D arrival minus boundary driver Z time in same reported path"
puts $fh "This is conditional path delay, not guaranteed intrinsic memory pin arc."
close $fh
puts "ORRAM_BOUNDARY_MECHANISM_PASS $size $mode $root"
