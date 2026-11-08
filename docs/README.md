# Documentation index

The root [README](../README.md) explains the research question and headline findings. A faculty reviewer should begin with [START_HERE.md](START_HERE.md), not with the first chronological feasibility document or the GitHub Actions list.

## 1. Current findings: recommended reading

| Document | Purpose |
|---|---|
| [Negative findings and failed experimental gates](NEGATIVE_RESULTS_AND_FAILURES.md) | Distinguishes scientific failures and negative conclusions from corrected CI problems |
| [Faculty briefing](START_HERE.md) | 2–3 minute overview of hypotheses, result, limitations and requested feedback |
| [Complete research report](M10_FACULTY_RESEARCH_REPORT_2026-11-05.md) | Controlled setup, full results, negative predictor outcome and novelty discussion |
| [Experiment and raw-evidence index](EXPERIMENT_EVIDENCE_INDEX.md) | Chronological successful run IDs and original experimental sources |
| [Reproduction and toolchain guide](REPRODUCIBILITY.md) | Pinning, lightweight tests, full flow limitations and artifact retention |
| [Final synthesized-RTL generalization and cost](SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md) | 12 holdout pairs and honest 9/12 versus 11/12 interpretation |
| [Physical timing and integrity audit](M5_POSTROUTE_INTEGRITY_2026-11-05.md) | ODB/SDC/SPEF rechecks, target/global winner agreement, signoff boundary |
| [Literature and novelty](M9_LITERATURE_AND_NOVELTY_REVIEW_2026-11-05.md) | ORRAM/OpenROAD prior art and realistic novelty limitations |

## 2. Timing mechanism and predictor development

| Document | Role |
|---|---|
| [Detailed timing mechanism](ORRAM_TIMING_MECHANISM_MILESTONE_2026-11-05.md) | Register-to-memory-to-output delay decomposition |
| [Fixed capture endpoint sensitivity](ORRAM_FIXED_ENDPOINT_SENSITIVITY_2026-11-05.md) | Experimental control for comparing paths to matched output pins |
| [Three-seed address sensitivity](ORRAM_THREE_SEED_ADDRESS_SENSITIVITY_2026-11-05.md) | 420 path records and 150 matched per-address comparisons |
| [Frozen heuristic predictor](FROZEN_PREPLACEMENT_PREDICTOR_HOLDOUT_2026-11-05.md) | Earlier experimental holdout and score; different test set |
| [Liberty pre-placement predictor](LIBERTY_PREPLACEMENT_PREDICTOR_HOLDOUT_2026-11-05.md) | Counter/Gray address producer timing; different test set |
| [Prospective predictor protocol](PREREGISTERED_PREPLACEMENT_PREDICTOR_2026-11-05.md) | Prediction design and freeze requirements |

## 3. Earlier experimental milestones — historical chronology

The following documents record decisions **at their respective stages**. An early "GO" for physical feasibility does **not** supersede the later **NO-GO for a generally effective predictor**.

| Document | Original role |
|---|---|
| [Initial feasibility protocol](FEASIBILITY_GATE.md) | Predefined baseline question and controls |
| [Initial feasibility results](FEASIBILITY_RESULTS_2026-11-05.md) | First isolated timing-context screening |
| [First milestone timing-model audit](MILESTONE1_TIMING_MODEL_AUDIT.md) | Identified isolated model concerns |
| [Initial physical wrapper results](STAGE2_ROUTED_INTEGRATION.md) | Registered physical integration pilot |
| [Bounded physical feasibility go/no-go](FINAL_FEASIBILITY_GO_NO_GO_2026-11-05.md) | Distinguishes observed physical effect from unproven algorithm |
| [Prior-art novelty gate](PRIOR_ART_NOVELTY_GATE_2026-11-05.md) | Earlier literature check |
| [Continuation checkpoint](CONTINUATION_CHECKPOINT_2026-11-05.md) | Historical next-step decisions |

## 4. Faculty-review package and internal planning records

These are *presentation and planning aids*, not separate independent experimental results:

- [Faculty briefing / slide outline / technical-defense Q&A](M10_FACULTY_BRIEF_SLIDES_DEFENSE_2026-11-05.md)
- [M5/M9/M10 closeout milestone index](M5_M9_M10_FACULTY_CLOSEOUT_INDEX.md)
- [Faculty closeout planning document](APPROVED_FACULTY_CLOSEOUT_PLAN_2026-11-05.md)
- [Unsent example faculty outreach](M10_FACULTY_FEEDBACK_OUTREACH_DRAFT.md)

## 5. Outside the documents directory

- [Final routed holdout compact scoreboard](../results/synthesized_rtl_holdout_pairs.csv) and [results index](../results/README.md).
- [Synthesized address RTL](../rtl_applications/): `ring24.v`, `serpentine_tile.v`, `dma_stride.v`.
- [Tool scripts](../scripts/) and [testbench](../tb/ram32x8_tb.v).
- [Workflow sources](../.github/workflows/), with their *specific roles* in [the experiment index](EXPERIMENT_EVIDENCE_INDEX.md).

No experimental scripts or result files have been renamed to construct this index; the original provenance and workflow links remain intact.
