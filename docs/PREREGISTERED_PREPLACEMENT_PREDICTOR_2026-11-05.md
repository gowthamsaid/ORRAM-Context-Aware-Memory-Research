# Frozen pre-placement predictor — experiment registration (November 5, 2026)

## Protocol and ordering
1. Characterization: use the archived **32×8 balanced**, seed-11 routed memory-boundary timing reports (GitHub run 42128929892). The reference uses both row and word implemented once; any subsequent circuit prediction requires neither of these candidates to be placed.
2. The frozen predictor and its predictions were successfully archived in **[run 42130789146](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42130789146)**, before the new holdout flow was launched.
3. The new physical holdout was launched as **[run 42130967413](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42130967413)**. Its 32×8 and 32×16 runs are not to be used for fitting or changing the decisions.
4. Every wrong prediction, tie and negative timing advantage is to be retained.

## Frozen model

For architecture `a` and memory-address bit `i`:

`estimated_path_ps(a,i) = A_ref(i) + 55*(XOR_depth(i)-1) + D_ref(a,i)`

where `A_ref(i)` is the mean of row/word observed boundary times in the one 32×8 balanced seed-11 calibration, and `D_ref(a,i)` is the worst output-capture path suffix through that address bit in that same reference. The method chooses the architecture with the smaller estimated maximum over five address bits.

This is a deliberately simple, interpretable **first prototype**, not a PDK-independent formula. The per-stage 55 ps increment is a heuristic from previously observed XOR logic delay, **not derived from a frozen standalone SPICE/cell library model**. It includes no slew/output-load or endpoint setup-time correction. It reuses 32×8 characterization without resizing memory arcs for 32×16, making cross-width transfer a real possibility for failure.

The scheme requires both candidates to have been physically characterized once on the reference circuit, but no candidate placement for each new circuit. Time/cost must include reference characterization amortized over a number of future designs; a speedup is not assumed.

## Frozen predictions

| Size | Late high | Late middle | Staggered |
|---|---|---|---|
| 32×8 | word, 28.619 ps | row, 2.779 ps | row, 2.779 ps |
| 32×16 | word, 28.619 ps | row, 2.779 ps | row, 2.779 ps |

The predicted margins are not calibrated confidence intervals. The small 2.779 ps margin should be treated as a low-confidence decision; the algorithm as frozen still selects row for scoring.

## Holdout test

A new physical flow implements 3 address-generation XOR contexts at two word widths and seeds 11/23, with matched row/word architecture choices, under the pinned Nangate45/OpenROAD environment. The physical oracle is the better **postroute** setup slack. Also compare early two-placement and always-word baselines and compute setup-slack regret.

These are new **hand-crafted** contexts but share the 32×8/32×16 ORRAM and underlying XOR design family; this is a limited controlled holdout, not external independently generated SoC RTL. Correlated placement seeds and reused memory module are not statistically independent data points.

## Research decision criteria

- More than finding some correct predictions, evaluate accuracy by context, mean and worst-case regret, and sensitivity to close estimated margins.
- **GO only for bounded predictive feasibility** if it beats blind word choice on unseen test circuits without large harmful regret.
- **NO-GO for generalization or publication-quality optimization** without real RTL holdouts, more configurations, power/area/compute measurements, physical signoff, and prior-art differentiation.
