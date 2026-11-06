# M10 — Faculty research report: Context-Dependent Timing of Standard-Cell Memories and Early Architecture Selection

**Status:** Faculty-review draft based on completed exploratory work. **Not** a published manuscript.  
**Date:** November 5–6, 2026.  
**Project:** Independent VLSI / Electronic Design Automation experimental study.

## Abstract

The physical timing of a standard-cell memory integrated into a surrounding circuit can depend on which address signals arrive late, because different memory decoder structures and physical routes have nonuniform timing sensitivity. This study investigates that relationship using OpenROAD's ORRAM row- and word-decoded memory alternatives, Nangate45, Yosys, OpenSTA, and routed parasitic extraction. Controlled registered address-generation wrappers were built around physically comparable 32×8 and 32×16 memories. An initial difference in preferred architecture was subsequently reproduced under placement perturbations, then investigated through cell/net-path decomposition and memory-address-boundary suffix measurements. An exploratory pre-placement decoder selector was preregistered and evaluated on multiple increasingly realistic holdouts. The strongest design-dependent reversal was reproducible in selected XOR address-generation contexts, yet the final synthesized-RTL holdout showed that the selector achieved only 9/12 correct choices while always selecting the word architecture achieved 11/12. Stage-level timing provided no demonstrated end-to-end speedup after calibration overhead. The current contribution is a reproducible, hypothesis-driven timing-characterization and model-generalization case study, not a validated novel architecture-selection algorithm. Future directions should be determined with faculty input.

## 1. Origin and separation from the FIFO technical paper

The earlier **FIFO RTL-to-GDSII** portfolio project implemented two synchronous FIFOs (8×16 and 32×32) and gathered synthesis-to-routing layout, timing and area evidence in a public repository: https://github.com/gowthamsaid/FIFO-RTL-to-GDS. Its Rutgers M.S. technical paper is separately titled **“Comparative RTL-to-GDSII Implementation and Physical Design Analysis of Synchronous FIFOs Using OpenROAD.”**

The research extension began with an attempted FIFO read-path timing question: could an indexed read or shared decoder provide an advantage in timing and area, and could any apparent speedup be identified as a causal effect rather than placement noise? The distinct private FIFO investigation repository is `gowthamsaid/FIFO-ReadPath-Research`. Its experimental history included width/depth comparisons, multiple seeds and a cell-arc critical-path audit; selective decoder sharing **did not clear a causal timing-mechanism gate**. Those outcomes were not renamed ORRAM or counted as independent ORRAM proof.

The shift to ORRAM was motivated by the desire for a cleaner, parameterized set of *functionally matched architecture choices* already supported by an established open-source memory generator, allowing a more controlled timing-context experiment. This was a **hypothesis change**, not proof that the FIFO result had succeeded.

## 2. Questions and explicitly separate hypotheses

**H1, completed limited observation:** With row and word ORRAM alternatives held functionally equivalent *within the same wrapper*, can changing the surrounding registered address-generation context reverse which alternative has better routed setup slack?

**H2, mechanism:** Is such a reversal consistent with address-bit-specific downstream timing paths and changes in the actual worst launch/endpoint?

**H3, exploratory predictor:** Can one calibration and pre-placement timing of a new address producer predict the preferred architecture without physically implementing both **new** candidate memories?

**H4, practical cost:** Does the predictor beat blind or dual-placement baselines in accuracy, regret and *total* implementation effort?

The data support **H1 and bounded H2**, show conditional feasibility but weak generalization for **H3**, and do **not** support a practical speedup or superior optimizer for **H4**.

## 3. Methods

**Architecture and flow.** ORRAM provides row and word decoder choices; neither is a proposed new memory topology. Standard-cell memories were generated with an explicitly pinned OpenROAD flow and Nangate45 typical Liberty. Register-based address producers fed an ORRAM memory, whose outputs were captured in output flip-flops. The surrounding wrapper, width, source mapped logic, constraint intent, and placement-seed choices were matched within each row–word pair. Original placement and routing checkpoints, SDC, physical layout and SPEF were preserved. Timing was compared from registered address launch points to output capture registers, with separate checks of whole-design worst setup paths. No new clock tree was constructed; the clock model was ideal.

**Physical timing metric.** Let \(S_{a,c,s}\) be postroute setup slack for architecture \(a\), context \(c\) and seed \(s\). Paired difference is \(\Delta S_{c,s}=S_{\mathrm{row},c,s}-S_{\mathrm{word},c,s}\), positive favoring row and negative favoring word. For prediction, oracle regret is \(S_{\mathrm{oracle}}-S_{\mathrm{selected}}\), not a universal physical delay reduction.

**Pin-sensitive mechanism.** Because the structural wrapper is flattened, we used the final address-logic cell's output pin feeding each RAM address bit as a physical boundary. The downstream suffix was the arrival at a named output capture D pin minus the boundary Z-pin arrival within the same OpenSTA path. That suffix includes input wire, decoder, selection, storage/output and capture-net delay; it is not a standalone RAM Liberty arc.

**Prospective controls.** Model outputs were frozen in artifacts *before* generating new matching routed candidate outcomes. Development, seed repetitions and hand-designed test contexts are correlated; we do not treat their observed classification percentages as population-level accuracy estimates.

## 4. Evidence and experiment chronology

| Research step | Verified outcome | GitHub Actions run |
|---|---|---|
| Initial isolated feasibility | Context-dependent preference in isolated boundary constraints; not full-system claim | 42053883466 |
| Timing-model validation | Suspicious response to output load; reason not to overinterpret isolated timing data | 42066620647 |
| Registered physical pilot | Routed top-level wrapper and SPEF timing; preliminary directional reversal | 42071621647 |
| Multi-seed physical repetition | 32×8 balanced word advantage ~31.589 ps; late-low row advantage ~37.360 ps (three seeds) | 42074091105 |
| Deliberate delayed-high control | Word advantage ~34.707 ps mean (three seeds) | 42074519388 |
| Dual-placement baseline | One group 9/9 and XOR groups 12/12 correct against own routing oracle; needs two placements for every candidate pair | 42077401815; 42079182085 |
| XOR structural address tests | 32×8 reversal with a 20 ps criterion failure in balanced case; 32×16 reversal with ~49.328 ps word balanced and ~45.960 ps row late-low mean advantages | 42078118809; 42078118831 |
| Detailed physical delay decomposition | Forty FF-to-output paths decomposed into XOR, RAM decoder/selection/storage and capture regions; mechanism consistent, not strictly causal | 42125976002; 42126639893 |
| Three-seed memory-address suffix study | 420 paths, 150 paired address comparisons: low-order A0/A1 row faster, high-order A3/A4 word faster within tested cases | 42128929892 |
| Simple pre-placement predictor | Frozen before holdouts; 9/12 correct, mean regret ~0.776 ps, gain over always-word ~3.961 ps on XOR-context holdout | 42130789146; 42130967413; 42131694295 |
| Liberty STA on manually built address producers | 10/12 correct on counter, Gray encode/decode; failure on 32×8 Gray encoder | 42132385070; 42132736843; 42133441297 |
| Synthesized behavior-level RTL study | Three separately synthesized and formally equivalent address producers; 24 routed implementations; predictor 9/12, blind word 11/12, dual-placement 11/12 | 42138305712; 42139114830; 42139806379 |
| M5 serialized integrity pass | 24/24 artifacts and 12/12 pairs audited; targeted and overall setup winners agree; SDC differences only autogenerated timestamps | 42144434576; 42144508832 |

Each run can be opened at:
`https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/<RUN_ID>`.

## 5. Principal observations and negative findings

**Result A — context-sensitive preferred architecture.** Under the original 32×8 balanced case, word had ~31.589 ps mean setup advantage; with the late-low address context, row had ~37.360 ps mean advantage. The XOR-based 32×16 experiments showed an even clearer sign change: balanced word ~49.328 ps mean advantage and late-low row ~45.960 ps. The analogous 32×8 XOR balanced condition did **not** meet a 20 ps mean-margin acceptance requirement; its actual ~18.098 ps advantage was retained rather than dismissed.

**Result B — mechanism.** The dominant launch address bit changed with context and decoder. In the suffix analysis across two widths, two contexts, and three seeds, per-address comparison on matched capture registers showed strong low-address versus high-address preference differences within this particular design family. This supports a path-dependent timing mechanism, but load, slew, routing and endpoint sensitization vary.

**Result C — predictor limitation.** The last and most realistic set used Yosys-mapped RTL functions (24-entry ring translation, serpentine tile, DMA stride). Frozen predictor accuracy was **9/12 (75%)**, compared with **11/12 (91.7%)** for the always-word baseline and **11/12** for the two-placement selector. The predictor's maximum regret was **20.681 ps**; mean regret **2.987 ps**; mean gain over always-word **0.1275 ps**, not a useful demonstrated benefit. Three of its errors came from the serpentine tile motif.

**Result D — implementation cost.** Mean sequential placement and route wall times: 14.642 s for one blind word, 14.499 s for predicted one candidate, 15.853 s for two placements and one route, and 28.749 s for both full routes. These are *stage-level* measurements; reference calibration and additional model generation are not included, so a net cost improvement has **not** been established.

**Result E — integrity and limits.** The preliminary M5 archive audit checked 24 artifacts and 12 matched pairs with 12/12 agreement between targeted read and overall worst-setup winner. Row/word SDC source differences were only write-time comments. An empty serialized setup-check report prompted a new explicit postroute OpenSTA `check_setup -verbose` rerun. This report must be amended with the precise recheck verdict before treating M5 as closed.

## 6. Related work and novelty

The underlying ORRAM compiler and architecture controls are introduced by Louie et al. (2026), arXiv:2607.12244. OpenROAD issue #9392 explicitly anticipates timing-guided choice of RAM configurations using external circuit constraints, strongly constraining any novelty claim for our selector. OpenRAM, DFFRAM, OpenGCRAM and OpenOpt demonstrate prior memory generation, timing characterization, design-space exploration and reduced-cost model-based optimization. A full source-by-source analysis is in [M9](M9_LITERATURE_AND_NOVELTY_REVIEW_2026-11-05.md).

**Novelty verdict:** The current result is a credible *independent EDA characterization and predictor evaluation*, including a negative generalization result. It is **not** a newly validated optimizer, unique memory compiler, published algorithm or first demonstration of context-aware memory selection.

## 7. Limitations

- Custom small memories and application-inspired address generators, not a population of industrial SoC designs.
- Same Nangate45 typical corner; no full PVT sweep or independent PDK replication.
- Correlated seeds and memory widths; no population confidence intervals.
- Ideal clock, no CTS, signoff DRC/LVS, IR/EM or power closure.
- The per-address suffix is not a standardized intrinsic memory arc, and routing/driver effects remain.
- Full model calibration cost omitted from stage-level runtime.
- Original FIFO causal decoder sharing hypothesis did not establish its desired mechanism and is not transmuted into an ORRAM success.

## 8. Questions for faculty and suggested follow-up work

**Scientific assessment:** Are the critical-address-path and address-sensitive decoder observations worth reporting as a characterization note even without a new selection method? Does #9392 or other timing-driven design-space research render the selection concept obvious?

**Method quality:** Is the preserved setup timing and physical-path mechanism adequate for a small standard-cell experiment? Should we prioritize a second PDK, more RAM depths or more external RTL?

**Possible future method, NOT claimed as implemented:** calibrated path/pin and width-sensitive memory timing libraries; independent modeled input slew/fanout; uncertainty and abstention policy; new prospective held-out circuits; runtime amortization and electrical/corner validity. These correspond to deferred M6–M8.

**Faculty request:** Feedback on the problem's research value, the methodological limitations, how to scope a credible next paper question, and possible independent study/PhD research direction. Recommendation letters should be requested separately with sufficient time before application deadlines.

## 9. Reproducibility and source ledger

Private project repo: https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research

Full evidence:
- ORRAM bounded feasibility and reversed contexts: [docs/FINAL_FEASIBILITY_GO_NO_GO_2026-11-05.md](FINAL_FEASIBILITY_GO_NO_GO_2026-11-05.md)
- Read-path mechanism anatomy: [docs/ORRAM_TIMING_MECHANISM_MILESTONE_2026-11-05.md](ORRAM_TIMING_MECHANISM_MILESTONE_2026-11-05.md)
- Multi-seed pin sensitivity: [docs/ORRAM_THREE_SEED_ADDRESS_SENSITIVITY_2026-11-05.md](ORRAM_THREE_SEED_ADDRESS_SENSITIVITY_2026-11-05.md)
- Frozen prospective heuristics: [docs/FROZEN_PREPLACEMENT_PREDICTOR_HOLDOUT_2026-11-05.md](FROZEN_PREPLACEMENT_PREDICTOR_HOLDOUT_2026-11-05.md)
- Frozen technology-library predictor: [docs/LIBERTY_PREPLACEMENT_PREDICTOR_HOLDOUT_2026-11-05.md](LIBERTY_PREPLACEMENT_PREDICTOR_HOLDOUT_2026-11-05.md)
- Final synthesized RTL and implementation-work study: [docs/SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md](SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md)
- Literature and novelty assessment: [docs/M9_LITERATURE_AND_NOVELTY_REVIEW_2026-11-05.md](M9_LITERATURE_AND_NOVELTY_REVIEW_2026-11-05.md)
- Source of frozen ABC-mapped RTL and equivalence: Actions 42138305712
- All 24 physical routed artifacts: Actions 42139114830
- All final prediction labels and implementation stage durations: Actions 42139806379
- M5 original-constraint equivalence: Actions 42144434576
- M5 archived physical audit: Actions 42144508832
- Postroute STA coverage audit: see [M5 audit](M5_POSTROUTE_INTEGRITY_2026-11-05.md) when completed.

## 10. Conclusion

The strongest defensible outcome is the demonstrated dependence of ORRAM decoder timing rank on address-arrival context in a limited standard-cell physical flow, backed by repeated matched routed experiments and a path-level physical explanation. A prospectively frozen architecture selector did **not** reliably outperform the blind word baseline on a later synthesized RTL holdout. We therefore propose the completed study for **faculty feedback as independent hypothesis-driven research** and defer further algorithm invention until the significance, novelty and next research question have been reviewed.
