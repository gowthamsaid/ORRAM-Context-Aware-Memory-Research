# ORRAM boundary-context-aware memory research

**Hypothesis:** The architecture preferred using isolated standard-cell memory timing may not be preferred under the timing budgets, address arrival asymmetry, and output loading of an enclosing design. Can early timing context inform architecture selection more effectively than standalone metrics?

**Scientific status: exploratory feasibility screening, not a publication, original optimization, or proof of novelty.** Existing ORRAM and other memory-generator work already investigate memory architectures and physical design.

## Initial experiment

- Generate two **same-interface** 32-word × 8-bit 1RW memory architectures with OpenROAD ORRAM, using row versus word decoding and identical technology settings.
- Preserve the exact same physical block per architecture, and vary boundary timing assumptions without rebuilding it.
- Check generated behavioral models for identity; execute independent write/read simulation against an in-testbench model.
- Require structurally distinct physical implementations; fail with a documented NO-GO if the two variants are identical.
- Analyze 5 boundary cases: reference, late low-order address bits, late high-order address bits, higher output load, tighter output timing requirement.
- Capture read-path STA reports, overall STA reports, SDCs, physical databases and structured outcomes.

**Crucial interpretation:** A ranking reversal arising from different input delays alone is a baseline observation, not evidence for a superior physical optimization algorithm. It licenses a more rigorous full-design test only. Failure to observe a reversal in this screen is a limited null result, not proof context is irrelevant.

## Reproduction and results

The GitHub Actions workflow `.github/workflows/feasibility.yml` uses a pinned OpenROAD-flow-scripts revision and Docker image, and emits artifacts with the raw reports and decision.

This repository is separate from the prior FIFO research; no FIFO files are altered.
