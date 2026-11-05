# Prior-art and publication novelty gate — 2026-11-05

## Candidate research question
For a standard-cell-based ORRAM block embedded in registered address-generation logic, do different physical arrival patterns change which decoder implementation minimizes post-route setup delay, and can a cheaper early selector identify the winner before routing?

## Prior work verified
1. Louie, Nguyen, Liberty, Rovinski, **ORRAM: An OpenROAD-Integrated RAM Generator Using Standard Cells**, 2026, https://arxiv.org/abs/2607.12244 . This is the upstream generator under test, not an architecture invented here. Its `-decoder row|word` switch already produces both variants.
2. Official OpenROAD RAM generator documentation: https://openroad.readthedocs.io/en/latest/main/src/ram/README.html . Generator is experimental, includes both row and word decoders and multi-dimension configuration. 
3. OpenRAM, https://openram.org/ , is a mature open-source memory compiler framework providing timing/power characterization and ASIC integration.
4. OpenGCRAM / heterogeneous memory design exploration (2025/2026), https://arxiv.org/abs/2602.21278 and https://arxiv.org/abs/2507.10849 , already conduct memory architecture/design-space exploration against timing/area/power/workload measures.

## Novelty risk (not claiming exhaustive literature search)
The original ORRAM paper explicitly lists tighter OpenSTA-based **timing and power optimization of RAM configurations** as future work. Therefore, simply evaluating both `-decoder` options at placement time and choosing the larger slack is **not** a defensible standalone algorithmic novelty claim. The 9/9 selector result is a small experimental demonstration, not a discovery of a new optimization algorithm. Design-specific arrival variation can cause a maximum-of-paths crossover by construction.

## Minimum credible research-method advancement
A publishable *method* should preferably:
- Predict selection without fully placing **both** candidates, using an analytical per-address-arc/arrival sensitivity model, or reduce total compute at equal or better PPA.
- Be independently evaluated against the same-budget context-blind choice and existing placement-stage exhaustive search, with held-out logic, different word widths/word counts, different physical seeds, and ideally a second PDK.
- Measure selection regret, net run time, additional area, power, and whole-design rather than just an isolated read-path slack metric.
- Show non-trivial benefit after a realistic physical flow (CTS, parasitic extraction, signoff-correct constraints) without using padded fixed-delay buffer chains.
- Avoid assigning rigorous statistical confidence to 3 seeds or treating hand-picked contexts as random representative systems.

## Scope decision
Engineering feasibility may be GO even when the publication-novelty decision is NO-GO. If the honest answer is: context matters but placement of both choices is required, the correct result is an informative **characterization/EDA benchmark**, not a completed publishable algorithm.
