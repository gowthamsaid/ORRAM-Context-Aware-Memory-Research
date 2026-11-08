# Reproducibility and toolchain notes

This study contains **source code, documented experiments, summary datasets and links to GitHub Actions runs**. It does not contain all routed ODB, DEF, SPEF and timing reports as ordinary Git files; many large physical checkpoints were archived as time-limited Actions artifacts. Reproduction depends on the toolchain and, for some later workflows, previously archived evidence.

## 1. Lightweight checks (no OpenROAD required)

Requires **Python 3**. From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py
```

These check the repository's contract assertions and Python syntax. **They do not validate the physical timing findings, model accuracy, SAT-equivalence results, or extraction.**

To examine the archived final paired results without tools, read [the 12-case derived CSV](../results/synthesized_rtl_holdout_pairs.csv) and [the signed comparison table](SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md).

## 2. Physical toolchain

The original workflow environment records:

- OpenROAD-flow-scripts revision: `d056a2b304182bf76ff10653531165b1dd9848d4`
- ORFS Docker image: `openroad/orfs@sha256:641c6870a2c64143464d46017dd25ab647900fd29dce502230a2db0682e69bc9`
- Process/library: Nangate45 **typical**.
- Timing model: nominal 4 ns ideal clock, simplified I/O constraints and output loading; **no clock-tree synthesis in the ORRAM integrated experiments**.
- Additional tools used in particular stages: Yosys + ABC, OpenSTA, Python, Icarus Verilog and GitHub Actions; versions/inputs are recorded by the run logs.

For exact invocations, inspect the corresponding workflow file and run log in [the experiment evidence index](EXPERIMENT_EVIDENCE_INDEX.md). A modern installed ORFS build may have incompatible interfaces; substituting the newest tool image is not an exact reproduction.

## 3. How the experiment was validated

**Generation and function:** [`scripts/generate_ram.tcl`](../scripts/generate_ram.tcl) generates ORRAM row/word alternatives. [`scripts/check_architectures.py`](../scripts/check_architectures.py) checks matching generated behavioral models and distinct implemented structures. The [memory testbench](../tb/ram32x8_tb.v) validates read/write responses in the initial configuration.

**Controlled physical tests:** The [three-seed registered implementation workflow](../.github/workflows/multiseed-integration.yml) and [32×16 XOR workflow](../.github/workflows/cross-size-xor.yml) preserve each matched pair's timing reports and routing artifacts. Within each pair, wrapper function, library, constraints and physical setup are matched.

**Freeze before holdout:** [`freeze-synthesized-rtl.yml`](../.github/workflows/freeze-synthesized-rtl.yml) synthesizes the three application-inspired address producers, checks RTL-to-mapped combinational equivalence and freezes model choices; [`synthesized-rtl-physical.yml`](../.github/workflows/synthesized-rtl-physical.yml) then implements each row/word candidate; [`score-synthesized-rtl-holdout.yml`](../.github/workflows/score-synthesized-rtl-holdout.yml) measures accuracy, regret and placement/route stage time. The predictions and routed labels are stored in **different chronological runs**. The final results are [summarized here](SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md).

**Routed timing integrity:** [M5 recheck](M5_POSTROUTE_INTEGRITY_2026-11-05.md) independently reopened 24 archived routed ODB/SDC/SPEF cases. The `check_setup -verbose` audit produced no matched errors or warnings, but was silent, so it **does not prove signoff constraint completeness**.

## 4. Raw artifacts and cost caveats

The saved Actions run bundles contain post-route STA reports, exact netlists/physical files, constraints and parsable metrics; use the [run index](EXPERIMENT_EVIDENCE_INDEX.md) to locate them. GitHub may expire artifacts. The new [tracked CSV](../results/synthesized_rtl_holdout_pairs.csv) preserves the final 12 signed margins in a human-readable form, but it is a **derived scoreboard**, not raw routing evidence.

Wall times in the [cost report](SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md) cover selected placement+route stages only. They exclude reference characterization, producer synthesis and prediction overhead, so no absolute end-to-end time gain is demonstrated.

## 5. Boundaries of reproducibility

- Workflows involving earlier, time-limited artifact IDs may require archive restoration or fresh generation after expiry; do not assume all old runs will remain downloadable.
- Only the measured Nangate45 corner, few address producers, widths and placement seeds were tested. Seed repetitions do not substitute for independent industrial designs.
- Some historical failed CI runs were tool/infrastructure/debugging issues and were corrected later. They are not adverse scientific results; see the [final holdout engineering corrections](SYNTHESIZED_RTL_GENERALIZATION_AND_COST_FINAL_2026-11-05.md).
- No CTS with propagated clocks, multi-corner PVT validation, DRC/LVS signoff, IR/EM signoff, calibrated electrical power measurement, or side-channel analysis has been completed.

For a faculty-level assessment, the recommended path is [brief](START_HERE.md) → [full report](M10_FACULTY_RESEARCH_REPORT_2026-11-05.md) → [held-out data](../results/synthesized_rtl_holdout_pairs.csv) → [original successful runs](EXPERIMENT_EVIDENCE_INDEX.md).
