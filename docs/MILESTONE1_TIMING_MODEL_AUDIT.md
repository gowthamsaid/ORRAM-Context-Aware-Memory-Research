# Milestone 1 — Memory Timing Model & Integration Readiness

**Run:** [Milestone-1 audit 42066620647](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42066620647)  
**Artifact:** [milestone1-model-audit-42066620647](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42066620647/artifacts/13433343845)  
**Source physical designs:** successful [feasibility run 42053883466](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42053883466)  
**Technology:** Nangate45, pinned ORFS revision and OpenROAD Docker digest as in the experiment.

## Outcome: INTEGRATION INTERFACE AVAILABLE; TIMING LOAD-MODEL NOT YET VALIDATED

The audit completed successfully as a **diagnostic**. It did **not** pass the timing model acceptance criterion. Do not interpret a successful GitHub job as physical or scientific validation.

## Test 1 — Output load sensitivity

Reopened each existing 32×8 RAM OpenDB and applied four distinct output loads: `0.005`, `0.050`, `0.500`, and `5.000` pF (OpenSTA `report_units`: 1 ns, 1 fF). Fixed all other STA boundary conditions. Recorded worst addr_rw → Q path and fixed Q[0] endpoint path at seven decimal places.

| Architecture | Q[0] path arrival at 0.005 pF | Q[0] path arrival at 5.000 pF | Change |
|---|---:|---:|---:|
| Row decoder | 0.4753254 ns | 0.4753254 ns | 0 ps |
| Word decoder | 0.4498572 ns | 0.4498572 ns | 0 ps |

The individual timing reports were byte-for-byte identical across the load sweep (apart from different file names). Previous saved SDCs confirmed the difference in `set_load -pin_load`, so this is **not a failure to issue the constraint**.

The output-stage timing report for both variants shows `TBUF_X1` driving Q[0], with reported fanout 1 and capacitance about 38.466 fF, invariant even when requested external load increases to 5,000 fF. Therefore this model does **not presently demonstrate responsive output-driver loading**. A possible cause is OpenSTA's analysis of ORRAM's multi-driver tri-state output bus, or the order/use of parasitic estimation; this experiment does **not** uniquely identify the cause. We must not use the null response to claim that external loading is irrelevant to real integrated circuits.

**Decision:** FAIL timing-load-model validation. Resolve by integrating a *real capture-register input* as a sink (or independently proving the library model/connection handles capacitive load), rather than relying on output-only SDC probing.

## Test 2 — Physical export and macro boundary contract

**PASS for a basic integration handoff:** Both existing design checkpoints can be reopened successfully, have the same 25-pin LEF interface (23 signal pins: clk, we, five address, eight data-in, eight data-out; VDD/VSS), have identical 45.6 × 46.2 μm abstract dimensions, and can export nonempty technology-mapped structural Verilog. Source OpenDB/DEF and LEF exist and are archived.

Important: This is **not a completed full-chip integration**. Macro hierarchical STA would additionally require validated Liberty timing arcs or a different flattening-based integration flow. Structural Verilog includes technology-specific tri-state drivers and clock-gating cells, so full-system simulation and STA must check that the library models and synthesis constraints are appropriate. A nonempty export does not itself prove integration correctness.

## Test 3 — Parasitic extraction support

**PARTIAL PASS:** The pinned OpenROAD image accepted `extract_parasitics -ext_model_file` against the existing design and emitted nonempty SPEF files for both architectures (row: 452,540 bytes; word: 440,516 bytes).

However, the 'extracted RC' read-path reports were **identical** to the placement-estimated ones. We have not shown that the extracted SPEF was actually used for STA, or that it yields independent parasitic results. Explicit `read_spef` reanalysis and reconciliation to extracted design nets are required before describing the timing results as extracted post-route STA.

## Signoff limitation

ORRAM emitted a missing-tapcell warning; a valid DRC/LVS or timing signoff was **not** established. This does not prevent a controlled feasibility study, but the results are not tapeout-ready.

## Research implications

1. The observed address-arrival ranking reversal in the previous feasibility experiment is real under its defined **placement-approximated boundary STA model**, but cannot yet be claimed as demonstrated full-chip ranking reversal.
2. The load-insensitivity is a **model-validation problem**, not a negative result for the proposed context-aware research hypothesis.
3. **GO** for narrowly scoped full-design integration preparations, using the exported mapped gates and real surrounding source/capture logic with timing endpoints validated before full routing.
4. **NO-GO** for treating current macro `set_load` results as signoff-grade evidence, and **NO-GO** for launching 12 expensive routed comparisons before timing and parasitics are reconciled.

## Next engineering task

Create the smallest deterministic test: for each exported memory variant, connect a registered address-generation cone and one output-register capture path, with the same top-level RTL except the memory architecture. Preserve clock, reset (if present), and timing constraints. Verify that (a) the same memory function is observed at the capture registers; (b) a change in real sink load or connectivity influences an actual register-to-register timing path; (c) routed SPEF can be read back into STA and changes/reconciles the measured path; (d) no unconstrained intended data paths remain. Use one seed first; only expand after these controls pass.

**Scientific gate:** No change to main hypothesis: system-level context-aware selection remains **unproven**, not refuted.
