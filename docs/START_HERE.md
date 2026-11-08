# Research briefing for faculty review

**Project:** Context-Dependent Physical Timing and Early Architecture Selection for Standard-Cell Memories  
**Student:** Gowtham Sai Damalacheruvu · Rutgers University, M.S. Electrical and Computer Engineering  
**Status:** Completed exploratory experiments, November 2026; seeking feedback on research significance and next steps.

## Question and motivation

My earlier [FIFO read-path study](https://github.com/gowthamsaid/FIFO-ReadPath-Research) investigated indexed versus shared decoder logic under RTL-to-GDSII implementation. That study suggested that physical timing differences were not explained simply by the assumed decoder-select routing mechanism. I then formulated a distinct question using the existing ORRAM memory generator:

> Does the arrival-time structure of surrounding address-generation logic change which *existing* standard-cell memory decoder architecture has better **post-route setup timing**? If so, can the better choice be predicted without placing and routing both alternatives?

The goal was not to invent a RAM decoder or to remedy an existing signoff violation; it was to formulate and test a controlled EDA timing question.

## Experimental setup

ORRAM-generated **row** and **word** decoder variants were integrated within matched registered address-generation and output-capture wrappers. For each matched pair, memory interface, address-producer function, Nangate45 typical library and timing-constraint intent were held fixed. Repeated physical implementations used separate placement seeds. The flows preserved routed physical checkpoints and extracted **SPEF** for path analysis.

The progression was: isolated feasibility screen → integrated 32×8 and 32×16 physical experiments → address-pin timing decomposition → pre-placement predictor → new synthesized-RTL holdout and measured stage cost → scoped timing-integrity and prior-art audits.

## Selected findings

- **Context-dependent timing preference:** In the 32×16 XOR wrapper, the balanced context favored the word decoder by **49.328 ps** on average (three seeds), while a late-low-address context favored the row decoder by **45.960 ps**. In a separate 32×8 buffered test, corresponding mean advantages were **31.589 ps** for word and **37.360 ps** for row. These are **matched post-route setup-slack comparisons**, not security/power measurements.
- **Path mechanism:** Across the focused multi-seed study, **420** path records and **150** matched address comparisons showed different downstream timing sensitivity by address bit. The measured suffix includes wires, decoder/selection logic, storage-output path and capture effects; it is not a pure decoder arc.
- **Prediction limitation:** In the most realistic tested synthesized-RTL holdout (ring, serpentine and DMA address-generation functions; two widths and two seeds), the frozen predictor selected the better decoder in **9/12** cases. An always-word choice won **11/12**, and the two-placement selector also won **11/12**. The early model's mean improvement versus always-word was only **0.1275 ps**; no full implementation-time saving was established.
- **Evidence audit:** All **24** final routed checkpoints were rechecked using ODB/SDC/SPEF in OpenSTA; the target-read and whole-design setup winners matched in **12/12** comparisons. No full signoff is claimed.

## Current conclusion

The experiments support a **bounded, reproducible observation of context-sensitive decoder timing**. They do **not** support a general-purpose early decoder-selection algorithm better than a simple baseline, nor a strong standalone novelty or publication claim. This negative evaluation is important to deciding what to study next.

## Suggested reading order

1. [Negative results and failure classification](NEGATIVE_RESULTS_AND_FAILURES.md) — explicit failed scientific criteria, corrected CI errors, and final NO-GO.
2. [Full faculty technical report](M10_FACULTY_RESEARCH_REPORT_2026-11-05.md) — hypotheses, controls, numerical outcomes, and limitations.
2. [Final 12-case held-out comparison](../results/synthesized_rtl_holdout_pairs.csv) and [interpretation](SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md).
3. [Address-pin sensitivity mechanism](ORRAM_THREE_SEED_ADDRESS_SENSITIVITY_2026-11-05.md).
4. [Post-route physical evidence audit](M5_POSTROUTE_INTEGRITY_2026-11-05.md).
5. [Literature and novelty assessment](M9_LITERATURE_AND_NOVELTY_REVIEW_2026-11-05.md).
6. [Completed workflow-run evidence](EXPERIMENT_EVIDENCE_INDEX.md).

## Questions for faculty feedback

1. Is the measured context dependence a useful scientific contribution on its own, or primarily an expected consequence of path maxima and known decoder structures?
2. Is there a stronger causal experiment or alternative hypothesis that would justify a novel method, rather than more hand-designed timing cases?
3. If continuing, would pin-/slew-/load-aware timing sensitivity plus an uncertainty-based abstention policy be a worthwhile method to test on independent RTL and a second library?
4. What research connection, if any, is most promising between this physical-design analysis and hardware-security problems? **No side-channel leakage has been measured in the current project.**

Original raw reports, logs and checkpoints are linked in [the evidence index](EXPERIMENT_EVIDENCE_INDEX.md). This briefing is a guide to the preserved work, not a substitute for those records.
