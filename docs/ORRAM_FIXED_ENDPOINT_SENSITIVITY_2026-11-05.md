# Milestone 1B — Fixed-output memory-address boundary sensitivity (November 5, 2026)

## Decision

**PASS for an observed, reproducible (seed 11), address-dependent timing-sensitivity pattern.** In matched output-register comparisons, the row decoder exhibits lower downstream delay from low address bits A0/A1 while the word decoder exhibits lower downstream delay from high address bits A3/A4, in every tested output/context/width combination. The middle bit A2 is near the crossover, with varying sign. This is **mechanism-consistent evidence**, not a uniquely causal proof of algorithm novelty or of universal memory-interface arc latency.

### Verified GitHub evidence

- [Full routed memory boundary STA run 42128198373](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42128198373), artifact `orram-memory-boundary-sensitivity-42128198373`. Includes full raw OpenSTA paths, `boundary_suffix_paths.csv`, and `boundary_suffix_summary.json`; **140 measurement records**.
- [Independent same-output comparison run 42128597674](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42128597674), artifact `orram-fixed-output-comparison-42128597674`. Includes **50 fixed-endpoint matched comparisons** for five address bits.
- Both workflows completed successfully. An earlier first attempt to author the Tcl and workflow was corrected before successful execution; the successful records above are the authoritative result.

## Measurement definition

Source design: frozen previously routed Nangate45 ORRAM 32×8 and 32×16 XOR-context circuits, **physical seed 11**, from successful runs 42078118809 and 42078118831. Same corresponding SDC and extracted SPEF reread for STA. Ideal clock, typical corner; not signoff.

Because the ORRAM structural Verilog is flattened, the tested design has no surviving hierarchical RAM `addr_rw[i]` port. We take the **Z pin of the last XOR driver** on the corresponding `addr_mem[i]` net as the physical address boundary. OpenSTA `report_checks -through` selects a real constrained launch-FF-to-capture-FF path through that pin.

For each path:

**Downstream suffix = arrival at capture D − arrival at final address XOR output Z.**

This captures the final address net and routed RAM decoder, selection, storage/output and capture net. It excludes the launch FF and upstream XOR logic already traversed *before* the chosen boundary. It remains dependent on the boundary driver's slew, physical placement, actual sensitized path, load and output endpoint. It should not be called an intrinsic, port-independent Liberty memory arc.

Per address: report the worst timing path to any capture FF, and a separate worst path terminating at fixed Q0/Q7 (and Q14 for 16-bit). Fixed-output comparisons pair row-vs-word at the identical data output register, but are not guaranteed to traverse identical selected storage words or edge polarities.

## Core result: Fixed Q14, 32×16, balanced context, row-minus-word suffix (ps)

| Memory input bit | Row minus word |
|---|---:|
| A0 | -58.5795 |
| A1 | -45.7964 |
| A2 | +2.1502 |
| A3 | +26.6226 |
| A4 | +102.0279 |

Negative is row downstream faster. Positive is word downstream faster.

## Complete fixed-endpoint differences (ps), A0 / A1 / A2 / A3 / A4

| Size | Context | Same capture | A0 | A1 | A2 | A3 | A4 |
|---|---|---|---:|---:|---:|---:|---:|
| 32×8 | Balanced | Q0 | -56.515 | -40.454 | -9.557 | +18.002 | +81.928 |
| 32×8 | Balanced | Q7 | -55.914 | -38.754 | -3.069 | +19.174 | +89.361 |
| 32×8 | Late-low | Q0 | -57.514 | -28.767 | -0.653 | +18.741 | +83.378 |
| 32×8 | Late-low | Q7 | -61.614 | -27.509 | +2.760 | +19.832 | +82.808 |
| 32×16 | Balanced | Q0 | -58.819 | -36.032 | -1.935 | +26.384 | +99.622 |
| 32×16 | Balanced | Q7 | -48.494 | -46.658 | +0.758 | +34.562 | +103.425 |
| 32×16 | Balanced | Q14 | -58.580 | -45.796 | +2.150 | +26.623 | +102.028 |
| 32×16 | Late-low | Q0 | -86.962 | -43.783 | -20.525 | +6.396 | +85.829 |
| 32×16 | Late-low | Q7 | -77.033 | -36.035 | -13.279 | +12.819 | +90.608 |
| 32×16 | Late-low | Q14 | -65.528 | -29.202 | -2.993 | +26.906 | +94.760 |

All ten matched cases have negative A0/A1 and positive A3/A4. Sign of A2 varies. These are correlated, hand-crafted circuit comparisons and must **not** be treated as ten statistically independent application samples.

## Interpretation

Previous whole-design timing reversal was observed because **which launch/cone dominates changes with surrounding logic**. The downstream per-address behavior is compatible with this: low-order address bit paths tend to prefer row while high-order address bit paths tend to prefer word. Different critical paths and endpoint setup requirements still affect the total setup-slack ranking.

This resolves part of the **how** beyond the initial path-decomposition report, but does not isolate all causes or demonstrate that swapping only one decoder gate changes one fixed path while all other physical variables remain identical. The per-address timing differences also include selection and output network differences, not only decoder AND logic.

## Limitations and scientific next gate

1. Single placement seed for this focused STA suffix audit. Expand to seeds 11, 23, 37 before claiming placement-robust per-address sensitivity.
2. Data-output endpoint is fixed, but sensitized internal word, launch register, path transition, placement and boundary slew need not match.
3. Address contexts are engineered XOR wrappers, not independently sourced real SoC RTL.
4. Typical Nangate45 and ideal clocks only; no rigorous signoff/CTS/power/multi-corner confirmation.
5. A new low-cost architecture predictor remains **unimplemented**. An early-arrival-plus-characterized-arc model requires calibration on separate training configurations and frozen evaluation on genuinely unseen designs, along with overhead accounting.

**Research status:** bounded feasibility and path-sensitivity mechanism supported; generality, predictor novelty and method-efficiency remain open.
