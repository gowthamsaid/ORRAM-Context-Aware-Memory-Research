# ORRAM milestone 1 — routed address-path timing mechanism (November 5, 2026)

## Provenance

- [Successful full routed OpenSTA per-launch audit, run 42125976002](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42125976002). Archived 90 report files including 40 source-register-specific worst paths. Artifact `orram-mechanism-audit-42125976002`.
- [Selected raw timing-path printout, run 42126469582](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42126469582).
- [Conservation-checked timing decomposition, run 42126639893](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42126639893). Artifact `orram-mechanism-components-42126639893`.
- Reopened original routed ODB, SDC, and routed SPEF from the successful 32×8 and 32×16 XOR circuits, seed 11. No synthesis, placement, routing or constraints were changed. Pinned Nangate45 OpenROAD/ORFS environment. `read_spef` applied before reports.
- **Status:** timing mechanism characterization PASS; **not yet a controlled architecture-specific intervention proving unique causation**.

## What was measured

For each width (32×8, 32×16), context (balanced, late-low), architecture (row, word), and five launch flip-flops (A0–A4), report the worst register-to-register path to the capture bank. Forty reports in total. Parse incremental pin delays and sum into six regions: launch flop, surrounding XOR logic, RAM decoder, internal selection buffer, storage/output tri-state circuitry, and routed net into capture flop. All 40 component sums match reported path arrival to 0.01 ps (parser tolerance 0.00001 ns).

### Per-context worst-path anatomy — ps (seed 11)

| Size / Context | Decoder | Critical launch bit | Launch FF | XOR address | RAM decoder | Select buffer | Storage/output | Capture net | Total arrival |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 32×8 balanced | row | A4 | 92.227 | 162.282 | 199.321 | 28.574 | 197.188 | 29.993 | 709.585 |
| 32×8 balanced | word | A3 | 92.591 | 177.780 | 173.600 | 28.224 | 197.148 | 23.788 | 693.132 |
| 32×8 late-low | row | A2 | 97.430 | 266.066 | 138.125 | 28.768 | 195.959 | 31.500 | 757.848 |
| 32×8 late-low | word | A2 | 98.011 | 265.690 | 167.025 | 28.608 | 197.242 | 29.149 | 785.725 |
| 32×16 balanced | row | A4 | 92.399 | 192.896 | 218.096 | 28.705 | 285.485 | 33.069 | 850.650 |
| 32×16 balanced | word | A1 | 92.811 | 192.685 | 184.857 | 28.028 | 275.893 | 42.074 | 816.348 |
| 32×16 late-low | row | A2 | 98.463 | 288.630 | 150.032 | 28.265 | 275.505 | 38.780 | 879.675 |
| 32×16 late-low | word | A2 | 97.575 | 305.032 | 191.024 | 28.372 | 284.195 | 26.663 | 932.861 |

**Important:** The component delay values include intrinsic cell delay on the relevant outputs and extracted interconnect time on relevant input pins. They are path-specific; they are not a property of an architecture independent of input sensitization and loading. Worst paths may terminate at different data outputs and belong to different source-input cones. Therefore differences between row and word components cannot be interpreted as strictly causal differences isolated to that region.

### What we learned

1. Both memory widths exhibit **an actual switch in the dominant launching address register:** for balanced 32×8 the row and word worst launches are A4/A3, and for balanced 32×16 they are A4/A1. In the late-low XOR contexts both architectures' worst launch is A2. A2 can feed the low-address XOR cones, so this is not inconsistent with stressing low memory-address bits.
2. **The decoder-region path delay changes substantially and in the direction of architecture preference.** For 32×16 balanced, row worst-path decoder region is 218.096 ps versus word 184.857 ps; for 32×16 late-low, row is 150.032 ps versus word 191.024 ps. At 32×8 balanced it is 199.321 versus 173.600 ps; late-low 138.125 versus 167.025 ps.
3. In the 32×16 late-low path, two extra XOR stages on a memory-address cone cause a substantial change in *which route through the RAM* governs worst timing. The measured cell-level route includes input inverter / AND decoder stages, selection buffer, storage select inverter, tri-state buffer, and output capture. This provides a concrete physical-path narrative beyond comparing headline slack.
4. The 32×16 late-low worst-path arrival difference is 53.185 ps (row faster), while balanced worst-path arrival difference is 34.302 ps (word faster). *Setup slack differences differ slightly* because different endpoints have different library setup requirements.
5. It is inappropriate to say that **the decoder logic alone** caused 100% of the rank reversal. The surrounding XOR stage, output driver, capture net, endpoint switching, and postroute loads can all contribute, and the selected paths are not necessarily endpoint matched. We have evidence of mechanism consistency, not complete uniquely causal attribution.
6. There is no independent proof that ORRAM's isolated Q load model is accurate in this study. This work uses real registered sinks and reread routed SPEF, but retains an ideal clock and incomplete signoff.
7. A pre-placement predictor that uses just a single constant decoder latency is unlikely to be satisfactory: there is strong variation by launch bit and critical-path identity. A useful model would need per-address-bit timing arcs, address cone dependencies, output loading/selection conditions, and explicit uncertainty. That model is still prospective, not validated.

### Remaining causality tests and next milestone

- For each decoder, generate **fixed memory-address-pin-to-capture** paths in the integrated routed design. This separates surrounding XOR launch-time differences from the RAM decode/output path and determines whether sensitivity is stable for each pin under both contexts.
- Match the target data output and launch-point where possible, and measure load/slew/fanout on path segments, avoiding conclusions from differing critical endpoints alone.
- Run additional placement seeds for timing decomposition and accept counterexamples.
- Freeze a simple arc-based predictor, characterize without two candidate placements in each new surrounding circuit, then test only on independently generated, held-out designs and compare total compute with blind/dual-placement selection.
- Preserve failed cases and apply timing-constraint/clock/signoff limitations.

## Decision

**Milestone 1 characterization: PASS.** We have identified actual decoder and surrounding-logic segments on which the observed rank reversal appears. **Full causal identification: PARTIAL.** Do not claim to have developed or validated the early prediction algorithm or a publishable technique.
