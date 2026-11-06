# M10 — Faculty briefing, slide narrative, and technical-defense guide

**Accompanies:** [complete research report](M10_FACULTY_RESEARCH_REPORT_2026-11-05.md).  
**Purpose:** faculty research assessment and constructive feedback, not a fabricated manuscript acceptance.

## One-page faculty briefing

**Working title:** *Context-Dependent Timing Sensitivity and Exploratory Architecture Selection for Standard-Cell Memories*

**Question.** Do the timing characteristics of the address-generation logic surrounding a standard-cell RAM change whether a row- or word-decoded ORRAM implementation is faster after physical design? If so, can the preferred decoder be selected before implementing both options?

**Methods.** Generate functionally matched 32×8 and 32×16 ORRAM alternatives; integrate registered address producers; perform matched placements, detailed routing and extracted-SPEF static timing; study per-input timing paths; freeze and test pre-placement selection rules on successively more distinct holdouts.

**Supported result.** An architecture ranking reversal was reproduced under controlled address timing contexts. The ORRAM per-address paths show a systematic, within-family timing asymmetry that helps explain why different launch bits dominate. The mechanism is not simply the decoder's nominal delay.

**Negative result.** A small prototype predictor looked promising on designed XOR/Gray contexts but selected only 9/12 winners in synthesized RTL holdouts, compared with 11/12 for always-word and 11/12 for dual-placement. Mean advantage over always-word was ~0.13 ps, not demonstrable optimization. Placement/route runtime measurements exclude calibration and do not establish end-to-end savings.

**Novelty check.** ORRAM already supports different decoder configurations. Its public OpenROAD roadmap explicitly calls for timing-guided choices based on external constraints; generic memory compiler characterization and architecture search predate this study. The current defensible contribution is controlled characterization and careful negative model evaluation, not a validated new optimization algorithm.

**Limitations.** Small artificial/application-inspired address producers; one standard-cell library/corner; no CTS, signoff PVT, power, DRC/LVS or IR/EM closure; physically extracted but non-signoff timing. Two-word-size and seed samples are not independent industrial benchmarks.

**Faculty feedback sought.** Is the underlying path-sensitive timing phenomenon a useful characterization contribution? Which prior method is closest? Should independent follow-on work target uncertainty-aware pin-delay models, more memory sizes, real workloads, or a different research question? Is this a suitable direction for a PhD project?

### Faculty conversation structure (10–15 minutes)

1. **Problem and motivation (1 min):** initial FIFO read-path physical timing research left causal questions unresolved; a controlled memory-generator comparison followed.
2. **Research hypotheses and setup (2 min):** show matched row/word memory wrappers, registered address logic, fixed SDC and routed SPEF.
3. **Core timing reversal (2 min):** 32×8 and 32×16 balanced vs late-low sign changes; call out 32×8 XOR's failure of the original 20 ps engineering threshold.
4. **Mechanism (2 min):** critical launch-bit switching; 420 path observations and 150 per-address same-output comparisons; explain what downstream suffix does/does not isolate.
5. **Prediction hypotheses (2 min):** freeze before physical data; compare simple XOR heuristic and Liberty-timed precursor; avoid conflating their distinct test sets.
6. **Synthesized RTL negative result (2 min):** present 9/12 vs 11/12 always-word, regret and measured stage-cost exclusions.
7. **Novelty, limitations, faculty questions (2–4 min):** OpenROAD issue #9392, no algorithm novelty yet; invite advice on what to pursue.

## Ten-slide suggested structure

| Slide | Title | Evidence/figure to show |
|---|---|---|
| 1 | Research question and contribution status | 1-sentence question; bounded observation vs unproven algorithm |
| 2 | From FIFO read path to ORRAM | Timeline, explicitly separate two repositories/questions |
| 3 | Controlled row- vs word-decoded RAM experiment | Two matched block diagrams around identical address producer |
| 4 | Extracted postroute timing ranking reversal | 32×16 balanced and late-low margins with seeds |
| 5 | Critical-path decomposition | Launch FF → address XOR → RAM decoder → select/storage/output → capture FF |
| 6 | Address-bit sensitivity | A0/A1 vs A3/A4 sign matrix; show 3 seeds but explain correlated cases |
| 7 | Pre-placement selector idea and freeze protocol | Model formula, training vs new contexts |
| 8 | Prospective synthesized RTL outcomes | Ring/serpentine/DMA 9/12, always-word 11/12; three errors |
| 9 | Validity, runtime, novelty | Cost chart, missing signoff, overlap with OpenROAD roadmap |
| 10 | Open research questions and feedback | Ask 3 specific questions; leave next model deferred |

Do not insert photographs or rendered layout images without their original artifact provenance; slides should use actual timing-data figures.

## Technical defense — fifteen questions and grounded answers

**1. What were you trying to prove?**  
First that context-dependent address arrivals affect the *relative* routed timing of functionally equivalent ORRAM implementations. Separately, that an early selector could avoid expensive dual implementation.

**2. Why change from the FIFO hypothesis?**  
The initial indexed-versus-shared FIFO experiments did not conclusively attribute the observed read delay to selective sharing. A generator providing two already supported memory implementations offered a cleaner paired comparison. The change was based on evidence, not just an attempt to report a positive result.

**3. What did you personally implement?**  
A versioned experiment harness, logic wrappers, scripts for OpenROAD/OpenSTA postroute and SPEF extraction, path decomposition, synthesis/equivalence, predictor calculation, holdout scoring and computational-cost analysis. Be ready to demonstrate each exact script and tool log; do not overclaim manual RTL contribution by conflating ORRAM author's source with yours.

**4. Are row and word decoders your invention?**  
No. Both are available in ORRAM. The investigation concerns their *integration timing sensitivity* and whether the system can choose efficiently.

**5. What is the clock setup?**  
Nominal 4.0 ns ideal clock with defined input/output delays, setup/hold uncertainty and output loads; no routed CTS. This is exploratory timing, not full clock-tree signoff.

**6. What does a positive row-minus-word slack difference mean?**  
Row has *more* setup margin and thus is preferred for that particular constrained physical pair. It is not a frequency claim unless constraints are translated carefully.

**7. Were the comparisons made on identical functions?**  
Within each address context, row/word RAM have matching functional interfaces and identical address-producer RTL. Across different contexts, address transformations may differ; we compare architecture alternatives within context, not product-equivalent cross-context designs.

**8. Why multiple seeds?**  
To check whether a direction repeats under placement perturbations. Seeds are correlated repetitions, not independent real applications, and cannot alone provide statistically general results.

**9. Did you really use parasitics?**  
Yes. The routed physical flows produced SPEF after detailed routing; the timing mechanism recheck reread the saved SPEF and associated ODB/SDC. The study still omits signoff corners and CTS.

**10. How was memory input delay measured?**  
Within a full FF-to-output-capture timing path forced through a physical address-driver output, subtract the boundary-driver arrival from capture D arrival. It is a path-specific downstream suffix, including surrounding physical effects, not a standalone memory timing arc.

**11. What is the strongest evidence of reversal?**  
The three-seed 32×16 XOR contexts: mean word advantage ~49.328 ps for balanced, then mean row advantage ~45.960 ps for late-low. The analogous 32×8 balanced XOR experiment failed the predefined 20 ps mean-margin threshold.

**12. How does the predictor work?**  
Combine a pre-placement registered address-cone arrival estimate with architecture-specific memory-side suffix timing from an earlier characterized reference, then compare the maximum estimated arrival across address bits. Reference characterization did use both architectures once.

**13. How did you prevent tuning on holdouts?**  
Archived predictions before new physical runs, scored all cases including failures, and kept calibration separate from new holdout labels. Later model versions used new holdout families, so percentage figures are not a head-to-head test set.

**14. Why is the algorithm NO-GO despite 9/12 correct?**  
Always-word achieved 11/12 on the same synthesized RTL sample, with essentially no mean timing benefit from the predictor. No full amortized compute-speedup was established. Correct prediction count alone is insufficient.

**15. Is the work publishable?**  
Not yet as a novel efficient selector. A bounded characterization note or reproducibility benchmark may have educational/faculty value, but publication potential and novelty must be judged by specialists and stronger independent evidence.

## Faculty feedback checklist

- [ ] Confirm significance of context-sensitive row/word timing and what is genuinely nontrivial.
- [ ] Check overlap with OpenROAD RAM feature tracker #9392 and any earlier timing-driven physical optimization.
- [ ] Critique the downstream timing suffix and the limited ideal-clock model.
- [ ] Recommend a feasible next research question or advise switching direction.
- [ ] Decide whether an independently conducted follow-up could become publication-worthy.
- [ ] If a recommendation letter is requested, supply an up-to-date CV, transcript, concise research brief, program deadlines and supporting statements. No promise or assumption of a strong letter.

## Appropriate PhD research résumé entry

**Independent VLSI/EDA Research — Context-Aware Standard-Cell Memory Timing (OpenROAD, ORRAM, OpenSTA, Yosys, Python)**

- Investigated context-dependent timing rankings between row- and word-decoded standard-cell memories using registered address RTL, matched physical design experiments and extracted-parasitic STA.
- Characterized critical-path switching and per-address delay sensitivity across 32×8/32×16 configurations, multiple placement seeds and controlled address-generation contexts.
- Developed and prospectively evaluated pre-placement architecture-choice models on synthesized RTL, documenting timing regret, runtime overhead and limitations against baseline approaches.

Avoid phrases such as *published*, *novel optimized selector*, *signoff clean*, *proven 83% accuracy in general*, or *improved runtime* without new evidence.
