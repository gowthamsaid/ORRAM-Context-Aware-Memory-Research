# Results and evidence provenance

The `results/` directory stores a **small, checked-in summary** of the research. It is not a complete physical-design output archive; large ODB/DEF/SPEF, netlists and timing logs are associated with the original GitHub Actions runs.

## Latest evaluated holdout

[`synthesized_rtl_holdout_pairs.csv`](synthesized_rtl_holdout_pairs.csv) contains the final 12 matched **post-route setup-slack differences** from the synthesized-RTL holdout.

- Each row is one width × address RTL × placement seed choice comparing ORRAM `row` vs `word`.
- Column `row_minus_word_setup_slack_ps` is **positive when row wins**, **negative when word wins**.
- `frozen_prediction` was fixed in the [pre-physical run](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42138305712); labels were obtained only after [physical holdout](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139114830).
- This file is a **derived, human-readable transcription** of the signed margins in the dated [final evaluation report](../docs/SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md), scored in [run 42139806379](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139806379). It is **not** a substitute for the original physical reports.
- In this set: predictor **9/12**, blind word **11/12**, two-placement selector **11/12**, predictor mean oracle regret **2.9871 ps**, and mean advantage vs blind word only **0.1275 ps**. The last two metrics should be interpreted with the exclusions/limits in the full report.

## Earlier preliminary gate files

- [`feasibility_gate_2026-11-05.json`](feasibility_gate_2026-11-05.json) — initial isolated architecture/boundary screen.
- [`milestone1_gate_2026-11-05.json`](milestone1_gate_2026-11-05.json) — initial timing model audit, before full integration.
- [`stage2_routed_four_cases.json`](stage2_routed_four_cases.json) — initial registered physical wrapper pilot.

These JSONs are **historical stage gates**, not substitutes for the later multi-seed results and prospective final holdout.

For all original run IDs and evidence instructions, see the [experiment evidence index](../docs/EXPERIMENT_EVIDENCE_INDEX.md). For scientific conclusions, start at the [root README](../README.md).
