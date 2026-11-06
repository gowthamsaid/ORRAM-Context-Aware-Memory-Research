# Sanitize only completely disconnected synthesized supply placeholders.
# These nets have no cell or top-level terminals and represent no circuit
# connection. TritonRoute refuses to route them as ordinary signal nets.
set supply_cleanup_count 0
foreach net [[ord::get_db_block] getNets] {
  set type [$net getSigType]
  if {$type ni {GROUND POWER}} {continue}
  set connected_cells [llength [$net getITerms]]
  set connected_ports [llength [$net getBTerms]]
  if {$connected_cells == 0 && $connected_ports == 0} {
    puts "REMOVING_DISCONNECTED_SUPPLY_PLACEHOLDER name=[$net getName] type=$type"
    odb::dbNet_destroy $net
    incr supply_cleanup_count
  } else {
    puts "PRESERVE_CONNECTED_SUPPLY name=[$net getName] cells=$connected_cells ports=$connected_ports"
  }
}
puts "SUPPLY_PLACEHOLDER_CLEANUP removed=$supply_cleanup_count"
