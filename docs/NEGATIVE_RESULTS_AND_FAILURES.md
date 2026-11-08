# Negative results, failed gates, and corrected failures — ORRAM study

**Research status (8 November 2026):** A **bounded address-context-dependent row/word post-route timing reversal** was observed in controlled tests. The broader **pre-placement architecture-selection algorithm is NO-GO** on final synthesized-RTL holdout and cost evidence. This ledger separates scientific failures, failed engineering criteria, historical CI failures, and unperformed extensions.

Read alongside the [faculty briefing](START_HERE.md), [full report](M10_FACULTY_RESEARCH_REPORT_2026-11-05.md), [experiment/run index](EXPERIMENT_EVIDENCE_INDEX.md) and [final results](SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md). An early GO for a feasibility stage **does not override the final predictor NO-GO**.

## Scientific and methodological outcomes

| Test or claim | Outcome | Observed result |
|---|---|---|
| Isolated row/word external-arrival screen | **EXPLORATORY PASS ONLY** | Altered SDC input arrival conditions reversed the preferred configuration, but the test relied on a simplified boundary model and placement RC, not a registered whole-system routed result. [Initial feasibility](FEASIBILITY_RESULTS_2026-11-05.md). |
| Initial output-load timing model | **FAIL model validation** | A successfully completed diagnostic job found implausibly invariant timing under deliberately changed output loads. Those timings were not accepted as a validated load model; the next experiment used real capture registers. **A green Actions run was not a scientific PASS.** [Milestone 1](MILESTONE1_TIMING_MODEL_AUDIT.md). |
| Four-case 32×8 registered pilot: predefined 20 ps two-context criterion | **FAIL criterion** | Balanced word advantage **18.768 ps**, below the threshold; late-low row advantage **27.925 ps**. Initial placements were deterministic, not different seeds. Later multiseed experiments were separate validation. [Stage 2](STAGE2_ROUTED_INTEGRATION.md). |
| 32×8 XOR: predefined 20 ps mean margin | **FAIL criterion** | Balanced word advantage **18.098 ps mean**; late-low row advantage **30.121 ps mean** but one seed below threshold. The separate 32×16 XOR control passed its margins. Do not call the 32×8 XOR batch a pass. [Bounded feasibility](FINAL_FEASIBILITY_GO_NO_GO_2026-11-05.md). |
| Two-placement architecture selector | **NOT a demonstrated efficient novel predictor** | It physically placed both candidates. Matching the routed oracle on controlled contexts did not prove a general original predictor or lower end-to-end cost. [Decision](FINAL_FEASIBILITY_GO_NO_GO_2026-11-05.md). |
| Earlier frozen heuristic XOR-context holdout | **PARTIAL, NOT GENERAL VALIDATION** | **9/12** on a different 12-case experiment; it must not be pooled with the later synthesized-RTL holdout. [Earlier holdout](FROZEN_PREPLACEMENT_PREDICTOR_HOLDOUT_2026-11-05.md). |
| Liberty-timed small-circuit holdout | **PARTIAL; TWO WRONG CHOICES** | **10/12** on hand-coded counter and Gray address logic; wrong in two 32×8 Gray encoder runs. Not an external application-RTL validation. [Liberty holdout](LIBERTY_PREPLACEMENT_PREDICTOR_HOLDOUT_2026-11-05.md). |
| Final prospective synthesized application-RTL predictor | **NO-GO for a generally useful selector** | **12 pairs / 24 routed designs:** frozen predictor **9/12**, always-word **11/12**, two-placement **11/12**. Three serpentine failures, max regret **20.681 ps**, mean gain against always-word only **0.1275 ps**. Do not retune on these labels and call them new held-out data. [Final interpretation](SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md), [CSV](../results/synthesized_rtl_holdout_pairs.csv), [physical run](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139114830). |
| End-to-end runtime advantage | **NOT DEMONSTRATED** | Stage-only timing excludes reference characterization, synthesis and prediction overhead; small observed one-candidate differences are not a proof of practical acceleration. [Cost report](SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md). |
| Standalone novelty of proposed selection method | **NOT ESTABLISHED / M9 NO-GO** | ORRAM already supplies row and word options; the prospective algorithm overlaps known timing-driven architecture-selection proposals. [Prior-art review](M9_LITERATURE_AND_NOVELTY_REVIEW_2026-11-05.md). |

## Historical Actions failures (engineering/debugging; not failed hypotheses)

Original failed GitHub runs remain available, including these representative retry sequences:

- [Initial feasibility 42050187798 — failed](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42050187798); [42053883466 — passed](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42053883466).
- [Registered integration 42070500424 — failed](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42070500424); [42071621647 — passed](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42071621647).
- [Synthesized-RTL physical holdout 42138571460 — failed](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42138571460); [42139114830 — passed](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139114830).
- [M5 integrity 42144346528 — failed](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42144346528); [42144508832 — passed](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42144508832), followed by [postroute STA 42155987361](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42155987361).

The [final report's engineering corrections section](SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md#engineering-corrections-and-audit-trail) records missing Yosys in the OpenROAD container, functional Liberty modeling for formal equivalence, an overly broad proof-success grep, and a disconnected supply-placeholder net that stopped routing. Early feasibility also encountered an incorrect TAPCELL_X1 LEF assumption. **Do not attach a specific root cause to an individual failed run without inspecting that run's logs.** Skipped conditional workflows are not scientific experiment failures.

## Final disposition and unperformed extensions

**Supported narrowly:** Address-producer context changed preferred row/word ORRAM setup timing within tested Nangate45 32×8 and 32×16 registered implementations, with routed SPEF and repeated seeds. [Timing sensitivity](ORRAM_THREE_SEED_ADDRESS_SENSITIVITY_2026-11-05.md).

**Not supported or not done:** Better-than-baseline general selection; a real total runtime benefit; industrial-workload generalization; new decoder invention; production clock-tree / multi-corner / physical signoff; power or side-channel measurements. M5 reopened 24/24 routed checkpoints but did not certify all signoff constraints. [M5 limits](M5_POSTROUTE_INTEGRITY_2026-11-05.md).

**Next step is proposed only:** Decide with faculty whether a fresh physical sensitivity / uncertainty-aware predictor could justify a separate, truly held-out validation study. Security/side-channel work is an idea, not an experimental outcome.