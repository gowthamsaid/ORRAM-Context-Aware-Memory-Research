# Stage 2 — Registered Physical Integration: first four routed controls

**GitHub Actions:** [run 42071621647](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42071621647) (all jobs passed). 
**Raw artifact:** [registered-integration-smoke-42071621647](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42071621647/artifacts/13435662967).

## Purpose
Test whether changing **physical address-arrival paths** in registered surrounding circuitry can alter which of two *identically functional* 32×8 ORRAM implementations has better **whole-design post-route setup slack**, without substituting input arrival SDC values.

The two wrapper versions are functionally identical. The late-low variant contains four additional BUF_X1 gates on each of address bits 0 and 1; these gate instances and their corresponding routed wires are retained, and the topology is no longer based solely on external timing budgets. Memory gate netlists are the previously validated same-interface row versus word decoder architectures.

## First completed results

| Surrounding circuit | Memory architecture | Extracted-SPEF read path arrival, ns | Post-route setup slack, ns | Path start → end |
|---|---|---:|---:|---|
| Balanced | Row | 0.622917 | 3.273390 | u_addrff_4 → u_capture_5 |
| Balanced | Word | 0.603694 | 3.292158 | u_addrff_1 → u_capture_6 |
| Late low-order bits | Row | 0.660943 | 3.235625 | u_addrff_1 → u_capture_0 |
| Late low-order bits | Word | 0.688698 | 3.207700 | u_addrff_0 → u_capture_0 |

- Balanced: **word beats row by 18.768 ps**, below the preregistered 20 ps threshold.
- Late low-order: **row beats word by 27.925 ps**.
- The **raw winner reverses** across the two contexts, but *does not clear the preregistered two-context >20 ps gate*.
- Both architectures were routed with the same fixed die/core and SDC for each context. Actual cell-level timing differs because physical placement and gate connectivity are different.
- Routed SPEF sizes 623,493; 630,772; 639,354; and 629,655 bytes. OpenROAD extraction and SPEF re-import completed; thus these are routed-parasitic timing reports, not just placement RC estimates.
- The complete-design worst path in all four cases is the intended address-register → capture-register read path.

## Why this is not a final research GO
1. The pinning of a 4 ns ideal common clock, omission of CTS and tapcells/power/signoff, and use of a synthesized-like flattened gate-level memory prevent signoff claims.
2. **All four implementations use deterministic global placement, not independent seeds.** The historical `-seed` parameter failed and was removed; a new workflow investigates supported `-random_seed` and verifies actual coordinate diversity.
3. Additional per-address buffer gates are a deliberately controlled integration perturbation; they are a valid feasibility experiment but not necessarily representative of surrounding optimized circuits.
4. The word architecture wins the balanced case by 18.768 ps, less than the predeclared 20 ps margin. Therefore this pilot does not satisfy the full statistical or engineering significance requirement.
5. No context-aware architecture-selection algorithm has been implemented, and no prior-work novelty comparison is established.
6. The empty `route_drc.rpt` file is **not** proof of DRC/LVS signoff. No signoff decks have been applied.

## Next gating experiment
Three independently perturbed GPL placements for each of four cases (12 physical implementations), compare means, sign consistency, and variance. Fail fast if the physical placement signatures do not differ or timing is invalid. Do not spend effort developing the selector before confirming an appropriate effect size and baseline.
