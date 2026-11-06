# Research continuation checkpoint — November 5, 2026

This file records the working state after the preceding ChatGPT conversation reached its length limit. It distinguishes confirmed GitHub artifacts from research goals, and is intended to make future handoffs auditable.

## Repositories and separation
- Original completed FIFO portfolio: `gowthamsaid/FIFO-RTL-to-GDS` (public). Its existing 8x16 / 32x32 M.S. technical-paper baseline must remain unchanged.
- FIFO read-path physical-design experiments: `gowthamsaid/FIFO-ReadPath-Research` (private). Historical five-seed width/depth experiments and mechanism audit archived. The detailed seed-1 STA audit showed cell arcs dominate selected paths; selective decoder sharing has **not** passed its causal mechanism GO gate.
- Current research feasibility study: `gowthamsaid/ORRAM-Context-Aware-Memory-Research` (private). This repo is the current focus.

## Scientific hypothesis
Can physical timing context of enclosing logic change which same-interface ORRAM row-/word-decoder memory implementation is preferable, and can an inexpensive early physical predictor select a better candidate than an isolated, context-blind baseline?

### Completed evidence
1. Isolated boundary feasibility: [Actions 42053883466](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42053883466). Demonstrated limited SDC-context rank reversal; not itself evidence of whole-chip optimization.
2. Timing model audit: [Actions 42066620647](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42066620647). Found unchanged ORRAM isolated output-path time despite a 0.005–5 pF load sweep. This is a model limitation, not a proof loading is irrelevant.
3. Registered physical pilot: [Actions 42071621647](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42071621647). Completed matched top-level routing and SPEF re-import; one deterministic placement showed rank reversal but did not fully clear the 20 ps two-context gate.
4. Three independent placement seeds: [Actions 42074091105](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42074091105). Verified different placed DEF coordinates for seeds 11, 23, 37 in each architecture/context and valid routed SPEF. Mean row-minus-word postroute setup slack: balanced -31.589 ps (word wins), late-low +37.360 ps (row wins). Every seed in each context shows the same direction.
5. Held-out late-high negative control: [Actions 42074519388](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42074519388). Three seeds, word wins, mean row-minus-word -34.707 ps. Three physical placement signatures per architecture.
6. Early-placement selector baseline: [Actions 42076289314](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42076289314). Workflow reuses frozen archived twelve physical implementations; all audit checks pass. A selector choosing the candidate with the better placement-stage register-to-register slack matches the postroute oracle in 6/6 balanced/late-low pairs; mean gain over blind word choice +18.680 ps; mean oracle regret zero. This is a **baseline evaluation**, not a novel method or proof of generalization.

### Current scientific decision
- **GO for continuing a bounded feasibility study**. Genuine context-dependent ranking reversal persists after three placement variations under the pinned exploratory flow.
- **NO-GO for claiming novel algorithm, generalized cross-design benefit, publication-quality result, or signoff.** Only one 32x8 memory size; buffer-chain interventions are artificial; ideal clock/no CTS, limited corner/power/signoff studies; selector currently physically places both candidates (unproven low overhead).
- Do **not** substitute FIFO results for ORRAM results; the projects ask different questions.
- Avoid confirmation bias: the late-high case was a deliberately chosen negative control. It is not a random population of independent systems.

## Next milestones
- Extend the early-placement selector score to held-out late-high data, with a frozen rule and no retuning. Compare to a word-only baseline and oracle; count correct predictions and compute regret per seed/context.
- Verify paired physical checks including start-/end-point constraints and whole-design worst setup vs targeted read path, matching true design constraints and no unconstrained endpoints.
- Test an additional memory size or a truly independently generated surrounding logic context as a **generalization gate**. Predeclare selection threshold, compute budget, and accept a null result.
- Profile the amount of implementation work needed for early selection versus a baseline, including whether parallel partial placement beats simply evaluating both full routes.
- Read prior art: ORRAM's architectural choices and prior context-aware physical/timing optimization; define a narrow distinguishing method *before* any paper claims.
- Inspect DRC/LVS, CTS, and signoff feasibility separately; existing results do **not** constitute tapeout-grade signoff.
- Ask user for local OpenROAD involvement only if CI cannot perform an indispensable step. Report blockers with full commands and required artifacts.

## Chat instruction
The user requests continued execution of GitHub-supported milestones without repeated prompting, stopping at indispensable local OpenROAD work, and discussion of GO/NO-GO only after meaningful feasibility gates. Do not describe any workflow as complete unless its GitHub run has reached a successful conclusion. Preserve raw reports, negative results, controls, and provenance.


## Updated continuation after synthesized RTL generalization milestone — November 5, 2026

**Current controlling result:** [Synthesized RTL generalization and implementation cost final report](SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md).

- Yosys/ABC Nangate-mapped RTL generated from three application-inspired address producers (circular ring, serpentine tile, DMA stride). Functional mapped combinational logic passed SAT equivalence for all three source modules. [Frozen producer timing and choices, run 42138305712](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42138305712).
- [Postroute matched physical run 42139114830](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139114830) passed for 32x8 and 32x16, two physical seeds each, both decoder architectures, using unchanged pre-registered predictions.
- [Frozen scoring and timing-cost run 42139806379](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139806379) passed. Predictor **9/12 correct**, dual-placement selector **11/12**, and blind word decoder **11/12**; predictor mean regret **2.987 ps**, max regret **20.681 ps**, mean gain over blind word **+0.1275 ps**.
- Measured implementation-stage runtime (seconds per case): blind word 14.642, selected candidate 14.499, dual placement 15.853, two complete routes 28.749. These are Docker stage wall times **excluding calibration and prediction setup**. No end-to-end speedup was demonstrated.
- A zero-terminal ground placeholder created by synthesis was safely removed from the OpenDB routing copy before physical implementation; connected power/ground nets were explicitly preserved.
- **Milestone closed as complete. Scientific GO:** address-context ranking reversal and mechanism-supported sensitivity. **Algorithmic NO-GO:** these results do not show a reliable or cheaper general-purpose predictor. Do **not** revise the frozen choices on these observed labels and present them as new holdouts.
- Faculty report can fairly emphasize transparent experimental method and original negative results, but should not advertise a published or validated efficient EDA tool.

The next truly separate algorithm-development experiment must include a richer width-/slew-/load-sensitive memory timing model and independent held-out address RTL, not additional unreported retuning of this completed dataset.
