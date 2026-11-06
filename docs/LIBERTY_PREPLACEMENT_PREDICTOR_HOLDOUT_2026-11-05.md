# Milestone 3 — Pre-placement Liberty-timed decoder selector on counter and Gray-code address generators

**Experiment date:** November 5, 2026

## GO/NO-GO

**GO for a narrow preliminary predictor demonstration, NOT a general or publication-ready EDA tool.** The frozen predictor selected the routed winner in **10/12** architecture comparisons (83.3%). The two incorrect decisions were both on the 32×8 Gray encoder, with **6.801 ps** and **0.584 ps** routed slack disadvantage. The mean regret was **0.6154 ps** and maximum **6.801 ps**. Mean selected timing gain over blindly selecting the word decoder was **16.7095 ps**; this is not a measured total wall-clock or power improvement. The two-placement early selector also scored **10/12** on these cases, but made different errors.

## Scientific controls and immutable provenance

1. Prediction uses pre-placement registered address-cone OpenSTA with pinned Nangate45 Liberty and a **fixed assumed 30 fF output load**, and the previously frozen 32×8 balanced seed-11 memory-side routed timing-suffix reference from run 42128929892.
2. [Frozen predictions from run 42132385070](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42132385070), **completed before new physical routing**: word for `binary_increment` (31.6319 ps modeled advantage), word for `gray_encode` (16.8299 ps), row for `gray_decode` (49.573 ps). These are duplicated unchanged across 32×8 and 32×16 widths, because only 32×8 reference suffixes were calibrated.
3. [Matched physical comparison run 42132736843](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42132736843) succeeded for both widths. Each of 3 circuits and seeds 11 and 23 had both row and word decoder implementation, routed SPEF and constrained register-to-register timing.
4. [Immutable scoring run 42133441297](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42133441297) succeeded, preserving `holdout_comparisons.csv` and `holdout_summary.json`.

The pre-placement timing run does **not** place either *new* memory architecture, but reference calibration required both candidate implementations previously. All latency and cost comparisons must amortize the reference characterization. Clock is ideal; Nangate45 typical; this is not signoff.

## Raw comparisons: row minus word post-route setup slack, picoseconds

Positive values mean the row architecture wins.

| Memory | Logic producer | Seed 11 | Seed 23 | Frozen choice | Correct |
|---|---|---:|---:|---|---|
| 32×8 | Binary increment | −21.762 | −17.432 | word | 2/2 |
| 32×8 | Gray encode | +6.801 | +0.584 | word | **0/2** |
| 32×8 | Gray decode | +93.093 | +45.621 | row | 2/2 |
| 32×16 | Binary increment | −0.987 | −4.745 | word | 2/2 |
| 32×16 | Gray encode | −24.682 | −38.004 | word | 2/2 |
| 32×16 | Gray decode | +46.460 | +15.340 | row | 2/2 |

- Selection accuracy: **10/12**
- Matched two-placement selector accuracy: **10/12** (different mistakes)
- Always-word baseline accuracy: **6/12**
- Mean oracle regret: **0.6154167 ps**
- Max oracle regret: **6.801 ps**
- Mean gain versus always word: **16.7095 ps**
- Errors specifically in 32×8 Gray encoding, where the routed architecture margin was small in both seeds.

## Research interpretation

The predictor is not simply counting assumed XOR stages: it evaluates actual combinational address circuits (binary incrementer, Gray encoder, Gray decoder) using a technology-library timing engine without placing RAM alternatives. This is an improvement in model fidelity relative to the earlier constant 55 ps-per-extra-XOR heuristic.

However, these are **hand-coded and small illustrative circuits**. They use explicit standard-cell gates rather than independently synthesized application RTL. The model's loaded producer output is not the actual routed memory input pin's characterized load. Reference memory-side suffixes were obtained from a single 32×8 circuit/seed and are not an isolated general timing-library model. It ignores input slew/arc transition, destination setup variation, output load, coupling, placement, and other physical effects.

The two incorrect choices both involve small actual timing margins (0.584 and 6.801 ps), highlighting instability near crossover. 10/12 is an observed small-sample outcome, NOT validated generalization probability. The 16.71 ps average benefit is dominated by the gray-decoder cases; there is no measured cost advantage or robust PPA advantage for most contexts.

The 12 prospective labels are now **used** and must not be described as unseen if this model is revised. Further testing requires novel circuit families and preregistered selection/uncertainty policies.

## Next gates before any publication claim

1. Create practical independent synthesized address-logic circuits, **distinct from all development motifs**, and hold them out before further model tuning.
2. Quantify actual setup/endpoints and output slew/load sensitivity; characterize reusable memory arcs across several widths and corners without placing both new alternatives.
3. Introduce a preregistered uncertainty/abstention rule for close timing predictions, evaluated on genuinely unseen contexts.
4. Benchmark total calibration time, per-circuit predictor time, additional placement/routing, physical PPA and power. Do not describe a workflow-level Docker download time as implementation runtime.
5. Compare with ORRAM built-in row/word selection and existing timing-driven design-space methods; verify novelty through related work and potentially seek upstream OpenROAD developer feedback.

**Scientific result:** some pre-placement selection capability is demonstrated in these controlled conditions; the method is not yet a general-purpose or proven lower-compute novel EDA selector.
