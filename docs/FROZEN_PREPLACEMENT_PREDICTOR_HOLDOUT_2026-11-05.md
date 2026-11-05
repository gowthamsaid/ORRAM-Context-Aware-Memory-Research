# Milestone 2: Frozen pre-placement predictor — prospective holdout results

**Date:** 2026-11-05

## Scientific verdict

**PARTIAL GO for first-prototype predictive feasibility**, not for a reliable, low-cost or publication-ready selection method. The model achieved 9/12 correct decoder selections (75%) against post-route timing on deliberately new XOR contexts, across two widths and two placement seeds. Average post-route timing regret versus the oracle was **0.7758 ps**, worst-case regret **4.818 ps**. Mean gain over always selecting the word decoder was **3.9613 ps** across all 12 comparisons, which is modest and has not been shown to justify characterization cost. Early two-placement selection also scored 9/12.

## Temporal integrity and provenance

1. Frozen model source: [`scripts/frozen_preplacement_predictor.py`](../scripts/frozen_preplacement_predictor.py), commit `17b5c3c`, using **only the earlier 32×8 balanced-context seed-11 per-address routed reference** from run 42128929892.
2. Immutable model predictions were produced in [run 42130789146](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42130789146), **before** the physical holdout experiments. Artifact: `orram-preplacement-frozen-42130789146`.
3. The independent (from calibration) XOR address cones were routed in two successful matched physical-width jobs under [run 42130967413](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42130967413). Artifacts: `orram-frozen-holdout-8-42130967413`, `orram-frozen-holdout-16-42130967413`.
4. [Run 42131694295](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42131694295) compared predictions with actual postroute routed-SPEF setup slack and archived `holdout_comparisons.csv` and `holdout_summary.json`.

## Registered comparison and controls

One 32×8 balanced seed-11 row/word set (previously placed/routed once) characterizes the physical reference. The model uses per-address timing suffixes and average boundary arrivals, plus a fixed 55 ps per additional XOR gate estimate. It does not place or route **new** candidates to predict them; however the initial one-time calibration had physically implemented **both** candidates. Reported cost claims must include this amortized reference expense.

Three newly registered address-logic contexts: delayed high bits, delayed middle bit, and staggered logic depth. Two memory widths (32×8 and 32×16), two placement seeds (11,23), two architecture implementations per case: 12 row-vs-word comparisons.

The same frozen predictions were used across both widths (no 32×16-specific characterization). The model is simplistic and does not adjust output setup checks, slew/drive loading, buffer sizing or physical placement.

## Individual results: postroute row-minus-word setup-slack differences (ps)

Positive means the row decoder wins. Negative means word wins. Predictions were frozen as word for late_high, row for late_mid, row for staggered.

| Size | Context | Seed 11 | Seed 23 | Prediction |
|---|---|---:|---:|---|
| 32×8 | late_high | −37.637 | −22.206 | word (correct both) |
| 32×8 | late_mid | −1.240 | −4.818 | row (**wrong both**) |
| 32×8 | staggered | +18.925 | +2.165 | row (correct both) |
| 32×16 | late_high | −28.498 | −45.763 | word (correct both) |
| 32×16 | late_mid | −3.252 | +30.583 | row (wrong seed 11, correct seed 23) |
| 32×16 | staggered | +2.758 | +2.414 | row (correct both) |

### Summary

- Frozen predictor accuracy: **9/12** (75%)
- Two-placement early selector accuracy on exact same holdout: **9/12** (75%)
- Always-word context-blind accuracy: **7/12** (58.3%)
- Mean predictor regret versus postroute best candidate: **0.775833 ps**
- Maximum predictor regret: **4.818 ps**
- Mean advantage over always-word: **3.96125 ps**
- Context accuracy: late_high 4/4, late_mid 1/4, staggered 4/4
- All incorrect decisions on late_mid, where model predicted just **2.779 ps** of row advantage, a clearly precarious estimated margin.

## Interpretation

The first low-computation model captured the sign of preferences in high-order delayed and staggered cases and transferred unchanged from reference width 8 to width 16. Its errors concentrate near the predicted crossover. Correct classification is not equivalent to useful optimization, particularly if actual advantage is only 2–4 ps while timing-model and placement variation can be larger.

There is no statistical population of independent design workloads: the two test widths share architecture and the same hand-crafted XOR generator. The observed 75% is a *descriptive result on this family*, not an expected accuracy on an arbitrary SoC.

The predictor currently estimates upstream delays by an arbitrary 55 ps XOR-stage heuristic. This is the next obvious model weakness to address, rather than retuning the heuristic against these newly seen oracle labels.

## Next research gate

1. Replace the guessed 55 ps increment with independent pre-placement gate-level STA of the source address cone, or calibrated Liberty delay approximations, **without using new memory architecture placement**.
2. Add explicit uncertainty intervals or an abstention/fallback when predicted architecture margins are smaller than expected physical variation. **Do not claim post-hoc thresholds evaluated on this run are prospective evidence.**
3. Lock new predictions before any **new** physical holdouts; use truly distinct address producer logic (e.g. synthesized counter/Gray-code/generic small controller address-generation RTL) rather than more XOR padding.
4. Measure calibration overhead, incremental prediction compute time, postroute regret, and net wall-clock cost versus blind, two-placement, and two-route baselines. No signoff/power novelty claim until measured.
5. Separate training and application data: these 12 holdout labels may now serve as diagnostics, **not** as fresh unseen tests for a revised predictor.

**Decision:** continue as research work because the mechanism and preliminary predictor are defensible; **NO-GO** for claiming a validated publishable efficient selection method on this battery.
