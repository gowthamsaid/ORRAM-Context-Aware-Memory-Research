# M9 — Literature and novelty assessment (November 5–6, 2026)

## Research question

Does address-generation context change the post-route timing preference between two standard-cell memory decoder architectures, and can a low-overhead predictor choose an architecture before the target memory alternatives are placed or routed?

## Source-by-source review (public, source-checked)

| Source | Established contribution | Relationship to the present work | Novelty constraint |
|---|---|---|---|
| Louie, Nguyen, Liberty, Rovinski (2026), *ORRAM: An OpenROAD-Integrated RAM Generator Using Standard Cells*, https://arxiv.org/abs/2607.12244 | Native OpenROAD standard-cell RAM generation with configuration, read selection, integration and OpenSTA characterization | We **use**, not invent, ORRAM and its row/word alternatives | Cannot claim invention of ORRAM, new RAM decoder or OpenSTA-timed standard-cell memory |
| OpenROAD RAM generator manual, https://openroad.readthedocs.io/en/latest/main/src/ram/README.html | Existing RAM configuration interface; officially experimental | Native integration and technology mapping are prior facilities | Merely measuring existing configuration options is characterization rather than a novel compiler |
| OpenROAD RAM feature tracker #9392, https://github.com/The-OpenROAD-Project/OpenROAD/issues/9392 | Public proposals explicitly discuss timing-guided decisions, STA comparisons of multiple RAM configurations, and incremental RAM substitution using external path/constraint information | **Most direct collision with our intended research direction** | An algorithm doing only that proposed operation is weak novelty without new method and demonstrated benefit |
| AUCOHL/DFFRAM, https://github.com/AUCOHL/DFFRAM | Standard-cell flip-flop/latch RAM compiler producing HDL, LEF, GDS and timing views | Memory generator precedent, physical verification context | Not a first standard-cell compiler |
| Guthaus et al., *OpenRAM: An Open-Source Memory Compiler*, https://escholarship.org/content/qt8x19c778/qt8x19c778_noSplash_b2b3fbbb57f1269f86d0de77865b0691.pdf | Custom-cell memory compilation and characterization across memory configurations | Characterizing memory delay is well established | No novelty in memory timing characterization alone |
| OpenRAM characterization docs, https://github.com/VLSIDA/OpenRAM/blob/stable/docs/source/characterization.md | SPICE-based timing/power tables including slew, load, setup/hold and clocked read paths | A reusable pin-/condition-sensitive timing model is familiar in memory compilers | A future model needs method-level originality, not just a Liberty timing table |
| Wang et al. (2025), *OpenGCRAM: An Open-Source Gain Cell Compiler Enabling Design-Space Exploration for AI Workloads*, https://arxiv.org/abs/2507.10849 | Area/delay/power characterization and memory parameter exploration | Memory design-space exploration exists; different device and architecture | Cannot claim first memory architecture search |
| Wang et al. (2026), *Heterogeneous Memory Design Exploration for AI Accelerators with a Gain Cell Memory Compiler*, https://arxiv.org/abs/2602.21278 | Application-/performance-metric-based heterogeneous memory choices | Adjacent context-aware exploration (not the same ORRAM decoder experiment) | Need distinguish workload/memory technology choice from path-arrival-conditioned decoder selection |
| Wang et al. (2026), *OpenOpt: An Open-Source SRAM Optimizer Based on Equivalent Circuit Model*, https://arxiv.org/abs/2606.09129 | Reduced-cost equivalent-circuit characterization for memory optimization | Model-driven efficient memory search is already actively studied | Efficiency, cost and accuracy need quantitative, prospective evidence; this work does not supply it |

## Contribution audit

### What our completed experiments do establish

1. **Controlled observation:** Under registered address producer RTL, word and row ORRAM variants can exchange timing rank when the surrounding address-generation cone changes. It is a genuine result for the studied configuration, but a plausible consequence of path maxima rather than inherently a new theorem.
2. **Physical mechanism:** Multiple seed checks with extracted routed parasitics show address-dependent delay and critical-path launch/endpoint switching. The focused per-address suffix study found row favorable for low bits and word favorable for high bits in this family. Downstream suffixes contain RAM selection, storage-output, input wire and captured-net effects, not just intrinsic decoder gate arcs.
3. **Prospective algorithms tested:** Heuristic 9/12, Liberty-timed manually built motifs 10/12, and separately synthesized application-inspired RTL 9/12, all with frozen predictions before matching physical experiments.
4. **Critical negative result:** On the independently synthesized three-motif holdout, blind always-word selection and dual-placement were both 11/12, surpassing the 9/12 predictor; average advantage over always-word was only +0.1275 ps with maximum predictor regret 20.681 ps.
5. **Cost:** Sequential per-case placement+route stage means were 14.642 s (blind word), 14.499 s (predictor-selected), 15.853 s (two placements, route chosen) and 28.749 s (route both). Reference training and pre-placement prediction overhead is excluded: no robust end-to-end speedup claim.

### What the present project cannot claim

- Not the invention of row- versus word-based decoder topology, ORRAM, OpenSTA, an SRAM compiler, application-aware optimization, or generic library timing characterization.
- Not a validated general-purpose pre-placement selector, not production timing closure, not proved cost reduction, not DRC/LVS/CTS/PVT signoff, not statistically demonstrated cross-workload effectiveness.
- Not a publication or accepted paper. A negative prospective model result does not invalidate the measured context-dependent timing phenomenon but limits the algorithm contribution.

## Novelty verdict and future research opportunities

**M9 COMPLETE — characterization / experimental-method contribution is credible; algorithmic novelty is currently inadequate for a strong publication submission.**

Most direct overlap: OpenROAD issue #9392 explicitly anticipates timing-guided RAM configuration selection using surrounding timing and replacement. A future defensible novelty claim must add a well-specified and externally validated method that goes beyond directly executing this roadmap, e.g., mathematically/physically modeled per-pin sensitivity with uncertainty and a cost-bounded abstention policy, compared prospectively with a two-placement budget, ideally with wider memory depth/width and external RTL. These are proposals **only**, not current achievements.

### Scope and review limitations

This is a *targeted* source review, not a systematic literature review over all EDA papers. Sources were read from primary public authors/project documentation and arXiv abstracts/text. It does not establish absolute novelty anywhere in the literature. Faculty feedback should challenge the novelty and identify closely related incremental timing-driven optimization techniques.

## Faculty-facing framing

**Accurate contribution sentence:** “I experimentally investigated how surrounding logic's address-path arrival pattern affects post-route timing preference among ORRAM decoder configurations, analyzed extracted-parasitic critical paths and address-pin sensitivity, and prospectively tested a low-cost architecture predictor. The experiments confirm timing-context sensitivity but the initial predictor did not consistently beat a context-blind baseline on synthesized RTL, motivating a more physically informed next research question.”

## References and direct links

- ORRAM paper: https://arxiv.org/abs/2607.12244
- ORRAM full-text view: https://academ.us/article/2607.12244/
- OpenROAD RAM manual: https://openroad.readthedocs.io/en/latest/main/src/ram/README.html
- RAM public feature tracker: https://github.com/The-OpenROAD-Project/OpenROAD/issues/9392
- DFFRAM: https://github.com/AUCOHL/DFFRAM
- OpenRAM characterization: https://github.com/VLSIDA/OpenRAM/blob/stable/docs/source/characterization.md
- OpenRAM paper: https://escholarship.org/content/qt8x19c778/qt8x19c778_noSplash_b2b3fbbb57f1269f86d0de77865b0691.pdf
- OpenGCRAM: https://arxiv.org/abs/2507.10849
- Heterogeneous memory exploration: https://arxiv.org/abs/2602.21278
- OpenOpt: https://arxiv.org/abs/2606.09129
