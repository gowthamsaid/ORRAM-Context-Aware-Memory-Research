# ORRAM context-aware decoder selection: final bounded feasibility GO/NO-GO — 2026-11-05

**Decision A — scientific effect:** **GO** for the *bounded claim* that enclosing address-generation timing context can reverse the preferred standard-cell ORRAM row-vs-word decoder after physical place, route, and extracted-SPEF setup analysis. A narrow experiment demonstrated this behavior at 32×8 and 32×16, with independently perturbed placements.

**Decision B — proposed EDA algorithm/publication claim:** **NO-GO as currently implemented.** The placement-stage selector places BOTH candidates; it is an exhaustive comparison at a cheaper stage, not a novel or demonstrated lower-total-cost architecture selection algorithm. Novelty and end-to-end area/power/runtime improvement are not established. No signoff or generalized reliability claims.

The decisions deliberately separate a reproducible observation from a publication-ready research contribution.

## Evidence ledger

| Test | Source successful GitHub Action | Result |
|---|---|---|
| Same-interface, differently connected 32×8 ORRAM generator baseline | [42053883466](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42053883466) | pass; models equal, structures different, initial controlled boundary reversal |
| Top-level registered buffer-context postroute pilot | [42071621647](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42071621647) | directional reversal; balanced winner <20 ps in pilot |
| Three physically distinct buffer contexts, 32×8 | [42074091105](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42074091105) | balanced word +31.589 ps, late-low row +37.360 ps, mean over three seeds |
| Held-out late-high buffer context, 32×8 | [42074519388](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42074519388) | word +34.707 ps mean, 3 seeds |
| Frozen placement-based selection, 32×8 buffer contexts | [42077401815](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42077401815) | 9/9 matches to routed oracle; +12.453 ps over blind word choice on average; zero observed oracle regret |
| Independent XOR address logic, 32×8 | [42078118809](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42078118809) | directional reversal; mean balanced word +18.098 ps, late-low row +30.121 ps; **does not pass the original 20 ps mean-margin requirement for both contexts** |
| Independent XOR address logic, 32×16 | [42078118831](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42078118831) | clear reversal; balanced word +49.328 ps, late-low row +45.960 ps; ALL six comparisons exceed 20 ps in the relevant winning direction |
| Frozen placement selector on XOR logic, both sizes | [42079182085](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42079182085) | 12/12 matches to routed oracle, zero observed regret; +15.061 ps (32×8) and +22.980 ps (32×16) over always-word baseline, each averaged over six samples |
| Selection implementation-work budget | [42079426830](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42079426830) | Audit passed. Blind selection needs **one placement + one route**; current selector needs **two placements + one route**; exhaustive routed oracle uses **two placements + two routes**. Log files contain no reliable elapsed-time markers. **No measured runtime speedup claim is justified.** |

### Independent XOR test: all raw route margins, row minus word, picoseconds

| Size | Context | Seed 11 | Seed 23 | Seed 37 | Mean | Original 20 ps rule |
|---|---|---:|---:|---:|---:|---|
| 32×8 | balanced | -16.863 | -6.106 | -31.325 | -18.098 | FAIL |
| 32×8 | late-low | +27.566 | +44.037 | +18.761 | +30.121 | mean PASS, one seed below threshold |
| 32×16 | balanced | -32.438 | -44.048 | -71.499 | -49.328 | PASS |
| 32×16 | late-low | +52.705 | +23.989 | +61.187 | +45.960 | PASS |

**Negative results were retained.** The earlier failed Actions attempts were infrastructure/code failures and were not interpreted as failed hypothesis tests; the successful patched reruns have immutable run links. The 32×8 XOR **statistical engineering-margin failure remains a scientific limitation**. The parser's inherited limitations string mentions 'buffer' and '32x8' even in XOR/32×16 jobs; the actual wrapper source and script modifications in these jobs are authoritative.

## Reliability and construct validity

- Row and word alternatives use matched process, memory interface, physical floorplan, SDC and surrounding gate topology *within each configuration*. The same behavioral ORRAM models were checked, and the constructed wrapper uses the same logic across the two decoder choices.
- XOR cones avoid the earlier artificial repeated BUF gates, but are still deliberately hand-crafted circuit examples. They do **not** represent a random survey of realistic SoCs or an independently synthesized application benchmark. Across *different* contexts, the address transformations need not compute identical functions, so these are within-context architecture comparisons, not an optimized design-vs-design product comparison.
- Three placement perturbations are neither a significant random population nor multiple independent technology/library corners. The sign is consistent across our samples, but margin stability is imperfect at 32×8.
- Full physical signoff is **not** demonstrated. Ideal clock/no full CTS, limited physical-design integrity checks, no IR/EM/DRC/LVS signoff, no power study, no inter-corner assessment, and no rigorously timed method benchmark.
- All 21 evaluated placement-based selections match their own post-route winners across the original buffer tests (9) and the XOR tests (12). Do **not** turn 21/21 into a statistical generalization probability; the inputs are hand-designed and correlated.
- Original architecture inference is already supported by ORRAM's `-decoder row|word` interface. Its published 2026 paper identifies timing/power-driven ORRAM optimization as future work. A two-placement slack comparison is not a clearly original EDA algorithm.

## What would be required to turn the limited GO into a research-method GO?

Define and freeze an actual pre-placement or single-candidate physical predictor (e.g., per-input arc sensitivity + estimated arrival distributions), and compare compute/time and post-route regret against (i) blind word choice, (ii) both-candidate-placement selector, and (iii) full-route oracle. Evaluate on independently sourced real address-generation RTL, at several depth/widths and preferably a second library/PDK, with proper constraints, corner/power and CTS validation. Analyze costs and negative outcomes. Do not merely expand the artificial XOR contexts until the effect looks impressive.

## Decision for this specific proposed hypothesis

**GO as a bounded research observation/portfolio experimental case study. NO-GO for the hypothesis understood as an already validated, publishable context-aware EDA selection method.** An original research direction remains possible, but it is a **new algorithm-development milestone**, not proof furnished by this completed feasibility battery.

No manual local OpenROAD step is currently required: the relevant successful experiments were executed in GitHub Actions.
