#!/usr/bin/env bash
# Map combinational synthesizable RTL and formally prove it after expanding Liberty cells.
set -euo pipefail
source_file="$1"
output_file="$2"
proof_file="$3"
lib="${NANGATE_LIB:-/tmp/orfs/flow/platforms/nangate45/lib/NangateOpenCellLibrary_typical.lib}"
mkdir -p "$(dirname "$output_file")" "$(dirname "$proof_file")"
trap 'echo "SYNTHESIS_OR_EQUIVALENCE_FAILED"; tail -n 70 "$output_file.log" 2>/dev/null || true; tail -n 100 "$proof_file" 2>/dev/null || true' ERR
yosys -Q -T -p "read_verilog -sv $source_file; synth -top address_logic -noabc; abc -liberty $lib; hilomap -hicell LOGIC1_X1 Z -locell LOGIC0_X1 Z; clean; write_verilog -noattr $output_file" > "$output_file.log" 2>&1
printf 'wrapped\nplus_three\nstride\nrow\ncolumn\nselected_col\n' > "$(dirname "$proof_file")/internal_blacklist.txt"
yosys -Q -T -p "read_verilog -sv $source_file; rename address_logic gold; read_liberty -ignore_miss_func $lib; read_verilog $output_file; rename address_logic gate; equiv_make -blacklist $(dirname "$proof_file")/internal_blacklist.txt gold gate equiv; hierarchy -top equiv; flatten; techmap; equiv_simple; equiv_status -assert" > "$proof_file" 2>&1
grep -q 'Equivalence successfully proven!' "$proof_file"
echo "RTL_MAP_EQUIVALENCE_PASS $source_file"
