# Approved research closeout sequence — M5, M9, M10

**Decision:** Pause all second-generation algorithm implementation (M6–M8). Preserve all previous predictor holdout failures and do not retrain on scored test cases.

## M5: physical timing and evidence validity

First independently verify archived SDCs, SPEF presence, paired constraints, launch/capture paths, targeted read setup vs whole-design worst setup, route checks and limits of signoff. **Preliminary serialized-artifact audit**: [successful run 42144508832](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42144508832). Verified 24 physical architecture artifacts, 12 matched pairs, and **12/12 same architecture winner for both targeted and overall worst setup slack**. The row and word SDC texts differ only in the auto-generated comment timestamp, as established by [diff run 42144434576](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42144434576). This is not a substantive constraint discrepancy.

**Open audit item:** The archived `check_setup.rpt` files contain no text. Consequently, serialized artifacts by themselves do **not** prove that all intended endpoints were constrained. Reopen actual routed OpenDB, reread each matching SDC and SPEF, and run explicit post-route `check_setup -verbose` before M5 can be called complete. Full CTS, power, corner sweeps, IR/EM, DRC/LVS signoff remain out of scope; report limitations rather than invent signoff.

## M9: literature and novelty

Independently assess ORRAM's paper and implementation claims, OpenROAD roadmap, OpenRAM, published memory characterization and timing-aware architecture selection. Create a dated source-by-source matrix; record what the existing `row|word` option already supports, what the present study adds, and what **cannot** be claimed as a unique method. A prospective original predictor is **not** a completed contribution. Use the negative synthesized RTL holdout as a direct limitation.

## M10: faculty-facing research package

Prepare a coherent, versioned technical report tracing five stages: original FIFO indexed-vs-shared read timing hypothesis; width/depth and fanout effects; detailed cell/net mechanism audit and unproven selective duplication; pivot to ORRAM row/word context-dependent ranking; frozen predictor trials, negative generalization and cost. Include figures, exact workflows, reproducibility guide, one-page executive brief, 10–15-minute slide outline, project-defense questions and a concise research CV description. Separate proposed future work from verified findings.

## Faculty feedback and recommendation planning

First share the honest technical report with faculty and invite critique on methodology, novelty and sensible extensions. Follow the research discussion with a **separate and timely** recommendation-letter request for Fall 2027 programs, including actual deadlines and supporting application materials. Do not delay recommendation requests until the research is publication-ready or after university deadlines. Once feedback arrives, decide whether a substantially new predictor method warrants investment.

**Scope discipline:** the original FIFO MS technical paper and this ORRAM independent study are distinct projects. Neither should be misrepresented as a published paper, validated full-chip signoff, or a proven general efficient optimization algorithm.
