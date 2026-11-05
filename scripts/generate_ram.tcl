# Generate a physically realized ORRAM block, with either row or word decoder.
set variant $::env(ORRAM_VARIANT)
set out $::env(ORRAM_OUTPUT_DIR)
if {$variant ni {row word}} {error "Invalid decoder: $variant"}
file mkdir $out
set platform /OpenROAD-flow-scripts/flow/platforms/nangate45
read_liberty "$platform/lib/NangateOpenCellLibrary_typical.lib"
read_lef "$platform/lef/NangateOpenCellLibrary.tech.lef"
read_lef "$platform/lef/NangateOpenCellLibrary.macro.lef"
set_thread_count 2
if {[llength [info commands generate_ram]]==0} {error "This pinned OpenROAD image does not expose generate_ram"}
generate_ram \
  -name RAM32x8 \
  -mask_size 8 \
  -word_size 8 \
  -num_words 32 \
  -rw_ports 1 \
  -decoder $variant \
  -column_mux_ratio 1 \
  -storage_cell DFF_X1 \
  -routing_layer {metal1 0.08} \
  -ver_layer {metal4 0.14 20} \
  -hor_layer {metal3 0.08 20} \
  -filler_cells {FILLCELL_X1 FILLCELL_X2 FILLCELL_X4 FILLCELL_X8} \
  -write_behavioral_verilog "$out/behavioral.v"
write_def "$out/ram.def"
write_db "$out/ram.odb"
write_abstract_lef -bloat_occupied_layers "$out/ram.lef"
puts "ORRAM generation complete: $variant"