# Context-Aware Physical Timing of Standard-Cell Memories

**Independent VLSI / EDA research study using ORRAM, OpenROAD, Yosys and OpenSTA.** The study compares existing **row-decoded and word-decoded** standard-cell memory implementations under different surrounding address-generation circuits. It grew out of a separate [FIFO read-path research study](https://github.com/gowthamsaid/FIFO-ReadPath-Research); the original [FIFO RTL-to-GDSII implementation](https://github.com/gowthamsaid/FIFO-RTL-to-GDS) is maintained independently.

**Research question.** Can the logic that generates memory addresses change which decoder organization provides better *post-route setup timing*? If it can, is there a reliable way to predict the preferred architecture **before** physically implementing both choices?

**Completed exploratory study (November 2026).** The experiments found **context-dependent reversals in timing preference** for certain matched row/word implementations. However, the final pre-placement architecture predictor chose the best option in only **9 of 12** synthesized-RTL cases, versus **11 of 12** for a simple always-word baseline. **The physical phenomenon is supported within the tested conditions; a generally useful or faster architecture-selection algorithm has not been established.** This is research-in-progress for faculty feedback, not a publication or a claim to have invented ORRAM.

**Start here:** [One-page research briefing](docs/START_HERE.md) · [Negative results and failed gates](docs/NEGATIVE_RESULTS_AND_FAILURES.md) · [Full faculty report](docs/M10_FACULTY_RESEARCH_REPORT_2026-11-05.md) · [Experiments and evidence](docs/EXPERIMENT_EVIDENCE_INDEX.md) · [Final 12-case dataset](results/synthesized_rtl_holdout_pairs.csv) · [Reproduction guide](docs/REPRODUCIBILITY.md)

## 1. Experimental approach

ORRAM already provides `row` and `word` decoder alternatives. The research compares **functionally matched memory choices within each test case**, while changing the address-generation context *between* test cases.

```text
                  same registered address-generation RTL
                                    |
                        address bits A[4:0]
                                    |
                 +------------------+------------------+
                 |                                     |
           ORRAM row decoder                      ORRAM word decoder
                 |                                     |
          identical interface                    identical interface
                 |                                     |
           output capture FF                      output capture FF
                 |                                     |
       post-route setup slack                  post-route setup slack
                 +------------------+------------------+
                                    |
                          paired timing comparison
```

- **Configurations:** 32-word × 8-bit and 32-word × 16-bit standard-cell memories; matching 1RW interface, registered address-generation wrapper and physical constraints *within each architecture pair*.
- **Address contexts:** initial buffered/late-bit examples; XOR-based cones; then three Yosys-synthesized application-inspired RTL generators (ring translation, serpentine tile and DMA stride).
- **Implementation:** Nangate45 typical-corner standard-cell library, matched physical implementation, detailed routing and extracted **SPEF** timing; setup slack compared at registered output endpoints and against overall worst setup paths.
- **Clock limitation:** a nominal 4.0 ns **ideal clock**, without a routed clock tree. These are exploratory physical-timing measurements, **not signoff**.

A *positive* `row minus word` setup-slack margin means **row is better** in that case; a *negative* value favors **word**. It does not by itself imply an equivalent overall frequency gain.

## 2. Findings at a glance

| Experiment | Measured finding | Interpretation |
|---|---|---|
| 32×8, registered buffered wrapper (three seeds) | Balanced: **word +31.589 ps** mean; late-low address: **row +37.360 ps** mean | Physical timing preference reverses with context |
| 32×16, XOR address wrapper (three seeds) | Balanced: **word +49.328 ps** mean; late-low address: **row +45.960 ps** mean | Reversal reproduced with a different address logic family |
| 32×8 XOR control | Balanced word advantage **18.098 ps** mean | Did **not** meet the predefined 20 ps margin; retained as a limitation |
| Address-pin sensitivity | **420** constrained timing-path records, **150** matched address comparisons | Low-order vs high-order address paths had different relative downstream delays in the studied cases; this is not a standalone decoder timing-arc characterization |
| Final synthesized-RTL holdout | **24** routed implementations, **12** matched row/word choices | Three application-inspired address RTLs × two widths × two seeds × two decoder choices |
| Frozen early predictor | **9/12** correct; mean oracle regret **2.987 ps**; max regret **20.681 ps** | **Inferior** to always choosing word (**11/12** correct) on this holdout |
| Runtime assessment | One-candidate route-stage timings similar to blind selection | No end-to-end speedup proven; calibration/prediction cost excluded |
| Physical evidence audit | **24/24** ODB/SDC/SPEF rechecks; whole-design vs read-path winner agreed in **12/12** pairs | Supports the narrow timing analysis, **not** full timing/signoff certification |

**Key negative outcome:** On the final three-circuit dataset, the predictor's mean improvement over an always-word choice was only **0.1275 ps**. The result does not justify a generalized optimization claim.

## 3. Research progression and navigation

| Stage | What was tested | Where to read |
|---|---|---|
| A. Feasibility | Same-interface row/word alternatives under controlled boundary assumptions | [Feasibility results](docs/FEASIBILITY_RESULTS_2026-11-05.md) |
| B. Integrated timing | Registered wrapper experiments, three placement seeds, higher-width XOR controls | [Final bounded feasibility decision](docs/FINAL_FEASIBILITY_GO_NO_GO_2026-11-05.md) |
| C. Physical mechanism | Critical-path decomposition and per-address downstream timing sensitivity | [Three-seed address sensitivity](docs/ORRAM_THREE_SEED_ADDRESS_SENSITIVITY_2026-11-05.md) |
| D. Early selection | Frozen pre-placement predictors tested before observing routed holdout labels | [Predictor evaluations](docs/FROZEN_PREPLACEMENT_PREDICTOR_HOLDOUT_2026-11-05.md) |
| E. Synthesized RTL holdout | Ring, serpentine and DMA address logic; final choice accuracy and cost | [Final generalization and cost report](docs/SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md) |
| F. Validity and novelty | Physical evidence integrity, literature overlap and limitations | [M5 integrity](docs/M5_POSTROUTE_INTEGRITY_2026-11-05.md) · [M9 literature](docs/M9_LITERATURE_AND_NOVELTY_REVIEW_2026-11-05.md) |

The [experiment index](docs/EXPERIMENT_EVIDENCE_INDEX.md) links the specific successful GitHub Actions runs, result files and workflow sources for each stage. The [documentation index](docs/README.md) separates the **current conclusions** from earlier feasibility protocols, planning notes and faculty-preparation materials.

## 4. Repository map

```text
README.md              This research overview
docs/
  START_HERE.md        Short faculty briefing and proposed reading order
  README.md            Categorized documentation index
  EXPERIMENT_EVIDENCE_INDEX.md   Completed experiments with original workflow run IDs
  REPRODUCIBILITY.md   Environment, testing, provenance and rerun instructions
  M10_FACULTY_RESEARCH_REPORT_2026-11-05.md   Full technical narrative
  ...                  Mechanism, predictor, literature and integrity reports
results/
  README.md            Compact evidence and provenance guide
  synthesized_rtl_holdout_pairs.csv   12-row derived scoreboard
  *.json               Earlier feasibility-stage gate summaries
rtl_applications/       Ring, serpentine and DMA address-generation RTL
scripts/                ORRAM generation, physical integration, STA, model and scoring scripts
tb/                     Behavioral memory testbench
tests/                  Lightweight repository contract checks
.github/workflows/      31 retained experiment / validation workflows
```

The 31 workflows document the progression of the experiments. They are **not all intended as steps to execute sequentially**; start with [the workflow/run map](docs/EXPERIMENT_EVIDENCE_INDEX.md), not the GitHub Actions list.

## 5. Check the repository or reproduce results

A quick source-level check requires Python 3:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py
```

Full physical reproduction also requires the explicitly pinned OpenROAD/ORFS image and source revision, a Linux/Docker-capable environment, and in some cases earlier Actions artifacts. It is **not** a single local command and should not be inferred from the tests above. See the [reproducibility guide](docs/REPRODUCIBILITY.md) and the original [physical holdout workflow](.github/workflows/synthesized-rtl-physical.yml).

## 6. What this research does—and does not—establish

**Supported within the study:** address-generation context can reverse which of the two *existing* ORRAM decoder organizations has the better extracted-SPEF setup slack in selected matched designs; per-address path analysis is consistent with this sensitivity.

**Not established:** a novel RAM generator or decoder, a broadly reliable architecture predictor, a meaningful implementation-cost reduction, power/security improvements, full multi-corner/CTS/DRC/LVS/IR-EM signoff, or a published result. Placement seeds and application-inspired contexts are correlated, not a population of independent industrial workloads. Related OpenROAD memory-optimization proposals limit novelty; see [the literature analysis](docs/M9_LITERATURE_AND_NOVELTY_REVIEW_2026-11-05.md).

**Research next step:** seek faculty feedback on whether a physically grounded per-pin arrival/slew/load-aware and uncertainty-aware predictor warrants a *new*, separately evaluated experiment. A potential hardware-security/side-channel extension is a **separate proposed question**; no side-channel or power-leakage experiments have been conducted here.

**Author:** Gowtham Sai Damalacheruvu · M.S. Electrical and Computer Engineering · Rutgers University.
