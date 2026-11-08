# Experiment timeline, artifacts and evidence

**Purpose:** Enable a reviewer to verify the claims without opening every workflow or guessing which experiment is the latest. These are original successful **GitHub Actions run IDs**, not merely workflow definitions. Runs preserve context and logs; downloadable artifacts have finite retention and may eventually expire.

**All runs belong to:** [ORRAM-Context-Aware-Memory-Research](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research). **Flow scope:** Nangate45 typical corner, controlled physical wrappers, ideal clock, routed parasitics, with additional qualifications in the cited stage reports.

## Research progression

| Phase | Evidence / reported result | Original successful run | Technical notes |
|---|---|---|---|
| 1. Initial isolated boundary study | Row and word generator alternatives differ structurally; initial timing-context screen | [42053883466](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42053883466) | [Feasibility results](FEASIBILITY_RESULTS_2026-11-05.md) — **not** by itself a full integrated timing finding |
| 2. Registered wrapper pilot | Physically integrated address producer + output capture; initial directional preference | [42071621647](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42071621647) | [Stage 2](STAGE2_ROUTED_INTEGRATION.md) |
| 3. Buffered wrapper multi-seed | 32×8: balanced word +31.589 ps; late-low row +37.360 ps | [42074091105](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42074091105) | [Bounded physical feasibility](FINAL_FEASIBILITY_GO_NO_GO_2026-11-05.md) |
| 4. Delayed-high control | 32×8: word +34.707 ps mean | [42074519388](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42074519388) | Controls for address position |
| 5. XOR wrapper 32×16 | Balanced word +49.328 ps; late-low row +45.960 ps | [42078118831](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42078118831) | Also see [32×8 XOR margin failure](FINAL_FEASIBILITY_GO_NO_GO_2026-11-05.md) |
| 6. Routed timing mechanism | Matched FF-to-output path decomposition, launcher differences, routing/cell effects | [42126639893](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42126639893) | [Mechanism report](ORRAM_TIMING_MECHANISM_MILESTONE_2026-11-05.md) |
| 7. Address-pin sensitivity | 420 downstream path records and 150 matched address comparisons | [42128929892](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42128929892) | [Multi-seed sensitivity](ORRAM_THREE_SEED_ADDRESS_SENSITIVITY_2026-11-05.md) |
| 8. Simple frozen model | 9/12 on controlled XOR-context holdout | [42131694295](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42131694295) | [Early predictor](FROZEN_PREPLACEMENT_PREDICTOR_HOLDOUT_2026-11-05.md); **different test set** |
| 9. Liberty-timed pre-placement model | 10/12 on counter/Gray address contexts | [42133441297](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42133441297) | [Liberty predictor](LIBERTY_PREPLACEMENT_PREDICTOR_HOLDOUT_2026-11-05.md); **different test set** |
| 10. Freeze synthesized RTL model | Source and predictor decisions recorded before routing | [42138305712](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42138305712) | [Frozen source producers](../rtl_applications/) |
| 11. Final synthesized-RTL physical holdout | 24 routed implementations, 12 architecture pairs | [42139114830](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139114830) | Original ODB, SPEF and timing reports |
| 12. Final scoring / cost | Frozen model **9/12**, blind word **11/12**, two-placement **11/12** | [42139806379](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139806379) | [Final evaluation](SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md); [checked-in derived CSV](../results/synthesized_rtl_holdout_pairs.csv) |
| 13. Physical integrity | 24/24 reread with ODB/SDC/SPEF, targeted/global setup winner 12/12 | [42155987361](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42155987361), [verification 42156452762](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42156452762) | [M5 scope and limitations](M5_POSTROUTE_INTEGRITY_2026-11-05.md) |
| 14. Literature and novelty | Existing RAM architecture-selection and timing optimization prior work limits novelty | — | [M9 prior-art review](M9_LITERATURE_AND_NOVELTY_REVIEW_2026-11-05.md) |

## Most important results to inspect

**Timing reversal:** [32×16 XOR physical flow](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42078118831) and the corresponding [bounded feasibility interpretation](FINAL_FEASIBILITY_GO_NO_GO_2026-11-05.md).

**Timing mechanism:** [address-suffix evidence run](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42128929892) and [the method and scientific caveats](ORRAM_THREE_SEED_ADDRESS_SENSITIVITY_2026-11-05.md).

**Unsuccessful selector generalization:** [frozen predictor run](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42138305712) precedes the [physical holdout](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139114830) and [score](https://github.com/gowthamsaid/ORRAM-Context-Aware-Memory-Research/actions/runs/42139806379). Do not treat 9/12 from two **different** holdout datasets as a pooled validation score.

**Integrity:** [M5 final recheck](M5_POSTROUTE_INTEGRITY_2026-11-05.md) explicitly distinguishes a scoped experiment audit from clock-tree, PVT and physical signoff.

## Workflow source map

| Purpose | Workflow source |
|---|---|
| Generate row/word RAM and initial functional/structural screen | [feasibility.yml](../.github/workflows/feasibility.yml) |
| Run three-seed physically integrated experiments | [multiseed-integration.yml](../.github/workflows/multiseed-integration.yml) |
| Test XOR context at 32×16 | [cross-size-xor.yml](../.github/workflows/cross-size-xor.yml) |
| Audit memory address-pin sensitivity from routed checkpoints | [memory-input-multiseed.yml](../.github/workflows/memory-input-multiseed.yml) |
| Freeze synthesized RTL and predictor | [freeze-synthesized-rtl.yml](../.github/workflows/freeze-synthesized-rtl.yml) |
| Implement physical holdout | [synthesized-rtl-physical.yml](../.github/workflows/synthesized-rtl-physical.yml) |
| Score architecture choices and stage timing | [score-synthesized-rtl-holdout.yml](../.github/workflows/score-synthesized-rtl-holdout.yml) |
| Reopen post-route ODB/SDC/SPEF and check timing | [m5-postroute-recheck.yml](../.github/workflows/m5-postroute-recheck.yml) |

Earlier diagnostics and intermediate exploration workflows remain tracked for reproducibility, but the above are the principal reader entry points.

## Evidence retention

The **checked-in** [`results/synthesized_rtl_holdout_pairs.csv`](../results/synthesized_rtl_holdout_pairs.csv) is a compact transcription of the published final 12-pair scoreboard, not replacement for the routed raw reports. Earlier stage-level [JSON result gates](../results/README.md) are also checked in. Complete per-case OpenDB, DEF, SPEF, log and timing bundles reside in downloadable Actions artifacts; GitHub's artifact retention window applies.

When reviewing a claim, prefer the dated report **plus** its linked successful run; do not infer missing physical data from an absent or expired artifact.
