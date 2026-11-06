#!/usr/bin/env bash
# Exact Nangate45 standard-cell mapping of standalone synthesizable RTL.
set -euo pipefail
source_file="$1"; output_file="$2"; proof_file="$3"
lib="${NANGATE_LIB:-/tmp/orfs/flow/platforms/nangate45/lib/NangateOpenCellLibrary_typical.lib}"
mkdir -p "$(dirname "$output_file")" "$(dirname "$proof_file")"
trap 'echo "SYNTHESIS_OR_EQUIVALENCE_FAILED"; tail -n 100 "$output_file.log" 2>/dev/null || true; tail -n 100 "$proof_file" 2>/dev/null || true' ERR
yosys -Q -T -p "read_verilog -sv $source_file; synth -top address_logic -noabc; abc -liberty $lib; clean; write_verilog -noattr $output_file" > "$output_file.log" 2>&1
yosys -Q -T -p "read_verilog -sv $source_file; rename address_logic gold; read_liberty -lib $lib; read_verilog $output_file; rename address_logic gate; equiv_make gold gate equiv; hierarchy -top equiv; equiv_simple; equiv_status -assert" > "$proof_file" 2>&1
grep -Ei 'Equivalence (successfully )?proven|Equivalence check successful|Unproven 
echo "RTL_MAP_EQUIVALENCE_PASS $source_file"
 "$proof_file" || true
! grep -qi 'unproven 
echo "RTL_MAP_EQUIVALENCE_PASS $source_file"
 "$proof_file" || { tail -n 80 "$proof_file"; exit 1; }
echo "RTL_MAP_EQUIVALENCE_PASS $source_file"
