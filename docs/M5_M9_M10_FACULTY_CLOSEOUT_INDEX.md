# Completed faculty closeout package — M5, M9, M10 (2026-11-05/06)

## Milestone status

- **M5 — CLOSED:** Matched 24/24 routed OpenROAD artifacts and 12/12 architecture comparisons; same read-path vs whole-design winner in all pairs; timing SDC differences only write-time comments; 24/24 reopened routed ODB, original SDC and SPEF OpenSTA reruns with explicit check_setup calls passed. This is *exploratory timing integrity*, not physical signoff.
- **M9 — CLOSED:** Dated, source-based literature review establishes substantial overlap with OpenROAD RAM feature roadmap, memory characterization and architecture design-space search. Current algorithmic novelty is not strong enough for a publication claim.
- **M10 — CLOSED as a faculty-review package:** Full report, two-page research brief, technical presentation, 15 technical-defense Q&As, qualified CV research entry and unsent faculty outreach drafts. Faculty feedback is *future external input*, not something the research report can guarantee.

## Read in this order

1. [M5 postroute integrity final](M5_POSTROUTE_INTEGRITY_2026-11-05.md)
2. [M9 literature, novelty and direct links](M9_LITERATURE_AND_NOVELTY_REVIEW_2026-11-05.md)
3. [M10 complete faculty report](M10_FACULTY_RESEARCH_REPORT_2026-11-05.md)
4. [M10 short brief, slide structure and Q&A](M10_FACULTY_BRIEF_SLIDES_DEFENSE_2026-11-05.md)
5. [M10 faculty feedback email draft](M10_FACULTY_FEEDBACK_OUTREACH_DRAFT.md)

## Immutable evidence

- M5 serialized audit: https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42144508832
- M5 postroute OpenSTA reread: https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42155987361
- M5 independent verification: https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42156452762
- ORRAM physical mechanism: https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42128929892
- Frozen synthesized RTL model: https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42138305712
- Matched physical synthesized RTL holdout: https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139114830
- Full prediction and stage-cost scoreboard: https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139806379

## Bottom line

**Validated within bounded exploratory conditions:** different surrounding address arrival profiles can reverse ORRAM row vs word physical timing preference; observed per-input path sensitivity is consistent with that effect.

**Explicit negative result:** the prototype selector obtained only 9/12 correct choices in synthesized RTL holdouts, versus 11/12 for always-word and 11/12 for a dual-placement selector, with no meaningful net timing gain or demonstrated total runtime advantage.

**Scope for faculty discussion:** Independent problem formulation, reproducible physical experiments, critical-path analysis, prospective algorithms and transparent failure analysis; not an accepted paper, novel RAM generator, generalized selector or full-chip tapeout signoff.

**Next work authorized by project plan:** Request faculty feedback, receive critique, prepare PhD applications, and only then consider new predictor research (M6–M8). No further frozen test-set tuning should be presented as prospective evidence.
