# Milestone 4 — Independently synthesized RTL generalization and implementation-cost audit

**Experiment closed:** November 5, 2026 (America/New_York).  
**Decision:** **COMPLETE for the preregistered three-circuit synthesized-RTL and stage-cost evaluation. NO-GO for a reliable or demonstrably more efficient general-purpose pre-placement selection algorithm.**

## Experimental provenance

- Sources were separately committed before timing prediction or holdout implementation:
  - [`rtl_applications/ring24.v`](../rtl_applications/ring24.v): 24-entry circular-address translation with offset.
  - [`rtl_applications/serpentine_tile.v`](../rtl_applications/serpentine_tile.v): alternating-direction tiled address mapping.
  - [`rtl_applications/dma_stride.v`](../rtl_applications/dma_stride.v): truncated fixed-stride DMA address mapping.
- Source RTL was synthesized with Yosys + ABC and Nangate45 Liberty; three *formal RTL-to-mapped combinational equivalence proofs* passed after the actual Nangate functional gate models were expanded in SAT. Mapped netlists were the same for row and word implementations within each test case.
- **Frozen before routing:** [run 42138305712](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42138305712). Predictions identical for 32×8 and 32×16, trained solely on earlier balanced 32×8 seed-11 per-address memory-side timing suffixes from [run 42128929892](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42128929892). Isolated pre-placement STA was run on the Yosys-mapped producer with fixed assumed 30 fF output load. Choices: ring24=word (16.8299 ps modeled advantage), serpentine_tile=row (2.7789 ps), dma_stride=word (36.7636 ps).
- **Actual physical test:** [run 42139114830](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139114830) completed successfully. Each of three circuits at both word widths and two placement seeds (11,23) was separately implemented with row and word ORRAM. This yields **12 paired architecture comparisons, 24 routed physical designs**, with original SDC and extracted SPEF imported for STA.
- **Scoring + stage timing:** [run 42139806379](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139806379) passed. Preserved `evaluation/holdout_comparisons.csv`, `evaluation/holdout_summary.json`, `evaluation/implementation_cost.csv`, and `evaluation/cost_summary.json` in artifact `orram-synthesized-rtl-cost-evaluation-42139806379`.

## Results — all held-out physical implementations

`row minus word` denotes post-route read-path setup-slack difference in **ps**. Positive favors row, negative favors word.

| Size | Address RTL | Seed 11 | Seed 23 | Frozen choice | Correct |
|---|---|---:|---:|---|---|
| 32×8 | Ring translator | -39.467 | -10.475 | word | 2/2 |
| 32×8 | Serpentine tile | +37.375 | -4.671 | row | 1/2 |
| 32×8 | DMA stride | -17.100 | -20.940 | word | 2/2 |
| 32×16 | Ring translator | -31.991 | -15.987 | word | 2/2 |
| 32×16 | Serpentine tile | -20.681 | -10.493 | row | **0/2** |
| 32×16 | DMA stride | -49.778 | -21.840 | word | 2/2 |

- **Frozen predictor accuracy:** 9/12 = 75.0%.
- **Two-placement early-slack baseline accuracy:** 11/12 = 91.7%.
- **Blind word decoder accuracy:** 11/12 = 91.7%.
- **Mean regret versus fully routed per-case oracle:** 2.9871 ps.
- **Maximum regret:** 20.681 ps (32×16 serpentine tile seed 11).
- **Mean post-route gain vs blind word choice:** +0.1275 ps, negligible.
- **All three predictor errors:** 32×8 serpentine seed23 (-4.671 ps), 32×16 serpentine seed11 (-20.681 ps), 32×16 serpentine seed23 (-10.493 ps).
- **Oracle / winner balance:** word wins 11 cases; row wins just one. Therefore 9/12 apparent correct predictions are **worse in classification accuracy than a simple always-word baseline (11/12)**. This severely weakens the claimed optimization contribution.

## Implementation-stage wall time

Each placement and route was timed with `/usr/bin/time -f %e` around the actual Docker/OpenROAD invocation. The table below is the **average sequential combination of measured stage durations per configuration**:

| Strategy | Mean timed placement+route seconds |
|---|---:|
| Blind choose word: one placement + one route | 14.642 |
| Frozen predictor: one selected placement + one selected route | 14.499 |
| Dual-placement selector: two placements + route selected decoder | 15.853 |
| Routed oracle: place+route both decoder architectures | 28.749 |

Differences of ~0.14 s between one-candidate strategies reflect **different selected cells and runner variation**, not proven computational speedups. The selection model is **not free**: reference two-architecture characterization, Yosys synthesis and isolated producer OpenSTA cost are not included in these numbers. We have not measured end-to-end startup-to-completion latency under controlled identical runner conditions, or energy/power. Therefore **NO speedup claim**.

## Engineering corrections and audit trail

Several Actions runs failed for infrastructure reasons; these were not counted as negative scientific outcomes:

1. The pinned OpenROAD Docker container did not contain Yosys; synthesis was moved to a separately version-recorded GitHub runner installation.
2. The first formal comparison treated Nangate cells as black boxes, then incorrectly matched optimized internal wires. The corrected proof imports functional Liberty cells, blacklists ambiguous intermediate names, flattens them into SAT-compatible logic, and asserts `equiv_status -assert` with zero unproven outputs.
3. An overly broad success-string grep falsely rejected an actual successful proof; the corrected proof checks only the conclusive Yosys success and its exit status.
4. Routed `ring24` initially failed because its placed DEF included **a disconnected `u_addr_gen/zero_` ground placeholder net with zero pin terminals**. A diagnostic successfully confirmed zero terminals in the DEF. The physical script now invokes `scripts/remove_empty_supply_placeholders.tcl` to remove **only unconnected** GROUND/POWER placeholders before routing. It preserves any connected supply net. The corrected physical workflow passed for both widths.
5. For transparency, the original failed jobs and their logs remain in Actions. They were not silently discarded or presented as unfavorable decoder performance.

## Scientific conclusion and remaining limits

**This preregistered milestone is complete even though it did not confirm the desired generalization.** A model trained on one physically characterized ORRAM reference plus pre-placement technology-library STA of new synthesized address logic can sometimes predict the correct decoder. However it failed three of four serpentine cases, and its small average benefit is indistinguishable from a blind word baseline for the tested cases. In this sample the blind baseline also had better win-rate.

This is not an independently sampled industrial RTL benchmark: the three application-inspired sources were created specifically for this study, share a five-bit address port and 32-entry memory, and use the same Nangate45 corner, floorplan and ideal-clock flow. Seeds and widths are correlated; 9/12 is not a defensible claim about general future designs. The predictor's pre-placement load assumption is not extracted target loading. Full CTS, PVT sweeps, electrical power, physical signoff, and calibrated compute cost remain unvalidated.

**Milestone recommendation:** preserve this complete negative generalization evaluation as credible independent research evidence, and **do not retune the frozen model on these labels and call it out-of-sample**. If pursuing algorithmic novelty further, launch a distinct research question with a new training/evaluation protocol: a width/size/corner-sensitive memory arc model, physically informed uncertainty and a conservative abstention policy on near-ties; require genuinely external or separately generated address RTL and a measured amortized total cost advantage before advancing to publication claims.

**Faculty reporting:** Present this as a transparent hypothesis-driven experimental result, not an invented successful EDA speedup. This is suitable for feedback and explanation of research ownership without asserting paper readiness.
