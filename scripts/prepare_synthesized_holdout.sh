#!/usr/bin/env bash
# Called after frozen model and mapped RTL archive have been verified.
set -euo pipefail
word_size="$1"
[[ "$word_size" == 8 || "$word_size" == 16 ]]
mkdir -p wrapper integration archive/results audit
if [[ "$word_size" == 16 ]]; then
 sed -i 's/RAM32x8/RAM32x16/g;s/-word_size 8/-word_size 16/g;s/-mask_size 8/-mask_size 16/g' scripts/generate_ram.tcl
 sed -i 's/RAM32x8/RAM32x16/g' scripts/check_architectures.py
 sed -i 's/\[llength \$captures\]!=8/[llength $captures]!=16/g' scripts/registered_smoke.tcl scripts/routed_integration.tcl
 sed -i 's/\[llength \$outputs\]!=8/[llength $outputs]!=16/g' scripts/milestone1_audit.tcl
fi
sed -i 's/{balanced late_low late_high}/{balanced late_low late_high ring24 serpentine_tile dma_stride}/g' scripts/registered_smoke.tcl scripts/routed_integration.tcl
sed -i '/read_verilog "\/study\/wrapper\/\$mode.v"/i read_verilog "/study/mapped/$mode.v"' scripts/registered_smoke.tcl
for kind in ring24 serpentine_tile dma_stride; do
 python3 scripts/generate_synthesized_rtl_wrappers.py "$kind" "$word_size" "wrapper/$kind.v" "producer/$kind.v"
 test -s "mapped/$kind.v"
done
echo "SYNTHESIZED_HOLDOUT_PREP_PASS width=$word_size"
